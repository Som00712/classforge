"""
Authentication Tests for ClassForge
"""

import pytest
import json
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    """Create test application"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def user_data():
    """Sample user data for testing"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }

def test_user_registration(client, user_data):
    """Test user registration"""
    response = client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['username'] == user_data['username']
    assert data['user']['email'] == user_data['email']

def test_user_registration_duplicate_username(client, user_data):
    """Test registration with duplicate username"""
    # Register first user
    client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    # Try to register with same username
    response = client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'Username already exists' in data['error']

def test_user_login(client, user_data):
    """Test user login"""
    # Register user first
    client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    # Login
    login_data = {
        'username': user_data['username'],
        'password': user_data['password']
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['message'] == 'Login successful'

def test_user_login_invalid_credentials(client, user_data):
    """Test login with invalid credentials"""
    # Register user first
    client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    # Try login with wrong password
    login_data = {
        'username': user_data['username'],
        'password': 'wrongpassword'
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'Invalid username or password' in data['error']

def test_get_profile(client, user_data):
    """Test getting user profile"""
    # Register user
    register_response = client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    token = json.loads(register_response.data)['access_token']
    
    # Get profile
    response = client.get(
        '/api/auth/profile',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user']['username'] == user_data['username'] 