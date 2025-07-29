"""
Enterprise Database Models for Infinex ROI Calculator
Professional data models with user management, analytics, and commercial features
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional
import json
import uuid
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

class SubscriptionTier(Enum):
    """Subscription tier enumeration"""
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

class CalculationStatus(Enum):
    """Calculation status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class User(db.Model, UserMixin):
    """Enhanced user model with commercial features"""
    __tablename__ = 'users'
    
    # Primary identification
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(50), unique=True, nullable=True, index=True)
    
    # Authentication
    password_hash = db.Column(db.String(255), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_at = db.Column(db.DateTime)
    
    # Profile information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    company_name = db.Column(db.String(200))
    job_title = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    # Subscription and billing
    subscription_tier = db.Column(db.Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    subscription_start = db.Column(db.DateTime)
    subscription_end = db.Column(db.DateTime)
    trial_start = db.Column(db.DateTime)
    trial_end = db.Column(db.DateTime)
    stripe_customer_id = db.Column(db.String(100))
    
    # Usage tracking
    calculations_used = db.Column(db.Integer, default=0)
    api_calls_used = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Account management
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Two-factor authentication
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(100))
    
    # Preferences
    preferences = db.Column(JSONB, default=lambda: {})
    
    # Relationships
    calculations = db.relationship('Calculation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    api_keys = db.relationship('APIKey', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password: str):
        """Set user password with secure hashing"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    @hybrid_property
    def full_name(self) -> str:
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
    
    @property
    def is_trial_active(self) -> bool:
        """Check if trial period is active"""
        if not self.trial_start or not self.trial_end:
            return False
        return datetime.utcnow() <= self.trial_end
    
    @property
    def is_subscription_active(self) -> bool:
        """Check if subscription is active"""
        if not self.subscription_end:
            return False
        return datetime.utcnow() <= self.subscription_end
    
    @property
    def can_calculate(self) -> bool:
        """Check if user can perform calculations"""
        if self.is_subscription_active:
            return True
        if self.is_trial_active:
            return True
        # Free tier limits
        return self.calculations_used < 10  # Free tier limit
    
    def get_limits(self) -> Dict:
        """Get user's current limits based on subscription"""
        limits = {
            SubscriptionTier.FREE: {
                'calculations_per_month': 10,
                'api_calls_per_hour': 100,
                'export_formats': ['json'],
                'advanced_analytics': False,
                'priority_support': False
            },
            SubscriptionTier.BASIC: {
                'calculations_per_month': 100,
                'api_calls_per_hour': 1000,
                'export_formats': ['json', 'csv', 'pdf'],
                'advanced_analytics': True,
                'priority_support': False
            },
            SubscriptionTier.PROFESSIONAL: {
                'calculations_per_month': 1000,
                'api_calls_per_hour': 10000,
                'export_formats': ['json', 'csv', 'pdf', 'xlsx', 'pptx'],
                'advanced_analytics': True,
                'priority_support': True
            },
            SubscriptionTier.ENTERPRISE: {
                'calculations_per_month': -1,  # Unlimited
                'api_calls_per_hour': -1,  # Unlimited
                'export_formats': ['json', 'csv', 'pdf', 'xlsx', 'pptx'],
                'advanced_analytics': True,
                'priority_support': True
            }
        }
        return limits.get(self.subscription_tier, limits[SubscriptionTier.FREE])
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            'id': str(self.id),
            'email': self.email,
            'username': self.username,
            'full_name': self.full_name,
            'company_name': self.company_name,
            'subscription_tier': self.subscription_tier.value,
            'is_trial_active': self.is_trial_active,
            'is_subscription_active': self.is_subscription_active,
            'calculations_used': self.calculations_used,
            'created_at': self.created_at.isoformat(),
            'limits': self.get_limits()
        }

class Calculation(db.Model):
    """Enhanced calculation model with full audit trail"""
    __tablename__ = 'calculations'
    
    # Primary identification
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    # Calculation metadata
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.Enum(CalculationStatus), default=CalculationStatus.PENDING)
    
    # Input parameters
    project_type = db.Column(db.String(50), nullable=False)
    company_size = db.Column(db.String(50), nullable=False)
    target_industry = db.Column(db.String(50), nullable=False)
    current_industry = db.Column(db.String(50))
    currency = db.Column(db.String(10), default='USD')
    
    # Financial inputs
    investment_amount = db.Column(db.Numeric(15, 2), nullable=False)
    expected_roi = db.Column(db.Numeric(8, 4))
    timeline_months = db.Column(db.Integer, nullable=False)
    
    # Complete input data (for audit and replay)
    input_data = db.Column(JSONB)
    
    # Results
    total_cost = db.Column(db.Numeric(15, 2))
    roi_percentage = db.Column(db.Numeric(8, 4))
    projected_revenue = db.Column(db.Numeric(15, 2))
    npv = db.Column(db.Numeric(15, 2))
    irr = db.Column(db.Numeric(8, 6))
    payback_period_months = db.Column(db.Integer)
    risk_score = db.Column(db.Numeric(5, 2))
    
    # Complete results data
    results_data = db.Column(JSONB)
    
    # Processing information
    processing_time_ms = db.Column(db.Integer)
    monte_carlo_iterations = db.Column(db.Integer)
    confidence_level = db.Column(db.Numeric(4, 3))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Error handling
    error_message = db.Column(db.Text)
    error_code = db.Column(db.String(50))
    
    # Sharing and collaboration
    is_public = db.Column(db.Boolean, default=False)
    share_token = db.Column(db.String(100), unique=True)
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_calculations_user_created', 'user_id', 'created_at'),
        Index('ix_calculations_status_created', 'status', 'created_at'),
        Index('ix_calculations_industry_created', 'target_industry', 'created_at'),
    )
    
    def to_dict(self) -> Dict:
        """Convert calculation to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'project_type': self.project_type,
            'company_size': self.company_size,
            'target_industry': self.target_industry,
            'currency': self.currency,
            'investment_amount': float(self.investment_amount) if self.investment_amount else None,
            'timeline_months': self.timeline_months,
            'total_cost': float(self.total_cost) if self.total_cost else None,
            'roi_percentage': float(self.roi_percentage) if self.roi_percentage else None,
            'projected_revenue': float(self.projected_revenue) if self.projected_revenue else None,
            'npv': float(self.npv) if self.npv else None,
            'irr': float(self.irr) if self.irr else None,
            'payback_period_months': self.payback_period_months,
            'risk_score': float(self.risk_score) if self.risk_score else None,
            'processing_time_ms': self.processing_time_ms,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_public': self.is_public,
            'share_token': self.share_token
        }

class APIKey(db.Model):
    """API key management for enterprise users"""
    __tablename__ = 'api_keys'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    # Key information
    name = db.Column(db.String(100), nullable=False)
    key_hash = db.Column(db.String(255), nullable=False, unique=True)
    key_prefix = db.Column(db.String(20), nullable=False)  # First few chars for identification
    
    # Permissions and limits
    permissions = db.Column(JSONB, default=lambda: ['read', 'calculate'])
    rate_limit_per_hour = db.Column(db.Integer, default=1000)
    
    # Usage tracking
    last_used = db.Column(db.DateTime)
    total_requests = db.Column(db.Integer, default=0)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self) -> Dict:
        """Convert API key to dictionary (without sensitive data)"""
        return {
            'id': str(self.id),
            'name': self.name,
            'key_prefix': self.key_prefix,
            'permissions': self.permissions,
            'rate_limit_per_hour': self.rate_limit_per_hour,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'total_requests': self.total_requests,
            'is_active': self.is_active,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat()
        }

class AuditLog(db.Model):
    """Comprehensive audit logging for compliance"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    
    # Event information
    event_type = db.Column(db.String(50), nullable=False, index=True)
    event_description = db.Column(db.String(255))
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.String(100))
    
    # Request details
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    request_method = db.Column(db.String(10))
    request_path = db.Column(db.String(255))
    
    # Additional data
    metadata = db.Column(JSONB)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_audit_logs_event_created', 'event_type', 'created_at'),
        Index('ix_audit_logs_user_created', 'user_id', 'created_at'),
    )

class Template(db.Model):
    """Calculation templates for reuse"""
    __tablename__ = 'templates'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    # Template information
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    
    # Template data
    template_data = db.Column(JSONB, nullable=False)
    
    # Sharing
    is_public = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Usage tracking
    usage_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Analytics(db.Model):
    """System analytics and metrics"""
    __tablename__ = 'analytics'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Metric information
    metric_name = db.Column(db.String(100), nullable=False, index=True)
    metric_value = db.Column(db.Numeric(15, 4))
    metric_data = db.Column(JSONB)
    
    # Dimensions
    date_dimension = db.Column(db.Date, index=True)
    user_dimension = db.Column(UUID(as_uuid=True))
    industry_dimension = db.Column(db.String(50))
    tier_dimension = db.Column(db.String(50))
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Indexes for analytics queries
    __table_args__ = (
        Index('ix_analytics_metric_date', 'metric_name', 'date_dimension'),
        Index('ix_analytics_metric_user', 'metric_name', 'user_dimension'),
    )

class License(db.Model):
    """License management for enterprise deployments"""
    __tablename__ = 'licenses'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # License information
    license_key = db.Column(db.String(255), unique=True, nullable=False)
    license_type = db.Column(db.String(50), nullable=False)
    organization_name = db.Column(db.String(200))
    
    # Limits and features
    max_users = db.Column(db.Integer)
    max_calculations_per_month = db.Column(db.Integer)
    features = db.Column(JSONB, default=lambda: [])
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    # Usage tracking
    current_users = db.Column(db.Integer, default=0)
    current_calculations = db.Column(db.Integer, default=0)
    
    def is_valid(self) -> bool:
        """Check if license is valid"""
        if not self.is_active:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

def init_db(app):
    """Initialize database with app"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin user if not exists
        admin_user = User.query.filter_by(email='admin@infinex.dev').first()
        if not admin_user:
            admin_user = User(
                email='admin@infinex.dev',
                username='admin',
                first_name='Admin',
                last_name='User',
                is_admin=True,
                is_active=True,
                email_confirmed=True,
                email_confirmed_at=datetime.utcnow(),
                subscription_tier=SubscriptionTier.ENTERPRISE
            )
            admin_user.set_password('admin123')  # Change in production
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Created default admin user: admin@infinex.dev / admin123")

# Export models for easy import
__all__ = [
    'db', 'User', 'Calculation', 'APIKey', 'AuditLog', 
    'Template', 'Analytics', 'License', 'SubscriptionTier', 
    'CalculationStatus', 'init_db'
]