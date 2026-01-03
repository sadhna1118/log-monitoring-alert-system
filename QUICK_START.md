# 🚀 Quick Start Guide - Log Monitoring & Alert System

## Step 1: Run Demo (Fastest Way to See It Working)

```powershell
python demo.py
```

This runs 5 interactive demos showing all features. **Press Enter** to go through each demo.

---

## Step 2: Configure Your Email (Optional but Recommended)

### Option A: Using .env file (Recommended)
```powershell
# Edit the .env file
notepad .env
```

Update these values:
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password
RECIPIENT_EMAIL=where-to-send-alerts@company.com
ENABLE_EMAIL_ALERTS=true
```

### Option B: Using config.json
```powershell
notepad config.json
```

Update the email section:
```json
{
  "email": {
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-gmail-app-password",
    "recipient_email": "where-to-send-alerts@company.com"
  }
}
```

### How to Get Gmail App Password:
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Go to App passwords
4. Generate password for "Mail"
5. Copy the 16-character password
6. Use this in config (NOT your regular Gmail password)

---

## Step 3: Choose Your Usage Mode

### Mode 1: 🌐 Web Dashboard (Best for Monitoring)

Start the dashboard:
```powershell
python src/dashboard.py
```

Then open your browser to:
```
http://localhost:5000
```

**What you'll see:**
- Real-time statistics
- Threat distribution charts
- Top suspicious IPs
- Event timeline
- Auto-refresh every 30 seconds

---

### Mode 2: 🔍 One-Time Log Analysis

Analyze any log file:
```powershell
python src/cli.py analyze --log-file logs/system.log
```

This will:
- Parse the entire log file
- Detect all threats
- Show statistics
- Display suspicious entries
- No ongoing monitoring

---

### Mode 3: ⏰ Continuous Monitoring

Start 24/7 monitoring:
```powershell
python src/monitor.py
```

This will:
- Monitor logs every 60 seconds (configurable)
- Detect new threats in real-time
- Send email alerts when threshold reached
- Store events in database
- Keep running until you stop it (Ctrl+C)

**Test mode** (processes sample log once):
```powershell
python src/monitor.py --test
```

---

### Mode 4: 📊 Generate Security Report

Create a detailed report:
```powershell
python src/report_generator.py logs/system.log
```

This generates:
- Executive summary
- Threat breakdown by type
- Top suspicious IPs
- Sample suspicious activities
- Recommendations
- Saved to `reports/` folder

---

## Step 4: Using with Your Own Logs

### Windows Event Logs
```powershell
# Export Security logs
wevtutil qe Security /f:text > logs/windows_security.log

# Update config to point to your log
notepad config.json
```

Change:
```json
{
  "monitoring": {
    "log_file_path": "logs/windows_security.log"
  }
}
```

### Application Logs
Just point to any text log file:
```json
{
  "monitoring": {
    "log_file_path": "C:/path/to/your/app.log"
  }
}
```

Or use environment variable:
```powershell
$env:LOG_FILE_PATH="C:/path/to/your/app.log"
python src/monitor.py
```

---

## Step 5: Advanced Features

### Enable Slack Notifications

1. Create Slack webhook:
   - Go to https://api.slack.com/apps
   - Create app → Incoming Webhooks
   - Copy webhook URL

2. Update .env:
```env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
ENABLE_SLACK_ALERTS=true
```

3. Restart monitor - alerts will go to Slack!

---

### Using Machine Learning Detection

ML is enabled by default. To see it in action:

```powershell
# First run trains the model
python src/monitor.py --test

# Model saved to models/anomaly_detector.pkl
# Future runs use the trained model
```

The ML detector learns from your logs and detects unusual patterns that don't match regex rules.

---

### Using Enhanced CLI

Beautiful command-line interface with progress bars:

```powershell
# Analyze with visual feedback
python src/cli.py analyze --log-file logs/system.log

# Start monitoring
python src/cli.py monitor

# Generate report
python src/cli.py report

# View statistics
python src/cli.py stats

# Start dashboard
python src/cli.py dashboard
```

---

## Step 6: Docker Deployment (For Production)

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access dashboard at: http://localhost:5000

---

## Common Usage Scenarios

### Scenario 1: "I just want to see it work"
```powershell
python demo.py
```

### Scenario 2: "Monitor my application logs"
1. Copy your log to `logs/myapp.log`
2. Update `config.json` to point to `logs/myapp.log`
3. Run: `python src/monitor.py`

### Scenario 3: "I want a web dashboard"
```powershell
python src/dashboard.py
# Open http://localhost:5000
```

### Scenario 4: "Generate a security report"
```powershell
python src/cli.py report
# Check reports/ folder
```

### Scenario 5: "Get email alerts for threats"
1. Configure email in .env
2. Run: `python src/monitor.py`
3. Wait for threats to be detected
4. Get email when threshold reached

---

## Troubleshooting

### "No threats detected"
- Make sure log file has content
- Check log format matches expected patterns
- Try with sample logs first: `logs/system.log`

### "Email not sending"
- Verify Gmail app password (not regular password)
- Check SMTP settings
- Enable 2-factor authentication first
- Test with `--test` mode first

### "Dashboard won't start"
- Check if port 5000 is free
- Try different port: `$env:DASHBOARD_PORT="5001"`
- Kill any existing Python processes

### "Import errors"
- Run: `pip install -r requirements.txt`
- Make sure you're in project directory

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Run demo | `python demo.py` |
| Start dashboard | `python src/dashboard.py` |
| Monitor logs | `python src/monitor.py` |
| Test monitoring | `python src/monitor.py --test` |
| Analyze logs | `python src/cli.py analyze --log-file logs/system.log` |
| Generate report | `python src/cli.py report` |
| View stats | `python src/cli.py stats` |
| Docker deploy | `docker-compose up -d` |

---

## Next Steps

1. ✅ Run the demo: `python demo.py`
2. ✅ Try the dashboard: `python src/dashboard.py`
3. ✅ Configure your email alerts
4. ✅ Point to your real logs
5. ✅ Start monitoring: `python src/monitor.py`

---

## Need Help?

- Check [SETUP.md](SETUP.md) for detailed setup
- See [README.md](README.md) for feature overview
- Read [ENTERPRISE_FEATURES.md](ENTERPRISE_FEATURES.md) for advanced features
- Review [PROJECT_STATUS.md](PROJECT_STATUS.md) for completion status

**Enjoy your enterprise-grade log monitoring system!** 🎉