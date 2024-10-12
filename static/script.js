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
                .html(`<img src="${user.avatar}" alt="${user.user} avatar" style="width: 40px; height: 40px; margin-right: 10px;">`);
            // 添加用户名
            row.append('div')
                .html(`<a href="https://codeforces.com/profile/${user.user}" target="_blank" style="color: ${user.color}; font-weight: bold;" title="Last update: ${formattedLastUpdate}">${user.user}</a>`)
                .style('margin-right', '10px');

            // 创建热力图容器
            const heatmapContainer = container.append('div').attr('class', 'heatmap-row').style('display', 'flex').style('align-items', 'center').style('margin-bottom', '10px');

            user.days.forEach(day => {
                const cellClass = `cell-${Math.min(day, 10)}`; // 确保最大值为10
                heatmapContainer.append('div')
                    .attr('class', `cell ${cellClass}`)
                    .text(day);
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