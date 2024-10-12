import pytz
from datetime import datetime
from flask import Flask, jsonify, render_template
import requests
from datetime import datetime, timedelta
import threading
import time
import yaml

app = Flask(__name__)

CODEFORCES_API_URL = "https://codeforces.com/api/user.status?handle={}&from=1&count=1000"
CODEFORCES_USER_INFO_URL = "https://codeforces.com/api/user.info?handles={}"
rank_colors = {  # Codeforces 用户等级对应的颜色
    "newbie": "#808080",
    "pupil":  "#008000",
    "specialist": "#03a89e",
    "expert": "#0000ff",
    "candidate master": "#aa00aa",
    "master": "#ff8c00",
    "international master": "#ff8c00",
    "grandmaster": "#ff0000",
    "international grandmaster": "#ff0000",
    "legendary grandmaster": "#ff0000"
}

# 全局变量来存储数据
data_cache = {
    "lastUpdate": None,
    "data": []
}

# 从 YAML 文件中读取 handles


def load_handles_from_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        return config['handles'] + config['unofficial'], config['unofficial']


def fetch_codeforces_data(handle):
    response = requests.get(CODEFORCES_API_URL.format(handle))
    if response.status_code == 200:
        return response.json()
    else:
        return None


def fetch_user_info(handles):
    response = requests.get(CODEFORCES_USER_INFO_URL.format(';'.join(handles)))
    if response.status_code == 200:
        return response.json()
    else:
        return None


def process_data(handles):
    global rank_colors
    data = []
    user_info = fetch_user_info(handles)
    if user_info and user_info['status'] == 'OK':
        user_info_dict = {user['handle']: user for user in user_info['result']}
        # print(user_info_dict)
        for handle in user_info_dict.keys():
            user_data = fetch_codeforces_data(handle)
            if user_data and user_data['status'] == 'OK':
                submissions = user_data['result']
                days = [[] for _ in range(30)]  # 创建30个独立的空列表
                now = datetime.now(pytz.timezone(
                    'Asia/Shanghai'))  # 当前时间转换为CST
                # 更改now为今天的23:59:59
                now = now.replace(hour=23, minute=59, second=59, microsecond=0)

                # 创建一个集合来存储唯一的题号
                unique_problems = set()

                for submission in submissions:
                    if submission['verdict'] != 'OK':
                        continue
                    problem_id = submission['problem']['contestId'], submission['problem']['index']
                    print(problem_id)
                    if problem_id in unique_problems:
                        continue
                    unique_problems.add(problem_id)

                    submission_time = datetime.fromtimestamp(
                        # 提交时间转换为CST
                        submission['creationTimeSeconds'], pytz.timezone('Asia/Shanghai'))
                    if (now - submission_time).days < 30:
                        days[(now - submission_time).days].append({
                            'problem': submission['problem']['name'],
                            'contestId': submission['problem']['contestId'],
                            'index': submission['problem']['index'],
                        })
                user_rank = user_info_dict[handle]['rank']
                user_color = rank_colors[user_rank.lower()]
                print(user_color)

                data.append({
                    "user": handle,
                    "color": user_color,  # 使用用户的颜色
                    "days": days,
                    "lastUpdate": datetime.now().isoformat(),
                    "avatar": user_info_dict[handle]['titlePhoto'],
                    "total": sum([len(day) for day in days])
                })
    # 按 total 降序排序
    data.sort(key=lambda x: x['total'], reverse=True)
    # 为unofficial用户添加颜色
    for i in range(len(data)):
        if data[i]['user'] in unofficial:
            data[i]['user'] += ' ⭐'
    print(data)
    return data


def update_user_data():
    global data_cache, handles, unofficial
    while True:
        try:
            data = process_data(handles)
            data_cache = {
                "lastUpdate": datetime.now().isoformat(),
                "data": data
            }
            print("Data updated at", datetime.now())
        except Exception as e:
            print("Error updating data:", e)
        time.sleep(60*20)  # 每隔20分钟更新一次数据


@app.route('/api/user-data', methods=['GET'])
def get_user_data():
    try:
        return jsonify(data_cache)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    global handles, unofficial
    handles, unofficial = load_handles_from_yaml('config.yaml')
    print(handles)
    # 启动后台线程
    update_thread = threading.Thread(target=update_user_data)
    update_thread.daemon = True
    update_thread.start()

    app.run(debug=False, port=5000)
