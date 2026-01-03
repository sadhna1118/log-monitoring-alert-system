"""
Database module for storing and retrieving security events.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class SecurityEvent(Base):
    """Model for security events."""
    
    __tablename__ = 'security_events'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    log_timestamp = Column(String(50))
    log_level = Column(String(20))
    message = Column(Text)
    raw_log = Column(Text)
    is_suspicious = Column(Boolean, default=False)
    threat_types = Column(String(500))  # Comma-separated
    source_ip = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<SecurityEvent(id={self.id}, timestamp={self.log_timestamp}, threats={self.threat_types})>"


class ThreatStatistics(Base):
    """Model for threat statistics."""
    
    __tablename__ = 'threat_statistics'
    
    id = Column(Integer, primary_key=True)
    date = Column(String(20), unique=True)
    total_threats = Column(Integer, default=0)
    failed_logins = Column(Integer, default=0)
    sql_injections = Column(Integer, default=0)
    xss_attempts = Column(Integer, default=0)
    directory_traversal = Column(Integer, default=0)
    unauthorized_access = Column(Integer, default=0)
    port_scans = Column(Integer, default=0)
    privilege_escalation = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<ThreatStatistics(date={self.date}, total={self.total_threats})>"


class DatabaseManager:
    """Manages database operations."""
    
    def __init__(self, database_url: str = None):
        """Initialize database manager."""
        if database_url is None:
            database_url = os.getenv('DATABASE_URL', 'sqlite:///security_logs.db')
        
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_security_event(self, log_entry) -> SecurityEvent:
        """Add a security event to database."""
        import re
        
        # Extract IP address
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, log_entry.raw_line)
        source_ip = ips[0] if ips else None
        
        # Get threat types
        threat_types = ','.join([t[0] for t in log_entry.threats])
        
        event = SecurityEvent(
            log_timestamp=log_entry.timestamp,
            log_level=log_entry.level,
            message=log_entry.message,
            raw_log=log_entry.raw_line,
            is_suspicious=log_entry.is_suspicious(),
            threat_types=threat_types,
            source_ip=source_ip
        )
        
        self.session.add(event)
        self.session.commit()
        
        return event
    
    def get_recent_events(self, limit: int = 100):
        """Get recent security events."""
        return self.session.query(SecurityEvent)\
            .order_by(SecurityEvent.created_at.desc())\
            .limit(limit)\
            .all()
    
    def get_suspicious_events(self, limit: int = 100):
        """Get suspicious events."""
        return self.session.query(SecurityEvent)\
            .filter(SecurityEvent.is_suspicious == True)\
            .order_by(SecurityEvent.created_at.desc())\
            .limit(limit)\
            .all()
    
    def get_events_by_date(self, date_str: str):
        """Get events for a specific date."""
        return self.session.query(SecurityEvent)\
            .filter(SecurityEvent.log_timestamp.like(f'{date_str}%'))\
            .all()
    
    def update_daily_statistics(self, statistics: dict, date_str: str = None):
        """Update daily threat statistics."""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Check if record exists
        stat = self.session.query(ThreatStatistics)\
            .filter(ThreatStatistics.date == date_str)\
            .first()
        
        if stat is None:
            stat = ThreatStatistics(date=date_str)
        
        # Update statistics
        stat.total_threats = statistics.get('total_threats', 0)
        
        threats_by_type = statistics.get('threats_by_type', {})
        stat.failed_logins = threats_by_type.get('Failed Login Attempts', 0)
        stat.sql_injections = threats_by_type.get('SQL Injection', 0)
        stat.xss_attempts = threats_by_type.get('Cross-Site Scripting (XSS)', 0)
        stat.directory_traversal = threats_by_type.get('Directory Traversal', 0)
        stat.unauthorized_access = threats_by_type.get('Unauthorized Access', 0)
        stat.port_scans = threats_by_type.get('Port Scanning', 0)
        stat.privilege_escalation = threats_by_type.get('Privilege Escalation', 0)
        
        self.session.add(stat)
        self.session.commit()
        
        return stat
    
    def get_statistics_by_date_range(self, start_date: str, end_date: str):
        """Get statistics for a date range."""
        return self.session.query(ThreatStatistics)\
            .filter(ThreatStatistics.date >= start_date)\
            .filter(ThreatStatistics.date <= end_date)\
            .order_by(ThreatStatistics.date)\
            .all()
    
    def get_top_ips(self, limit: int = 10):
        """Get top suspicious IP addresses."""
        from sqlalchemy import func
        
        return self.session.query(
            SecurityEvent.source_ip,
            func.count(SecurityEvent.id).label('count')
        )\
        .filter(SecurityEvent.is_suspicious == True)\
        .filter(SecurityEvent.source_ip.isnot(None))\
        .group_by(SecurityEvent.source_ip)\
        .order_by(func.count(SecurityEvent.id).desc())\
        .limit(limit)\
        .all()
    
    def close(self):
        """Close database connection."""
        self.session.close()