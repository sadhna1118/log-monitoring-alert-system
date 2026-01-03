"""
Log parser module for analyzing system logs and detecting suspicious activities.
"""

import re
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict
from patterns import SecurityPatterns


class LogEntry:
    """Represents a single log entry with metadata."""
    
    def __init__(self, timestamp: str, level: str, message: str, raw_line: str):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.raw_line = raw_line
        self.threats: List[tuple] = []
    
    def add_threat(self, threat_type: str, pattern: str):
        """Add a detected threat to this log entry."""
        self.threats.append((threat_type, pattern))
    
    def is_suspicious(self) -> bool:
        """Check if this log entry contains suspicious activity."""
        return len(self.threats) > 0
    
    def __repr__(self):
        return f"LogEntry(timestamp={self.timestamp}, level={self.level}, threats={len(self.threats)})"


class LogParser:
    """Parses and analyzes log files for security threats."""
    
    def __init__(self):
        self.patterns = SecurityPatterns()
        self.threat_counts = defaultdict(int)
        self.suspicious_ips = defaultdict(int)
    
    def parse_log_line(self, line: str) -> Optional[LogEntry]:
        """
        Parse a single log line and extract metadata.
        
        Args:
            line: Raw log line
            
        Returns:
            LogEntry object or None if parsing fails
        """
        # Try different log formats
        
        # Format 1: Standard syslog format
        # Jan 15 10:23:45 hostname service[pid]: message
        syslog_pattern = r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+\S+\s+(\w+)(?:\[\d+\])?: (.+)'
        match = re.match(syslog_pattern, line)
        if match:
            timestamp, level, message = match.groups()
            return LogEntry(timestamp, level, message, line)
        
        # Format 2: ISO timestamp format
        # 2024-01-15T10:23:45Z [ERROR] message
        iso_pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z?)\s+\[(\w+)\]\s+(.+)'
        match = re.match(iso_pattern, line)
        if match:
            timestamp, level, message = match.groups()
            return LogEntry(timestamp, level, message, line)
        
        # Format 3: Simple format with date
        # [2024-01-15 10:23:45] ERROR: message
        simple_pattern = r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s+(\w+):\s+(.+)'
        match = re.match(simple_pattern, line)
        if match:
            timestamp, level, message = match.groups()
            return LogEntry(timestamp, level, message, line)
        
        # If no pattern matches, create entry with current timestamp
        return LogEntry(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "UNKNOWN",
            line,
            line
        )
    
    def analyze_log_entry(self, log_entry: LogEntry) -> LogEntry:
        """
        Analyze a log entry for security threats.
        
        Args:
            log_entry: LogEntry object to analyze
            
        Returns:
            Updated LogEntry with detected threats
        """
        matches = self.patterns.check_patterns(log_entry.raw_line)
        
        for threat_type, pattern in matches:
            log_entry.add_threat(threat_type, pattern)
            self.threat_counts[threat_type] += 1
        
        # Extract and track suspicious IPs
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, log_entry.raw_line)
        for ip in ips:
            if log_entry.is_suspicious():
                self.suspicious_ips[ip] += 1
        
        return log_entry
    
    def parse_log_file(self, file_path: str) -> List[LogEntry]:
        """
        Parse an entire log file.
        
        Args:
            file_path: Path to log file
            
        Returns:
            List of LogEntry objects
        """
        entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    log_entry = self.parse_log_line(line)
                    if log_entry:
                        log_entry = self.analyze_log_entry(log_entry)
                        entries.append(log_entry)
        
        except FileNotFoundError:
            print(f"Error: Log file not found: {file_path}")
        except Exception as e:
            print(f"Error parsing log file: {str(e)}")
        
        return entries
    
    def get_suspicious_entries(self, entries: List[LogEntry]) -> List[LogEntry]:
        """Filter and return only suspicious log entries."""
        return [entry for entry in entries if entry.is_suspicious()]
    
    def get_statistics(self) -> Dict:
        """Get statistics about detected threats."""
        return {
            "total_threats": sum(self.threat_counts.values()),
            "threats_by_type": dict(self.threat_counts),
            "suspicious_ips": dict(self.suspicious_ips),
            "top_suspicious_ips": sorted(
                self.suspicious_ips.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }
    
    def reset_statistics(self):
        """Reset threat counters."""
        self.threat_counts.clear()
        self.suspicious_ips.clear()