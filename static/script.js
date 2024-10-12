// 从后端获取数据
fetch('/api/user-data')
    .then(response => response.json())
    .then(responseData => {
        const { lastUpdate, data } = responseData;

        // 创建热力图
        const container = d3.select('#heatmap-container');
        data.forEach((user, index) => {
            const row = container.append('div').attr('class', 'heatmap-row').style('display', 'flex').style('align-items', 'center').style('margin-bottom', '10px');
            const formattedLastUpdate = new Date(user.lastUpdate).toLocaleString();
            const userRank = `#${index + 1}`; // 按顺序显示排名

            // 添加排名
            row.append('div')
                .html(`<span style="font-weight: bold;">${userRank}</span>`)
                .style('margin-right', '10px');

            // 添加头像
            row.append('div')
                .html(`<img src="${user.avatar}" alt="${user.user} avatar" style="width: 40px; height: 40px; margin-right: 10px; border-radius: 5px;">`);
            // 添加用户名
            row.append('div')
                .html(`<a href="https://codeforces.com/profile/${user.user}" target="_blank" style="color: ${user.color}; font-weight: bold; text-decoration: none;" title="Last update: ${formattedLastUpdate}">${user.user}</a>`)
                .style('margin-right', '10px');
            // 添加总分数
            row.append('div')
                .html(`<span style="font-weight: bold;">∑${user.total}</span>`)
                .style('margin-right', '10px');

            // 创建热力图容器
            const heatmapContainer = container.append('div').attr('class', 'heatmap-row').style('display', 'flex').style('align-items', 'center').style('margin-bottom', '10px');

            user.days.forEach((day, index) => {
                const cellClass = `cell-${Math.min(day.length, 10)}`; // 确保最大值为10
                const date = new Date();
                date.setDate(date.getDate() - index); // 计算对应的日期
                const formattedDate = date.toISOString().split('T')[0]; // 格式化日期为 YYYY-MM-DD
                const problems = day.map(d => `<a href="https://codeforces.com/contest/${d.contestId}/problem/${d.index}" target="_blank" style="text-decoration: none;">${d.contestId}${d.index} ${d.problem}</a>`).join('<br>'); // 显示当天做的题目并添加链接

                const cell = heatmapContainer.append('div')
                    .attr('class', `cell ${cellClass}`)
                    .text(day.length);

                // 添加点击事件监听器
                cell.on('click', () => showPopup(formattedDate, problems));
            });
        });

        // 显示上次更新时间
        const formattedLastUpdate = new Date(lastUpdate).toLocaleString();
        d3.select('#last-update')
            .text(`Last update: ${formattedLastUpdate}`)
            .style('margin-top', '20px')
            .style('font-size', '14px')
            .style('color', '#555')
            .style('text-align', 'center');
    })
    .catch(error => console.error('Error fetching data:', error));

// 创建一个函数来显示弹出页面
function showPopup(date, problems) {
    closePopup(); // 在显示新弹窗之前关闭现有的弹窗
    const popup = document.createElement('div');
    popup.className = 'popup';
    popup.innerHTML = `<h3>${date}</h3><pre>${problems}</pre><button onclick="closePopup()">关闭</button>`;
    document.body.appendChild(popup);
}

// 创建一个函数来关闭弹出页面
function closePopup() {
    const popup = document.querySelector('.popup');
    if (popup) {
        document.body.removeChild(popup);
    }
}