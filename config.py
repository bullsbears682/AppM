"""
Enterprise Configuration Management for VoidSight Analytics
Production-ready configuration with security, scaling, and commercial features
"""

import os
import secrets
from datetime import timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional
from decimal import Decimal

@dataclass
class CurrencyConfig:
    """Enhanced currency configuration for international markets"""
    symbol: str
    name: str
    code: str
    precision: int
    format_pattern: str
    rate: float  # Exchange rate relative to USD (1.0 for USD)
    
    def format_amount(self, amount: float) -> str:
        """Format amount according to currency rules"""
        if self.precision == 0:
            return f"{self.symbol}{int(amount):,}"
        else:
            return f"{self.symbol}{amount:,.{self.precision}f}"

class BaseConfig:
    """Enhanced base configuration for enterprise deployment"""
    
    # Environment Configuration
    ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Application Metadata
    APP_NAME = "VoidSight Analytics"
    APP_VERSION = "2.0 Enterprise"
    APP_DESCRIPTION = "Professional ROI Intelligence Platform"
    COMPANY_NAME = "VoidSight Analytics"
    
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_urlsafe(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///voidsight_analytics.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Redis Configuration for Caching
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Server Configuration
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 5000)
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # CORS and Security
    ENABLE_CORS = os.environ.get('ENABLE_CORS', 'True').lower() == 'true'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'memory://'
    RATELIMIT_DEFAULT = "100 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'xlsx', 'json'}
    
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    LOG_FILE = os.environ.get('LOG_FILE') or 'infinex_roi.log'
    
    # Business Logic Configuration
    CALCULATION_PRECISION = int(os.environ.get('CALCULATION_PRECISION') or 4)
    DEFAULT_CURRENCY = os.environ.get('DEFAULT_CURRENCY') or 'USD'
    MIN_INVESTMENT = Decimal(os.environ.get('MIN_INVESTMENT') or '1000')
    MAX_INVESTMENT = Decimal(os.environ.get('MAX_INVESTMENT') or '100000000')
    MIN_TIMELINE = int(os.environ.get('MIN_TIMELINE') or 1)
    MAX_TIMELINE = int(os.environ.get('MAX_TIMELINE') or 120)
    MIN_ROI = Decimal(os.environ.get('MIN_ROI') or '0.1')
    MAX_ROI = Decimal(os.environ.get('MAX_ROI') or '1000')
    
    # Monte Carlo Simulation
    MONTE_CARLO_ITERATIONS = int(os.environ.get('MONTE_CARLO_ITERATIONS') or 10000)
    CONFIDENCE_LEVEL = float(os.environ.get('CONFIDENCE_LEVEL') or 0.95)
    
    # Enhanced Currency Support
    CURRENCIES: Dict[str, CurrencyConfig] = {
        'USD': CurrencyConfig('$', 'US Dollar', 'USD', 2, '${:,.2f}', 1.0),
        'EUR': CurrencyConfig('€', 'Euro', 'EUR', 2, '€{:,.2f}', 1.05),
        'GBP': CurrencyConfig('£', 'British Pound', 'GBP', 2, '£{:,.2f}', 1.25),
        'JPY': CurrencyConfig('¥', 'Japanese Yen', 'JPY', 0, '¥{:,}', 0.007),
        'CAD': CurrencyConfig('C$', 'Canadian Dollar', 'CAD', 2, 'C${:,.2f}', 0.75),
        'AUD': CurrencyConfig('A$', 'Australian Dollar', 'AUD', 2, 'A${:,.2f}', 0.65),
        'CHF': CurrencyConfig('Fr', 'Swiss Franc', 'CHF', 2, 'Fr{:,.2f}', 1.10),
        'CNY': CurrencyConfig('¥', 'Chinese Yuan', 'CNY', 2, '¥{:,.2f}', 0.15),
        'INR': CurrencyConfig('₹', 'Indian Rupee', 'INR', 2, '₹{:,.2f}', 0.013),
        'KRW': CurrencyConfig('₩', 'South Korean Won', 'KRW', 0, '₩{:,}', 0.0008),
        'SGD': CurrencyConfig('S$', 'Singapore Dollar', 'SGD', 2, 'S${:,.2f}', 0.70),
        'HKD': CurrencyConfig('HK$', 'Hong Kong Dollar', 'HKD', 2, 'HK${:,.2f}', 0.13),
        'BTC': CurrencyConfig('₿', 'Bitcoin', 'BTC', 8, '₿{:.8f}', 30000.0),
        'ETH': CurrencyConfig('Ξ', 'Ethereum', 'ETH', 6, 'Ξ{:.6f}', 2000.0),
    }
    
    # Industry Configuration with Enhanced Metadata
    INDUSTRIES = {
        'fintech': {
            'name': 'FinTech & Digital Banking',
            'growth_rate': 0.15,
            'risk_factor': 0.7,
            'market_size': 150_000_000_000,
            'volatility': 0.3,
            'description': 'Financial technology and digital banking solutions'
        },
        'healthtech': {
            'name': 'HealthTech & MedTech',
            'growth_rate': 0.18,
            'risk_factor': 0.8,
            'market_size': 250_000_000_000,
            'volatility': 0.25,
            'description': 'Healthcare technology and medical device innovation'
        },
        'edtech': {
            'name': 'EdTech & Learning Platforms',
            'growth_rate': 0.12,
            'risk_factor': 0.6,
            'market_size': 90_000_000_000,
            'volatility': 0.35,
            'description': 'Educational technology and e-learning platforms'
        },
        'ecommerce': {
            'name': 'E-commerce & Digital Retail',
            'growth_rate': 0.14,
            'risk_factor': 0.5,
            'market_size': 450_000_000_000,
            'volatility': 0.28,
            'description': 'Online retail and digital commerce platforms'
        },
        'saas': {
            'name': 'SaaS & Cloud Solutions',
            'growth_rate': 0.16,
            'risk_factor': 0.6,
            'market_size': 180_000_000_000,
            'volatility': 0.32,
            'description': 'Software as a Service and cloud computing'
        },
        'gaming': {
            'name': 'Gaming & Interactive Entertainment',
            'growth_rate': 0.13,
            'risk_factor': 0.7,
            'market_size': 200_000_000_000,
            'volatility': 0.4,
            'description': 'Video games and interactive entertainment'
        },
        'realestate': {
            'name': 'PropTech & Real Estate',
            'growth_rate': 0.08,
            'risk_factor': 0.4,
            'market_size': 320_000_000_000,
            'volatility': 0.2,
            'description': 'Property technology and real estate innovation'
        },
        'foodbeverage': {
            'name': 'Food & Beverage Innovation',
            'growth_rate': 0.06,
            'risk_factor': 0.3,
            'market_size': 180_000_000_000,
            'volatility': 0.15,
            'description': 'Food technology and beverage innovation'
        },
        'manufacturing': {
            'name': 'Smart Manufacturing & Industry 4.0',
            'growth_rate': 0.09,
            'risk_factor': 0.4,
            'market_size': 400_000_000_000,
            'volatility': 0.22,
            'description': 'Advanced manufacturing and industrial automation'
        },
        'logistics': {
            'name': 'Logistics & Supply Chain Tech',
            'growth_rate': 0.11,
            'risk_factor': 0.5,
            'market_size': 140_000_000_000,
            'volatility': 0.25,
            'description': 'Supply chain technology and logistics optimization'
        },
        'crypto': {
            'name': 'Cryptocurrency & DeFi',
            'growth_rate': 0.25,
            'risk_factor': 0.9,
            'market_size': 120_000_000_000,
            'volatility': 0.6,
            'description': 'Cryptocurrency and decentralized finance'
        },
        'nft': {
            'name': 'NFT & Digital Assets',
            'growth_rate': 0.35,
            'risk_factor': 0.95,
            'market_size': 25_000_000_000,
            'volatility': 0.8,
            'description': 'Non-fungible tokens and digital collectibles'
        },
        'web3': {
            'name': 'Web3 & Metaverse',
            'growth_rate': 0.40,
            'risk_factor': 0.9,
            'market_size': 80_000_000_000,
            'volatility': 0.7,
            'description': 'Decentralized web and virtual worlds'
        },
        'sustainability': {
            'name': 'GreenTech & Sustainability',
            'growth_rate': 0.20,
            'risk_factor': 0.6,
            'market_size': 110_000_000_000,
            'volatility': 0.3,
            'description': 'Environmental technology and sustainable solutions'
        },
        'biotech': {
            'name': 'BioTech & Life Sciences',
            'growth_rate': 0.12,
            'risk_factor': 0.8,
            'market_size': 200_000_000_000,
            'volatility': 0.35,
            'description': 'Biotechnology and life sciences innovation'
        },
        'ai': {
            'name': 'Artificial Intelligence & ML',
            'growth_rate': 0.30,
            'risk_factor': 0.7,
            'market_size': 95_000_000_000,
            'volatility': 0.45,
            'description': 'AI, machine learning, and cognitive computing'
        },
        'iot': {
            'name': 'IoT & Connected Devices',
            'growth_rate': 0.18,
            'risk_factor': 0.6,
            'market_size': 130_000_000_000,
            'volatility': 0.35,
            'description': 'Internet of Things and connected device ecosystems'
        },
        'blockchain': {
            'name': 'Blockchain Infrastructure',
            'growth_rate': 0.28,
            'risk_factor': 0.8,
            'market_size': 70_000_000_000,
            'volatility': 0.5,
            'description': 'Blockchain technology and distributed ledger systems'
        }
    }
    
    # Project Type Configuration with Enhanced Metadata
    PROJECT_TYPES = {
        'product_development': {
            'description': 'New Product Development',
            'complexity': 'High',
            'timeline': 12,
            'base_cost': 75000,  # Reduced from 150000
            'roi_potential': 2.5,
            'risk_level': 0.3,
            'required_skills': ['Product Manager', 'Software Engineer', 'Designer', 'QA Engineer']
        },
        'digital_transformation': {
            'description': 'Digital Transformation',
            'complexity': 'Very High',
            'timeline': 18,
            'base_cost': 100000,  # Reduced from 200000
            'roi_potential': 3.0,
            'risk_level': 0.25,
            'required_skills': ['Solution Architect', 'Change Manager', 'Software Engineer', 'Business Analyst']
        },
        'market_expansion': {
            'description': 'Market Expansion',
            'complexity': 'Medium',
            'timeline': 8,
            'base_cost': 50000,  # Reduced from 100000
            'roi_potential': 2.2,
            'risk_level': 0.35,
            'required_skills': ['Marketing Manager', 'Sales Representative', 'Market Researcher']
        },
        'tech_upgrade': {
            'description': 'Technology Upgrade',
            'complexity': 'Medium',
            'timeline': 6,
            'base_cost': 40000,  # Reduced from 80000
            'roi_potential': 1.8,
            'risk_level': 0.2,
            'required_skills': ['System Administrator', 'Software Engineer', 'Technical Lead']
        },
        'marketing_campaign': {
            'description': 'Marketing Campaign',
            'complexity': 'Low',
            'timeline': 4,
            'base_cost': 25000,  # Reduced from 50000
            'roi_potential': 1.5,
            'risk_level': 0.25,
            'required_skills': ['Marketing Manager', 'Graphic Designer', 'Content Writer']
        },
        'ecommerce_platform': {
            'description': 'E-commerce Platform',
            'complexity': 'High',
            'timeline': 10,
            'base_cost': 60000,  # Reduced from 120000
            'roi_potential': 2.8,
            'risk_level': 0.28,
            'required_skills': ['E-commerce Developer', 'UX Designer', 'Payment Integration Specialist']
        },
        'mobile_app': {
            'description': 'Mobile Application',
            'complexity': 'High',
            'timeline': 8,
            'base_cost': 45000,  # Reduced from 90000
            'roi_potential': 2.4,
            'risk_level': 0.32,
            'required_skills': ['Mobile Developer', 'UI/UX Designer', 'Backend Developer']
        },
        'ai_integration': {
            'description': 'AI Integration',
            'complexity': 'Very High',
            'timeline': 14,
            'base_cost': 90000,  # Reduced from 180000
            'roi_potential': 3.5,
            'risk_level': 0.4,
            'required_skills': ['AI Engineer', 'Data Scientist', 'ML Engineer', 'Software Architect']
        },
        'blockchain_platform': {
            'description': 'Blockchain Platform',
            'complexity': 'Very High',
            'timeline': 16,
            'base_cost': 250000,
            'roi_potential': 4.0,
            'risk_level': 0.5,
            'required_skills': ['Blockchain Developer', 'Smart Contract Engineer', 'Security Auditor']
        },
        'iot_solution': {
            'description': 'IoT Solution',
            'complexity': 'High',
            'timeline': 12,
            'base_cost': 160000,
            'roi_potential': 2.6,
            'risk_level': 0.35,
            'required_skills': ['IoT Engineer', 'Embedded Developer', 'Cloud Architect']
        },
        'data_analytics': {
            'description': 'Data Analytics Platform',
            'complexity': 'High',
            'timeline': 10,
            'base_cost': 140000,
            'roi_potential': 2.9,
            'risk_level': 0.28,
            'required_skills': ['Data Engineer', 'Data Analyst', 'BI Developer']
        },
        'subscription_service': {
            'description': 'Subscription Service',
            'complexity': 'Medium',
            'timeline': 6,
            'base_cost': 75000,
            'roi_potential': 2.1,
            'risk_level': 0.22,
            'required_skills': ['Backend Developer', 'Payment Specialist', 'Customer Success Manager']
        },
        'automation_system': {
            'description': 'Automation System',
            'complexity': 'High',
            'timeline': 9,
            'base_cost': 110000,
            'roi_potential': 3.2,
            'risk_level': 0.25,
            'required_skills': ['Automation Engineer', 'System Integrator', 'Process Analyst']
        },
        'cybersecurity_upgrade': {
            'description': 'Cybersecurity Upgrade',
            'complexity': 'Medium',
            'timeline': 7,
            'base_cost': 95000,
            'roi_potential': 1.9,
            'risk_level': 0.15,
            'required_skills': ['Security Engineer', 'Penetration Tester', 'Compliance Specialist']
        },
        'cloud_migration': {
            'description': 'Cloud Migration',
            'complexity': 'High',
            'timeline': 11,
            'base_cost': 130000,
            'roi_potential': 2.3,
            'risk_level': 0.18,
            'required_skills': ['Cloud Architect', 'DevOps Engineer', 'Migration Specialist']
        }
    }

    # Company Size Configuration
    COMPANY_SIZES = {
        'startup': {
            'name': 'Startup Ecosystem',
            'employees': '1-10',
            'cost_multiplier': 0.8,
            'risk_multiplier': 1.3,
            'agility_factor': 1.5,
            'min_budget': 5000,
            'max_budget': 100000,
            'typical_team_size': 5,
            'description': 'Early-stage startups and entrepreneurial ventures'
        },
        'small': {
            'name': 'Small Enterprise',
            'employees': '11-50',
            'cost_multiplier': 1.0,
            'risk_multiplier': 1.1,
            'agility_factor': 1.3,
            'min_budget': 25000,
            'max_budget': 500000,
            'typical_team_size': 15,
            'description': 'Small businesses and growing companies'
        },
        'medium': {
            'name': 'Medium Corporation',
            'employees': '51-200',
            'cost_multiplier': 1.2,
            'risk_multiplier': 0.9,
            'agility_factor': 1.1,
            'min_budget': 100000,
            'max_budget': 2000000,
            'typical_team_size': 50,
            'description': 'Mid-sized corporations and established businesses'
        },
        'large': {
            'name': 'Large Organization',
            'employees': '201-1000',
            'cost_multiplier': 1.5,
            'risk_multiplier': 0.7,
            'agility_factor': 0.9,
            'min_budget': 1000000,
            'max_budget': 25000000,
            'typical_team_size': 100,
            'description': 'Large corporations and multinational enterprises'
        },
        'enterprise': {
            'name': 'Global Enterprise',
            'employees': '1000+',
            'cost_multiplier': 2.0,
            'risk_multiplier': 0.5,
            'agility_factor': 0.7,
            'min_budget': 5000000,
            'max_budget': 100000000,
            'typical_team_size': 200,
            'description': 'Fortune 500 companies and global enterprises'
        }
    }
    
    # API Configuration
    API_RATE_LIMIT = "1000 per hour"
    API_VERSION = "v3.0"
    API_TITLE = "Infinex ROI Calculator API"
    API_DESCRIPTION = "Professional Investment Analysis and ROI Calculation API"
    
    # Feature Flags
    ENABLE_USER_AUTHENTICATION = os.environ.get('ENABLE_AUTH', 'True').lower() == 'true'
    ENABLE_DATA_PERSISTENCE = os.environ.get('ENABLE_PERSISTENCE', 'True').lower() == 'true'
    ENABLE_REAL_TIME_DATA = os.environ.get('ENABLE_REAL_TIME', 'False').lower() == 'true'
    ENABLE_ADVANCED_ANALYTICS = os.environ.get('ENABLE_ANALYTICS', 'True').lower() == 'true'
    ENABLE_EXPORT_FEATURES = os.environ.get('ENABLE_EXPORT', 'True').lower() == 'true'
    
    # Licensing and Monetization
    LICENSE_CHECK_INTERVAL = int(os.environ.get('LICENSE_CHECK_INTERVAL') or 3600)  # 1 hour
    TRIAL_PERIOD_DAYS = int(os.environ.get('TRIAL_PERIOD_DAYS') or 30)
    MAX_CALCULATIONS_FREE = int(os.environ.get('MAX_CALCULATIONS_FREE') or 10)
    
    # Performance Configuration
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT') or 300)
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT') or 3600)
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS') or 4)
    
    @classmethod
    def init_app(cls, app):
        """Initialize application with configuration"""
        pass

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    ENV = 'development'
    DEBUG = True  # Enabled for development
    TESTING = False
    LOG_LEVEL = 'DEBUG'
    MONTE_CARLO_ITERATIONS = 1000  # Reduced for faster development

class TestingConfig(BaseConfig):
    """Testing configuration"""
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    ENV = 'testing'
    TESTING = True
    DEBUG = False  # Disabled for security
    DATABASE_URL = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = True
    MONTE_CARLO_ITERATIONS = 100  # Minimal for testing

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'WARNING'
    
    # Production security enhancements
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Production database configuration
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 0
    }
    
    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)
        
        # Production-specific initialization
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug:
            file_handler = RotatingFileHandler(
                cls.LOG_FILE, maxBytes=10240000, backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

class EnterpriseConfig(ProductionConfig):
    """Enterprise configuration with advanced features"""
    
    # Enhanced security
    ENABLE_TWO_FACTOR_AUTH = True
    ENABLE_AUDIT_LOGGING = True
    ENABLE_IP_WHITELIST = True
    
    # Advanced features
    ENABLE_REAL_TIME_DATA = True
    ENABLE_ADVANCED_ANALYTICS = True
    ENABLE_CUSTOM_BRANDING = True
    ENABLE_API_INTEGRATION = True
    
    # Performance optimization
    MONTE_CARLO_ITERATIONS = 50000
    MAX_WORKERS = 16
    
    # Enterprise licensing
    REQUIRE_LICENSE_KEY = True
    ENABLE_USAGE_ANALYTICS = True

def get_config(config_name=None):
    """Get configuration based on environment"""
    config_name = config_name or os.environ.get('FLASK_ENV', 'production')
    
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'enterprise': EnterpriseConfig
    }
    
    return configs.get(config_name, DevelopmentConfig)

# Export the current configuration
Config = get_config()