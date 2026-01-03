"""
Webhook notification module for Slack and other services.
"""

import requests
import json
from typing import Dict, List
from datetime import datetime
import os


class WebhookNotifier:
    """Send notifications to webhook endpoints like Slack."""
    
    def __init__(self):
        """Initialize webhook notifier."""
        self.slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL', '')
        self.enable_slack = os.getenv('ENABLE_SLACK_ALERTS', 'false').lower() == 'true'
    
    def send_slack_message(self, message: str, severity: str = "warning") -> bool:
        """
        Send a message to Slack.
        
        Args:
            message: Message text
            severity: Severity level (info, warning, error, critical)
            
        Returns:
            True if message sent successfully
        """
        if not self.enable_slack or not self.slack_webhook_url:
            return False
        
        # Color coding based on severity
        color_map = {
            "info": "#36a64f",      # Green
            "warning": "#ff9800",   # Orange
            "error": "#f44336",     # Red
            "critical": "#9c27b0"   # Purple
        }
        
        color = color_map.get(severity, "#808080")
        
        # Emoji based on severity
        emoji_map = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "🚨",
            "critical": "🔴"
        }
        
        emoji = emoji_map.get(severity, "📢")
        
        payload = {
            "attachments": [{
                "color": color,
                "title": f"{emoji} Security Alert",
                "text": message,
                "footer": "Log Monitoring System",
                "ts": int(datetime.now().timestamp())
            }]
        }
        
        try:
            response = requests.post(
                self.slack_webhook_url,
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Slack notification sent")
                return True
            else:
                print(f"❌ Slack notification failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending Slack notification: {str(e)}")
            return False
    
    def send_threat_alert_slack(self, suspicious_entries: List, statistics: Dict) -> bool:
        """
        Send threat alert to Slack.
        
        Args:
            suspicious_entries: List of suspicious log entries
            statistics: Statistics dictionary
            
        Returns:
            True if alert sent successfully
        """
        if not suspicious_entries:
            return False
        
        threat_count = statistics.get('total_threats', 0)
        
        # Build message
        message_parts = [
            f"*{threat_count} Security Threats Detected*\n",
            "*Threat Breakdown:*"
        ]
        
        # Add threats by type
        for threat_type, count in list(statistics.get('threats_by_type', {}).items())[:5]:
            message_parts.append(f"• {threat_type}: {count}")
        
        # Add top IPs
        message_parts.append("\n*Top Suspicious IPs:*")
        for ip, count in statistics.get('top_suspicious_ips', [])[:3]:
            message_parts.append(f"• {ip}: {count} activities")
        
        # Add sample entries
        message_parts.append("\n*Sample Activity:*")
        for entry in suspicious_entries[:2]:
            message_parts.append(f"• [{entry.level}] {entry.message[:80]}...")
        
        message = "\n".join(message_parts)
        
        # Determine severity
        severity = "critical" if threat_count > 20 else "error" if threat_count > 10 else "warning"
        
        return self.send_slack_message(message, severity)
    
    def send_custom_webhook(self, url: str, payload: Dict) -> bool:
        """
        Send to custom webhook endpoint.
        
        Args:
            url: Webhook URL
            payload: Data to send
            
        Returns:
            True if successful
        """
        try:
            response = requests.post(
                url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            return response.status_code in [200, 201, 202]
            
        except Exception as e:
            print(f"❌ Error sending to webhook: {str(e)}")
            return False