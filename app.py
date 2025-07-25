#!/usr/bin/env python3
"""
Business ROI Calculator - Enhanced Version
Advanced web application with PDF reports, multi-currency, user auth, and more
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import json
import random
import sqlite3
import hashlib
import requests
from datetime import datetime, timedelta
from functools import wraps
import io
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

app = Flask(__name__)
app.secret_key = 'business_roi_calculator_secret_key_2024'

# Enhanced business data and calculations
COMPANY_SIZES = {
    'startup': {'multiplier': 0.7, 'min_budget': 5000, 'max_budget': 100000, 'risk_factor': 0.3},
    'small': {'multiplier': 1.0, 'min_budget': 25000, 'max_budget': 500000, 'risk_factor': 0.2},
    'medium': {'multiplier': 1.5, 'min_budget': 100000, 'max_budget': 2000000, 'risk_factor': 0.15},
    'enterprise': {'multiplier': 2.5, 'min_budget': 500000, 'max_budget': 10000000, 'risk_factor': 0.1}
}

INDUSTRIES = {
    'fintech': {'growth_rate': 0.25, 'risk_factor': 0.15, 'market_size': 'Large', 'volatility': 0.2},
    'healthtech': {'growth_rate': 0.30, 'risk_factor': 0.20, 'market_size': 'Huge', 'volatility': 0.15},
    'edtech': {'growth_rate': 0.22, 'risk_factor': 0.12, 'market_size': 'Large', 'volatility': 0.18},
    'ecommerce': {'growth_rate': 0.18, 'risk_factor': 0.08, 'market_size': 'Massive', 'volatility': 0.12},
    'saas': {'growth_rate': 0.35, 'risk_factor': 0.18, 'market_size': 'Large', 'volatility': 0.22},
    'gaming': {'growth_rate': 0.20, 'risk_factor': 0.25, 'market_size': 'Medium', 'volatility': 0.3},
    'realEstate': {'growth_rate': 0.15, 'risk_factor': 0.10, 'market_size': 'Stable', 'volatility': 0.08},
    'foodBeverage': {'growth_rate': 0.12, 'risk_factor': 0.15, 'market_size': 'Medium', 'volatility': 0.1},
    'manufacturing': {'growth_rate': 0.10, 'risk_factor': 0.08, 'market_size': 'Large', 'volatility': 0.06},
    'logistics': {'growth_rate': 0.16, 'risk_factor': 0.12, 'market_size': 'Large', 'volatility': 0.14},
    'crypto': {'growth_rate': 0.45, 'risk_factor': 0.40, 'market_size': 'Volatile', 'volatility': 0.5},
    'nft': {'growth_rate': 0.35, 'risk_factor': 0.45, 'market_size': 'Emerging', 'volatility': 0.6},
    'web3': {'growth_rate': 0.40, 'risk_factor': 0.35, 'market_size': 'Growing', 'volatility': 0.4},
    'sustainability': {'growth_rate': 0.28, 'risk_factor': 0.18, 'market_size': 'Expanding', 'volatility': 0.16},
    'biotech': {'growth_rate': 0.32, 'risk_factor': 0.25, 'market_size': 'Specialized', 'volatility': 0.28}
}

# Enhanced project types
PROJECT_TYPES = {
    'product_development': {
        'base_cost': 150000, 'timeline': 12, 'roi_potential': 2.5,
        'description': 'New Product Development', 'complexity': 'High', 'risk_level': 0.2
    },
    'digital_transformation': {
        'base_cost': 200000, 'timeline': 18, 'roi_potential': 3.0,
        'description': 'Digital Transformation', 'complexity': 'Very High', 'risk_level': 0.15
    },
    'market_expansion': {
        'base_cost': 100000, 'timeline': 8, 'roi_potential': 2.0,
        'description': 'Market Expansion', 'complexity': 'Medium', 'risk_level': 0.18
    },
    'tech_upgrade': {
        'base_cost': 80000, 'timeline': 6, 'roi_potential': 1.8,
        'description': 'Technology Upgrade', 'complexity': 'Medium', 'risk_level': 0.12
    },
    'marketing_campaign': {
        'base_cost': 50000, 'timeline': 4, 'roi_potential': 1.5,
        'description': 'Marketing Campaign', 'complexity': 'Low', 'risk_level': 0.15
    },
    'ecommerce_platform': {
        'base_cost': 120000, 'timeline': 10, 'roi_potential': 2.2,
        'description': 'E-commerce Platform', 'complexity': 'High', 'risk_level': 0.16
    },
    'mobile_app': {
        'base_cost': 90000, 'timeline': 8, 'roi_potential': 2.0,
        'description': 'Mobile Application', 'complexity': 'High', 'risk_level': 0.18
    },
    'ai_integration': {
        'base_cost': 180000, 'timeline': 14, 'roi_potential': 2.8,
        'description': 'AI Integration', 'complexity': 'Very High', 'risk_level': 0.22
    },
    'blockchain_platform': {
        'base_cost': 250000, 'timeline': 16, 'roi_potential': 3.5,
        'description': 'Blockchain Platform', 'complexity': 'Very High', 'risk_level': 0.35
    },
    'iot_solution': {
        'base_cost': 160000, 'timeline': 12, 'roi_potential': 2.3,
        'description': 'IoT Solution', 'complexity': 'High', 'risk_level': 0.20
    },
    'data_analytics': {
        'base_cost': 140000, 'timeline': 10, 'roi_potential': 2.4,
        'description': 'Data Analytics Platform', 'complexity': 'High', 'risk_level': 0.17
    },
    'subscription_service': {
        'base_cost': 75000, 'timeline': 6, 'roi_potential': 2.1,
        'description': 'Subscription Service', 'complexity': 'Medium', 'risk_level': 0.14
    },
    'automation_system': {
        'base_cost': 110000, 'timeline': 9, 'roi_potential': 2.6,
        'description': 'Automation System', 'complexity': 'High', 'risk_level': 0.13
    },
    'cybersecurity_upgrade': {
        'base_cost': 95000, 'timeline': 7, 'roi_potential': 1.9,
        'description': 'Cybersecurity Upgrade', 'complexity': 'Medium', 'risk_level': 0.08
    },
    'cloud_migration': {
        'base_cost': 130000, 'timeline': 11, 'roi_potential': 2.2,
        'description': 'Cloud Migration', 'complexity': 'High', 'risk_level': 0.11
    }
}

# Currency exchange rates (simplified - in production, use real-time API)
CURRENCIES = {
    'USD': {'symbol': '$', 'rate': 1.0, 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'rate': 0.85, 'name': 'Euro'},
    'GBP': {'symbol': '£', 'rate': 0.73, 'name': 'British Pound'},
    'JPY': {'symbol': '¥', 'rate': 110.0, 'name': 'Japanese Yen'},
    'CAD': {'symbol': 'C$', 'rate': 1.25, 'name': 'Canadian Dollar'},
    'AUD': {'symbol': 'A$', 'rate': 1.35, 'name': 'Australian Dollar'},
    'CHF': {'symbol': 'CHF', 'rate': 0.92, 'name': 'Swiss Franc'},
    'CNY': {'symbol': '¥', 'rate': 6.45, 'name': 'Chinese Yuan'},
    'INR': {'symbol': '₹', 'rate': 74.5, 'name': 'Indian Rupee'},
    'BRL': {'symbol': 'R$', 'rate': 5.2, 'name': 'Brazilian Real'}
}

class DatabaseManager:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect('business_roi.db')
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                subscription_tier TEXT DEFAULT 'basic'
            )
        ''')
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                project_name TEXT NOT NULL,
                company_name TEXT,
                company_size TEXT,
                current_industry TEXT,
                project_type TEXT,
                target_industry TEXT,
                currency TEXT DEFAULT 'USD',
                results TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, email, password):
        """Create a new user"""
        conn = sqlite3.connect('business_roi.db')
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = sqlite3.connect('business_roi.db')
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT id, username, email, subscription_tier FROM users
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'subscription_tier': user[3]
            }
        return None
    
    def save_project(self, user_id, project_data, results):
        """Save project calculation"""
        conn = sqlite3.connect('business_roi.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO projects (user_id, project_name, company_name, company_size,
                                current_industry, project_type, target_industry, currency, results)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            f"{project_data.get('company_name', 'Project')} - {PROJECT_TYPES[project_data['project_type']]['description']}",
            project_data.get('company_name'),
            project_data.get('company_size'),
            project_data.get('current_industry'),
            project_data.get('project_type'),
            project_data.get('target_industry'),
            project_data.get('currency', 'USD'),
            json.dumps(results)
        ))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id
    
    def get_user_projects(self, user_id):
        """Get all projects for a user"""
        conn = sqlite3.connect('business_roi.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, project_name, created_at, currency, results FROM projects
            WHERE user_id = ? ORDER BY created_at DESC
        ''', (user_id,))
        
        projects = cursor.fetchall()
        conn.close()
        
        return [{
            'id': p[0],
            'name': p[1],
            'created_at': p[2],
            'currency': p[3],
            'results': json.loads(p[4]) if p[4] else {}
        } for p in projects]

class EnhancedROICalculator:
    def __init__(self):
        pass
    
    def convert_currency(self, amount, from_currency, to_currency):
        """Convert amount between currencies"""
        if from_currency == to_currency:
            return amount
        
        # Convert to USD first, then to target currency
        usd_amount = amount / CURRENCIES[from_currency]['rate']
        converted_amount = usd_amount * CURRENCIES[to_currency]['rate']
        
        return converted_amount
    
    def calculate_risk_assessment(self, company_size, project_type, industry):
        """Calculate comprehensive risk assessment"""
        size_data = COMPANY_SIZES.get(company_size, COMPANY_SIZES['small'])
        project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        
        # Base risk factors
        company_risk = size_data['risk_factor']
        project_risk = project_data['risk_level']
        industry_risk = industry_data['risk_factor']
        market_volatility = industry_data['volatility']
        
        # Calculate composite risk score
        overall_risk = (company_risk * 0.3 + project_risk * 0.4 + industry_risk * 0.2 + market_volatility * 0.1)
        
        # Risk categories
        if overall_risk <= 0.15:
            risk_category = 'Low'
            risk_color = '#00ff88'
        elif overall_risk <= 0.25:
            risk_category = 'Medium'
            risk_color = '#ffaa00'
        else:
            risk_category = 'High'
            risk_color = '#ff4757'
        
        return {
            'overall_risk': round(overall_risk, 3),
            'risk_category': risk_category,
            'risk_color': risk_color,
            'risk_factors': {
                'company_size_risk': round(company_risk, 3),
                'project_complexity_risk': round(project_risk, 3),
                'industry_risk': round(industry_risk, 3),
                'market_volatility': round(market_volatility, 3)
            },
            'risk_mitigation': self._get_risk_mitigation_strategies(overall_risk, project_type, industry)
        }
    
    def _get_risk_mitigation_strategies(self, risk_level, project_type, industry):
        """Get risk mitigation strategies"""
        strategies = []
        
        if risk_level > 0.25:
            strategies.append("Consider phased implementation to reduce upfront investment")
            strategies.append("Establish clear success metrics and exit criteria")
            strategies.append("Allocate 20-30% contingency budget")
        
        if project_type in ['blockchain_platform', 'ai_integration', 'crypto']:
            strategies.append("Invest in specialized expertise and training")
            strategies.append("Stay updated with regulatory changes")
        
        if industry in ['crypto', 'nft', 'gaming']:
            strategies.append("Diversify market exposure")
            strategies.append("Monitor market trends closely")
        
        strategies.append("Regular progress reviews and milestone assessments")
        strategies.append("Maintain flexible project scope and timeline")
        
        return strategies
    
    def calculate_project_cost(self, company_size, project_type, industry, currency='USD', custom_requirements=None):
        """Enhanced cost calculation with currency support"""
        
        # Base calculations
        size_data = COMPANY_SIZES.get(company_size, COMPANY_SIZES['small'])
        project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        
        # Calculate base cost with size multiplier
        base_cost = project_data['base_cost'] * size_data['multiplier']
        
        # Industry complexity adjustment
        industry_multiplier = 1.0 + (industry_data['risk_factor'] * 0.5)
        adjusted_cost = base_cost * industry_multiplier
        
        # Add some realistic variance
        variance = random.uniform(0.85, 1.15)
        final_cost_usd = int(adjusted_cost * variance)
        
        # Convert to requested currency
        final_cost = self.convert_currency(final_cost_usd, 'USD', currency)
        
        return {
            'total_cost': int(final_cost),
            'total_cost_usd': final_cost_usd,
            'currency': currency,
            'currency_symbol': CURRENCIES[currency]['symbol'],
            'breakdown': {
                'development': int(final_cost * 0.6),
                'design': int(final_cost * 0.15),
                'testing': int(final_cost * 0.1),
                'deployment': int(final_cost * 0.05),
                'project_management': int(final_cost * 0.1)
            },
            'timeline_months': project_data['timeline'],
            'complexity': project_data['complexity']
        }
    
    def calculate_roi_projection(self, investment, industry, project_type, timeline_months, currency='USD'):
        """Enhanced ROI projections with risk-adjusted scenarios"""
        
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
        
        # Base ROI calculation
        base_roi = project_data['roi_potential']
        growth_rate = industry_data['growth_rate']
        volatility = industry_data['volatility']
        
        # Enhanced scenarios with risk adjustment
        scenarios = {
            'pessimistic': {
                'multiplier': 0.6 - (volatility * 0.2),
                'probability': 0.2,
                'description': 'Worst case with significant market challenges'
            },
            'conservative': {
                'multiplier': 0.8 - (volatility * 0.1),
                'probability': 0.3,
                'description': 'Conservative estimate with market challenges'
            },
            'realistic': {
                'multiplier': 1.0,
                'probability': 0.4,
                'description': 'Most likely scenario based on market data'
            },
            'optimistic': {
                'multiplier': 1.3 + (growth_rate * 0.2),
                'probability': 0.1,
                'description': 'Best case with optimal market conditions'
            }
        }
        
        projections = {}
        investment_usd = investment if currency == 'USD' else self.convert_currency(investment, currency, 'USD')
        
        for scenario, data in scenarios.items():
            roi_multiplier = max(0.1, base_roi * data['multiplier'])  # Ensure positive ROI
            annual_return_usd = investment_usd * roi_multiplier * growth_rate
            
            # Convert back to requested currency
            annual_return = self.convert_currency(annual_return_usd, 'USD', currency)
            total_roi = annual_return * 3  # 3-year projection
            
            projections[scenario] = {
                'annual_return': int(annual_return),
                'total_roi': int(total_roi),
                'roi_percentage': int((roi_multiplier - 1) * 100),
                'break_even_months': max(3, int(timeline_months / roi_multiplier)),
                'probability': data['probability'],
                'description': data['description'],
                'net_present_value': int(total_roi - investment)
            }
        
        return projections
    
    def get_market_insights(self, industry):
        """Enhanced market insights"""
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        
        insights = {
            'market_size': industry_data['market_size'],
            'growth_rate': f"{industry_data['growth_rate']*100:.0f}%",
            'risk_level': 'Low' if industry_data['risk_factor'] < 0.1 else 'Medium' if industry_data['risk_factor'] < 0.2 else 'High',
            'volatility': f"{industry_data['volatility']*100:.0f}%",
            'trends': self._get_industry_trends(industry),
            'opportunities': self._get_industry_opportunities(industry),
            'challenges': self._get_industry_challenges(industry)
        }
        
        return insights
    
    def _get_industry_trends(self, industry):
        trends = {
            'fintech': ['Digital payments growth', 'Blockchain adoption', 'RegTech expansion', 'Open banking APIs'],
            'healthtech': ['Telemedicine boom', 'AI diagnostics', 'Wearable health devices', 'Personalized medicine'],
            'edtech': ['Remote learning', 'Personalized education', 'VR/AR in education', 'Microlearning platforms'],
            'ecommerce': ['Mobile commerce', 'Social selling', 'Same-day delivery', 'Voice commerce'],
            'saas': ['AI-powered tools', 'Industry-specific solutions', 'Integration platforms', 'No-code/low-code'],
            'gaming': ['Mobile gaming', 'Cloud gaming', 'NFT integration', 'Metaverse development'],
            'crypto': ['DeFi protocols', 'NFT marketplaces', 'Layer 2 solutions', 'Central bank digital currencies'],
            'web3': ['Decentralized apps', 'DAOs', 'Metaverse platforms', 'Blockchain interoperability'],
            'sustainability': ['Carbon tracking', 'Renewable energy tech', 'Circular economy', 'ESG reporting']
        }
        return trends.get(industry, ['Market digitization', 'Customer experience focus', 'Operational efficiency'])
    
    def _get_industry_opportunities(self, industry):
        opportunities = {
            'fintech': ['Emerging markets', 'SME banking', 'Crypto services', 'Embedded finance'],
            'healthtech': ['Remote monitoring', 'Mental health apps', 'Elderly care tech', 'Precision medicine'],
            'crypto': ['Institutional adoption', 'DeFi yield farming', 'NFT utilities', 'Cross-chain bridges'],
            'web3': ['Creator economy', 'Decentralized identity', 'Web3 gaming', 'Social tokens']
        }
        return opportunities.get(industry, ['Digital innovation', 'Market expansion', 'Efficiency improvements'])
    
    def _get_industry_challenges(self, industry):
        challenges = {
            'fintech': ['Regulatory compliance', 'Security concerns', 'Competition from big tech'],
            'crypto': ['Regulatory uncertainty', 'Market volatility', 'Scalability issues'],
            'web3': ['User adoption', 'Technical complexity', 'Environmental concerns'],
            'gaming': ['Market saturation', 'Platform dependencies', 'User acquisition costs']
        }
        return challenges.get(industry, ['Market competition', 'Technology changes', 'Economic uncertainty'])

# Initialize components
db_manager = DatabaseManager()
calculator = EnhancedROICalculator()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html', currencies=CURRENCIES)

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/register')
def register():
    """Registration page"""
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_projects = db_manager.get_user_projects(session['user_id'])
    return render_template('dashboard.html', projects=user_projects, currencies=CURRENCIES)

@app.route('/api/register', methods=['POST'])
def api_register():
    """User registration API"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'All fields are required'}), 400
        
        user_id = db_manager.create_user(username, email, password)
        if user_id:
            return jsonify({'success': True, 'message': 'User registered successfully'})
        else:
            return jsonify({'error': 'Username or email already exists'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """User login API"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        user = db_manager.authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['subscription_tier'] = user['subscription_tier']
            return jsonify({'success': True, 'user': user})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """User logout API"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/calculate', methods=['POST'])
def calculate_roi():
    """Enhanced ROI calculation API"""
    try:
        data = request.json
        
        company_name = data.get('company_name', 'Your Company')
        company_size = data.get('company_size', 'small')
        current_industry = data.get('current_industry', 'saas')
        project_type = data.get('project_type', 'product_development')
        target_industry = data.get('target_industry', current_industry)
        currency = data.get('currency', 'USD')
        
        # Calculate project costs
        cost_analysis = calculator.calculate_project_cost(
            company_size, project_type, target_industry, currency
        )
        
        # Calculate ROI projections
        roi_projections = calculator.calculate_roi_projection(
            cost_analysis['total_cost'], 
            target_industry, 
            project_type, 
            cost_analysis['timeline_months'],
            currency
        )
        
        # Get market insights
        market_insights = calculator.get_market_insights(target_industry)
        
        # Calculate risk assessment
        risk_assessment = calculator.calculate_risk_assessment(
            company_size, project_type, target_industry
        )
        
        # Compile response
        response = {
            'company_name': company_name,
            'project_summary': {
                'type': PROJECT_TYPES[project_type]['description'],
                'industry': target_industry.replace('_', ' ').title(),
                'timeline': f"{cost_analysis['timeline_months']} months",
                'complexity': cost_analysis['complexity']
            },
            'cost_analysis': cost_analysis,
            'roi_projections': roi_projections,
            'market_insights': market_insights,
            'risk_assessment': risk_assessment,
            'recommendations': calculator._get_recommendations(company_size, project_type, target_industry),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save project if user is logged in
        if 'user_id' in session:
            project_id = db_manager.save_project(session['user_id'], data, response)
            response['project_id'] = project_id
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/currencies')
def get_currencies():
    """Get available currencies"""
    return jsonify(CURRENCIES)

@app.route('/api/industries')
def get_industries():
    """Get available industries"""
    industries = []
    for key, value in INDUSTRIES.items():
        industries.append({
            'id': key,
            'name': key.replace('_', ' ').title(),
            'growth_rate': f"{value['growth_rate']*100:.0f}%",
            'market_size': value['market_size'],
            'risk_level': 'Low' if value['risk_factor'] < 0.1 else 'Medium' if value['risk_factor'] < 0.2 else 'High'
        })
    return jsonify(industries)

@app.route('/api/projects')
def get_projects():
    """Get available project types"""
    projects = []
    for key, value in PROJECT_TYPES.items():
        projects.append({
            'id': key,
            'name': value['description'],
            'complexity': value['complexity'],
            'timeline': f"{value['timeline']} months",
            'base_cost': f"${value['base_cost']:,}"
        })
    return jsonify(projects)

@app.route('/api/generate-pdf/<int:project_id>')
@login_required
def generate_pdf_report(project_id):
    """Generate PDF report for a project"""
    try:
        # Get project data
        conn = sqlite3.connect('business_roi.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT project_name, company_name, results, created_at, currency FROM projects
            WHERE id = ? AND user_id = ?
        ''', (project_id, session['user_id']))
        
        project = cursor.fetchone()
        conn.close()
        
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        project_name, company_name, results_json, created_at, currency = project
        results = json.loads(results_json)
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center
            textColor=colors.HexColor('#667eea')
        )
        story.append(Paragraph("Business ROI Analysis Report", title_style))
        story.append(Spacer(1, 20))
        
        # Project info
        info_data = [
            ['Company:', company_name or 'N/A'],
            ['Project:', project_name],
            ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M')],
            ['Currency:', currency]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Cost Analysis
        story.append(Paragraph("Cost Analysis", styles['Heading2']))
        cost_data = [
            ['Component', 'Amount'],
            ['Total Project Cost', f"{CURRENCIES[currency]['symbol']}{results['cost_analysis']['total_cost']:,}"],
            ['Development', f"{CURRENCIES[currency]['symbol']}{results['cost_analysis']['breakdown']['development']:,}"],
            ['Design', f"{CURRENCIES[currency]['symbol']}{results['cost_analysis']['breakdown']['design']:,}"],
            ['Testing', f"{CURRENCIES[currency]['symbol']}{results['cost_analysis']['breakdown']['testing']:,}"],
            ['Timeline', f"{results['cost_analysis']['timeline_months']} months"],
            ['Complexity', results['cost_analysis']['complexity']]
        ]
        
        cost_table = Table(cost_data, colWidths=[3*inch, 2*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(cost_table)
        story.append(Spacer(1, 20))
        
        # ROI Projections
        story.append(Paragraph("ROI Projections", styles['Heading2']))
        roi_data = [['Scenario', 'ROI %', 'Annual Return', 'Break-even']]
        
        for scenario, data in results['roi_projections'].items():
            roi_data.append([
                scenario.title(),
                f"{data['roi_percentage']}%",
                f"{CURRENCIES[currency]['symbol']}{data['annual_return']:,}",
                f"{data['break_even_months']} months"
            ])
        
        roi_table = Table(roi_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        roi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(roi_table)
        story.append(Spacer(1, 20))
        
        # Risk Assessment
        if 'risk_assessment' in results:
            story.append(Paragraph("Risk Assessment", styles['Heading2']))
            risk = results['risk_assessment']
            story.append(Paragraph(f"Overall Risk Level: <b>{risk['risk_category']}</b>", styles['Normal']))
            story.append(Paragraph(f"Risk Score: {risk['overall_risk']:.3f}", styles['Normal']))
            story.append(Spacer(1, 10))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"{project_name.replace(' ', '_')}_ROI_Report.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add recommendations method to calculator
def _get_recommendations(self, company_size, project_type, industry):
    """Generate enhanced personalized recommendations"""
    recommendations = []
    
    if company_size == 'startup':
        recommendations.append("Consider MVP approach to minimize initial investment")
        recommendations.append("Focus on core features first, expand later")
        recommendations.append("Seek angel investors or venture capital for funding")
    elif company_size == 'enterprise':
        recommendations.append("Leverage existing infrastructure for cost savings")
        recommendations.append("Consider phased rollout across departments")
        recommendations.append("Implement comprehensive change management")
    
    if industry in ['fintech', 'healthtech']:
        recommendations.append("Budget extra for compliance and security requirements")
        recommendations.append("Engage with regulatory bodies early in the process")
    
    if industry in ['crypto', 'nft', 'web3']:
        recommendations.append("Stay updated with rapidly changing regulations")
        recommendations.append("Consider market volatility in financial planning")
        recommendations.append("Build strong community engagement strategies")
    
    if project_type == 'ai_integration':
        recommendations.append("Start with pilot program to validate AI use cases")
        recommendations.append("Ensure data quality before implementation")
        recommendations.append("Invest in AI ethics and bias mitigation")
    
    if project_type == 'blockchain_platform':
        recommendations.append("Choose the right blockchain network for your needs")
        recommendations.append("Plan for scalability from the beginning")
        recommendations.append("Consider environmental impact and sustainability")
    
    recommendations.append("Establish clear KPIs and success metrics")
    recommendations.append("Plan for ongoing maintenance and updates")
    
    return recommendations

# Bind the method to the calculator instance
calculator._get_recommendations = _get_recommendations.__get__(calculator, EnhancedROICalculator)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)