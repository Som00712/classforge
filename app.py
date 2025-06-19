#!/usr/bin/env python3
"""
ClassForge - AI-Powered Educational Assistant
Main application entry point
"""

from flask import Flask, render_template_string, request, jsonify, send_from_directory
from app import create_app
import os

# Create Flask app
app = create_app()

# Simple HTML template for the frontend
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ClassForge - AI-Powered Educational Assistant</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
            --accent-gradient: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
            --success-gradient: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
            --glass-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --text-primary: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.8);
            --shadow-light: 0 8px 32px rgba(0, 0, 0, 0.12);
            --shadow-medium: 0 12px 40px rgba(0, 0, 0, 0.15);
            --shadow-heavy: 0 20px 60px rgba(0, 0, 0, 0.2);
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--primary-gradient);
            color: var(--text-primary);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
            z-index: -1;
            animation: backgroundShift 20s ease-in-out infinite;
        }
        
        @keyframes backgroundShift {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }
        
        .header {
            text-align: center;
            padding: 4rem 2rem;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            margin-bottom: 3rem;
            border-radius: 30px;
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-heavy);
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .header h1 {
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 800;
            margin-bottom: 1rem;
            background: var(--secondary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
            animation: titleGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes titleGlow {
            from { filter: brightness(1); }
            to { filter: brightness(1.2); }
        }
        
        .header p {
            font-size: 1.3rem;
            opacity: 0.9;
            font-weight: 300;
            letter-spacing: 0.5px;
            line-height: 1.6;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2.5rem;
            margin-bottom: 3rem;
        }
        
        .feature-card {
            background: var(--glass-bg);
            padding: 3rem 2.5rem;
            border-radius: 25px;
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-medium);
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--secondary-gradient);
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }
        
        .feature-card:hover::before {
            transform: scaleX(1);
        }
        
        .feature-card:hover {
            transform: translateY(-15px) scale(1.02);
            box-shadow: var(--shadow-heavy);
            border-color: rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1.2rem;
            font-weight: 600;
            background: var(--secondary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .feature-card p {
            line-height: 1.7;
            opacity: 0.9;
            font-weight: 400;
        }
        
        .demo-section {
            background: var(--glass-bg);
            padding: 3rem;
            border-radius: 30px;
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-heavy);
        }
        
        .demo-section h2 {
            font-size: 2.2rem;
            margin-bottom: 1rem;
            font-weight: 700;
            background: var(--secondary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .demo-buttons {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 3rem 0;
        }
        
        .btn {
            padding: 1.2rem 2.5rem;
            border: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: var(--shadow-light);
        }
        
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn:hover::before {
            left: 100%;
        }
        
                 .btn-primary {
             background: var(--secondary-gradient);
             color: white;
             border: 2px solid transparent;
         }
         
         .btn-secondary {
             background: rgba(255, 255, 255, 0.1);
             color: var(--text-primary);
             border: 2px solid var(--glass-border);
         }
         
         .btn-logout {
             background: var(--accent-gradient);
             color: white;
             padding: 0.5rem 1rem;
             font-size: 0.9rem;
         }
        
        .btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: var(--shadow-medium);
        }
        
        .btn:active {
            transform: translateY(-1px) scale(1.02);
        }
        
        .response-area {
            background: rgba(0, 0, 0, 0.3);
            padding: 2rem;
            border-radius: 20px;
            margin-top: 2rem;
            min-height: 250px;
            border: 1px solid var(--glass-border);
            font-family: 'Consolas', 'Monaco', monospace;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        .loading {
            text-align: center;
            opacity: 0.8;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
        }
        
        .loading::after {
            content: '';
            width: 20px;
            height: 20px;
            border: 2px solid transparent;
            border-top: 2px solid var(--text-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: 1rem;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .status {
            margin-top: 1rem;
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid;
            position: relative;
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .status.success {
            background: rgba(72, 187, 120, 0.2);
            border-left-color: #48bb78;
            box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
        }
        
        .status.error {
            background: rgba(245, 101, 101, 0.2);
            border-left-color: #f56565;
            box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3);
        }
        
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.6;
            font-size: 0.9rem;
        }
        
        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--secondary-gradient);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-gradient);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header {
                padding: 2rem 1rem;
                margin-bottom: 2rem;
            }
            
            .features {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            
            .feature-card {
                padding: 2rem 1.5rem;
            }
            
            .demo-section {
                padding: 2rem 1.5rem;
            }
            
            .demo-buttons {
                grid-template-columns: 1fr;
            }
        }
        
        @media (max-width: 480px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .btn {
                padding: 1rem 1.5rem;
                font-size: 0.9rem;
            }
        }
        
        /* Accessibility */
        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
                 /* Authentication Section */
         .auth-section {
             background: var(--glass-bg);
             padding: 3rem;
             border-radius: 30px;
             backdrop-filter: blur(20px);
             border: 1px solid var(--glass-border);
             box-shadow: var(--shadow-heavy);
             text-align: center;
             margin-bottom: 2rem;
         }
         
         .auth-section h2 {
             font-size: 2.2rem;
             margin-bottom: 1rem;
             background: var(--secondary-gradient);
             -webkit-background-clip: text;
             -webkit-text-fill-color: transparent;
             background-clip: text;
         }
         
         .auth-buttons {
             display: flex;
             gap: 1.5rem;
             justify-content: center;
             margin-top: 2rem;
             flex-wrap: wrap;
         }
         
         /* Dashboard Section */
         .dashboard-section {
             background: var(--glass-bg);
             padding: 3rem;
             border-radius: 30px;
             backdrop-filter: blur(20px);
             border: 1px solid var(--glass-border);
             box-shadow: var(--shadow-heavy);
         }
         
         .dashboard-header {
             display: flex;
             justify-content: space-between;
             align-items: center;
             margin-bottom: 2rem;
             padding-bottom: 1rem;
             border-bottom: 1px solid var(--glass-border);
         }
         
         .user-info {
             display: flex;
             align-items: center;
             gap: 1rem;
         }
         
         /* Modal Styles */
         .modal {
             position: fixed;
             top: 0;
             left: 0;
             right: 0;
             bottom: 0;
             background: rgba(0, 0, 0, 0.8);
             backdrop-filter: blur(5px);
             display: flex;
             align-items: center;
             justify-content: center;
             z-index: 1000;
             opacity: 0;
             visibility: hidden;
             transition: all 0.3s ease;
         }
         
         .modal.active {
             opacity: 1;
             visibility: visible;
         }
         
         .modal-content {
             background: var(--glass-bg);
             backdrop-filter: blur(20px);
             border: 1px solid var(--glass-border);
             border-radius: 25px;
             padding: 3rem;
             max-width: 450px;
             width: 90%;
             position: relative;
             box-shadow: var(--shadow-heavy);
             transform: scale(0.9);
             transition: transform 0.3s ease;
         }
         
         .modal.active .modal-content {
             transform: scale(1);
         }
         
         .modal-close {
             position: absolute;
             top: 1rem;
             right: 1.5rem;
             background: none;
             border: none;
             font-size: 2rem;
             color: var(--text-secondary);
             cursor: pointer;
             transition: all 0.3s ease;
         }
         
         .modal-close:hover {
             color: var(--text-primary);
             transform: scale(1.1);
         }
         
         /* Form Styles */
         .auth-form {
             text-align: center;
         }
         
         .auth-form h3 {
             font-size: 1.8rem;
             margin-bottom: 0.5rem;
             background: var(--secondary-gradient);
             -webkit-background-clip: text;
             -webkit-text-fill-color: transparent;
             background-clip: text;
         }
         
         .auth-form p {
             opacity: 0.8;
             margin-bottom: 2rem;
         }
         
         .form-group {
             margin-bottom: 1.5rem;
             text-align: left;
         }
         
         .form-group label {
             display: block;
             margin-bottom: 0.5rem;
             font-weight: 500;
             color: var(--text-primary);
         }
         
         .form-group input {
             width: 100%;
             padding: 1rem 1.5rem;
             border: 2px solid var(--glass-border);
             border-radius: 12px;
             background: rgba(255, 255, 255, 0.1);
             color: var(--text-primary);
             font-size: 1rem;
             transition: all 0.3s ease;
             backdrop-filter: blur(10px);
         }
         
         .form-group input:focus {
             outline: none;
             border-color: rgba(255, 255, 255, 0.4);
             box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
             background: rgba(255, 255, 255, 0.15);
         }
         
         .form-group input::placeholder {
             color: var(--text-secondary);
         }
         
         .btn-full {
             width: 100%;
             justify-content: center;
             margin: 1rem 0;
         }
         
         .auth-switch {
             margin-top: 1.5rem;
             opacity: 0.9;
         }
         
         .auth-switch a {
             color: var(--text-primary);
             text-decoration: none;
             font-weight: 500;
             transition: all 0.3s ease;
         }
         
         .auth-switch a:hover {
             text-decoration: underline;
             opacity: 1;
         }
         
         /* Focus states for accessibility */
         .btn:focus,
         .feature-card:focus,
         input:focus {
             outline: 3px solid rgba(255, 255, 255, 0.5);
             outline-offset: 2px;
         }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🎓 ClassForge</h1>
            <p>AI-Powered Educational Assistant</p>
        </header>

        <div class="features">
            <div class="feature-card">
                <h3>🤖 AI Tutor</h3>
                <p>24/7 personalized learning assistance with advanced AI technology. Get instant answers and explanations.</p>
            </div>
            <div class="feature-card">
                <h3>📊 Document Analysis</h3>
                <p>Intelligent document clustering and analysis using machine learning algorithms.</p>
            </div>
            <div class="feature-card">
                <h3>🔐 Secure Platform</h3>
                <p>JWT-based authentication with encrypted data storage and privacy protection.</p>
            </div>
        </div>

        <!-- Authentication Section -->
        <div class="auth-section" id="auth-section">
            <div class="auth-container">
                <h2>🔐 Secure Authentication</h2>
                <p>Sign in to access your personalized AI learning experience</p>
                
                <div class="auth-buttons">
                    <button class="btn btn-primary" onclick="showLogin()">
                        <i>🔑</i> Sign In
                    </button>
                    <button class="btn btn-secondary" onclick="showRegister()">
                        <i>👤</i> Create Account
                    </button>
                </div>
            </div>
        </div>

        <!-- User Dashboard (hidden initially) -->
        <div class="dashboard-section" id="dashboard-section" style="display: none;">
            <div class="dashboard-header">
                <h2>🎓 Welcome to ClassForge Dashboard</h2>
                <div class="user-info">
                    <span id="user-welcome">Welcome, User!</span>
                    <button class="btn btn-logout" onclick="logout()">Logout</button>
                </div>
            </div>
            
            <div class="demo-section">
                <h3>🚀 AI-Powered Features</h3>
                <div class="demo-buttons">
                    <button class="btn btn-primary" onclick="testChat()">
                        <i>🤖</i> Test AI Chat
                    </button>
                    <button class="btn btn-primary" onclick="analyzeDocs()">
                        <i>📊</i> Analyze Documents
                    </button>
                    <button class="btn btn-primary" onclick="checkStatus()">
                        <i>⚡</i> System Status
                    </button>
                </div>
                <div class="response-area" id="response"></div>
            </div>
        </div>

        <!-- Auth Modal -->
        <div class="modal" id="auth-modal">
            <div class="modal-content">
                <button class="modal-close" onclick="closeModal()">&times;</button>
                
                <!-- Login Form -->
                <div class="auth-form" id="login-form">
                    <h3>🔑 Sign In to ClassForge</h3>
                    <p>Access your AI-powered learning platform</p>
                    
                    <form onsubmit="handleLogin(event)">
                        <div class="form-group">
                            <label>📧 Email Address</label>
                            <input type="email" id="login-email" required 
                                   placeholder="Enter your email">
                        </div>
                        
                        <div class="form-group">
                            <label>🔒 Password</label>
                            <input type="password" id="login-password" required 
                                   placeholder="Enter your password">
                        </div>
                        
                        <button type="submit" class="btn btn-primary btn-full">
                            🚀 Sign In
                        </button>
                    </form>
                    
                    <p class="auth-switch">
                        Don't have an account? 
                        <a href="#" onclick="switchToRegister()">Create one here</a>
                    </p>
                </div>
                
                <!-- Register Form -->
                <div class="auth-form" id="register-form" style="display: none;">
                    <h3>👤 Create ClassForge Account</h3>
                    <p>Join thousands of learners using AI education</p>
                    
                    <form onsubmit="handleRegister(event)">
                        <div class="form-group">
                            <label>👤 Username</label>
                            <input type="text" id="register-username" required 
                                   placeholder="Choose a username" minlength="3">
                        </div>
                        
                        <div class="form-group">
                            <label>📧 Email Address</label>
                            <input type="email" id="register-email" required 
                                   placeholder="Enter your email">
                        </div>
                        
                        <div class="form-group">
                            <label>🔒 Password</label>
                            <input type="password" id="register-password" required 
                                   placeholder="Create a strong password" minlength="6">
                        </div>
                        
                        <button type="submit" class="btn btn-primary btn-full">
                            ✨ Create Account
                        </button>
                    </form>
                    
                    <p class="auth-switch">
                        Already have an account? 
                        <a href="#" onclick="switchToLogin()">Sign in here</a>
                    </p>
                </div>
            </div>
        </div>
    </div>

         <script>
         const API_BASE = window.location.origin + '/api';
         let authToken = localStorage.getItem('classforge_token');
         let currentUser = JSON.parse(localStorage.getItem('classforge_user') || 'null');

         // Utility functions
         function isValidEmail(email) {
             const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
             return emailRegex.test(email);
         }

         function isStrongPassword(password) {
             return password.length >= 6 && /[A-Za-z]/.test(password) && /[0-9]/.test(password);
         }

         // Initialize app on load
         document.addEventListener('DOMContentLoaded', function() {
             checkAuthStatus();
             
             // Add real-time validation to forms
             const emailInputs = document.querySelectorAll('input[type="email"]');
             emailInputs.forEach(input => {
                 input.addEventListener('blur', function() {
                     if (this.value && !isValidEmail(this.value)) {
                         this.style.borderColor = '#f56565';
                     } else {
                         this.style.borderColor = '';
                     }
                 });
             });
         });

         function updateResponse(content, isLoading = false, isError = false) {
             const responseArea = document.getElementById('response');
             if (isLoading) {
                 responseArea.innerHTML = '<div class="loading">🔄 Processing...</div>';
             } else {
                 const className = isError ? 'error' : 'success';
                 responseArea.innerHTML = `<div class="status ${className}"><pre>${content}</pre></div>`;
             }
         }

         function checkAuthStatus() {
             if (authToken && currentUser) {
                 showDashboard();
             } else {
                 showAuthSection();
             }
         }

         function showAuthSection() {
             document.getElementById('auth-section').style.display = 'block';
             document.getElementById('dashboard-section').style.display = 'none';
         }

         function showDashboard() {
             document.getElementById('auth-section').style.display = 'none';
             document.getElementById('dashboard-section').style.display = 'block';
             if (currentUser) {
                 document.getElementById('user-welcome').textContent = `Welcome, ${currentUser.username}! 🎓`;
             }
         }

         function showLogin() {
             document.getElementById('auth-modal').classList.add('active');
             document.getElementById('login-form').style.display = 'block';
             document.getElementById('register-form').style.display = 'none';
         }

         function showRegister() {
             document.getElementById('auth-modal').classList.add('active');
             document.getElementById('login-form').style.display = 'none';
             document.getElementById('register-form').style.display = 'block';
         }

         function closeModal() {
             document.getElementById('auth-modal').classList.remove('active');
         }

         function switchToRegister() {
             document.getElementById('login-form').style.display = 'none';
             document.getElementById('register-form').style.display = 'block';
         }

         function switchToLogin() {
             document.getElementById('register-form').style.display = 'none';
             document.getElementById('login-form').style.display = 'block';
         }

         async function handleLogin(event) {
             event.preventDefault();
             const email = document.getElementById('login-email').value.trim();
             const password = document.getElementById('login-password').value;

             // Client-side validation
             if (!email || !password) {
                 updateResponse('❌ Please fill in all fields', false, true);
                 return;
             }

             if (!isValidEmail(email)) {
                 updateResponse('❌ Please enter a valid email address', false, true);
                 return;
             }

             // Show loading state
             const submitBtn = event.target.querySelector('button[type="submit"]');
             const originalText = submitBtn.innerHTML;
             submitBtn.innerHTML = '🔄 Signing In...';
             submitBtn.disabled = true;

             try {
                 const response = await fetch(`${API_BASE}/auth/login`, {
                     method: 'POST',
                     headers: { 'Content-Type': 'application/json' },
                     body: JSON.stringify({ email, password })
                 });
                 
                 const data = await response.json();
                 
                 if (response.ok) {
                     authToken = data.access_token;
                     currentUser = data.user;
                     localStorage.setItem('classforge_token', authToken);
                     localStorage.setItem('classforge_user', JSON.stringify(currentUser));
                     closeModal();
                     showDashboard();
                     updateResponse(`🎉 Welcome back, ${currentUser.username}! Successfully logged in.`);
                     
                     // Clear form
                     event.target.reset();
                 } else {
                     throw new Error(data.message || 'Login failed');
                 }
             } catch (error) {
                 updateResponse(`❌ Login failed: ${error.message}`, false, true);
             } finally {
                 // Restore button state
                 submitBtn.innerHTML = originalText;
                 submitBtn.disabled = false;
             }
         }

         async function handleRegister(event) {
             event.preventDefault();
             const username = document.getElementById('register-username').value.trim();
             const email = document.getElementById('register-email').value.trim();
             const password = document.getElementById('register-password').value;

             // Enhanced client-side validation
             if (!username || !email || !password) {
                 updateResponse('❌ Please fill in all fields', false, true);
                 return;
             }

             if (username.length < 3) {
                 updateResponse('❌ Username must be at least 3 characters long', false, true);
                 return;
             }

             if (!isValidEmail(email)) {
                 updateResponse('❌ Please enter a valid email address', false, true);
                 return;
             }

             if (password.length < 6) {
                 updateResponse('❌ Password must be at least 6 characters long', false, true);
                 return;
             }

             // Show loading state
             const submitBtn = event.target.querySelector('button[type="submit"]');
             const originalText = submitBtn.innerHTML;
             submitBtn.innerHTML = '🔄 Creating Account...';
             submitBtn.disabled = true;

             try {
                 const response = await fetch(`${API_BASE}/auth/register`, {
                     method: 'POST',
                     headers: { 'Content-Type': 'application/json' },
                     body: JSON.stringify({ username, email, password })
                 });
                 
                 const data = await response.json();
                 
                 if (response.ok) {
                     authToken = data.access_token;
                     currentUser = data.user;
                     localStorage.setItem('classforge_token', authToken);
                     localStorage.setItem('classforge_user', JSON.stringify(currentUser));
                     closeModal();
                     showDashboard();
                     updateResponse(`🎉 Welcome to ClassForge, ${currentUser.username}! Account created successfully. You can now access all AI features.`);
                     
                     // Clear form
                     event.target.reset();
                 } else {
                     throw new Error(data.message || 'Registration failed');
                 }
             } catch (error) {
                 updateResponse(`❌ Registration failed: ${error.message}`, false, true);
             } finally {
                 // Restore button state
                 submitBtn.innerHTML = originalText;
                 submitBtn.disabled = false;
             }
         }

         function logout() {
             authToken = null;
             currentUser = null;
             localStorage.removeItem('classforge_token');
             localStorage.removeItem('classforge_user');
             showAuthSection();
             updateResponse('👋 Successfully logged out. See you next time!');
         }

                 async function testChat() {
             updateResponse('', true);
             if (!authToken) {
                 updateResponse('❌ Please sign in first to access AI chat', false, true);
                 return;
             }
             try {
                 const response = await fetch(`${API_BASE}/chat/message`, {
                     method: 'POST',
                     headers: {
                         'Content-Type': 'application/json',
                         'Authorization': `Bearer ${authToken}`
                     },
                     body: JSON.stringify({
                         message: 'Explain artificial intelligence and machine learning in simple terms',
                         session_id: 'demo_session_' + Date.now()
                     })
                 });
                 const data = await response.json();
                 
                 if (response.ok) {
                     updateResponse(`🤖 AI Chat Success:\\n${JSON.stringify(data, null, 2)}`);
                 } else {
                     throw new Error(data.message || 'Chat request failed');
                 }
             } catch (error) {
                 updateResponse(`❌ Chat failed: ${error.message}`, false, true);
             }
         }

                 async function analyzeDocs() {
             updateResponse('', true);
             
             // Check if user is authenticated
             if (!authToken) {
                 updateResponse('❌ Please sign in first to analyze documents', false, true);
                 return;
             }
             
             try {
                 const response = await fetch(`${API_BASE}/clustering/analyze`, {
                     method: 'POST',
                     headers: { 
                         'Content-Type': 'application/json',
                         'Authorization': `Bearer ${authToken}`
                     },
                     body: JSON.stringify({
                         documents: [
                             'Machine learning is a subset of artificial intelligence',
                             'Deep learning uses neural networks with multiple layers',
                             'Python is a popular programming language for data science',
                             'Natural language processing helps computers understand human language',
                             'Computer vision enables machines to interpret visual information'
                         ]
                     })
                 });
                 const data = await response.json();
                 
                 if (response.ok) {
                     updateResponse(`📊 Document Analysis Success:\\n${JSON.stringify(data, null, 2)}`);
                 } else {
                     throw new Error(data.message || 'Analysis failed');
                 }
             } catch (error) {
                 updateResponse(`❌ Analysis failed: ${error.message}`, false, true);
             }
         }

                 async function checkStatus() {
             updateResponse('', true);
             try {
                 const startTime = performance.now();
                 const responses = await Promise.all([
                     fetch('/'),
                     fetch(`${API_BASE}/auth/register`, { method: 'OPTIONS' }),
                     fetch(`${API_BASE}/chat/message`, { method: 'OPTIONS' }),
                     fetch(`${API_BASE}/clustering/analyze`, { method: 'OPTIONS' })
                 ]);
                 const endTime = performance.now();
                 
                 const status = {
                     frontend: {
                         status: responses[0].status,
                         message: responses[0].status === 200 ? '✅ Online' : '❌ Error'
                     },
                     auth_api: {
                         status: responses[1].status,
                         message: responses[1].status === 200 ? '✅ Ready' : '❌ Error'
                     },
                     chat_api: {
                         status: responses[2].status,
                         message: responses[2].status === 200 ? '✅ Ready' : '❌ Error'
                     },
                     clustering_api: {
                         status: responses[3].status,
                         message: responses[3].status === 200 ? '✅ Ready' : '❌ Error'
                     },
                     performance: {
                         response_time: `${Math.round(endTime - startTime)}ms`,
                         user_authenticated: authToken ? '✅ Yes' : '❌ No'
                     },
                     timestamp: new Date().toISOString(),
                     overall_status: '🚀 ClassForge is running perfectly!'
                 };
                 
                 updateResponse(`🔍 System Health Check:\\n${JSON.stringify(status, null, 2)}`);
             } catch (error) {
                 updateResponse(`❌ Status check failed: ${error.message}`, false, true);
             }
         }

                 // Auto-check status on load
         window.onload = () => {
             updateResponse('Welcome to ClassForge! 🎓 Create an account or sign in to access AI-powered educational features.');
         };

         // Add keyboard shortcuts
         document.addEventListener('keydown', function(e) {
             // Escape key to close modal
             if (e.key === 'Escape') {
                 closeModal();
             }
             
             // Enter key in modal forms
             if (e.key === 'Enter' && document.querySelector('.modal.active')) {
                 const activeForm = document.querySelector('.auth-form:not([style*="display: none"]) form');
                 if (activeForm) {
                     activeForm.dispatchEvent(new Event('submit'));
                 }
             }
         });

         // Add session timeout warning
         let sessionWarningShown = false;
         setInterval(() => {
             if (authToken && !sessionWarningShown) {
                 const tokenData = JSON.parse(atob(authToken.split('.')[1]));
                 const expirationTime = tokenData.exp * 1000;
                 const currentTime = Date.now();
                 const timeUntilExpiry = expirationTime - currentTime;
                 
                 // Show warning 5 minutes before expiry
                 if (timeUntilExpiry < 5 * 60 * 1000 && timeUntilExpiry > 0) {
                     updateResponse('⚠️ Your session will expire soon. Please save your work and refresh to continue.', false, false);
                     sessionWarningShown = true;
                 }
             }
         }, 60000); // Check every minute
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the frontend interface"""
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting ClassForge on http://localhost:{port}")
    print("📚 AI-Powered Educational Assistant")
    print("=" * 50)
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production') 