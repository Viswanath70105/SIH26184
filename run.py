"""
Cyber-Drishti: Single-Command Entrypoint with Smart Self-Healing Dependency Loader
Run this script to launch the full system locally at http://127.0.0.1:8000
"""

import sys
import subprocess
import time
import threading

REQUIRED_PACKAGES = ["fastapi", "uvicorn", "pydantic"]

def ensure_dependencies():
    """Checks for required packages and automatically installs them if missing."""
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
            
    if missing:
        print("=" * 70)
        print(f"⚠️  Missing required packages: {', '.join(missing)}")
        print("📦 Attempting automatic self-healing installation via pip...")
        print("=" * 70)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("\n✅ All dependencies successfully installed!\n")
        except Exception:
            print("\n❌ Automatic installation failed (you might be offline or using a managed environment).")
            print(f"👉 Please run manually: pip install {' '.join(missing)}\n")
            sys.exit(1)

# Ensure dependencies before importing framework components
ensure_dependencies()

import uvicorn
import webbrowser

def open_browser():
    time.sleep(1.2)
    print("\n🌐 Launching CYBER-DRISHTI in your web browser: http://127.0.0.1:8000\n")
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass

if __name__ == "__main__":
    print("=" * 70)
    print("🛡️  CYBER-DRISHTI // I4C-MHA PREDICTIVE CYBERCRIME ANALYTICS SYSTEM")
    print("    SIH 2026 Problem Statement ID: 26184")
    print("=" * 70)
    print("⚡ Tactical Command Dashboard: http://127.0.0.1:8000")
    print("📖 Interactive API Swagger Docs: http://127.0.0.1:8000/docs")
    print("=" * 70)
    
    # Auto launch browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=True)
