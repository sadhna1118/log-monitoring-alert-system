"""
Web dashboard for visualizing security events.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from database import DatabaseManager, SecurityEvent, ThreatStatistics
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__, template_folder='../dashboard/templates', static_folder='../dashboard/static')
CORS(app)

db = DatabaseManager()


@app.route('/')
def index():
    """Dashboard home page."""
    return render_template('index.html')


@app.route('/api/stats')
def get_stats():
    """Get current statistics."""
    # Get recent events
    recent_events = db.get_recent_events(limit=100)
    suspicious_events = db.get_suspicious_events(limit=50)
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get today's statistics
    stats = db.session.query(ThreatStatistics).filter_by(date=today).first()
    
    if stats:
        total_threats = stats.total_threats
        threats_by_type = {
            'Failed Login Attempts': stats.failed_logins,
            'SQL Injection': stats.sql_injections,
            'Cross-Site Scripting (XSS)': stats.xss_attempts,
            'Directory Traversal': stats.directory_traversal,
            'Unauthorized Access': stats.unauthorized_access,
            'Port Scanning': stats.port_scans,
            'Privilege Escalation': stats.privilege_escalation
        }
    else:
        total_threats = 0
        threats_by_type = {}
    
    # Get top IPs
    top_ips = db.get_top_ips(limit=10)
    
    return jsonify({
        'total_events': len(recent_events),
        'suspicious_events': len(suspicious_events),
        'total_threats': total_threats,
        'threats_by_type': threats_by_type,
        'top_ips': [{'ip': ip, 'count': count} for ip, count in top_ips]
    })


@app.route('/api/events/recent')
def get_recent_events():
    """Get recent security events."""
    limit = request.args.get('limit', 50, type=int)
    events = db.get_recent_events(limit=limit)
    
    return jsonify([{
        'id': e.id,
        'timestamp': e.log_timestamp,
        'level': e.log_level,
        'message': e.message,
        'is_suspicious': e.is_suspicious,
        'threats': e.threat_types.split(',') if e.threat_types else [],
        'source_ip': e.source_ip
    } for e in events])


@app.route('/api/events/suspicious')
def get_suspicious_events():
    """Get suspicious events only."""
    limit = request.args.get('limit', 50, type=int)
    events = db.get_suspicious_events(limit=limit)
    
    return jsonify([{
        'id': e.id,
        'timestamp': e.log_timestamp,
        'level': e.log_level,
        'message': e.message,
        'threats': e.threat_types.split(',') if e.threat_types else [],
        'source_ip': e.source_ip
    } for e in events])


@app.route('/api/trends')
def get_trends():
    """Get threat trends over time."""
    days = request.args.get('days', 7, type=int)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    stats = db.get_statistics_by_date_range(
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    return jsonify([{
        'date': s.date,
        'total_threats': s.total_threats,
        'failed_logins': s.failed_logins,
        'sql_injections': s.sql_injections,
        'xss_attempts': s.xss_attempts,
        'directory_traversal': s.directory_traversal,
        'unauthorized_access': s.unauthorized_access,
        'port_scans': s.port_scans,
        'privilege_escalation': s.privilege_escalation
    } for s in stats])


@app.route('/api/top_ips')
def get_top_ips():
    """Get top suspicious IP addresses."""
    limit = request.args.get('limit', 10, type=int)
    ips = db.get_top_ips(limit=limit)
    
    return jsonify([{
        'ip': ip,
        'count': count
    } for ip, count in ips])


def run_dashboard(host='0.0.0.0', port=5000):
    """Run the dashboard server."""
    print("=" * 80)
    print("🌐 SECURITY DASHBOARD STARTING")
    print("=" * 80)
    print(f"Dashboard URL: http://{host}:{port}")
    print("Press Ctrl+C to stop")
    print("=" * 80)
    
    app.run(host=host, port=port, debug=False)


if __name__ == '__main__':
    port = int(os.getenv('DASHBOARD_PORT', 5000))
    host = os.getenv('DASHBOARD_HOST', '0.0.0.0')
    run_dashboard(host=host, port=port)