#!/usr/bin/env python3
"""
Test script for export/import functionality
Usage: python test_export_import.py
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost/api"
USERNAME = "levgorev"  # Change to your admin username
PASSWORD = "super-password-for-admin"  # Change to your admin password

def login():
    """Login and get access token"""
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": USERNAME, "password": PASSWORD}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Logged in successfully")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None

def export_poems(token):
    """Export all poems"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/poems/export/all", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Exported {data['total']} poems")

        # Save to file
        filename = f"poems_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"📁 Saved to {filename}")
        return data
    else:
        print(f"❌ Export failed: {response.status_code}")
        print(response.text)
        return None

def export_comments(token):
    """Export all comments"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/poems/export/comments", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Exported {data['total']} comments")

        # Save to file
        filename = f"comments_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"📁 Saved to {filename}")
        return data
    else:
        print(f"❌ Export failed: {response.status_code}")
        print(response.text)
        return None

def import_poems(token, data):
    """Import poems from data"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/poems/import/all",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Import completed:")
        print(f"   - Imported: {result['imported']}")
        print(f"   - Total attempted: {result['total_attempted']}")
        if result['errors']:
            print(f"   - Errors: {len(result['errors'])}")
            for error in result['errors']:
                print(f"     • {error}")
        return result
    else:
        print(f"❌ Import failed: {response.status_code}")
        print(response.text)
        return None

def test_export_import():
    """Test complete export/import cycle"""
    print("=" * 60)
    print("Testing Export/Import Functionality")
    print("=" * 60)
    print()

    # Login
    print("1. Logging in...")
    token = login()
    if not token:
        return
    print()

    # Export poems
    print("2. Exporting poems...")
    poems_data = export_poems(token)
    if not poems_data:
        return
    print()

    # Export comments
    print("3. Exporting comments...")
    comments_data = export_comments(token)
    print()

    # Test import with sample data
    print("4. Testing import with sample data...")
    sample_data = {
        "poems": [
            {
                "title": "Test Import Poem",
                "body": "This is a test poem created by the import script.",
                "tags": ["test", "import"]
            }
        ]
    }

    print("   Would you like to test import? This will add a test poem.")
    print("   Type 'yes' to continue: ", end='')
    choice = input().strip().lower()

    if choice == 'yes':
        import_result = import_poems(token, sample_data)
        print()
    else:
        print("   Skipping import test.")
        print()

    print("=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_export_import()
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

