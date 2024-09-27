// 从后端获取数据
fetch('/api/user-data')
    .then(response => response.json())
    .then(responseData => {
        const { lastUpdate, data } = responseData;

        // 创建热力图
        const container = d3.select('#heatmap-container');
        data.forEach((user, index) => {
            const row = container.append('div').attr('class', 'heatmap');
            const formattedLastUpdate = new Date(user.lastUpdate).toLocaleString();
            const userRank = `#${index + 1}`; // 按顺序显示排名
            row.append('div')
                .html(`<a href="https://codeforces.com/profile/${user.user}" target="_blank" style="color: ${user.color}; font-weight: bold;" title="Last update: ${formattedLastUpdate}">${userRank} ${user.user}</a>`)
                .style('grid-column', 'span 30');
            user.days.forEach(day => {
                const cellClass = `cell-${Math.min(day, 10)}`; // 确保最大值为10
                row.append('div')
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
            .style('color', '#555');
    })
    .catch(error => console.error('Error fetching data:', error));