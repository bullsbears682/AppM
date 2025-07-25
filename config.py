"""
Configuration management for Business ROI Calculator
Centralized configuration with environment-based settings
"""

import os
from dataclasses import dataclass, field
from typing import Dict, Any
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class CurrencyConfig:
    symbol: str
    rate: float
    name: str
    precision: int = 2

@dataclass
class IndustryConfig:
    growth_rate: float
    risk_factor: float
    market_size: str
    volatility: float
    regulatory_complexity: str = "Medium"
    
    def __post_init__(self):
        # Validate ranges
        if not (0 <= self.growth_rate <= 1):
            raise ValueError(f"Growth rate must be between 0 and 1, got {self.growth_rate}")
        if not (0 <= self.risk_factor <= 1):
            raise ValueError(f"Risk factor must be between 0 and 1, got {self.risk_factor}")
        if not (0 <= self.volatility <= 1):
            raise ValueError(f"Volatility must be between 0 and 1, got {self.volatility}")

@dataclass
class CompanySizeConfig:
    multiplier: float
    min_budget: int
    max_budget: int
    risk_factor: float
    typical_team_size: int = 10
    
    def __post_init__(self):
        if self.min_budget >= self.max_budget:
            raise ValueError("Min budget must be less than max budget")

@dataclass
class ProjectTypeConfig:
    base_cost: int
    timeline: int
    roi_potential: float
    description: str
    complexity: str
    risk_level: float
    required_skills: list = field(default_factory=list)

class Config:
    """Main configuration class with environment-specific settings"""
    
    # Environment settings
    ENV = os.getenv('FLASK_ENV', Environment.DEVELOPMENT.value)
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # API settings
    API_RATE_LIMIT = os.getenv('API_RATE_LIMIT', '100 per hour')
    ENABLE_CORS = os.getenv('ENABLE_CORS', 'True').lower() == 'true'
    
    # Currency settings with validation
    CURRENCIES = {
        'USD': CurrencyConfig('$', 1.0, 'US Dollar'),
        'EUR': CurrencyConfig('€', 0.85, 'Euro'),
        'GBP': CurrencyConfig('£', 0.73, 'British Pound'),
        'JPY': CurrencyConfig('¥', 110.0, 'Japanese Yen', precision=0),
        'CAD': CurrencyConfig('C$', 1.25, 'Canadian Dollar'),
        'AUD': CurrencyConfig('A$', 1.35, 'Australian Dollar'),
        'CHF': CurrencyConfig('CHF', 0.92, 'Swiss Franc'),
        'CNY': CurrencyConfig('¥', 6.45, 'Chinese Yuan'),
        'INR': CurrencyConfig('₹', 74.5, 'Indian Rupee'),
        'BRL': CurrencyConfig('R$', 5.2, 'Brazilian Real')
    }
    
    # Company size configurations
    COMPANY_SIZES = {
        'startup': CompanySizeConfig(0.7, 5000, 100000, 0.3, 5),
        'small': CompanySizeConfig(1.0, 25000, 500000, 0.2, 15),
        'medium': CompanySizeConfig(1.5, 100000, 2000000, 0.15, 50),
        'enterprise': CompanySizeConfig(2.5, 500000, 10000000, 0.1, 200)
    }
    
    # Industry configurations with enhanced validation
    INDUSTRIES = {
        'fintech': IndustryConfig(0.25, 0.15, 'Large', 0.2, 'High'),
        'healthtech': IndustryConfig(0.30, 0.20, 'Huge', 0.15, 'Very High'),
        'edtech': IndustryConfig(0.22, 0.12, 'Large', 0.18, 'Medium'),
        'ecommerce': IndustryConfig(0.18, 0.08, 'Massive', 0.12, 'Low'),
        'saas': IndustryConfig(0.35, 0.18, 'Large', 0.22, 'Medium'),
        'gaming': IndustryConfig(0.20, 0.25, 'Medium', 0.3, 'Medium'),
        'realEstate': IndustryConfig(0.15, 0.10, 'Stable', 0.08, 'High'),
        'foodBeverage': IndustryConfig(0.12, 0.15, 'Medium', 0.1, 'High'),
        'manufacturing': IndustryConfig(0.10, 0.08, 'Large', 0.06, 'High'),
        'logistics': IndustryConfig(0.16, 0.12, 'Large', 0.14, 'Medium'),
        'crypto': IndustryConfig(0.45, 0.40, 'Volatile', 0.5, 'Very High'),
        'nft': IndustryConfig(0.35, 0.45, 'Emerging', 0.6, 'Very High'),
        'web3': IndustryConfig(0.40, 0.35, 'Growing', 0.4, 'High'),
        'sustainability': IndustryConfig(0.28, 0.18, 'Expanding', 0.16, 'Medium'),
        'biotech': IndustryConfig(0.32, 0.25, 'Specialized', 0.28, 'Very High')
    }
    
    # Project type configurations
    PROJECT_TYPES = {
        'product_development': ProjectTypeConfig(
            150000, 12, 2.5, 'New Product Development', 'High', 0.2,
            ['Product Manager', 'Software Engineer', 'Designer', 'QA Engineer']
        ),
        'digital_transformation': ProjectTypeConfig(
            200000, 18, 3.0, 'Digital Transformation', 'Very High', 0.15,
            ['Solution Architect', 'Change Manager', 'Software Engineer', 'Business Analyst']
        ),
        'market_expansion': ProjectTypeConfig(
            100000, 8, 2.0, 'Market Expansion', 'Medium', 0.18,
            ['Marketing Manager', 'Sales Representative', 'Market Researcher']
        ),
        'tech_upgrade': ProjectTypeConfig(
            80000, 6, 1.8, 'Technology Upgrade', 'Medium', 0.12,
            ['System Administrator', 'Software Engineer', 'Technical Lead']
        ),
        'marketing_campaign': ProjectTypeConfig(
            50000, 4, 1.5, 'Marketing Campaign', 'Low', 0.15,
            ['Marketing Manager', 'Graphic Designer', 'Content Writer']
        ),
        'ecommerce_platform': ProjectTypeConfig(
            120000, 10, 2.2, 'E-commerce Platform', 'High', 0.16,
            ['E-commerce Developer', 'UX Designer', 'Payment Integration Specialist']
        ),
        'mobile_app': ProjectTypeConfig(
            90000, 8, 2.0, 'Mobile Application', 'High', 0.18,
            ['Mobile Developer', 'UI/UX Designer', 'Backend Developer']
        ),
        'ai_integration': ProjectTypeConfig(
            180000, 14, 2.8, 'AI Integration', 'Very High', 0.22,
            ['AI Engineer', 'Data Scientist', 'ML Engineer', 'Software Architect']
        ),
        'blockchain_platform': ProjectTypeConfig(
            250000, 16, 3.5, 'Blockchain Platform', 'Very High', 0.35,
            ['Blockchain Developer', 'Smart Contract Engineer', 'Security Auditor']
        ),
        'iot_solution': ProjectTypeConfig(
            160000, 12, 2.3, 'IoT Solution', 'High', 0.20,
            ['IoT Engineer', 'Embedded Developer', 'Cloud Architect']
        ),
        'data_analytics': ProjectTypeConfig(
            140000, 10, 2.4, 'Data Analytics Platform', 'High', 0.17,
            ['Data Engineer', 'Data Analyst', 'BI Developer']
        ),
        'subscription_service': ProjectTypeConfig(
            75000, 6, 2.1, 'Subscription Service', 'Medium', 0.14,
            ['Backend Developer', 'Payment Specialist', 'Customer Success Manager']
        ),
        'automation_system': ProjectTypeConfig(
            110000, 9, 2.6, 'Automation System', 'High', 0.13,
            ['Automation Engineer', 'System Integrator', 'Process Analyst']
        ),
        'cybersecurity_upgrade': ProjectTypeConfig(
            95000, 7, 1.9, 'Cybersecurity Upgrade', 'Medium', 0.08,
            ['Security Engineer', 'Penetration Tester', 'Compliance Specialist']
        ),
        'cloud_migration': ProjectTypeConfig(
            130000, 11, 2.2, 'Cloud Migration', 'High', 0.11,
            ['Cloud Architect', 'DevOps Engineer', 'Migration Specialist']
        )
    }
    
    # Calculation settings
    CALCULATION_PRECISION = 4
    DEFAULT_CURRENCY = 'USD'
    MIN_INVESTMENT = 1000
    MAX_INVESTMENT = 50000000
    
    # Validation settings
    ENABLE_STRICT_VALIDATION = True
    MAX_REQUEST_SIZE = 16 * 1024 * 1024  # 16MB
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def validate_config(cls):
        """Validate all configuration settings"""
        errors = []
        
        # Validate currencies
        for currency_code, currency_config in cls.CURRENCIES.items():
            if not isinstance(currency_config, CurrencyConfig):
                errors.append(f"Invalid currency config for {currency_code}")
            elif currency_config.rate <= 0:
                errors.append(f"Invalid exchange rate for {currency_code}")
        
        # Validate industries
        for industry_code, industry_config in cls.INDUSTRIES.items():
            try:
                # This will trigger validation in __post_init__
                IndustryConfig(**industry_config.__dict__)
            except ValueError as e:
                errors.append(f"Invalid industry config for {industry_code}: {e}")
        
        # Validate company sizes
        for size_code, size_config in cls.COMPANY_SIZES.items():
            try:
                CompanySizeConfig(**size_config.__dict__)
            except ValueError as e:
                errors.append(f"Invalid company size config for {size_code}: {e}")
        
        if errors:
            raise ValueError(f"Configuration validation failed: {'; '.join(errors)}")
        
        return True

# Production-specific configuration
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production
    
    # Enhanced security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Database settings (if needed)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # External API settings
    CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')
    ENABLE_REAL_TIME_RATES = True

# Development-specific configuration  
class DevelopmentConfig(Config):
    DEBUG = True
    
# Testing configuration
class TestingConfig(Config):
    TESTING = True
    DEBUG = True

# Configuration factory
def get_config():
    """Factory function to get appropriate configuration based on environment"""
    env = os.getenv('FLASK_ENV', Environment.DEVELOPMENT.value)
    
    if env == Environment.PRODUCTION.value:
        return ProductionConfig
    elif env == Environment.TESTING.value:
        return TestingConfig
    else:
        return DevelopmentConfig