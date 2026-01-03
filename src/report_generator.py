"""
Report generator for creating daily security summaries.
"""

import os
import json
from datetime import datetime
from typing import List, Dict
from log_parser import LogParser, LogEntry


class ReportGenerator:
    """Generates comprehensive security reports."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize report generator.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.report_dir = self.config.get("reporting", {}).get("report_directory", "reports")
        self._ensure_report_directory()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return {"reporting": {"report_directory": "reports"}}
    
    def _ensure_report_directory(self):
        """Create reports directory if it doesn't exist."""
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def generate_report(self, log_entries: List[LogEntry], statistics: Dict) -> str:
        """
        Generate a comprehensive security report.
        
        Args:
            log_entries: List of log entries analyzed
            statistics: Statistics from log analysis
            
        Returns:
            Report content as string
        """
        suspicious_entries = [entry for entry in log_entries if entry.is_suspicious()]
        
        report_lines = [
            "=" * 80,
            "SECURITY LOG ANALYSIS REPORT",
            "=" * 80,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 80,
            f"Total Log Entries Analyzed: {len(log_entries)}",
            f"Suspicious Activities Detected: {len(suspicious_entries)}",
            f"Total Security Threats: {statistics.get('total_threats', 0)}",
            f"Unique Suspicious IPs: {len(statistics.get('suspicious_ips', {}))}",
            "",
            "THREAT ANALYSIS BY CATEGORY",
            "-" * 80
        ]
        
        # Add threat breakdown
        threats_by_type = statistics.get("threats_by_type", {})
        if threats_by_type:
            for threat_type, count in sorted(threats_by_type.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / statistics['total_threats'] * 100) if statistics['total_threats'] > 0 else 0
                report_lines.append(f"  • {threat_type}: {count} ({percentage:.1f}%)")
        else:
            report_lines.append("  No threats detected")
        
        report_lines.extend([
            "",
            "TOP 10 SUSPICIOUS IP ADDRESSES",
            "-" * 80
        ])
        
        # Add top suspicious IPs
        top_ips = statistics.get("top_suspicious_ips", [])
        if top_ips:
            for i, (ip, count) in enumerate(top_ips, 1):
                report_lines.append(f"  {i:2d}. {ip:15s} - {count} suspicious activities")
        else:
            report_lines.append("  No suspicious IPs detected")
        
        report_lines.extend([
            "",
            "DETAILED SUSPICIOUS ACTIVITIES",
            "-" * 80
        ])
        
        # Add sample suspicious entries
        if suspicious_entries:
            for i, entry in enumerate(suspicious_entries[:20], 1):
                report_lines.append(f"\n{i}. [{entry.timestamp}] {entry.level}")
                report_lines.append(f"   Threats: {', '.join([t[0] for t in entry.threats])}")
                report_lines.append(f"   Message: {entry.message[:120]}")
        else:
            report_lines.append("  No suspicious activities detected")
        
        report_lines.extend([
            "",
            "=" * 80,
            "SECURITY RECOMMENDATIONS",
            "-" * 80,
            "  1. Review and investigate all suspicious IP addresses",
            "  2. Implement IP blocking for repeated failed login attempts",
            "  3. Enable two-factor authentication for all accounts",
            "  4. Update security policies and access controls",
            "  5. Conduct security awareness training for staff",
            "  6. Review and update firewall rules",
            "  7. Monitor for privilege escalation attempts",
            "  8. Implement intrusion detection system (IDS)",
            "",
            "=" * 80,
            "END OF REPORT",
            "=" * 80
        ])
        
        return "\n".join(report_lines)
    
    def save_report(self, report_content: str, filename: str = None) -> str:
        """
        Save report to file.
        
        Args:
            report_content: Report content as string
            filename: Optional custom filename
            
        Returns:
            Path to saved report file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_report_{timestamp}.txt"
        
        filepath = os.path.join(self.report_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📊 Report saved: {filepath}")
        return filepath
    
    def generate_and_save_report(self, log_file_path: str) -> str:
        """
        Generate and save a complete security report.
        
        Args:
            log_file_path: Path to log file to analyze
            
        Returns:
            Path to saved report file
        """
        print(f"Analyzing log file: {log_file_path}")
        
        parser = LogParser()
        log_entries = parser.parse_log_file(log_file_path)
        statistics = parser.get_statistics()
        
        report_content = self.generate_report(log_entries, statistics)
        report_path = self.save_report(report_content)
        
        print(f"✅ Report generation complete!")
        print(f"   Total entries analyzed: {len(log_entries)}")
        print(f"   Suspicious activities: {len([e for e in log_entries if e.is_suspicious()])}")
        print(f"   Total threats: {statistics.get('total_threats', 0)}")
        
        return report_path


def main():
    """Main function for standalone report generation."""
    import sys
    
    # Default log file path
    log_file = "logs/system.log"
    
    # Allow custom log file path from command line
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    
    print("=" * 80)
    print("SECURITY REPORT GENERATOR")
    print("=" * 80)
    print()
    
    generator = ReportGenerator()
    generator.generate_and_save_report(log_file)


if __name__ == "__main__":
    main()