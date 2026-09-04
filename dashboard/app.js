// API Configuration
const API_URL = 'https://7ejkhfnocl.execute-api.us-east-1.amazonaws.com/prod';

// Chart instances
let commitsChart = null;
let activityChart = null;

// Fetch data from API
async function fetchData() {
    try {
        const response = await fetch(`${API_URL}/activity`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

// Process data for charts and table
function processData(data) {
    if (!data || !data.students || data.students.length === 0) {
        return null;
    }

    // Aggregate data by student
    const studentMap = {};
    data.students.forEach(item => {
        const name = item.student_id;
        if (!studentMap[name]) {
            studentMap[name] = { commits: 0, mergeRequests: 0, count: 0 };
        }
        studentMap[name].commits += item.commits || 0;
        studentMap[name].mergeRequests += item.merge_requests || 0;
        studentMap[name].count += 1;
    });

    // Sort by total activity
    const sortedStudents = Object.entries(studentMap)
        .map(([name, data]) => ({
            name,
            commits: data.commits,
            mergeRequests: data.mergeRequests,
            total: data.commits + data.mergeRequests,
            records: data.count
        }))
        .sort((a, b) => b.total - a.total);

    return {
        students: sortedStudents,
        totalCommits: sortedStudents.reduce((sum, s) => sum + s.commits, 0),
        totalMRs: sortedStudents.reduce((sum, s) => sum + s.mergeRequests, 0),
        totalStudents: sortedStudents.length,
        mostActive: sortedStudents.length > 0 ? sortedStudents[0].name : '-'
    };
}

// Update summary cards
function updateSummary(data) {
    document.getElementById('totalStudents').textContent = data.totalStudents || 0;
    document.getElementById('totalCommits').textContent = data.totalCommits || 0;
    document.getElementById('totalMRs').textContent = data.totalMRs || 0;
    document.getElementById('mostActive').textContent = data.mostActive || '-';
}

// Update student table
function updateTable(data) {
    const tbody = document.getElementById('studentTableBody');
    if (!data || data.students.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4">No student activity data found</td></tr>';
        return;
    }

    tbody.innerHTML = data.students.map(student => `
        <tr>
            <td><strong>${student.name}</strong></td>
            <td>${student.commits}</td>
            <td>${student.mergeRequests}</td>
            <td>${student.total}</td>
        </tr>
    `).join('');
}

// Update charts
function updateCharts(data) {
    if (!data || data.students.length === 0) {
        return;
    }

    const labels = data.students.map(s => s.name);
    const commitsData = data.students.map(s => s.commits);
    const mrsData = data.students.map(s => s.mergeRequests);

    // Commits Chart
    const commitsCtx = document.getElementById('commitsChart').getContext('2d');
    if (commitsChart) {
        commitsChart.destroy();
    }
    commitsChart = new Chart(commitsCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Commits',
                    data: commitsData,
                    backgroundColor: 'rgba(102, 126, 234, 0.7)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Merge Requests',
                    data: mrsData,
                    backgroundColor: 'rgba(118, 75, 162, 0.7)',
                    borderColor: 'rgba(118, 75, 162, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });

    // Activity Chart (Pie)
    const activityCtx = document.getElementById('activityChart').getContext('2d');
    if (activityChart) {
        activityChart.destroy();
    }
    activityChart = new Chart(activityCtx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data.students.map(s => s.total),
                backgroundColor: [
                    '#667eea', '#764ba2', '#f093fb', '#4facfe',
                    '#43e97b', '#fa709a', '#fee140', '#f6d365',
                    '#a18cd1', '#fbc2eb'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right',
                }
            }
        }
    });
}

// Refresh all data
async function refreshData() {
    const loadingMsg = document.getElementById('studentTableBody');
    loadingMsg.innerHTML = '<tr><td colspan="4">Loading data...</td></tr>';
    
    const rawData = await fetchData();
    if (!rawData) {
        document.getElementById('studentTableBody').innerHTML = 
            '<tr><td colspan="4">Error loading data. Please try again.</td></tr>';
        return;
    }

    const processedData = processData(rawData);
    if (!processedData) {
        document.getElementById('studentTableBody').innerHTML = 
            '<tr><td colspan="4">No data found. Students may not have activity yet.</td></tr>';
        return;
    }

    updateSummary(processedData);
    updateTable(processedData);
    updateCharts(processedData);
}

// Auto-refresh on load
document.addEventListener('DOMContentLoaded', () => {
    refreshData();
    // Refresh every 30 seconds
    setInterval(refreshData, 30000);
});
