"""
Demo script to showcase the Log Monitoring & Alert System capabilities.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from log_parser import LogParser
from alert_system import AlertSystem
from report_generator import ReportGenerator


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_log_parsing():
    """Demonstrate log parsing capabilities."""
    print_section("DEMO 1: LOG PARSING & THREAT DETECTION")
    
    parser = LogParser()
    
    # Sample log entries with various threats
    sample_logs = [
        "[2024-01-15 10:23:45] INFO: User admin logged in successfully",
        "[2024-01-15 10:24:12] WARNING: Failed password for user test from 203.0.113.45",
        "[2024-01-15 10:25:30] ERROR: SQL injection attempt: SELECT * FROM users WHERE '1'='1'",
        "[2024-01-15 10:26:15] WARNING: XSS detected: <script>alert('hack')</script>",
        "[2024-01-15 10:27:00] ERROR: Directory traversal: ../../etc/passwd",
    ]
    
    print("Analyzing sample log entries...\n")
    
    for log_line in sample_logs:
        entry = parser.parse_log_line(log_line)
        entry = parser.analyze_log_entry(entry)
        
        status = "🚨 SUSPICIOUS" if entry.is_suspicious() else "✅ NORMAL"
        print(f"{status} | {log_line[:70]}")
        
        if entry.threats:
            for threat_type, _ in entry.threats:
                print(f"         ⚠️  Threat: {threat_type}")
        print()


def demo_statistics():
    """Demonstrate statistics gathering."""
    print_section("DEMO 2: THREAT STATISTICS & ANALYSIS")
    
    parser = LogParser()
    log_file = "logs/system.log"
    
    print(f"Analyzing complete log file: {log_file}\n")
    
    entries = parser.parse_log_file(log_file)
    suspicious = parser.get_suspicious_entries(entries)
    stats = parser.get_statistics()
    
    print(f"📊 Total Log Entries: {len(entries)}")
    print(f"🚨 Suspicious Activities: {len(suspicious)}")
    print(f"⚠️  Total Threats: {stats['total_threats']}\n")
    
    print("Threat Breakdown:")
    print("-" * 80)
    for threat_type, count in sorted(stats['threats_by_type'].items(), key=lambda x: x[1], reverse=True):
        bar = "█" * min(count, 40)
        print(f"  {threat_type:30s} | {bar} {count}")
    
    print("\n" + "Top Suspicious IP Addresses:")
    print("-" * 80)
    for i, (ip, count) in enumerate(stats['top_suspicious_ips'][:5], 1):
        print(f"  {i}. {ip:15s} → {count} suspicious activities")


def demo_pattern_detection():
    """Demonstrate specific threat pattern detection."""
    print_section("DEMO 3: SECURITY PATTERN DETECTION")
    
    from patterns import SecurityPatterns
    
    patterns = SecurityPatterns.get_all_patterns()
    
    print("Configured Security Patterns:\n")
    
    for threat_type, pattern_list in patterns.items():
        print(f"🔍 {threat_type}")
        print(f"   → {len(pattern_list)} detection patterns configured")
        print(f"   → Sample: {pattern_list[0][:60]}...")
        print()


def demo_report_generation():
    """Demonstrate report generation."""
    print_section("DEMO 4: SECURITY REPORT GENERATION")
    
    print("Generating comprehensive security report...\n")
    
    generator = ReportGenerator()
    report_path = generator.generate_and_save_report("logs/system.log")
    
    print(f"\n✅ Report saved to: {report_path}")
    print("\nReport Preview:")
    print("-" * 80)
    
    # Show first 30 lines of the report
    with open(report_path, 'r') as f:
        lines = f.readlines()[:30]
        for line in lines:
            print(line.rstrip())
    
    print("\n... (truncated for demo)")


def demo_alert_system():
    """Demonstrate alert system (without actually sending email)."""
    print_section("DEMO 5: EMAIL ALERT SYSTEM")
    
    alert_system = AlertSystem()
    
    print("Alert System Configuration:")
    print("-" * 80)
    print(f"  SMTP Server: {alert_system.config['email']['smtp_server']}")
    print(f"  SMTP Port: {alert_system.config['email']['smtp_port']}")
    print(f"  Email Alerts: {'Enabled' if alert_system.config['monitoring'].get('enable_email_alerts') else 'Disabled'}")
    print(f"  Alert Threshold: {alert_system.config['monitoring'].get('alert_threshold', 5)} threats")
    print()
    
    print("📧 Alert Types:")
    print("  1. Real-time threat alerts")
    print("  2. Daily security reports")
    print("  3. Critical incident notifications")
    print()
    
    if not alert_system.config['monitoring'].get('enable_email_alerts'):
        print("⚠️  Note: Email alerts are currently disabled in config.json")
        print("   To enable, update config.json and add your email credentials")
    else:
        print("✅ Email alerts are configured and ready")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "LOG MONITORING & ALERT SYSTEM - DEMO" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        demo_log_parsing()
        input("\nPress Enter to continue to next demo...")
        
        demo_pattern_detection()
        input("\nPress Enter to continue to next demo...")
        
        demo_statistics()
        input("\nPress Enter to continue to next demo...")
        
        demo_report_generation()
        input("\nPress Enter to continue to next demo...")
        
        demo_alert_system()
        
        print_section("DEMO COMPLETE")
        print("✅ All demos executed successfully!")
        print("\nNext Steps:")
        print("  1. Configure email settings in config.json")
        print("  2. Run: python src/monitor.py --test")
        print("  3. Review generated reports in reports/ directory")
        print("  4. Start monitoring: python src/monitor.py")
        print("\n" + "=" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {str(e)}")


if __name__ == "__main__":
    main()