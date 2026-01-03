"""
Alert system for sending email notifications about security events.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
import json


class AlertSystem:
    """Handles email alerts for security events."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize alert system with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.alert_count = 0
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Config file not found: {config_path}")
            return self._get_default_config()
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in config file: {config_path}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipient_email": ""
            },
            "monitoring": {
                "enable_email_alerts": False,
                "alert_threshold": 5
            }
        }
    
    def send_alert(self, subject: str, body: str) -> bool:
        """
        Send an email alert.
        
        Args:
            subject: Email subject
            body: Email body content
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.config["monitoring"].get("enable_email_alerts", False):
            print("Email alerts are disabled in configuration")
            return False
        
        email_config = self.config["email"]
        
        # Validate email configuration
        if not all([
            email_config.get("sender_email"),
            email_config.get("sender_password"),
            email_config.get("recipient_email")
        ]):
            print("Warning: Email configuration incomplete. Please update config.json")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_config["sender_email"]
            msg['To'] = email_config["recipient_email"]
            msg['Subject'] = f"🚨 SECURITY ALERT: {subject}"
            
            # Add timestamp to body
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_body = f"Alert Generated: {timestamp}\n\n{body}"
            
            msg.attach(MIMEText(full_body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(
                email_config["smtp_server"],
                email_config["smtp_port"]
            )
            server.starttls()
            server.login(
                email_config["sender_email"],
                email_config["sender_password"]
            )
            
            text = msg.as_string()
            server.sendmail(
                email_config["sender_email"],
                email_config["recipient_email"],
                text
            )
            server.quit()
            
            self.alert_count += 1
            print(f"✅ Alert email sent successfully: {subject}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Email authentication failed. Check credentials in config.json")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error sending alert: {str(e)}")
            return False
    
    def send_threat_alert(self, suspicious_entries: List, statistics: Dict) -> bool:
        """
        Send alert about detected security threats.
        
        Args:
            suspicious_entries: List of suspicious log entries
            statistics: Statistics dictionary
            
        Returns:
            True if alert sent successfully
        """
        if not suspicious_entries:
            return False
        
        # Check if we've reached the alert threshold
        threshold = self.config["monitoring"].get("alert_threshold", 5)
        threat_count = statistics.get("total_threats", 0)
        
        if threat_count < threshold:
            print(f"Threat count ({threat_count}) below threshold ({threshold}). No alert sent.")
            return False
        
        # Build alert message
        subject = f"{threat_count} Security Threats Detected"
        
        body_lines = [
            "=" * 70,
            "SECURITY THREAT DETECTION REPORT",
            "=" * 70,
            "",
            f"Total Threats Detected: {threat_count}",
            "",
            "THREAT BREAKDOWN:",
            "-" * 70
        ]
        
        # Add threats by type
        for threat_type, count in statistics.get("threats_by_type", {}).items():
            body_lines.append(f"  • {threat_type}: {count}")
        
        body_lines.extend(["", "TOP SUSPICIOUS IP ADDRESSES:", "-" * 70])
        
        # Add top suspicious IPs
        for ip, count in statistics.get("top_suspicious_ips", [])[:5]:
            body_lines.append(f"  • {ip}: {count} suspicious activities")
        
        body_lines.extend(["", "SAMPLE SUSPICIOUS ACTIVITIES:", "-" * 70])
        
        # Add sample log entries
        for entry in suspicious_entries[:5]:
            body_lines.append(f"\n[{entry.timestamp}] {entry.level}")
            body_lines.append(f"  Threats: {', '.join([t[0] for t in entry.threats])}")
            body_lines.append(f"  Log: {entry.message[:100]}...")
        
        body_lines.extend([
            "",
            "=" * 70,
            "RECOMMENDED ACTIONS:",
            "  1. Review the suspicious log entries immediately",
            "  2. Block suspicious IP addresses if necessary",
            "  3. Check for unauthorized access attempts",
            "  4. Verify system integrity",
            "=" * 70
        ])
        
        body = "\n".join(body_lines)
        
        return self.send_alert(subject, body)
    
    def send_daily_report(self, report_content: str) -> bool:
        """
        Send daily security report.
        
        Args:
            report_content: Report content as string
            
        Returns:
            True if report sent successfully
        """
        subject = f"Daily Security Report - {datetime.now().strftime('%Y-%m-%d')}"
        return self.send_alert(subject, report_content)
    
    def get_alert_count(self) -> int:
        """Return the number of alerts sent."""
        return self.alert_count