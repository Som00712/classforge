"""
Chat Message Model for ClassForge
"""

from datetime import datetime
from app import db

class ChatMessage(db.Model):
    """Chat message model for storing conversations"""
    
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        """Convert chat message object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'response': self.response,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'session_id': self.session_id
        }
    
    def __repr__(self):
        return f'<ChatMessage {self.id}>' 