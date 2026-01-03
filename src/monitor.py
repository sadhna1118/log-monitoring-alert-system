"""
Main monitoring script for continuous log analysis.
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict
from log_parser import LogParser
from alert_system import AlertSystem
from report_generator import ReportGenerator
from database import DatabaseManager
from webhook_notifier import WebhookNotifier
from ml_detector import MLAnomalyDetector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LogMonitor:
    """Main monitoring class for continuous log analysis."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize log monitor.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.parser = LogParser()
        self.alert_system = AlertSystem(config_path)
        self.report_generator = ReportGenerator(config_path)
        self.db = DatabaseManager()
        self.webhook = WebhookNotifier()
        self.ml_detector = MLAnomalyDetector()
        self.last_position = 0
        self.running = True
        
        # Enable ML if configured
        self.enable_ml = os.getenv('ENABLE_ML_DETECTION', 'true').lower() == 'true'
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found: {config_path}")
            print("Please create config.json with proper settings.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in configuration file: {config_path}")
            sys.exit(1)
    
    def check_new_logs(self, log_file_path: str) -> bool:
        """
        Check for new log entries since last check.
        
        Args:
            log_file_path: Path to log file
            
        Returns:
            True if new logs detected and analyzed
        """
        if not os.path.exists(log_file_path):
            print(f"Warning: Log file not found: {log_file_path}")
            return False
        
        try:
            file_size = os.path.getsize(log_file_path)
            
            # Check if file has grown
            if file_size <= self.last_position:
                return False
            
            # Read new lines
            with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()
            
            if not new_lines:
                return False
            
            # Analyze new log entries
            suspicious_entries = []
            for line in new_lines:
                line = line.strip()
                if not line:
                    continue
                
                log_entry = self.parser.parse_log_line(line)
                if log_entry:
                    log_entry = self.parser.analyze_log_entry(log_entry)
                    
                    # ML anomaly detection
                    if self.enable_ml and self.ml_detector.is_trained:
                        is_anomaly, score = self.ml_detector.predict(log_entry.raw_line)
                        if is_anomaly and score > 0.5:
                            log_entry.add_threat('ML Anomaly Detection', f'Score: {score:.2f}')
                    
                    # Store in database
                    self.db.add_security_event(log_entry)
                    
                    if log_entry.is_suspicious():
                        suspicious_entries.append(log_entry)
                        print(f"⚠️  Suspicious activity detected:")
                        print(f"    [{log_entry.timestamp}] {log_entry.message[:80]}")
                        print(f"    Threats: {', '.join([t[0] for t in log_entry.threats])}")
            
            # Send alerts if suspicious activities found
            if suspicious_entries:
                statistics = self.parser.get_statistics()
                
                # Update daily statistics
                today = datetime.now().strftime('%Y-%m-%d')
                self.db.update_daily_statistics(statistics, today)
                
                # Send email alert
                self.alert_system.send_threat_alert(suspicious_entries, statistics)
                
                # Send webhook notification
                self.webhook.send_threat_alert_slack(suspicious_entries, statistics)
            
            return True
            
        except Exception as e:
            print(f"Error checking logs: {str(e)}")
            return False
    
    def run_continuous_monitoring(self):
        """Run continuous monitoring loop."""
        log_file_path = self.config["monitoring"]["log_file_path"]
        check_interval = self.config["monitoring"]["check_interval_seconds"]
        
        print("=" * 80)
        print("LOG MONITORING & ALERT SYSTEM")
        print("=" * 80)
        print(f"Monitoring: {log_file_path}")
        print(f"Check Interval: {check_interval} seconds")
        print(f"Email Alerts: {'Enabled' if self.config['monitoring'].get('enable_email_alerts') else 'Disabled'}")
        print("=" * 80)
        print("Press Ctrl+C to stop monitoring...")
        print()
        
        try:
            while self.running:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Checking for new log entries...")
                
                self.check_new_logs(log_file_path)
                
                time.sleep(check_interval)
        
        except KeyboardInterrupt:
            print("\n\n" + "=" * 80)
            print("Monitoring stopped by user")
            self.print_summary()
        except Exception as e:
            print(f"\nError during monitoring: {str(e)}")
            self.print_summary()
    
    def run_one_time_analysis(self, log_file_path: str = None):
        """
        Run one-time analysis of log file.
        
        Args:
            log_file_path: Optional custom log file path
        """
        if log_file_path is None:
            log_file_path = self.config["monitoring"]["log_file_path"]
        
        print("=" * 80)
        print("LOG ANALYSIS - ONE-TIME SCAN")
        print("=" * 80)
        print(f"Analyzing: {log_file_path}")
        print()
        
        # Parse all log entries
        log_entries = self.parser.parse_log_file(log_file_path)
        
        # Train ML model if not trained
        if self.enable_ml and not self.ml_detector.is_trained:
            print("Training ML model on historical data...")
            self.ml_detector.train([e.raw_line for e in log_entries])
        
        # Store events in database
        for entry in log_entries:
            self.db.add_security_event(entry)
        
        suspicious_entries = self.parser.get_suspicious_entries(log_entries)
        statistics = self.parser.get_statistics()
        
        # Update statistics
        today = datetime.now().strftime('%Y-%m-%d')
        self.db.update_daily_statistics(statistics, today)
        
        # Display results
        print(f"✅ Analysis Complete!")
        print(f"   Total entries: {len(log_entries)}")
        print(f"   Suspicious activities: {len(suspicious_entries)}")
        print(f"   Total threats: {statistics['total_threats']}")
        print()
        
        if suspicious_entries:
            print("SUSPICIOUS ACTIVITIES:")
            print("-" * 80)
            for entry in suspicious_entries[:10]:
                print(f"[{entry.timestamp}] {entry.message[:70]}")
                print(f"  Threats: {', '.join([t[0] for t in entry.threats])}")
                print()
        
        # Generate report
        report_content = self.report_generator.generate_report(log_entries, statistics)
        report_path = self.report_generator.save_report(report_content)
        
        # Send alerts if configured
        if self.config["monitoring"].get("enable_email_alerts"):
            self.alert_system.send_threat_alert(suspicious_entries, statistics)
        
        # Send webhook notification
        self.webhook.send_threat_alert_slack(suspicious_entries, statistics)
        
        self.print_summary()
    
    def print_summary(self):
        """Print monitoring summary."""
        statistics = self.parser.get_statistics()
        
        print("=" * 80)
        print("MONITORING SUMMARY")
        print("=" * 80)
        print(f"Total Threats Detected: {statistics['total_threats']}")
        print(f"Alerts Sent: {self.alert_system.get_alert_count()}")
        print()
        
        if statistics['threats_by_type']:
            print("Threats by Type:")
            for threat_type, count in statistics['threats_by_type'].items():
                print(f"  • {threat_type}: {count}")
            print()
        
        if statistics['top_suspicious_ips']:
            print("Top Suspicious IPs:")
            for ip, count in statistics['top_suspicious_ips'][:5]:
                print(f"  • {ip}: {count} activities")
        
        print("=" * 80)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Log Monitoring & Alert System"
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run one-time analysis on sample log file'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        help='Custom log file path'
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help='Configuration file path'
    )
    
    args = parser.parse_args()
    
    monitor = LogMonitor(args.config)
    
    if args.test:
        log_file = args.log_file if args.log_file else 'logs/system.log'
        monitor.run_one_time_analysis(log_file)
    else:
        monitor.run_continuous_monitoring()


if __name__ == "__main__":
    main()