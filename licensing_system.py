"""
Professional Licensing and White-Label System for VoidSight Analytics
Enterprise-grade licensing with white-label capabilities for resellers and buyers
"""

import os
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import jwt
from cryptography.fernet import Fernet
import requests

class LicenseType(Enum):
    """Available license types"""
    TRIAL = "trial"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    WHITE_LABEL = "white_label"
    RESELLER = "reseller"
    UNLIMITED = "unlimited"

class LicenseStatus(Enum):
    """License status enumeration"""
    ACTIVE = "active"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    PENDING = "pending"

@dataclass
class LicenseFeatures:
    """Define features available for each license type"""
    calculations_per_month: int
    api_calls_per_hour: int
    users_limit: int
    reports_export: bool
    white_label_branding: bool
    custom_domains: bool
    api_access: bool
    priority_support: bool
    sla_guarantee: bool
    monte_carlo_simulations: bool
    advanced_analytics: bool
    custom_integrations: bool
    reseller_rights: bool
    source_code_access: bool

@dataclass
class License:
    """Professional license data structure"""
    license_id: str
    license_key: str
    license_type: LicenseType
    customer_name: str
    customer_email: str
    company_name: str
    issued_date: datetime
    expiry_date: datetime
    status: LicenseStatus
    features: LicenseFeatures
    usage_stats: Dict[str, Any]
    billing_info: Dict[str, Any]
    white_label_config: Optional[Dict[str, Any]] = None
    reseller_config: Optional[Dict[str, Any]] = None

class LicenseManager:
    """Professional license management system"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or os.environ.get('LICENSE_SECRET_KEY', secrets.token_urlsafe(32))
        self.encryption_key = Fernet.generate_key()
        self.fernet = Fernet(self.encryption_key)
        
        # License type configurations
        self.license_configs = {
            LicenseType.TRIAL: LicenseFeatures(
                calculations_per_month=50,
                api_calls_per_hour=100,
                users_limit=1,
                reports_export=True,
                white_label_branding=False,
                custom_domains=False,
                api_access=False,
                priority_support=False,
                sla_guarantee=False,
                monte_carlo_simulations=False,
                advanced_analytics=False,
                custom_integrations=False,
                reseller_rights=False,
                source_code_access=False
            ),
            LicenseType.BASIC: LicenseFeatures(
                calculations_per_month=500,
                api_calls_per_hour=1000,
                users_limit=5,
                reports_export=True,
                white_label_branding=False,
                custom_domains=False,
                api_access=True,
                priority_support=False,
                sla_guarantee=False,
                monte_carlo_simulations=True,
                advanced_analytics=False,
                custom_integrations=False,
                reseller_rights=False,
                source_code_access=False
            ),
            LicenseType.PROFESSIONAL: LicenseFeatures(
                calculations_per_month=2500,
                api_calls_per_hour=5000,
                users_limit=25,
                reports_export=True,
                white_label_branding=True,
                custom_domains=True,
                api_access=True,
                priority_support=True,
                sla_guarantee=True,
                monte_carlo_simulations=True,
                advanced_analytics=True,
                custom_integrations=False,
                reseller_rights=False,
                source_code_access=False
            ),
            LicenseType.ENTERPRISE: LicenseFeatures(
                calculations_per_month=10000,
                api_calls_per_hour=25000,
                users_limit=100,
                reports_export=True,
                white_label_branding=True,
                custom_domains=True,
                api_access=True,
                priority_support=True,
                sla_guarantee=True,
                monte_carlo_simulations=True,
                advanced_analytics=True,
                custom_integrations=True,
                reseller_rights=False,
                source_code_access=False
            ),
            LicenseType.WHITE_LABEL: LicenseFeatures(
                calculations_per_month=50000,
                api_calls_per_hour=100000,
                users_limit=1000,
                reports_export=True,
                white_label_branding=True,
                custom_domains=True,
                api_access=True,
                priority_support=True,
                sla_guarantee=True,
                monte_carlo_simulations=True,
                advanced_analytics=True,
                custom_integrations=True,
                reseller_rights=True,
                source_code_access=True
            ),
            LicenseType.RESELLER: LicenseFeatures(
                calculations_per_month=100000,
                api_calls_per_hour=250000,
                users_limit=10000,
                reports_export=True,
                white_label_branding=True,
                custom_domains=True,
                api_access=True,
                priority_support=True,
                sla_guarantee=True,
                monte_carlo_simulations=True,
                advanced_analytics=True,
                custom_integrations=True,
                reseller_rights=True,
                source_code_access=True
            ),
            LicenseType.UNLIMITED: LicenseFeatures(
                calculations_per_month=-1,  # Unlimited
                api_calls_per_hour=-1,      # Unlimited
                users_limit=-1,             # Unlimited
                reports_export=True,
                white_label_branding=True,
                custom_domains=True,
                api_access=True,
                priority_support=True,
                sla_guarantee=True,
                monte_carlo_simulations=True,
                advanced_analytics=True,
                custom_integrations=True,
                reseller_rights=True,
                source_code_access=True
            )
        }
    
    def generate_license_key(self, license_type: LicenseType, customer_email: str) -> str:
        """Generate secure license key"""
        timestamp = int(datetime.now().timestamp())
        data = f"{license_type.value}-{customer_email}-{timestamp}"
        hash_obj = hashlib.sha256(data.encode()).hexdigest()
        
        # Format as professional license key: XXXX-XXXX-XXXX-XXXX
        key_parts = [hash_obj[i:i+4].upper() for i in range(0, 16, 4)]
        return "-".join(key_parts)
    
    def create_license(self, 
                      license_type: LicenseType,
                      customer_name: str,
                      customer_email: str,
                      company_name: str,
                      duration_days: int = 365,
                      white_label_config: Dict = None,
                      reseller_config: Dict = None) -> License:
        """Create a new professional license"""
        
        license_id = secrets.token_urlsafe(16)
        license_key = self.generate_license_key(license_type, customer_email)
        
        issued_date = datetime.now()
        expiry_date = issued_date + timedelta(days=duration_days)
        
        features = self.license_configs[license_type]
        
        license_obj = License(
            license_id=license_id,
            license_key=license_key,
            license_type=license_type,
            customer_name=customer_name,
            customer_email=customer_email,
            company_name=company_name,
            issued_date=issued_date,
            expiry_date=expiry_date,
            status=LicenseStatus.ACTIVE,
            features=features,
            usage_stats={
                'calculations_used': 0,
                'api_calls_used': 0,
                'last_used': None,
                'total_users': 0
            },
            billing_info={
                'plan': license_type.value,
                'billing_cycle': 'annual' if duration_days >= 365 else 'monthly',
                'next_billing_date': expiry_date.isoformat(),
                'auto_renew': True
            },
            white_label_config=white_label_config,
            reseller_config=reseller_config
        )
        
        return license_obj
    
    def validate_license(self, license_key: str) -> Dict[str, Any]:
        """Validate license key and return status"""
        try:
            # In a real implementation, this would query a database
            # For demo purposes, we'll validate the format
            if not self._is_valid_license_format(license_key):
                return {
                    'valid': False,
                    'status': 'invalid_format',
                    'message': 'Invalid license key format'
                }
            
            # Simulate license lookup (in real implementation, query database)
            license_data = self._mock_license_lookup(license_key)
            
            if not license_data:
                return {
                    'valid': False,
                    'status': 'not_found',
                    'message': 'License key not found'
                }
            
            # Check expiry
            if license_data['expiry_date'] < datetime.now():
                return {
                    'valid': False,
                    'status': 'expired',
                    'message': 'License has expired',
                    'expiry_date': license_data['expiry_date'].isoformat()
                }
            
            # Check if suspended or revoked
            if license_data['status'] != LicenseStatus.ACTIVE:
                return {
                    'valid': False,
                    'status': license_data['status'].value,
                    'message': f'License is {license_data["status"].value}'
                }
            
            return {
                'valid': True,
                'status': 'active',
                'license_data': license_data,
                'features': asdict(license_data['features']),
                'usage_stats': license_data['usage_stats'],
                'expires_in_days': (license_data['expiry_date'] - datetime.now()).days
            }
            
        except Exception as e:
            return {
                'valid': False,
                'status': 'error',
                'message': f'License validation error: {str(e)}'
            }
    
    def _is_valid_license_format(self, license_key: str) -> bool:
        """Check if license key has valid format"""
        import re
        pattern = r'^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$'
        return bool(re.match(pattern, license_key))
    
    def _mock_license_lookup(self, license_key: str) -> Optional[Dict]:
        """Mock license lookup for demonstration"""
        # In real implementation, this would query your database
        # This is just for demonstration purposes
        
        # Generate a mock license based on the key
        if license_key.startswith('PROF'):
            license_type = LicenseType.PROFESSIONAL
        elif license_key.startswith('ENTR'):
            license_type = LicenseType.ENTERPRISE
        elif license_key.startswith('WHIT'):
            license_type = LicenseType.WHITE_LABEL
        else:
            license_type = LicenseType.BASIC
        
        return {
            'license_key': license_key,
            'license_type': license_type,
            'status': LicenseStatus.ACTIVE,
            'expiry_date': datetime.now() + timedelta(days=365),
            'features': self.license_configs[license_type],
            'usage_stats': {
                'calculations_used': 145,
                'api_calls_used': 1250,
                'last_used': datetime.now().isoformat(),
                'total_users': 3
            }
        }

class WhiteLabelManager:
    """White-label branding and customization manager"""
    
    def __init__(self):
        self.default_config = {
            'app_name': 'VoidSight Analytics',
            'company_name': 'VoidSight',
            'logo_url': '/static/images/logo.png',
            'favicon_url': '/static/images/favicon.ico',
            'primary_color': '#6366f1',
            'secondary_color': '#8b5cf6',
            'accent_color': '#06b6d4',
            'font_family': 'Inter',
            'custom_css': '',
            'custom_js': '',
            'footer_text': 'Powered by VoidSight Analytics',
            'support_email': 'support@voidsight.com',
            'documentation_url': 'https://docs.voidsight.com',
            'privacy_policy_url': 'https://voidsight.com/privacy',
            'terms_of_service_url': 'https://voidsight.com/terms'
        }
    
    def create_white_label_config(self, 
                                 license_key: str,
                                 customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Create white-label configuration"""
        
        config = self.default_config.copy()
        config.update(customizations)
        
        # Add license-specific settings
        config['license_key'] = license_key
        config['created_at'] = datetime.now().isoformat()
        config['last_updated'] = datetime.now().isoformat()
        
        # Generate custom domain settings if provided
        if 'custom_domain' in customizations:
            config['custom_domain'] = customizations['custom_domain']
            config['ssl_enabled'] = customizations.get('ssl_enabled', True)
        
        return config
    
    def apply_white_label_theme(self, config: Dict[str, Any]) -> str:
        """Generate custom CSS for white-label theme"""
        
        css_template = f"""
        /* White-Label Theme for {config.get('app_name', 'Custom App')} */
        :root {{
            --primary-color: {config.get('primary_color', '#6366f1')};
            --secondary-color: {config.get('secondary_color', '#8b5cf6')};
            --accent-color: {config.get('accent_color', '#06b6d4')};
            --font-family: {config.get('font_family', 'Inter')}, sans-serif;
        }}
        
        .navbar-brand img {{
            content: url('{config.get('logo_url', '/static/images/logo.png')}');
        }}
        
        .app-title {{
            font-family: var(--font-family);
        }}
        
        .btn-primary {{
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }}
        
        .btn-secondary {{
            background-color: var(--secondary-color);
            border-color: var(--secondary-color);
        }}
        
        .text-accent {{
            color: var(--accent-color);
        }}
        
        .footer-custom {{
            font-size: 0.9rem;
            color: #6b7280;
        }}
        
        {config.get('custom_css', '')}
        """
        
        return css_template

class ResellerManager:
    """Reseller program management"""
    
    def __init__(self):
        self.commission_rates = {
            LicenseType.BASIC: 0.30,        # 30% commission
            LicenseType.PROFESSIONAL: 0.35,  # 35% commission
            LicenseType.ENTERPRISE: 0.40,    # 40% commission
            LicenseType.WHITE_LABEL: 0.45,   # 45% commission
        }
    
    def create_reseller_account(self, 
                               reseller_name: str,
                               reseller_email: str,
                               company_name: str,
                               territory: str = 'global') -> Dict[str, Any]:
        """Create reseller account with tracking capabilities"""
        
        reseller_id = secrets.token_urlsafe(12)
        reseller_code = f"RSL-{reseller_id[:8].upper()}"
        
        reseller_config = {
            'reseller_id': reseller_id,
            'reseller_code': reseller_code,
            'reseller_name': reseller_name,
            'reseller_email': reseller_email,
            'company_name': company_name,
            'territory': territory,
            'commission_rates': self.commission_rates,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'total_sales': 0,
            'total_commission': 0,
            'tracking_links': {
                'signup': f"https://voidsight.com/signup?ref={reseller_code}",
                'demo': f"https://voidsight.com/demo?ref={reseller_code}",
                'pricing': f"https://voidsight.com/pricing?ref={reseller_code}"
            },
            'marketing_materials': {
                'brochures': '/assets/reseller/brochures/',
                'presentations': '/assets/reseller/presentations/',
                'case_studies': '/assets/reseller/case_studies/',
                'logos': '/assets/reseller/logos/'
            }
        }
        
        return reseller_config
    
    def calculate_commission(self, 
                           license_type: LicenseType, 
                           sale_amount: float, 
                           reseller_id: str) -> Dict[str, Any]:
        """Calculate commission for reseller"""
        
        commission_rate = self.commission_rates.get(license_type, 0.30)
        commission_amount = sale_amount * commission_rate
        
        return {
            'reseller_id': reseller_id,
            'license_type': license_type.value,
            'sale_amount': sale_amount,
            'commission_rate': commission_rate,
            'commission_amount': commission_amount,
            'payment_due_date': (datetime.now() + timedelta(days=30)).isoformat(),
            'status': 'pending'
        }

# Demo license keys for immediate testing
DEMO_LICENSE_KEYS = {
    'PROF-1234-5678-9ABC-DEF0': {
        'type': 'Professional',
        'status': 'Active',
        'expires': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
        'features': 'Full professional features with white-label branding'
    },
    'ENTR-ABCD-1234-EFGH-5678': {
        'type': 'Enterprise',
        'status': 'Active', 
        'expires': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
        'features': 'Enterprise features with custom integrations'
    },
    'WHIT-XYZ1-2345-ABC6-789D': {
        'type': 'White Label',
        'status': 'Active',
        'expires': (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'),
        'features': 'Full white-label rights with reseller capabilities'
    }
}

def create_licensing_routes(app):
    """Create licensing routes for Flask application"""
    
    license_manager = LicenseManager()
    
    @app.route('/api/license/validate', methods=['POST'])
    def validate_license():
        """Validate license key endpoint"""
        from flask import request, jsonify
        
        data = request.get_json()
        license_key = data.get('license_key')
        
        if not license_key:
            return jsonify({'error': 'License key required'}), 400
        
        validation_result = license_manager.validate_license(license_key)
        return jsonify(validation_result)
    
    @app.route('/api/license/demo-keys')
    def get_demo_keys():
        """Get demo license keys for testing"""
        from flask import jsonify
        
        return jsonify({
            'demo_keys': DEMO_LICENSE_KEYS,
            'message': 'Demo license keys for testing purposes'
        })
    
    return app