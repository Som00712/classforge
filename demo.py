#!/usr/bin/env python3
"""
ClassForge API Demonstration Script
This script demonstrates how to interact with the ClassForge API
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000/api"

def demo_authentication():
    """Demonstrate user registration and login"""
    print("🔐 Authentication Demo")
    print("-" * 40)
    
    # Register a new user
    user_data = {
        "username": "demo_user",
        "email": "demo@classforge.com",
        "password": "demo_password123"
    }
    
    print("📝 Registering new user...")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Registration successful! User ID: {data['user']['id']}")
            access_token = data['access_token']
        else:
            print(f"❌ Registration failed: {response.json()}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running!")
        return None
    
    # Login
    print("\n🔑 Logging in...")
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful! Welcome, {data['user']['username']}")
        return data['access_token']
    else:
        print(f"❌ Login failed: {response.json()}")
        return access_token

def demo_chat(token):
    """Demonstrate chatbot functionality"""
    print("\n💬 Chat Demo")
    print("-" * 40)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Send messages
    messages = [
        "Hello! Can you help me understand machine learning?",
        "What are the main types of machine learning algorithms?",
        "Can you explain supervised learning?"
    ]
    
    session_id = f"demo_session_{int(time.time())}"
    
    for i, message in enumerate(messages, 1):
        print(f"\n📤 Message {i}: {message}")
        
        chat_data = {
            "message": message,
            "session_id": session_id
        }
        
        response = requests.post(f"{BASE_URL}/chat/message", json=chat_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"🤖 ClassForge: {data['response']}")
        else:
            print(f"❌ Chat failed: {response.json()}")
    
    # Get chat history
    print(f"\n📜 Retrieving chat history...")
    response = requests.get(f"{BASE_URL}/chat/history?session_id={session_id}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {len(data['chat_history'])} messages from history")
    else:
        print(f"❌ Failed to get history: {response.json()}")

def demo_clustering(token):
    """Demonstrate content clustering"""
    print("\n📊 Content Clustering Demo")
    print("-" * 40)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Sample documents for clustering
    documents = [
        {
            "title": "Introduction to Python",
            "content": "Python is a high-level programming language known for its simplicity and readability. It's widely used in web development, data science, and artificial intelligence."
        },
        {
            "title": "Machine Learning Basics",
            "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without explicit programming. It includes supervised, unsupervised, and reinforcement learning."
        },
        {
            "title": "Web Development with Flask",
            "content": "Flask is a lightweight web framework for Python. It's simple to use and perfect for building web applications and APIs. Flask follows the WSGI standard and is very flexible."
        },
        {
            "title": "Data Science with Pandas",
            "content": "Pandas is a powerful Python library for data manipulation and analysis. It provides data structures like DataFrames and Series that make working with structured data easy and intuitive."
        },
        {
            "title": "Neural Networks",
            "content": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information and are fundamental to deep learning algorithms."
        }
    ]
    
    clustering_data = {
        "documents": documents,
        "n_clusters": 3,
        "save_to_db": True
    }
    
    print("🔍 Analyzing and clustering documents...")
    response = requests.post(f"{BASE_URL}/clustering/analyze", json=clustering_data, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Clustering completed! Found {data['n_clusters']} clusters")
        print(f"📈 Accuracy: {data['accuracy_score']:.2%}")
        
        for cluster in data['clusters']:
            print(f"\n📂 Cluster {cluster['cluster_id']} ({cluster['size']} documents)")
            print(f"🏷️  Top terms: {', '.join(cluster['top_terms'])}")
            for doc in cluster['documents']:
                print(f"   📄 {doc['title']}")
    else:
        print(f"❌ Clustering failed: {response.json()}")

def main():
    """Main demonstration function"""
    print("🤖 ClassForge API Demonstration")
    print("=" * 50)
    print("This script demonstrates the key features of ClassForge:")
    print("• User authentication (register/login)")
    print("• AI chatbot interactions")
    print("• Document clustering and analysis")
    print("\n⚠️  Make sure the ClassForge server is running on localhost:5000")
    print("   Run: python run.py")
    print("=" * 50)
    
    # Run demonstrations
    token = demo_authentication()
    if token:
        demo_chat(token)
        demo_clustering(token)
        
        print("\n🎉 Demo completed successfully!")
        print("📚 You can now use ClassForge API for your educational applications!")
    else:
        print("\n❌ Demo failed. Please check the server and try again.")

if __name__ == "__main__":
    main() 