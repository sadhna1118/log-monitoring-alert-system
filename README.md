# Log Monitoring & Alert System
http://localhost:5000/
A Python-based security operations tool that automatically monitors system logs, detects suspicious activities, and sends real-time email alerts.

## Features

- 🔍 **Automated Log Parsing**: Continuously monitors system logs for security events
- 🚨 **Regex Pattern Matching**: Detects 7+ categories of security threats
- 🤖 **Machine Learning**: AI-powered anomaly detection for unknown threats
- 📧 **Email Alerts**: Instant notifications via SMTP for critical events
- 💬 **Slack Integration**: Real-time alerts to your Slack workspace
- 🌐 **Web Dashboard**: Beautiful real-time visualization of security events
- 💾 **Database Storage**: Historical tracking with SQLite/PostgreSQL
- 📊 **Advanced Reports**: Comprehensive daily/weekly security summaries
- 🐳 **Docker Support**: Easy deployment with Docker Compose
- 🎨 **Rich CLI**: Beautiful command-line interface with progress bars

## Tech Stack

**Core:**
- Python 3.12+
- Regex for pattern matching
- SQLAlchemy for database ORM
- scikit-learn for ML anomaly detection

**Web Stack:**
- Flask for web dashboard
- Chart.js for visualizations
- HTML/CSS/JavaScript

**Integrations:**
- SMTP for email alerts
- Webhooks for Slack/Teams
- Docker for containerization

**CLI:**
- Rich for beautiful terminal UI
- Click for command parsing

## Installation

1. Clone the repository
2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Set up environment variables:
```powershell
copy .env.example .env
# Edit .env with your settings
```

Or configure settings in `config.json`:
```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "recipient_email": "security-team@company.com"
  },
  "monitoring": {
    "log_file_path": "logs/system.log",
    "check_interval_seconds": 60,
    "alert_threshold": 5
  }
}
```

## Usage

### Start Web Dashboard

```powershell
python src/dashboard.py
```

Then open http://localhost:5000 in your browser

### Run the Monitor

```powershell
python src/monitor.py
```

### Generate Daily Report

```powershell
python src/report_generator.py
```

### Enhanced CLI

```powershell
# Analyze logs
python src/cli.py analyze --log-file logs/system.log

# Start monitoring
python src/cli.py monitor

# Generate report
python src/cli.py report

# Start dashboard
python src/cli.py dashboard

# View statistics
python src/cli.py stats
```

### Docker Deployment

```powershell
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Detection Capabilities

### Regex Pattern Detection
- Failed login attempts (brute force attacks)
- SQL injection attempts
- Cross-site scripting (XSS)
- Directory traversal attacks
- Unauthorized access attempts
- Port scanning activities
- Privilege escalation attempts

### Machine Learning Detection
- Anomaly detection for unknown threats
- Behavioral analysis
- Pattern learning from historical data
- Adaptive threat detection

## Project Structure

```
Log Monitoring & Alert System/
├── src/
│   ├── monitor.py           # Main monitoring script
│   ├── log_parser.py        # Log parsing with regex
│   ├── alert_system.py      # SMTP email alerts
│   ├── report_generator.py  # Daily report generation
│   ├── patterns.py          # Security pattern definitions
│   ├── database.py          # Database management
│   ├── ml_detector.py       # ML anomaly detection
│   ├── webhook_notifier.py  # Slack/webhook integration
│   ├── dashboard.py         # Web dashboard API
│   └── cli.py               # Enhanced CLI
├── dashboard/
│   ├── templates/
│   │   └── index.html       # Dashboard HTML
│   └── static/
│       ├── css/
│       │   └── style.css    # Dashboard styles
│       └── js/
│           └── dashboard.js # Dashboard logic
├── logs/
│   └── system.log           # Sample system logs
├── reports/
│   └── (generated reports)
├── models/
│   └── (ML models)
├── tests/
│   └── test_*.py            # Unit tests
├── config.json              # Configuration file
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose config
└── README.md
```

## Configuration

### Email Setup (Gmail)

1. Enable 2-factor authentication in your Gmail account
2. Generate an app-specific password
3. Use the app password in `config.json`

### Log File Path

Update `log_file_path` in `config.json` to point to your actual system logs:
- **Linux**: `/var/log/auth.log`, `/var/log/syslog`
- **Windows**: `C:\Windows\System32\winevt\Logs\Security.evtx` (requires conversion)

## Testing

Run with sample logs:
```bash
python src/monitor.py --test
```

This will process the sample log file and generate test alerts.

## Resume Line

✅ Implemented a Python-based log monitoring system to detect anomalies and generate automated alerts for enterprise security operations.

## Advanced Features

### Web Dashboard
- Real-time event visualization
- Interactive threat charts
- Historical trend analysis
- Top suspicious IPs tracking
- Filterable event tables

### Machine Learning
- Unsupervised anomaly detection
- Pattern learning from logs
- Adaptive threat identification
- Model persistence and retraining

### Integrations
- Slack webhook notifications
- Custom webhook support
- Email alerts with detailed reports
- Database-backed historical tracking

### Docker Support
- One-command deployment
- Microservices architecture
- Automatic restarts
- Volume persistence

## Security Note

⚠️ Keep `config.json` secure and never commit credentials to version control. Use environment variables for production deployments.

## License

MIT License
