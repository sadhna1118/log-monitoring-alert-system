# Logs Directory

This directory contains log files for monitoring and analysis.

## Files

- `system.log` - Sample log file with various security events for testing
- Your actual log files go here for monitoring

## Usage

### For Testing
The system comes with `system.log` which contains sample security events to test the monitoring system.

### For Production
Point the system to your actual log files by updating `config.json`:

```json
{
  "monitoring": {
    "log_file_path": "logs/your-actual-log-file.log"
  }
}
```

Or use environment variable:
```bash
LOG_FILE_PATH=logs/your-actual-log-file.log
```

## Common Log File Locations

### Linux
- `/var/log/auth.log` - Authentication logs
- `/var/log/syslog` - System logs
- `/var/log/apache2/access.log` - Apache access logs
- `/var/log/nginx/access.log` - Nginx access logs

### Windows
- `C:\Windows\System32\winevt\Logs\Security.evtx` - Security event logs (needs conversion)
- Application logs from Event Viewer

### Copy logs to this directory
```bash
# Linux
sudo cp /var/log/auth.log logs/auth.log

# Windows (PowerShell)
wevtutil qe Security /f:text > logs/security.log
```

## Note
Real log files are gitignored for security reasons (except system.log for demo purposes).