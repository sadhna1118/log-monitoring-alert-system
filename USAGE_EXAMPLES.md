# 💡 Usage Examples - Real-World Scenarios

## Example 1: Monitor Web Server Logs

### Scenario
You have a web server and want to monitor for SQL injection and XSS attacks.

### Setup
```powershell
# Copy your web server log
copy C:\inetpub\logs\LogFiles\W3SVC1\u_ex*.log logs\webserver.log

# Update config
notepad config.json
```

Update to:
```json
{
  "monitoring": {
    "log_file_path": "logs/webserver.log",
    "check_interval_seconds": 30
  }
}
```

### Run
```powershell
# Start monitoring
python src/monitor.py

# Open dashboard in another terminal
python src/dashboard.py
```

### What Happens
- System checks log every 30 seconds
- Detects SQL injection attempts
- Detects XSS attacks
- Sends email if 5+ threats found
- Updates dashboard in real-time

---

## Example 2: Analyze Failed Login Attempts

### Scenario
Check authentication logs for brute force attacks.

### Run
```powershell
# Analyze auth logs
python src/cli.py analyze --log-file logs/system.log
```

### Output Example
```
📊 Total Log Entries: 49
🚨 Suspicious Activities: 17
⚠️  Total Threats: 20

Threat Breakdown:
  Failed Login Attempts    | █████ 5
  Unauthorized Access      | █████ 5
  SQL Injection            | ████ 4

Top Suspicious IP Addresses:
  1. 203.0.113.45    → 3 suspicious activities
  2. 203.0.113.89    → 1 suspicious activities
```

---

## Example 3: Daily Security Reports

### Scenario
Generate daily reports for security team review.

### Setup
Create a scheduled task (Windows):

```powershell
# Create batch file: daily_report.bat
@echo off
cd "C:\Users\HP\OneDrive\Documents\Desktop\Log Monitoring & Alert System"
python src/report_generator.py logs/system.log
```

Schedule in Task Scheduler:
- Trigger: Daily at 11:59 PM
- Action: Run `daily_report.bat`

### Result
- Report generated daily in `reports/`
- Email sent to security team
- Historical tracking of threats

---

## Example 4: Real-Time Dashboard for SOC Team

### Scenario
Security Operations Center needs real-time visibility.

### Setup
```powershell
# Terminal 1: Start continuous monitoring
python src/monitor.py

# Terminal 2: Start dashboard
python src/dashboard.py

# Terminal 3: Optional - tail logs
Get-Content logs\system.log -Wait -Tail 10
```

### Access
```
http://localhost:5000
```

### Features Available
- Real-time statistics
- Threat distribution charts
- Top suspicious IPs bar chart
- Filterable event table
- Auto-refresh every 30 seconds

---

## Example 5: Investigate Specific IP Address

### Scenario
IP address 203.0.113.45 is suspicious. Investigate all activities.

### Method 1: Using Database
```python
from database import DatabaseManager

db = DatabaseManager()
events = db.session.query(db.SecurityEvent).filter_by(source_ip='203.0.113.45').all()

for event in events:
    print(f"{event.log_timestamp} - {event.message}")
    print(f"Threats: {event.threat_types}")
    print()
```

### Method 2: Using CLI
```powershell
python src/cli.py stats
# Shows top suspicious IPs
```

### Method 3: Using Dashboard
1. Open http://localhost:5000
2. Check "Top Suspicious IPs" chart
3. Click on the IP to filter events

---

## Example 6: ML Anomaly Detection for Unknown Threats

### Scenario
Detect unusual patterns that don't match known attack signatures.

### Setup
```powershell
# Enable ML in .env
notepad .env
```

Add:
```env
ENABLE_ML_DETECTION=true
```

### First Run (Training)
```powershell
python src/monitor.py --test
```

Output:
```
🤖 Training ML model on 49 log entries...
✅ Model trained and saved to models/anomaly_detector.pkl
```

### Subsequent Runs (Detection)
```powershell
python src/monitor.py
```

The system now:
- Uses regex for known threats
- Uses ML for unknown anomalies
- Flags entries that are statistically unusual
- Learns from your specific environment

---

## Example 7: Slack Alerts for Incident Response

### Scenario
Get instant Slack notifications when threats detected.

### Setup
```powershell
# Configure Slack webhook
notepad .env
```

Update:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
ENABLE_SLACK_ALERTS=true
ENABLE_EMAIL_ALERTS=true
```

### Run
```powershell
python src/monitor.py
```

### What Happens
When 5+ threats detected:
1. Email sent to security team
2. Slack message posted to channel
3. Database updated
4. Dashboard refreshed

### Slack Message Format
```
🔴 CRITICAL: Security Alert Detected

Total Threats: 12
Failed Login Attempts: 5
SQL Injection: 4
XSS Attempts: 3

Top Suspicious IPs:
• 203.0.113.45 (3 activities)
• 198.51.100.99 (2 activities)

Time: 2026-01-02 14:30:45
```

---

## Example 8: Docker Production Deployment

### Scenario
Deploy to production server with high availability.

### Setup
```powershell
# Update docker-compose.yml for production
notepad docker-compose.yml
```

Add environment variables:
```yaml
environment:
  - LOG_FILE_PATH=/app/logs/production.log
  - ENABLE_EMAIL_ALERTS=true
  - ENABLE_SLACK_ALERTS=true
  - DATABASE_URL=postgresql://user:pass@db/security_logs
```

### Deploy
```powershell
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f monitor
docker-compose logs -f dashboard
```

### Access
```
http://your-server-ip:5000
```

---

## Example 9: Weekly Executive Report

### Scenario
Generate comprehensive report for management review.

### Create Script: `weekly_report.py`
```python
from report_generator import ReportGenerator
from log_parser import LogParser
from datetime import datetime, timedelta

# Get logs from last 7 days
parser = LogParser()
entries = parser.parse_log_file('logs/system.log')

# Generate report
generator = ReportGenerator()
statistics = parser.get_statistics()
report = generator.generate_report(entries, statistics)

# Save with date
date_str = datetime.now().strftime('%Y-%m-%d')
filename = f'reports/weekly_report_{date_str}.txt'
generator.save_report(report, filename)

print(f"✅ Weekly report saved: {filename}")
```

### Schedule
Run every Sunday at 6 PM using Task Scheduler.

---

## Example 10: Custom Threat Pattern

### Scenario
Add detection for custom application-specific threats.

### Edit `src/patterns.py`
```python
class SecurityPatterns:
    # ... existing patterns ...
    
    # Add your custom pattern
    CUSTOM_APP_PATTERNS = [
        r'PAYMENT_FRAUD_DETECTED',
        r'SUSPICIOUS_TRANSACTION.*amount>\$1000',
        r'ACCOUNT_TAKEOVER_ATTEMPT',
    ]
```

### Update `src/log_parser.py`
```python
def analyze_log_entry(self, entry: LogEntry) -> LogEntry:
    # ... existing checks ...
    
    # Add custom check
    if self.patterns.detect_custom_threats(entry.message):
        entry.add_threat("Payment Fraud", "custom")
    
    return entry
```

### Test
```powershell
python src/monitor.py --test
```

---

## Example 11: Performance Monitoring

### Scenario
Monitor system performance while processing logs.

### Enable Detailed Logging
```python
# In src/monitor.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Run with Metrics
```powershell
python src/monitor.py --test
```

### Output
```
2026-01-02 14:30:45 - INFO - Parsing log file: logs/system.log
2026-01-02 14:30:45 - DEBUG - Processing line 1/49
2026-01-02 14:30:45 - DEBUG - ML prediction took 0.05s
2026-01-02 14:30:46 - INFO - Analysis complete: 49 entries in 1.2s
2026-01-02 14:30:46 - INFO - Detected 17 suspicious activities
```

---

## Example 12: Integration with Existing SIEM

### Scenario
Forward alerts to enterprise SIEM system.

### Create Custom Integration: `src/siem_forwarder.py`
```python
import requests

class SIEMForwarder:
    def __init__(self, siem_url):
        self.siem_url = siem_url
    
    def forward_alert(self, threats, statistics):
        payload = {
            'timestamp': datetime.now().isoformat(),
            'source': 'log-monitoring-system',
            'threats': threats,
            'stats': statistics
        }
        
        response = requests.post(
            f'{self.siem_url}/api/alerts',
            json=payload,
            headers={'Authorization': 'Bearer YOUR_TOKEN'}
        )
        
        return response.status_code == 200
```

### Use in Monitor
```python
# In src/monitor.py
from siem_forwarder import SIEMForwarder

siem = SIEMForwarder('https://your-siem.company.com')
siem.forward_alert(threats, statistics)
```

---

## Quick Command Reference

| Use Case | Command |
|----------|---------|
| Demo all features | `python demo.py` |
| Real-time dashboard | `python src/dashboard.py` |
| One-time analysis | `python src/cli.py analyze --log-file logs/system.log` |
| Continuous monitoring | `python src/monitor.py` |
| Test mode | `python src/monitor.py --test` |
| Generate report | `python src/cli.py report` |
| View statistics | `python src/cli.py stats` |
| Docker deployment | `docker-compose up -d` |
| Stop monitoring | Press Ctrl+C |

---

## Tips & Best Practices

1. **Start with Demo**: Always run `python demo.py` first to understand capabilities

2. **Test with Sample Logs**: Use provided `logs/system.log` before your real logs

3. **Configure Email Last**: Get the system working first, then add email alerts

4. **Use Dashboard for Visibility**: Most intuitive way to see what's happening

5. **Enable ML Gradually**: Start with regex patterns, add ML once comfortable

6. **Schedule Reports**: Automate daily/weekly reports for consistency

7. **Monitor Dashboard Performance**: Auto-refresh every 30s, adjust if needed

8. **Backup Database**: Regularly backup `security_logs.db` for historical data

9. **Review Patterns Regularly**: Update `patterns.py` based on your environment

10. **Use Docker for Production**: More reliable than running Python directly

---

**You now have everything you need to use the system! Start with `python demo.py`** 🚀