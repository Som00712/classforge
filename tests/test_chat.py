"""
Chat Tests for ClassForge
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
def auth_token(client):
    """Create authenticated user and return token"""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }
    
    response = client.post(
        '/api/auth/register',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    return json.loads(response.data)['access_token']

def test_send_message(client, auth_token):
    """Test sending a message to the chatbot"""
    message_data = {
        'message': 'Hello, can you help me with mathematics?',
        'session_id': 'test_session_1'
    }
    
    response = client.post(
        '/api/chat/message',
        data=json.dumps(message_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == message_data['message']
    assert 'response' in data
    assert 'timestamp' in data

def test_send_message_no_auth(client):
    """Test sending message without authentication"""
    message_data = {
        'message': 'Hello, can you help me with mathematics?'
    }
    
    response = client.post(
        '/api/chat/message',
        data=json.dumps(message_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401

def test_get_chat_history(client, auth_token):
    """Test retrieving chat history"""
    # Send a message first
    message_data = {
        'message': 'Test message for history',
        'session_id': 'test_session_1'
    }
    
    client.post(
        '/api/chat/message',
        data=json.dumps(message_data),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    # Get chat history
    response = client.get(
        '/api/chat/history',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'chat_history' in data
    assert len(data['chat_history']) > 0
    assert data['chat_history'][0]['message'] == message_data['message']

def test_get_chat_sessions(client, auth_token):
    """Test retrieving chat sessions"""
    # Send messages in different sessions
    sessions = ['session_1', 'session_2', 'session_3']
    
    for session in sessions:
        message_data = {
            'message': f'Test message for {session}',
            'session_id': session
        }
        
        client.post(
            '/api/chat/message',
            data=json.dumps(message_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {auth_token}'}
        )
    
    # Get sessions
    response = client.get(
        '/api/chat/sessions',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'sessions' in data
    assert len(data['sessions']) == 3
    for session in sessions:
        assert session in data['sessions'] 