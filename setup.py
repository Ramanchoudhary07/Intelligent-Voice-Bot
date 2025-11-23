"""
Setup script for Intelligent Voice Bot
"""
import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "audio_files",
        "logs",
        "analytics_data",
        "src",
        "dashboard/templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_env_file():
    """Create .env file from example if it doesn't exist"""
    if not Path(".env").exists():
        if Path("env.example").exists():
            import shutil
            shutil.copy("env.example", ".env")
            print("✓ Created .env file from env.example")
            print("⚠  Please update .env with your API keys!")
        else:
            print("⚠  env.example not found. Please create .env manually.")
    else:
        print("✓ .env file already exists")

def main():
    """Main setup function"""
    print("=" * 50)
    print("Intelligent Voice Bot - Setup")
    print("=" * 50)
    print()
    
    print("Creating directories...")
    create_directories()
    print()
    
    print("Setting up environment file...")
    create_env_file()
    print()
    
    print("=" * 50)
    print("Setup complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Activate your virtual environment")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Update .env with your API keys")
    print("4. Run: python main.py --text 'Hello'")

if __name__ == "__main__":
    main()

