"""
Unit tests for log parser module.
"""

import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from log_parser import LogParser, LogEntry


class TestLogParser:
    """Test cases for LogParser class."""
    
    def test_parse_syslog_format(self):
        """Test parsing standard syslog format."""
        parser = LogParser()
        line = "Jan 15 10:23:45 hostname sshd[1234]: Failed password for admin from 192.168.1.1"
        
        entry = parser.parse_log_line(line)
        
        assert entry is not None
        assert "10:23:45" in entry.timestamp
        assert entry.level == "sshd"
    
    def test_parse_iso_format(self):
        """Test parsing ISO timestamp format."""
        parser = LogParser()
        line = "2024-01-15T10:23:45Z [ERROR] Database connection failed"
        
        entry = parser.parse_log_line(line)
        
        assert entry is not None
        assert "2024-01-15" in entry.timestamp
        assert entry.level == "ERROR"
        assert "Database" in entry.message
    
    def test_parse_simple_format(self):
        """Test parsing simple bracket format."""
        parser = LogParser()
        line = "[2024-01-15 10:23:45] WARNING: Suspicious activity detected"
        
        entry = parser.parse_log_line(line)
        
        assert entry is not None
        assert entry.level == "WARNING"
        assert "Suspicious" in entry.message
    
    def test_detect_failed_login(self):
        """Test detection of failed login attempts."""
        parser = LogParser()
        line = "[2024-01-15 10:23:45] WARNING: Failed password for admin from 192.168.1.1"
        
        entry = parser.parse_log_line(line)
        entry = parser.analyze_log_entry(entry)
        
        assert entry.is_suspicious()
        assert any("Failed Login" in threat[0] for threat in entry.threats)
    
    def test_detect_sql_injection(self):
        """Test detection of SQL injection attempts."""
        parser = LogParser()
        line = "[2024-01-15 10:23:45] ERROR: Query: SELECT * FROM users WHERE id=1 OR '1'='1'"
        
        entry = parser.parse_log_line(line)
        entry = parser.analyze_log_entry(entry)
        
        assert entry.is_suspicious()
        assert any("SQL Injection" in threat[0] for threat in entry.threats)
    
    def test_detect_xss(self):
        """Test detection of XSS attempts."""
        parser = LogParser()
        line = "[2024-01-15 10:23:45] WARNING: Payload detected: <script>alert('XSS')</script>"
        
        entry = parser.parse_log_line(line)
        entry = parser.analyze_log_entry(entry)
        
        assert entry.is_suspicious()
        assert any("XSS" in threat[0] for threat in entry.threats)
    
    def test_statistics(self):
        """Test statistics gathering."""
        parser = LogParser()
        
        lines = [
            "[2024-01-15 10:23:45] WARNING: Failed password from 192.168.1.1",
            "[2024-01-15 10:23:46] WARNING: Failed password from 192.168.1.1",
            "[2024-01-15 10:23:47] ERROR: SQL injection: SELECT * FROM users WHERE '1'='1'",
        ]
        
        for line in lines:
            entry = parser.parse_log_line(line)
            parser.analyze_log_entry(entry)
        
        stats = parser.get_statistics()
        
        assert stats['total_threats'] > 0
        assert '192.168.1.1' in stats['suspicious_ips']
        assert stats['suspicious_ips']['192.168.1.1'] >= 2
    
    def test_get_suspicious_entries(self):
        """Test filtering suspicious entries."""
        parser = LogParser()
        
        entries = [
            parser.analyze_log_entry(parser.parse_log_line(
                "[2024-01-15 10:23:45] INFO: Normal log entry"
            )),
            parser.analyze_log_entry(parser.parse_log_line(
                "[2024-01-15 10:23:46] WARNING: Failed password from 192.168.1.1"
            )),
        ]
        
        suspicious = parser.get_suspicious_entries(entries)
        
        assert len(suspicious) == 1
        assert suspicious[0].is_suspicious()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])