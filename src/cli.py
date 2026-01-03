"""
Enhanced CLI with rich formatting.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich import box
import time
from datetime import datetime

console = Console()


@click.group()
def cli():
    """Log Monitoring & Alert System - CLI"""
    pass


@cli.command()
@click.option('--log-file', default='logs/system.log', help='Path to log file')
def analyze(log_file):
    """Analyze a log file and display results."""
    from log_parser import LogParser
    
    console.print(Panel.fit(
        "[bold cyan]Log Analysis[/bold cyan]",
        border_style="cyan"
    ))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing logs...", total=None)
        
        parser = LogParser()
        entries = parser.parse_log_file(log_file)
        suspicious = parser.get_suspicious_entries(entries)
        stats = parser.get_statistics()
        
        progress.stop()
    
    # Display summary
    console.print()
    console.print(f"[green]✓[/green] Analysis complete!")
    console.print(f"  Total entries: [cyan]{len(entries)}[/cyan]")
    console.print(f"  Suspicious: [yellow]{len(suspicious)}[/yellow]")
    console.print(f"  Total threats: [red]{stats['total_threats']}[/red]")
    console.print()
    
    # Threat breakdown table
    if stats['threats_by_type']:
        table = Table(title="Threat Breakdown", box=box.ROUNDED)
        table.add_column("Threat Type", style="cyan")
        table.add_column("Count", style="red", justify="right")
        table.add_column("Percentage", style="yellow", justify="right")
        
        total = stats['total_threats']
        for threat_type, count in sorted(stats['threats_by_type'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            table.add_row(threat_type, str(count), f"{percentage:.1f}%")
        
        console.print(table)
        console.print()
    
    # Top IPs table
    if stats['top_suspicious_ips']:
        table = Table(title="Top Suspicious IPs", box=box.ROUNDED)
        table.add_column("Rank", style="cyan")
        table.add_column("IP Address", style="yellow")
        table.add_column("Activities", style="red", justify="right")
        
        for i, (ip, count) in enumerate(stats['top_suspicious_ips'][:10], 1):
            table.add_row(str(i), ip, str(count))
        
        console.print(table)


@cli.command()
@click.option('--config', default='config.json', help='Config file path')
def monitor(config):
    """Start continuous monitoring."""
    from monitor import LogMonitor
    
    console.print(Panel.fit(
        "[bold cyan]Starting Log Monitor[/bold cyan]",
        border_style="cyan"
    ))
    
    monitor = LogMonitor(config)
    monitor.run_continuous_monitoring()


@cli.command()
@click.option('--log-file', default='logs/system.log', help='Path to log file')
def report(log_file):
    """Generate security report."""
    from report_generator import ReportGenerator
    
    console.print(Panel.fit(
        "[bold cyan]Generating Report[/bold cyan]",
        border_style="cyan"
    ))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Generating report...", total=None)
        
        generator = ReportGenerator()
        report_path = generator.generate_and_save_report(log_file)
        
        progress.stop()
    
    console.print()
    console.print(f"[green]✓[/green] Report generated: [cyan]{report_path}[/cyan]")


@cli.command()
def dashboard():
    """Start web dashboard."""
    from dashboard import run_dashboard
    import os
    
    console.print(Panel.fit(
        "[bold cyan]Starting Web Dashboard[/bold cyan]",
        border_style="cyan"
    ))
    
    port = int(os.getenv('DASHBOARD_PORT', 5000))
    host = os.getenv('DASHBOARD_HOST', '0.0.0.0')
    
    console.print()
    console.print(f"[green]Dashboard will be available at:[/green]")
    console.print(f"  [cyan]http://localhost:{port}[/cyan]")
    console.print()
    
    run_dashboard(host, port)


@cli.command()
def stats():
    """Display current statistics."""
    from database import DatabaseManager
    
    console.print(Panel.fit(
        "[bold cyan]Security Statistics[/bold cyan]",
        border_style="cyan"
    ))
    
    db = DatabaseManager()
    
    # Get today's stats
    today = datetime.now().strftime('%Y-%m-%d')
    stats = db.session.query(db.ThreatStatistics).filter_by(date=today).first()
    
    if stats:
        console.print()
        console.print(f"[bold]Date:[/bold] {stats.date}")
        console.print(f"[bold]Total Threats:[/bold] [red]{stats.total_threats}[/red]")
        console.print()
        
        table = Table(box=box.SIMPLE)
        table.add_column("Threat Type", style="cyan")
        table.add_column("Count", style="red", justify="right")
        
        table.add_row("Failed Logins", str(stats.failed_logins))
        table.add_row("SQL Injections", str(stats.sql_injections))
        table.add_row("XSS Attempts", str(stats.xss_attempts))
        table.add_row("Directory Traversal", str(stats.directory_traversal))
        table.add_row("Unauthorized Access", str(stats.unauthorized_access))
        table.add_row("Port Scans", str(stats.port_scans))
        table.add_row("Privilege Escalation", str(stats.privilege_escalation))
        
        console.print(table)
    else:
        console.print("\n[yellow]No statistics available for today[/yellow]\n")
    
    db.close()


if __name__ == '__main__':
    cli()