"""
Chat Routes for ClassForge
"""

import openai
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.chat import ChatMessage

chat_bp = Blueprint('chat', __name__)

# Configure OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

@chat_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """Send message to AI chatbot"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data or not data.get('message'):
            return jsonify({'error': 'Message is required'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        message = data['message']
        session_id = data.get('session_id')
        
        # Get AI response from OpenAI
        try:
            if not openai.api_key:
                # Fallback response when OpenAI API key is not configured
                ai_response = "I'm ClassForge, your AI educational assistant! I'm ready to help you with your learning journey. Please note that to use full AI capabilities, you'll need to configure your OpenAI API key."
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are ClassForge, an AI-powered educational assistant. Help students with their learning by providing clear, informative, and engaging responses."},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                ai_response = response.choices[0].message.content.strip()
        except Exception as openai_error:
            ai_response = f"I apologize, but I'm having trouble processing your request right now. Here's a general response: I'm here to help with your educational needs! Please try rephrasing your question."
        
        # Save chat message to database
        chat_message = ChatMessage(
            user_id=user_id,
            message=message,
            response=ai_response,
            session_id=session_id
        )
        
        db.session.add(chat_message)
        db.session.commit()
        
        return jsonify({
            'message': message,
            'response': ai_response,
            'timestamp': chat_message.timestamp.isoformat(),
            'session_id': session_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Retrieve user's chat history"""
    try:
        user_id = int(get_jwt_identity())
        session_id = request.args.get('session_id')
        limit = int(request.args.get('limit', 50))
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Query chat messages
        query = ChatMessage.query.filter_by(user_id=user_id)
        
        if session_id:
            query = query.filter_by(session_id=session_id)
        
        messages = query.order_by(ChatMessage.timestamp.desc()).limit(limit).all()
        
        return jsonify({
            'chat_history': [msg.to_dict() for msg in messages]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_chat_sessions():
    """Get distinct chat sessions for the user"""
    try:
        user_id = int(get_jwt_identity())
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get distinct session IDs
        sessions = db.session.query(ChatMessage.session_id)\
                           .filter(ChatMessage.user_id == user_id)\
                           .filter(ChatMessage.session_id.isnot(None))\
                           .distinct().all()
        
        session_list = [session[0] for session in sessions]
        
        return jsonify({
            'sessions': session_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 