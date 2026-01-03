"""
Quick setup script for Log Monitoring & Alert System.
Run this to initialize the project structure and verify installation.
"""

import os
import sys
from pathlib import Path


def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'logs',
        'reports',
        'models',
        'tests'
    ]
    
    print("📁 Creating directories...")
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"   ✅ Created: {directory}/")
        else:
            print(f"   ℹ️  Exists: {directory}/")


def create_env_file():
    """Create .env file if it doesn't exist."""
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    print("\n🔧 Setting up environment variables...")
    if not env_path.exists():
        if env_example_path.exists():
            # Copy from example
            with open(env_example_path, 'r') as f:
                content = f.read()
            with open(env_path, 'w') as f:
                f.write(content)
            print("   ✅ Created .env from .env.example")
            print("   ⚠️  Remember to update .env with your actual credentials!")
        else:
            print("   ⚠️  .env.example not found, skipping .env creation")
    else:
        print("   ℹ️  .env already exists")


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'flask',
        'sqlalchemy',
        'sklearn',
        'rich',
        'click',
        'requests',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True


def create_sample_log():
    """Ensure sample log file exists."""
    log_file = Path('logs/system.log')
    
    print("\n📝 Checking sample logs...")
    if not log_file.exists():
        sample_logs = """[2024-01-15 10:23:45] INFO: User admin logged in successfully
[2024-01-15 10:24:12] WARNING: Failed password for user test from 203.0.113.45
[2024-01-15 10:25:30] ERROR: SQL injection attempt: SELECT * FROM users WHERE '1'='1'
[2024-01-15 10:26:15] WARNING: XSS detected: <script>alert('hack')</script>
[2024-01-15 10:27:00] ERROR: Directory traversal: ../../etc/passwd
[2024-01-15 10:28:30] INFO: System backup completed successfully
[2024-01-15 10:29:45] WARNING: Unauthorized access attempt from 198.51.100.50
[2024-01-15 10:30:12] ERROR: Port scan detected from 203.0.113.89
[2024-01-15 10:31:00] INFO: Database maintenance completed
[2024-01-15 10:32:15] WARNING: Failed password for root from 203.0.113.45
"""
        with open(log_file, 'w') as f:
            f.write(sample_logs)
        print("   ✅ Created sample log file: logs/system.log")
    else:
        print("   ℹ️  Sample log already exists")


def verify_config():
    """Verify config.json exists."""
    config_file = Path('config.json')
    
    print("\n⚙️  Checking configuration...")
    if config_file.exists():
        print("   ✅ config.json found")
        print("   💡 Remember to update email settings in config.json")
    else:
        print("   ⚠️  config.json not found")


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*80)
    print("✅ SETUP COMPLETE!")
    print("="*80)
    print("\n📋 Next Steps:\n")
    print("1. Update your email credentials:")
    print("   - Edit config.json or .env")
    print("   - Add Gmail app password (not your regular password)")
    print()
    print("2. Test the system:")
    print("   python demo.py")
    print()
    print("3. Start monitoring:")
    print("   python src/monitor.py --test")
    print()
    print("4. Launch web dashboard:")
    print("   python src/dashboard.py")
    print("   Then open: http://localhost:5000")
    print()
    print("5. Run analysis:")
    print("   python src/cli.py analyze --log-file logs/system.log")
    print()
    print("="*80)
    print("📖 For more information, see README.md and SETUP.md")
    print("="*80)


def main():
    """Main setup function."""
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "LOG MONITORING & ALERT SYSTEM" + " "*28 + "║")
    print("║" + " "*30 + "Quick Setup" + " "*36 + "║")
    print("╚" + "="*78 + "╝")
    print()
    
    try:
        create_directories()
        create_env_file()
        dependencies_ok = check_dependencies()
        create_sample_log()
        verify_config()
        print_next_steps()
        
        if not dependencies_ok:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()