// Dashboard JavaScript

let threatChart = null;
let ipChart = null;
let currentView = 'all';

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    loadData();
    
    // Auto-refresh every 30 seconds
    setInterval(loadData, 30000);
});

function initCharts() {
    // Threat Distribution Chart
    const threatCtx = document.getElementById('threatChart').getContext('2d');
    threatChart = new Chart(threatCtx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#f56565',
                    '#ed8936',
                    '#ecc94b',
                    '#48bb78',
                    '#4299e1',
                    '#9f7aea',
                    '#ed64a6'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    // Top IPs Chart
    const ipCtx = document.getElementById('ipChart').getContext('2d');
    ipChart = new Chart(ipCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Suspicious Activities',
                data: [],
                backgroundColor: '#f56565'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
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
}

async function loadData() {
    try {
        // Load statistics
        const statsResponse = await fetch('/api/stats');
        const stats = await statsResponse.json();
        
        updateStatistics(stats);
        updateCharts(stats);
        
        // Load events
        if (currentView === 'all') {
            await loadAllEvents();
        } else {
            await loadSuspiciousEvents();
        }
        
        // Update last update time
        document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
        
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('statusText').textContent = 'Connection Error';
        document.getElementById('statusDot').style.background = '#f56565';
    }
}

function updateStatistics(stats) {
    document.getElementById('totalEvents').textContent = stats.total_events || 0;
    document.getElementById('suspiciousEvents').textContent = stats.suspicious_events || 0;
    document.getElementById('totalThreats').textContent = stats.total_threats || 0;
    document.getElementById('suspiciousIPs').textContent = stats.top_ips?.length || 0;
}

function updateCharts(stats) {
    // Update threat distribution chart
    if (stats.threats_by_type && Object.keys(stats.threats_by_type).length > 0) {
        const labels = [];
        const data = [];
        
        for (const [type, count] of Object.entries(stats.threats_by_type)) {
            if (count > 0) {
                labels.push(type);
                data.push(count);
            }
        }
        
        threatChart.data.labels = labels;
        threatChart.data.datasets[0].data = data;
        threatChart.update();
    }
    
    // Update IP chart
    if (stats.top_ips && stats.top_ips.length > 0) {
        const labels = stats.top_ips.map(item => item.ip);
        const data = stats.top_ips.map(item => item.count);
        
        ipChart.data.labels = labels;
        ipChart.data.datasets[0].data = data;
        ipChart.update();
    }
}

async function loadAllEvents() {
    try {
        const response = await fetch('/api/events/recent?limit=50');
        const events = await response.json();
        displayEvents(events);
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

async function loadSuspiciousEvents() {
    try {
        const response = await fetch('/api/events/suspicious?limit=50');
        const events = await response.json();
        displayEvents(events);
    } catch (error) {
        console.error('Error loading suspicious events:', error);
    }
}

function displayEvents(events) {
    const tbody = document.getElementById('eventsTableBody');
    
    if (events.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="loading">No events found</td></tr>';
        return;
    }
    
    tbody.innerHTML = events.map(event => {
        const levelClass = `level-${event.level}`;
        const threats = event.threats.filter(t => t).map(t => 
            `<span class="threat-tag">${t}</span>`
        ).join('');
        
        return `
            <tr>
                <td>${event.timestamp || '-'}</td>
                <td><span class="level-badge ${levelClass}">${event.level}</span></td>
                <td>${truncate(event.message, 100)}</td>
                <td><div class="threats-list">${threats || '-'}</div></td>
                <td>${event.source_ip || '-'}</td>
            </tr>
        `;
    }).join('');
}

function truncate(str, length) {
    if (!str) return '-';
    return str.length > length ? str.substring(0, length) + '...' : str;
}

function showAllEvents() {
    currentView = 'all';
    loadAllEvents();
}

function showSuspiciousOnly() {
    currentView = 'suspicious';
    loadSuspiciousEvents();
}

function refreshData() {
    loadData();
}