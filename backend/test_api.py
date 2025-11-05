"""
Test API endpoints
"""
import requests

print("Testing API endpoints...")
print("=" * 50)

# Test categories endpoint (should require auth)
try:
    response = requests.get('http://localhost:8000/api/categories/')
    print(f"\nGET /api/categories/ (no auth)")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test login
try:
    response = requests.post('http://localhost:8000/api/auth/login/', 
                           json={'username': 'demo', 'password': 'demo123456'})
    print(f"\n\nPOST /api/auth/login/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        print(f"Token: {token[:20]}...")
        
        # Test categories with auth
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('http://localhost:8000/api/categories/', headers=headers)
        print(f"\n\nGET /api/categories/ (with auth)")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()
            print(f"Categories count: {len(categories)}")
            print(f"First 3 categories:")
            for cat in categories[:3]:
                print(f"  - {cat['name']} ({cat['type']})")
    else:
        print(f"Login failed: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)

