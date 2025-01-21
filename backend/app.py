import pytz
from datetime import datetime
from flask import Flask, jsonify, render_template
import requests
from datetime import datetime, timedelta
import threading
import time
import yaml
import json

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


def load_config_from_json(file_path):
    """
    Loads configuration data from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the configuration.

    Returns:
        dict: The configuration data loaded from the JSON file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config


def fetch_codeforces_data(handle):
    """
    Fetches data from the Codeforces API for a given user handle.

    Args:
        handle (str): The Codeforces user handle.

    Returns:
        dict or None: The JSON response from the Codeforces API if the request is successful,
                      otherwise None.
    """
    # encode url
    url = CODEFORCES_API_URL.format(handle)
    # encode to URL
    url = requests.utils.quote(url, safe='/:?=&')
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def fetch_user_info(handles):
    """
    Fetches user information from the Codeforces API.

    Args:
        handles (list of str): A list of Codeforces user handles.

    Returns:
        dict or None: A dictionary containing user information if the request is successful,
                      otherwise None.
    """
    response = requests.get(CODEFORCES_USER_INFO_URL.format(';'.join(handles)))
    if response.status_code == 200:
        return response.json()
    else:
        print(response.text)
        return None


def get_user_info_dict(handles: list) -> dict:
    """
    Fetches user information for a list of handles in batches and returns a dictionary of user info.

    Args:
        handles (list): A list of user handles to fetch information for.

    Returns:
        dict: A dictionary where the keys are user handles and the values are user information dictionaries.

    Raises:
        AssertionError: If the fetched user information batch is empty or invalid.

    Notes:
        - The function processes the handles in batches of 30.
        - If the total number of handles is not a multiple of the batch size, the remaining handles are processed in a final batch.
    """
    user_info_dict = {}
    batch_size = 30
    for i in range(0, len(handles), batch_size):
        batch_handles = handles[i:i + batch_size]
        user_info_batch = fetch_user_info(batch_handles)
        print(user_info_batch)
        assert user_info_batch
        if user_info_batch and user_info_batch['status'] == 'OK':
            user_info_dict.update(
                {user['handle']: user for user in user_info_batch['result']})
    if len(handles) % batch_size != 0:
        batch_handles = handles[-(len(handles) % batch_size):]
        user_info_batch = fetch_user_info(batch_handles)
        if user_info_batch and user_info_batch['status'] == 'OK':
            user_info_dict.update(
                {user['handle']: user for user in user_info_batch['result']}
            )
    return user_info_dict


def process_data(config):
    """
    Processes Codeforces data for a given configuration.
    Args:
        config (dict): A dictionary containing configuration data. It must include a 'handles' key,
                       which is a dictionary where keys are user handles and values are dictionaries
                       containing user-specific configuration, including a 'group' key.
    Returns:
        list: A list of dictionaries, each containing processed data for a user. Each dictionary includes:
              - "user": The user's handle.
              - "group": The user's group from the configuration.
              - "color": The user's rank color.
              - "days": A list of lists, each containing problems solved on a specific day within the last 30 days.
              - "lastUpdate": The timestamp of the last update in ISO format.
              - "avatar": The URL of the user's avatar.
              - "total": The total number of unique problems solved in the last 30 days.
    Note:
        - The function fetches user information and submission data from Codeforces.
        - Only submissions with a verdict of 'OK' are considered.
        - The function filters out duplicate problems and considers only unique problems.
        - The data is sorted in descending order based on the total number of problems solved.
    """
    data = []
    user_info_dict = get_user_info_dict(list(config['handles'].keys()))
    print(user_info_dict)
    for handle in user_info_dict.keys():
        user_data = fetch_codeforces_data(handle)
        if user_data is None or user_data['status'] != 'OK':
            continue
        submissions = user_data['result']
        days = [[] for _ in range(30)]  # Create a list of 30 empty lists
        tonight = datetime.now(pytz.timezone('Asia/Shanghai')).replace(hour=23,
                                                                       minute=59, second=59, microsecond=0)  # Tonight at 23:59:59
        unique_problems = set()
        for submission in submissions:
            if submission.get('verdict') != 'OK':
                continue
            problem_id = submission['problem']['contestId'], submission['problem']['index']
            # print(problem_id)
            if problem_id in unique_problems:
                continue
            unique_problems.add(problem_id)

            submission_time = datetime.fromtimestamp(
                # Submission time in Shanghai timezone
                submission['creationTimeSeconds'], pytz.timezone('Asia/Shanghai'))
            if (tonight - submission_time).days < 30:
                days[(tonight - submission_time).days].append({
                    'problem': submission['problem']['name'],
                    'contestId': submission['problem']['contestId'],
                    'index': submission['problem']['index'],
                })
        if user_info_dict[handle].get('rank') is None:
            user_rank = 'newbie'
        else:
            user_rank = user_info_dict[handle]['rank']

        user_color = rank_colors[user_rank.lower()]
        print(user_color)
        data.append({
            "user": handle,
            "group": config['handles'][handle]['group'],
            "color": user_color,  # 使用用户的颜色
            "days": days,
            "lastUpdate": datetime.now().isoformat(),
            "avatar": user_info_dict[handle]['titlePhoto'],
            "total": sum([len(day) for day in days]),  # 总题数
        })
    # 按 total 降序排序
    data.sort(key=lambda x: x['total'], reverse=True)
    print(data)
    return data


def update_user_data():
    """
    Continuously updates the global user data cache every 20 minutes.

    This function runs an infinite loop where it processes user data and updates
    the global `data_cache` dictionary with the latest data and the timestamp of
    the last update. If an error occurs during data processing, it catches the
    exception and prints an error message.

    Globals:
        data_cache (dict): A dictionary to store the last update timestamp and user data.
        handles (list): A list of user handles to process.
        unofficial (bool): A flag indicating whether to include unofficial data.

    Raises:
        Exception: If an error occurs during data processing.

    Note:
        The function sleeps for 20 minutes between each update cycle.
    """
    global data_cache, config
    while True:
        try:
            data = process_data(config)
            data_cache = {
                "lastUpdate": datetime.now().isoformat(),
                "data": data
            }
            print("Data updated at", datetime.now())
        except Exception as e:
            print("Error updating data:", e)
        time.sleep(60*40)  # 每隔20分钟更新一次数据


@ app.route('/api/user-data', methods=['GET'])
def get_user_data():
    """
    Retrieve user data from the data cache and return it as a JSON response.

    Returns:
        Response: A Flask JSON response containing the user data from the cache.
                  If an error occurs, returns a JSON response with an error message
                  and a 500 status code.
    """
    try:
        return jsonify(data_cache)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # 加载配置
    config = load_config_from_json('config.json')
    # 启动后台线程
    update_thread = threading.Thread(target=update_user_data)
    update_thread.daemon = True
    update_thread.start()

    app.run(debug=False, host='::', port=5000)
