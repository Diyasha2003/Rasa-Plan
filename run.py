#!/usr/bin/env python3
"""
RasaPlan Quick Start Script
Run this to launch the app: python run.py
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if all required packages are installed."""
    required = [
        "streamlit", "langchain", "langchain_openai",
        "langchain_community", "openai", "dotenv"
    ]
    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing.append(pkg)
    return missing

def main():
    print("🍛 RasaPlan | රිස බාසි")
    print("=" * 40)
    print("The Broke Student Sri Lankan Meal Planner")
    print("LB3114 · KDU · Intake 41")
    print("=" * 40)

    # Check for .env
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("\n⚠️  No .env file found.")
            print("   Copy .env.example to .env and add your OPENAI_API_KEY")
            print("   You can also enter the API key directly in the Streamlit app.")
        else:
            print("\n⚠️  No .env file found. You will need to enter your API key in the app.")

    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed!\n")

    # Launch Streamlit
    print("\n🚀 Launching RasaPlan...")
    print("   Open your browser at: http://localhost:8501")
    print("   Press Ctrl+C to stop\n")

    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "false",
        "--theme.primaryColor", "#F5C842",
        "--theme.backgroundColor", "#0a0a0f",
        "--theme.secondaryBackgroundColor", "#1C2C6B",
        "--theme.textColor", "#ffffff",
    ])

if __name__ == "__main__":
    main()
