document.addEventListener('DOMContentLoaded', function() {
    // Read data from data attributes
    const chartData = document.getElementById('chart-data');
    const statusLabels = JSON.parse(chartData.dataset.statusLabels);
    const statusData = JSON.parse(chartData.dataset.statusData);
    const priorityLabels = JSON.parse(chartData.dataset.priorityLabels);
    const priorityData = JSON.parse(chartData.dataset.priorityData);
    const monthlyLabels = JSON.parse(chartData.dataset.monthlyLabels);
    const monthlyTotal = JSON.parse(chartData.dataset.monthlyTotal);
    const monthlyCompleted = JSON.parse(chartData.dataset.monthlyCompleted);

    // Status Pie Chart
    const statusCtx = document.getElementById('statusChart').getContext('2d');
    new Chart(statusCtx, {
        type: 'pie',
        data: {
            labels: statusLabels,
            datasets: [{
                data: statusData,
                backgroundColor: ['#6c757d', '#0dcaf0', '#ffc107', '#198754']
            }]
        }
    });

    // Priority Bar Chart
    const priorityCtx = document.getElementById('priorityChart').getContext('2d');
    new Chart(priorityCtx, {
        type: 'bar',
        data: {
            labels: priorityLabels,
            datasets: [{
                label: 'Tasks',
                data: priorityData,
                backgroundColor: ['#198754', '#0dcaf0', '#ffc107', '#dc3545']
            }]
        }
    });

    // Monthly Trend Line Chart
    if (monthlyLabels.length > 0) {
        const trendCtx = document.getElementById('trendChart').getContext('2d');
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: 'Total Tasks',
                    data: monthlyTotal,
                    borderColor: '#0d6efd',
                    tension: 0.3
                }, {
                    label: 'Completed',
                    data: monthlyCompleted,
                    borderColor: '#198754',
                    tension: 0.3
                }]
            }
        });
    }
});
