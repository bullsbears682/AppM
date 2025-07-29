"""
Enterprise Authentication & Authorization System
Advanced user management, JWT tokens, role-based access control, and subscription management
"""

import os
import uuid
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from functools import wraps
from dataclasses import dataclass

from flask import Blueprint, request, jsonify, current_app, g
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request
)
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import qrcode
from io import BytesIO
import base64

from models import db, User, AuditLog, APIKey, SubscriptionTier
from config import Config

# Authentication Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# JWT Manager
jwt = JWTManager()

@dataclass
class AuthResponse:
    """Standardized authentication response"""
    success: bool
    message: str
    data: Optional[Dict] = None
    errors: Optional[List[str]] = None

class AuthenticationError(Exception):
    """Custom authentication exception"""
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthorizationError(Exception):
    """Custom authorization exception"""
    def __init__(self, message: str, status_code: int = 403):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def init_auth(app):
    """Initialize authentication system"""
    jwt.init_app(app)
    app.register_blueprint(auth_bp)
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.JWT_REFRESH_TOKEN_EXPIRES
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    
    # JWT Callbacks
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Check if JWT token is revoked"""
        # Implement token blacklist logic here
        return False
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired token"""
        log_security_event('token_expired', {
            'token_type': jwt_payload.get('type'),
            'user_id': jwt_payload.get('sub')
        })
        return jsonify({'error': 'Token has expired'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid token"""
        log_security_event('invalid_token', {'error': str(error)})
        return jsonify({'error': 'Invalid token'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing token"""
        return jsonify({'error': 'Authentication token required'}), 401

def log_security_event(event_type: str, metadata: Dict):
    """Log security events for audit trail"""
    try:
        audit_log = AuditLog(
            event_type=event_type,
            event_description=f"Security event: {event_type}",
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            request_method=request.method,
            request_path=request.path,
            metadata=metadata
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Failed to log security event: {e}")

def require_subscription(tiers: List[SubscriptionTier] = None):
    """Decorator to require specific subscription tiers"""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or not user.is_active:
                raise AuthenticationError("User not found or inactive")
            
            if tiers:
                if user.subscription_tier not in tiers:
                    if not user.is_trial_active and not user.is_subscription_active:
                        raise AuthorizationError(
                            f"This feature requires a subscription. Your current tier: {user.subscription_tier.value}"
                        )
            
            g.current_user = user
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin():
    """Decorator to require admin privileges"""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or not user.is_active or not user.is_admin:
                raise AuthorizationError("Admin privileges required")
            
            g.current_user = user
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def rate_limit_by_user():
    """Rate limiting based on user subscription tier"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if hasattr(g, 'current_user'):
                user = g.current_user
                limits = user.get_limits()
                # Implement rate limiting logic based on user tier
                # This would integrate with Flask-Limiter
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Authentication Routes

@auth_bp.route('/register', methods=['POST'])
def register():
    """Enhanced user registration with validation"""
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['email', 'password', 'first_name', 'last_name']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields',
                'errors': [f'Field {field} is required' for field in required_fields if field not in data]
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409
        
        # Password strength validation
        password = data['password']
        if len(password) < 8:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 8 characters long'
            }), 400
        
        # Create new user
        user = User(
            email=data['email'],
            username=data.get('username'),
            first_name=data['first_name'],
            last_name=data['last_name'],
            company_name=data.get('company_name'),
            job_title=data.get('job_title'),
            phone=data.get('phone'),
            trial_start=datetime.utcnow(),
            trial_end=datetime.utcnow() + timedelta(days=Config.TRIAL_PERIOD_DAYS)
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        # Log registration
        log_security_event('user_registered', {
            'user_id': str(user.id),
            'email': user.email
        })
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'trial_days_remaining': Config.TRIAL_PERIOD_DAYS
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {e}")
        return jsonify({
            'success': False,
            'message': 'Registration failed',
            'errors': [str(e)]
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Enhanced login with 2FA support and security monitoring"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password required'
            }), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            log_security_event('failed_login', {
                'email': data['email'],
                'reason': 'invalid_credentials'
            })
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        if not user.is_active:
            log_security_event('failed_login', {
                'user_id': str(user.id),
                'reason': 'account_inactive'
            })
            return jsonify({
                'success': False,
                'message': 'Account is inactive'
            }), 401
        
        # Check 2FA if enabled
        if user.two_factor_enabled:
            if not data.get('totp_code'):
                return jsonify({
                    'success': False,
                    'message': 'Two-factor authentication code required',
                    'requires_2fa': True
                }), 400
            
            totp = pyotp.TOTP(user.two_factor_secret)
            if not totp.verify(data['totp_code']):
                log_security_event('failed_2fa', {
                    'user_id': str(user.id)
                })
                return jsonify({
                    'success': False,
                    'message': 'Invalid two-factor authentication code'
                }), 401
        
        # Update last active
        user.last_active = datetime.utcnow()
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        # Log successful login
        log_security_event('successful_login', {
            'user_id': str(user.id)
        })
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {e}")
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'errors': [str(e)]
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'message': 'User not found or inactive'
            }), 401
        
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'success': True,
            'data': {
                'access_token': access_token
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {e}")
        return jsonify({
            'success': False,
            'message': 'Token refresh failed'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get profile error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get profile'
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        
        # Updatable fields
        updatable_fields = [
            'first_name', 'last_name', 'company_name', 
            'job_title', 'phone', 'preferences'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        log_security_event('profile_updated', {
            'user_id': str(user.id),
            'updated_fields': list(data.keys())
        })
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update profile error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to update profile'
        }), 500

@auth_bp.route('/2fa/setup', methods=['POST'])
@jwt_required()
def setup_2fa():
    """Set up two-factor authentication"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        if user.two_factor_enabled:
            return jsonify({
                'success': False,
                'message': 'Two-factor authentication already enabled'
            }), 400
        
        # Generate secret
        secret = pyotp.random_base32()
        user.two_factor_secret = secret
        
        # Generate QR code
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="Infinex ROI Calculator"
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '2FA setup initiated',
            'data': {
                'secret': secret,
                'qr_code': f"data:image/png;base64,{img_str}",
                'backup_codes': [secrets.token_hex(4) for _ in range(10)]  # Generate backup codes
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"2FA setup error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to setup 2FA'
        }), 500

@auth_bp.route('/2fa/verify', methods=['POST'])
@jwt_required()
def verify_2fa():
    """Verify and enable two-factor authentication"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.two_factor_secret:
            return jsonify({
                'success': False,
                'message': 'User not found or 2FA not set up'
            }), 404
        
        data = request.get_json()
        if not data.get('totp_code'):
            return jsonify({
                'success': False,
                'message': 'TOTP code required'
            }), 400
        
        totp = pyotp.TOTP(user.two_factor_secret)
        if not totp.verify(data['totp_code']):
            return jsonify({
                'success': False,
                'message': 'Invalid TOTP code'
            }), 400
        
        user.two_factor_enabled = True
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        log_security_event('2fa_enabled', {
            'user_id': str(user.id)
        })
        
        return jsonify({
            'success': True,
            'message': 'Two-factor authentication enabled successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"2FA verification error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to verify 2FA'
        }), 500

@auth_bp.route('/api-keys', methods=['GET'])
@jwt_required()
def list_api_keys():
    """List user's API keys"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        api_keys = user.api_keys.filter_by(is_active=True).all()
        
        return jsonify({
            'success': True,
            'data': {
                'api_keys': [key.to_dict() for key in api_keys]
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"List API keys error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to list API keys'
        }), 500

@auth_bp.route('/api-keys', methods=['POST'])
@require_subscription([SubscriptionTier.PROFESSIONAL, SubscriptionTier.ENTERPRISE])
def create_api_key():
    """Create new API key"""
    try:
        user = g.current_user
        data = request.get_json()
        
        if not data.get('name'):
            return jsonify({
                'success': False,
                'message': 'API key name required'
            }), 400
        
        # Generate API key
        key = f"infinex_{secrets.token_urlsafe(32)}"
        key_hash = generate_password_hash(key)
        key_prefix = key[:12] + "..."
        
        api_key = APIKey(
            user_id=user.id,
            name=data['name'],
            key_hash=key_hash,
            key_prefix=key_prefix,
            permissions=data.get('permissions', ['read', 'calculate']),
            rate_limit_per_hour=data.get('rate_limit', 1000),
            expires_at=datetime.utcnow() + timedelta(days=365) if data.get('expires_in_days') else None
        )
        
        db.session.add(api_key)
        db.session.commit()
        
        log_security_event('api_key_created', {
            'user_id': str(user.id),
            'api_key_id': str(api_key.id),
            'name': data['name']
        })
        
        return jsonify({
            'success': True,
            'message': 'API key created successfully',
            'data': {
                'api_key': key,  # Only return once
                'key_info': api_key.to_dict()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create API key error: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to create API key'
        }), 500

# Export authentication utilities
__all__ = [
    'auth_bp', 'init_auth', 'jwt', 'require_subscription', 
    'require_admin', 'rate_limit_by_user', 'log_security_event',
    'AuthenticationError', 'AuthorizationError'
]