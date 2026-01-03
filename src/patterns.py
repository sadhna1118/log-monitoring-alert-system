"""
Security patterns for detecting suspicious activities in logs.
Uses regex patterns to identify common attack vectors.
"""

import re
from typing import Dict, List, Tuple

class SecurityPatterns:
    """Defines regex patterns for detecting security threats."""
    
    # Failed authentication patterns
    FAILED_LOGIN_PATTERNS = [
        r'Failed password for .+ from ([\d.]+)',
        r'authentication failure.*rhost=([\d.]+)',
        r'Invalid user .+ from ([\d.]+)',
        r'Failed login attempt.*from ([\d.]+)',
        r'FAILED LOGIN.*FROM ([\d.]+)',
    ]
    
    # SQL Injection patterns
    SQL_INJECTION_PATTERNS = [
        r"(?i)(union.*select|select.*from.*where|drop.*table|insert.*into|delete.*from)",
        r"(?i)('.*or.*'.*=.*'|'.*or.*1.*=.*1)",
        r"(?i)(exec.*xp_|execute.*sp_|';.*--)",
        r"(?i)(char.*\(|concat.*\(|load_file)",
    ]
    
    # XSS (Cross-Site Scripting) patterns
    XSS_PATTERNS = [
        r"(?i)<script[^>]*>.*?</script>",
        r"(?i)javascript:",
        r"(?i)onerror\s*=",
        r"(?i)onload\s*=",
        r"(?i)<iframe[^>]*>",
    ]
    
    # Directory Traversal patterns
    DIRECTORY_TRAVERSAL_PATTERNS = [
        r"\.\./",
        r"\.\.\\",
        r"%2e%2e/",
        r"\.\.%2f",
    ]
    
    # Unauthorized access patterns
    UNAUTHORIZED_ACCESS_PATTERNS = [
        r"(?i)access denied",
        r"(?i)unauthorized access",
        r"(?i)permission denied",
        r"(?i)403 Forbidden",
        r"(?i)401 Unauthorized",
    ]
    
    # Port scanning patterns
    PORT_SCAN_PATTERNS = [
        r"SYN.*scan.*detected",
        r"Port\s+scan.*from\s+([\d.]+)",
        r"Multiple connection attempts.*from\s+([\d.]+)",
    ]
    
    # Privilege escalation patterns
    PRIVILEGE_ESCALATION_PATTERNS = [
        r"(?i)sudo.*su\s+root",
        r"(?i)privilege.*escalation",
        r"(?i)root.*access.*granted",
        r"su:\s+authentication\s+failure",
    ]
    
    @staticmethod
    def get_all_patterns() -> Dict[str, List[str]]:
        """Returns all security patterns categorized by threat type."""
        return {
            "Failed Login Attempts": SecurityPatterns.FAILED_LOGIN_PATTERNS,
            "SQL Injection": SecurityPatterns.SQL_INJECTION_PATTERNS,
            "Cross-Site Scripting (XSS)": SecurityPatterns.XSS_PATTERNS,
            "Directory Traversal": SecurityPatterns.DIRECTORY_TRAVERSAL_PATTERNS,
            "Unauthorized Access": SecurityPatterns.UNAUTHORIZED_ACCESS_PATTERNS,
            "Port Scanning": SecurityPatterns.PORT_SCAN_PATTERNS,
            "Privilege Escalation": SecurityPatterns.PRIVILEGE_ESCALATION_PATTERNS,
        }
    
    @staticmethod
    def check_patterns(log_line: str) -> List[Tuple[str, str]]:
        """
        Check a log line against all security patterns.
        
        Args:
            log_line: Single line from log file
            
        Returns:
            List of tuples containing (threat_type, matched_pattern)
        """
        matches = []
        
        for threat_type, patterns in SecurityPatterns.get_all_patterns().items():
            for pattern in patterns:
                if re.search(pattern, log_line):
                    matches.append((threat_type, pattern))
        
        return matches