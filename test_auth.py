"""
Test script for the authorization system.
This script tests the basic functionality of the auth system.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from controller.app_controller import AppController
from model.auth_models import AuthUtils, Permission


def test_auth_system():
    """Test the authorization system functionality."""
    print("🧪 Testing Authorization System...")
    
    # Initialize controller
    controller = AppController()
    
    # Test 1: Password strength validation
    print("\n1. Testing password strength validation...")
    test_passwords = [
        "weak",
        "Strong123!",
        "veryweak",
        "ComplexP@ssw0rd!"
    ]
    
    for password in test_passwords:
        is_strong, issues = AuthUtils.is_password_strong(password)
        status = "✅ Strong" if is_strong else "❌ Weak"
        print(f"   Password '{password}': {status}")
        if not is_strong:
            for issue in issues:
                print(f"     - {issue}")
    
    # Test 2: User registration
    print("\n2. Testing user registration...")
    test_email = "test@example.com"
    test_password = "StrongP@ss123!"
    test_name = "Test User"
    
    success, message = controller.register_user(test_email, test_password, test_name, "user")
    print(f"   Registration result: {message}")
    
    # Test 3: User login
    print("\n3. Testing user login...")
    success, message = controller.login_user(test_email, test_password)
    print(f"   Login result: {message}")
    
    if success:
        # Test 4: Session verification
        print("\n4. Testing session verification...")
        session_token = controller.get_session_token()
        if session_token:
            is_valid = controller.verify_session(session_token)
            print(f"   Session valid: {is_valid}")
            
            if is_valid:
                current_user = controller.get_current_user()
                print(f"   Current user: {current_user}")
                
                # Test 5: Permission checking
                print("\n5. Testing permission checking...")
                has_read = controller.has_permission("read")
                has_write = controller.has_permission("write")
                has_admin = controller.has_permission("admin")
                print(f"   Has READ permission: {has_read}")
                print(f"   Has WRITE permission: {has_write}")
                print(f"   Has ADMIN permission: {has_admin}")
                
                # Test 6: Role checking
                print("\n6. Testing role checking...")
                has_user_role = controller.has_role("user")
                has_admin_role = controller.has_role("admin")
                print(f"   Has 'user' role: {has_user_role}")
                print(f"   Has 'admin' role: {has_admin_role}")
                
                # Test 7: Logout
                print("\n7. Testing logout...")
                logout_success = controller.logout_user()
                print(f"   Logout successful: {logout_success}")
                
                # Verify logout
                is_authenticated = controller.is_authenticated()
                print(f"   Still authenticated: {is_authenticated}")
    
    print("\n✅ Authorization system test completed!")


if __name__ == "__main__":
    test_auth_system() 