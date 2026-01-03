# 🚀 HOW TO RUN - Log Monitoring & Alert System

## Quick Reference - 4 Ways to Run

### Option 1️⃣: Run Demo (Easiest - See Everything)
```powershell
python demo.py
```
**What it does:** Shows all features in 5 interactive demos. Press Enter to continue through each demo.

---

### Option 2️⃣: Web Dashboard (Visual Monitoring)
```powershell
python src/dashboard.py
```
**What it does:** 
- Starts web server at http://localhost:5000
- Shows real-time statistics
- Displays threat charts
- Lists all security events
- Auto-refreshes every 30 seconds

**Access:** Open your browser to **http://localhost:5000**

---

### Option 3️⃣: Monitor Logs (Continuous Monitoring)
```powershell
# Test mode - Run once
python src/monitor.py --test

# Production mode - Run continuously (checks every 60 seconds)
python src/monitor.py
```
**What it does:**
- Monitors log files for threats
- Sends email alerts (if configured)
- Stores events in database
- Runs until you stop it (Ctrl+C)

---

### Option 4️⃣: Command-Line Analysis (One-Time)
```powershell
python src/cli.py analyze --log-file logs/system.log
```
**What it does:**
- Analyzes the log file once
- Shows statistics and threats
- Beautiful CLI output with progress bars
- No continuous monitoring

---

## Complete Step-by-Step Guide

### Step 1: First Time Setup (Do This Once)

```powershell
# Run setup script
python setup.py
```

This creates all necessary folders and checks dependencies.

---

### Step 2: Configure Email (Optional)

If you want email alerts:

```powershell
# Edit configuration
notepad .env
```

Update these lines:
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password
RECIPIENT_EMAIL=security-team@company.com
ENABLE_EMAIL_ALERTS=true
```

**Get Gmail App Password:**
1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Create App Password for "Mail"
4. Copy the 16-character password
5. Paste into SENDER_PASSWORD above

---

### Step 3: Choose Your Mode

#### Mode A: Quick Demo (Best for First Time)
```powershell
python demo.py
```
Press Enter to go through 5 demos.

#### Mode B: Web Dashboard (Best for Monitoring)
```powershell
# Terminal 1: Start Dashboard
python src/dashboard.py

# Open browser to: http://localhost:5000
```

Leave this running, it will show live data!

#### Mode C: Continuous Monitoring (24/7)
```powershell
python src/monitor.py
```

This runs forever, checking logs every 60 seconds.

#### Mode D: One-Time Analysis
```powershell
python src/cli.py analyze --log-file logs/system.log
```

Analyze once and exit.

---

## Using with Your Own Logs

### Windows Event Logs
```powershell
# Export Windows Security logs
wevtutil qe Security /f:text > logs/windows_security.log

# Edit config to use your log
notepad config.json
```

Change the log path:
```json
{
  "monitoring": {
    "log_file_path": "logs/windows_security.log"
  }
}
```

Then run:
```powershell
python src/monitor.py
```

### Application Logs
```powershell
# Just point to any text log file
$env:LOG_FILE_PATH="C:\path\to\your\app.log"
python src/monitor.py
```

---

## All Available Commands

| Command | What It Does |
|---------|--------------|
| `python demo.py` | Interactive demo of all features |
| `python src/dashboard.py` | Start web dashboard (http://localhost:5000) |
| `python src/monitor.py --test` | Test monitoring (run once) |
| `python src/monitor.py` | Continuous monitoring (24/7) |
| `python src/cli.py analyze --log-file logs/system.log` | Analyze a log file |
| `python src/cli.py report` | Generate security report |
| `python src/cli.py stats` | View statistics |
| `python src/cli.py monitor` | Start monitoring via CLI |
| `python src/cli.py dashboard` | Start dashboard via CLI |
| `docker-compose up -d` | Run with Docker (all services) |

---

## Docker Deployment (Advanced)

```powershell
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

Access dashboard at: http://localhost:5000

---

## Common Scenarios

### "I want to see it work NOW"
```powershell
python demo.py
```

### "I want a web interface"
```powershell
python src/dashboard.py
# Then open http://localhost:5000
```

### "I want to monitor my server logs"
```powershell
# Copy your logs to logs/ folder
copy C:\MyServer\logs\*.log logs\myserver.log

# Edit config.json to point to your log
notepad config.json

# Start monitoring
python src/monitor.py
```

### "I want email alerts"
1. Configure email in `.env` file
2. Run: `python src/monitor.py`
3. System sends email when 5+ threats found

### "I want to analyze logs once"
```powershell
python src/cli.py analyze --log-file logs/system.log
```

### "I want a security report"
```powershell
python src/cli.py report
# Report saved to reports/ folder
```

---

## Stop Running Services

### Stop Dashboard or Monitor
Press **Ctrl+C** in the terminal

### Stop Docker Services
```powershell
docker-compose down
```

---

## Troubleshooting

### "Port 5000 already in use"
```powershell
# Use different port
$env:DASHBOARD_PORT="5001"
python src/dashboard.py
```

### "Module not found"
```powershell
# Install dependencies
pip install -r requirements.txt
```

### "No threats detected"
- Use sample logs first: `python src/monitor.py --test`
- Check if log file exists
- Verify log file has content

### "Email not working"
- Check Gmail app password (not regular password)
- Verify SMTP settings in .env
- Test with `--test` mode first

---

## What's Running Right Now

**Currently Active:**
- ✅ Dashboard server at http://127.0.0.1:5000 (execution id: toolu_e83fc78936)

**To stop it:**
Press Ctrl+C in the terminal where it's running

---

## Next Steps

1. ✅ **Try the demo first**: `python demo.py`
2. ✅ **Open the dashboard**: Already running at http://localhost:5000
3. ✅ **Configure email alerts**: Edit `.env` file
4. ✅ **Point to your logs**: Edit `config.json`
5. ✅ **Start monitoring**: `python src/monitor.py`

---

## Need More Help?

- **Quick Start**: See [QUICK_START.md](QUICK_START.md)
- **Examples**: See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
- **Setup Details**: See [SETUP.md](SETUP.md)
- **Features**: See [README.md](README.md)

---

## TL;DR - Fastest Way to Run

```powershell
# See demo
python demo.py

# Or open web dashboard (already running)
# Just open browser: http://localhost:5000
```

**That's it! Your system is ready to use!** 🎉