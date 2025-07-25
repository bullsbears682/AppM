#!/usr/bin/env python3
"""
Configuration management for Business ROI Calculator
Centralized settings and constants
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Application settings
    APP_NAME = "Business ROI Calculator"
    VERSION = "2.0.0"
    AUTHOR = "Enhanced Edition"
    
    # Currency API settings (for future real-time rates)
    CURRENCY_API_URL = os.environ.get('CURRENCY_API_URL', 'https://api.exchangerate-api.com/v4/latest/USD')
    CURRENCY_UPDATE_INTERVAL = timedelta(hours=1)
    
    # Rate limiting settings
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    DEFAULT_RATE_LIMIT = "100 per hour"
    
    # Cache settings
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    CACHE_TYPE = "simple"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

class TestConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    CACHE_TYPE = "null"

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}

# Business constants
COMPANY_SIZES = {
    'startup': {
        'multiplier': 0.7, 
        'min_budget': 5000, 
        'max_budget': 100000, 
        'risk_factor': 0.3,
        'description': 'Early-stage startup (1-10 employees)',
        'typical_revenue': '< $1M'
    },
    'small': {
        'multiplier': 1.0, 
        'min_budget': 25000, 
        'max_budget': 500000, 
        'risk_factor': 0.2,
        'description': 'Small business (11-50 employees)',
        'typical_revenue': '$1M - $10M'
    },
    'medium': {
        'multiplier': 1.5, 
        'min_budget': 100000, 
        'max_budget': 2000000, 
        'risk_factor': 0.15,
        'description': 'Medium enterprise (51-500 employees)',
        'typical_revenue': '$10M - $100M'
    },
    'enterprise': {
        'multiplier': 2.5, 
        'min_budget': 500000, 
        'max_budget': 10000000, 
        'risk_factor': 0.1,
        'description': 'Large enterprise (500+ employees)',
        'typical_revenue': '$100M+'
    }
}

INDUSTRIES = {
    'fintech': {
        'growth_rate': 0.25, 
        'risk_factor': 0.15, 
        'market_size': 'Large', 
        'volatility': 0.2,
        'description': 'Financial Technology',
        'regulatory_complexity': 'High'
    },
    'healthtech': {
        'growth_rate': 0.30, 
        'risk_factor': 0.20, 
        'market_size': 'Huge', 
        'volatility': 0.15,
        'description': 'Healthcare Technology',
        'regulatory_complexity': 'Very High'
    },
    'edtech': {
        'growth_rate': 0.22, 
        'risk_factor': 0.12, 
        'market_size': 'Large', 
        'volatility': 0.18,
        'description': 'Education Technology',
        'regulatory_complexity': 'Medium'
    },
    'ecommerce': {
        'growth_rate': 0.18, 
        'risk_factor': 0.08, 
        'market_size': 'Massive', 
        'volatility': 0.12,
        'description': 'E-commerce & Retail',
        'regulatory_complexity': 'Low'
    },
    'saas': {
        'growth_rate': 0.35, 
        'risk_factor': 0.18, 
        'market_size': 'Large', 
        'volatility': 0.22,
        'description': 'Software as a Service',
        'regulatory_complexity': 'Medium'
    },
    'gaming': {
        'growth_rate': 0.20, 
        'risk_factor': 0.25, 
        'market_size': 'Medium', 
        'volatility': 0.3,
        'description': 'Gaming & Entertainment',
        'regulatory_complexity': 'Low'
    },
    'realEstate': {
        'growth_rate': 0.15, 
        'risk_factor': 0.10, 
        'market_size': 'Stable', 
        'volatility': 0.08,
        'description': 'Real Estate Technology',
        'regulatory_complexity': 'High'
    },
    'foodBeverage': {
        'growth_rate': 0.12, 
        'risk_factor': 0.15, 
        'market_size': 'Medium', 
        'volatility': 0.1,
        'description': 'Food & Beverage',
        'regulatory_complexity': 'Medium'
    },
    'manufacturing': {
        'growth_rate': 0.10, 
        'risk_factor': 0.08, 
        'market_size': 'Large', 
        'volatility': 0.06,
        'description': 'Manufacturing & Industrial',
        'regulatory_complexity': 'Medium'
    },
    'logistics': {
        'growth_rate': 0.16, 
        'risk_factor': 0.12, 
        'market_size': 'Large', 
        'volatility': 0.14,
        'description': 'Logistics & Transportation',
        'regulatory_complexity': 'Medium'
    },
    'crypto': {
        'growth_rate': 0.45, 
        'risk_factor': 0.40, 
        'market_size': 'Volatile', 
        'volatility': 0.5,
        'description': 'Cryptocurrency & DeFi',
        'regulatory_complexity': 'Very High'
    },
    'web3': {
        'growth_rate': 0.40, 
        'risk_factor': 0.35, 
        'market_size': 'Growing', 
        'volatility': 0.4,
        'description': 'Web3 & Blockchain',
        'regulatory_complexity': 'High'
    },
    'sustainability': {
        'growth_rate': 0.28, 
        'risk_factor': 0.18, 
        'market_size': 'Expanding', 
        'volatility': 0.16,
        'description': 'Sustainability & CleanTech',
        'regulatory_complexity': 'Medium'
    },
    'biotech': {
        'growth_rate': 0.32, 
        'risk_factor': 0.25, 
        'market_size': 'Specialized', 
        'volatility': 0.28,
        'description': 'Biotechnology',
        'regulatory_complexity': 'Very High'
    }
}

PROJECT_TYPES = {
    'product_development': {
        'base_cost': 150000, 
        'timeline': 12, 
        'roi_potential': 2.5,
        'description': 'New Product Development', 
        'complexity': 'High', 
        'risk_level': 0.2,
        'required_skills': ['Product Management', 'Development', 'Design', 'Testing']
    },
    'digital_transformation': {
        'base_cost': 200000, 
        'timeline': 18, 
        'roi_potential': 3.0,
        'description': 'Digital Transformation', 
        'complexity': 'Very High', 
        'risk_level': 0.15,
        'required_skills': ['Change Management', 'System Integration', 'Data Migration', 'Training']
    },
    'market_expansion': {
        'base_cost': 100000, 
        'timeline': 8, 
        'roi_potential': 2.0,
        'description': 'Market Expansion', 
        'complexity': 'Medium', 
        'risk_level': 0.18,
        'required_skills': ['Market Research', 'Sales', 'Localization', 'Marketing']
    },
    'tech_upgrade': {
        'base_cost': 80000, 
        'timeline': 6, 
        'roi_potential': 1.8,
        'description': 'Technology Upgrade', 
        'complexity': 'Medium', 
        'risk_level': 0.12,
        'required_skills': ['System Administration', 'Migration', 'Training', 'Support']
    },
    'marketing_campaign': {
        'base_cost': 50000, 
        'timeline': 4, 
        'roi_potential': 1.5,
        'description': 'Marketing Campaign', 
        'complexity': 'Low', 
        'risk_level': 0.15,
        'required_skills': ['Marketing', 'Creative Design', 'Analytics', 'Campaign Management']
    },
    'ecommerce_platform': {
        'base_cost': 120000, 
        'timeline': 10, 
        'roi_potential': 2.2,
        'description': 'E-commerce Platform', 
        'complexity': 'High', 
        'risk_level': 0.16,
        'required_skills': ['E-commerce Development', 'Payment Integration', 'Security', 'UX Design']
    },
    'mobile_app': {
        'base_cost': 90000, 
        'timeline': 8, 
        'roi_potential': 2.0,
        'description': 'Mobile Application', 
        'complexity': 'High', 
        'risk_level': 0.18,
        'required_skills': ['Mobile Development', 'UI/UX Design', 'Backend Development', 'Testing']
    },
    'ai_integration': {
        'base_cost': 180000, 
        'timeline': 14, 
        'roi_potential': 2.8,
        'description': 'AI Integration', 
        'complexity': 'Very High', 
        'risk_level': 0.22,
        'required_skills': ['Machine Learning', 'Data Science', 'AI Engineering', 'Ethics & Compliance']
    },
    'blockchain_platform': {
        'base_cost': 250000, 
        'timeline': 16, 
        'roi_potential': 3.5,
        'description': 'Blockchain Platform', 
        'complexity': 'Very High', 
        'risk_level': 0.35,
        'required_skills': ['Blockchain Development', 'Smart Contracts', 'Security', 'Tokenomics']
    },
    'iot_solution': {
        'base_cost': 160000, 
        'timeline': 12, 
        'roi_potential': 2.3,
        'description': 'IoT Solution', 
        'complexity': 'High', 
        'risk_level': 0.20,
        'required_skills': ['IoT Development', 'Hardware Integration', 'Data Analytics', 'Security']
    },
    'data_analytics': {
        'base_cost': 140000, 
        'timeline': 10, 
        'roi_potential': 2.4,
        'description': 'Data Analytics Platform', 
        'complexity': 'High', 
        'risk_level': 0.17,
        'required_skills': ['Data Engineering', 'Analytics', 'Visualization', 'Machine Learning']
    },
    'cloud_migration': {
        'base_cost': 130000, 
        'timeline': 11, 
        'roi_potential': 2.2,
        'description': 'Cloud Migration', 
        'complexity': 'High', 
        'risk_level': 0.11,
        'required_skills': ['Cloud Architecture', 'Migration', 'Security', 'Cost Optimization']
    }
}

# Enhanced currency data with more accurate exchange rates
CURRENCIES = {
    'USD': {'symbol': '$', 'rate': 1.0, 'name': 'US Dollar', 'decimal_places': 2},
    'EUR': {'symbol': '€', 'rate': 0.85, 'name': 'Euro', 'decimal_places': 2},
    'GBP': {'symbol': '£', 'rate': 0.73, 'name': 'British Pound', 'decimal_places': 2},
    'JPY': {'symbol': '¥', 'rate': 110.0, 'name': 'Japanese Yen', 'decimal_places': 0},
    'CAD': {'symbol': 'C$', 'rate': 1.25, 'name': 'Canadian Dollar', 'decimal_places': 2},
    'AUD': {'symbol': 'A$', 'rate': 1.35, 'name': 'Australian Dollar', 'decimal_places': 2},
    'CHF': {'symbol': 'CHF', 'rate': 0.92, 'name': 'Swiss Franc', 'decimal_places': 2},
    'CNY': {'symbol': '¥', 'rate': 6.45, 'name': 'Chinese Yuan', 'decimal_places': 2},
    'INR': {'symbol': '₹', 'rate': 74.5, 'name': 'Indian Rupee', 'decimal_places': 2},
    'BRL': {'symbol': 'R$', 'rate': 5.2, 'name': 'Brazilian Real', 'decimal_places': 2}
}

# Validation constants
VALIDATION_RULES = {
    'company_name': {
        'min_length': 2,
        'max_length': 100,
        'pattern': r'^[a-zA-Z0-9\s\-\.\&]+$'
    },
    'company_size': {
        'allowed_values': list(COMPANY_SIZES.keys())
    },
    'industry': {
        'allowed_values': list(INDUSTRIES.keys())
    },
    'project_type': {
        'allowed_values': list(PROJECT_TYPES.keys())
    },
    'currency': {
        'allowed_values': list(CURRENCIES.keys())
    },
    'custom_budget': {
        'min_value': 1000,
        'max_value': 50000000
    }
}

# Error messages
ERROR_MESSAGES = {
    'validation_error': 'Invalid input provided. Please check your data and try again.',
    'calculation_error': 'Unable to calculate ROI. Please verify your inputs.',
    'currency_error': 'Currency conversion failed. Using default currency.',
    'data_not_found': 'Requested data not found.',
    'server_error': 'Internal server error. Please try again later.',
    'rate_limit_exceeded': 'Too many requests. Please wait before trying again.',
    'invalid_company_name': 'Company name must be 2-100 characters and contain only letters, numbers, spaces, hyphens, dots, and ampersands.',
    'invalid_budget': 'Budget must be between $1,000 and $50,000,000.',
    'missing_required_field': 'Required field is missing.',
    'invalid_enum_value': 'Selected value is not valid for this field.'
}

# UI Constants
UI_CONSTANTS = {
    'animation_duration': 300,
    'chart_colors': {
        'primary': '#00f2fe',
        'secondary': '#667eea',
        'success': '#00ff88',
        'warning': '#ffaa00',
        'danger': '#ff4757',
        'gradient_start': '#4facfe',
        'gradient_end': '#00f2fe'
    },
    'breakpoints': {
        'mobile': 768,
        'tablet': 1024,
        'desktop': 1200
    }
}