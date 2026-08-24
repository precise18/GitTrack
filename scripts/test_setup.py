"""
Test script to verify GitTrack environment setup.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to path so we can import src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_environment():
    """Test environment setup"""
    print("🔍 Testing GitTrack Environment...")
    print("-" * 40)
    
    # Test Python
    print(f"✅ Python: {sys.version}")
    
    # Test config - import from src package
    try:
        from src import config
        print("✅ Configuration loaded")
        # config is the instance, not the class
        print(f"   - Using mock data: {config.USE_MOCK_DATA}")
        if config.USE_MOCK_DATA:
            print("   - Mode: Development (mock data)")
        else:
            print("   - Mode: Production (real GitLab)")
    except ImportError as e:
        print(f"❌ Config import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False
    
    # Test packages
    packages = ['requests', 'boto3', 'dotenv', 'pandas']
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} installed")
        except ImportError:
            print(f"❌ {pkg} missing")
            return False
    
    print("-" * 40)
    print("✅ Environment is ready!")
    print("\n📚 Next Steps:")
    print("  1. Generate mock data: python scripts/generate_mock_data.py")
    print("  2. Fetch commits: python scripts/fetch_commits.py")
    print("  3. Start Week 2: AWS Setup")
    
    return True

if __name__ == "__main__":
    test_environment()
