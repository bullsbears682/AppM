"""
Enhanced validation utilities for Business ROI Calculator
Comprehensive input validation with detailed error messages
"""

import re
import logging
from typing import Any, Dict, List, Optional, Union, Tuple
from functools import wraps
from datetime import datetime
from decimal import Decimal, InvalidOperation
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation error with detailed error information"""
    def __init__(self, message: str, field: str = None, value: Any = None, code: str = None, details: List = None):
        self.message = message
        self.field = field
        self.value = value
        self.code = code
        self.details = details
        super().__init__(self.message)
    
    def to_dict(self):
        result = {
            'error': 'validation_error',
            'message': self.message,
            'field': self.field,
            'value': str(self.value) if self.value is not None else None,
            'code': self.code,
            'timestamp': datetime.utcnow().isoformat()
        }
        if self.details:
            result['details'] = self.details
        return result

class BusinessLogicError(Exception):
    """Custom error for business logic violations"""
    def __init__(self, message: str, details: Dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self):
        return {
            'error': 'business_logic_error',
            'message': self.message,
            'details': self.details,
            'timestamp': datetime.utcnow().isoformat()
        }

class APIValidator:
    """Comprehensive API input validator"""
    
    @staticmethod
    def validate_currency(currency: str) -> str:
        """Validate currency code"""
        if not currency:
            raise ValidationError("Currency is required", "currency", currency, "REQUIRED")
        
        currency = currency.upper().strip()
        
        if currency not in Config.CURRENCIES:
            valid_currencies = list(Config.CURRENCIES.keys())
            raise ValidationError(
                f"Invalid currency '{currency}'. Valid currencies: {', '.join(valid_currencies)}",
                "currency", currency, "INVALID_CURRENCY"
            )
        
        return currency
    
    @staticmethod
    def validate_company_size(company_size: str) -> str:
        """Validate company size"""
        if not company_size:
            raise ValidationError("Company size is required", "company_size", company_size, "REQUIRED")
        
        company_size = company_size.lower().strip()
        
        if company_size not in Config.COMPANY_SIZES:
            valid_sizes = list(Config.COMPANY_SIZES.keys())
            raise ValidationError(
                f"Invalid company size '{company_size}'. Valid sizes: {', '.join(valid_sizes)}",
                "company_size", company_size, "INVALID_COMPANY_SIZE"
            )
        
        return company_size
    
    @staticmethod
    def validate_industry(industry: str) -> str:
        """Validate industry code"""
        if not industry:
            raise ValidationError("Industry is required", "industry", industry, "REQUIRED")
        
        industry = industry.lower().strip()
        
        if industry not in Config.INDUSTRIES:
            valid_industries = list(Config.INDUSTRIES.keys())
            raise ValidationError(
                f"Invalid industry '{industry}'. Valid industries: {', '.join(valid_industries)}",
                "industry", industry, "INVALID_INDUSTRY"
            )
        
        return industry
    
    @staticmethod
    def validate_project_type(project_type: str) -> str:
        """Validate project type"""
        if not project_type:
            raise ValidationError("Project type is required", "project_type", project_type, "REQUIRED")
        
        project_type = project_type.lower().strip()
        
        if project_type not in Config.PROJECT_TYPES:
            valid_types = list(Config.PROJECT_TYPES.keys())
            raise ValidationError(
                f"Invalid project type '{project_type}'. Valid types: {', '.join(valid_types)}",
                "project_type", project_type, "INVALID_PROJECT_TYPE"
            )
        
        return project_type
    
    @staticmethod
    def validate_investment_amount(amount: Union[str, int, float], currency: str = 'USD') -> Decimal:
        """Validate investment amount with currency-specific precision"""
        if amount is None:
            raise ValidationError("Investment amount is required", "amount", amount, "REQUIRED")
        
        try:
            # Convert to Decimal for precise calculations
            if isinstance(amount, str):
                # Remove currency symbols and formatting
                cleaned_amount = re.sub(r'[^\d.-]', '', amount)
                decimal_amount = Decimal(cleaned_amount)
            else:
                decimal_amount = Decimal(str(amount))
            
            # Validate range
            min_investment = Decimal(str(Config.MIN_INVESTMENT))
            max_investment = Decimal(str(Config.MAX_INVESTMENT))
            
            if decimal_amount < min_investment:
                raise ValidationError(
                    f"Investment amount must be at least {Config.CURRENCIES[currency].symbol}{min_investment:,}",
                    "amount", amount, "AMOUNT_TOO_LOW"
                )
            
            if decimal_amount > max_investment:
                raise ValidationError(
                    f"Investment amount cannot exceed {Config.CURRENCIES[currency].symbol}{max_investment:,}",
                    "amount", amount, "AMOUNT_TOO_HIGH"
                )
            
            # Apply currency-specific precision
            currency_config = Config.CURRENCIES[currency]
            precision = currency_config.precision
            
            return decimal_amount.quantize(Decimal('0.1') ** precision)
            
        except (InvalidOperation, ValueError) as e:
            raise ValidationError(
                f"Invalid investment amount '{amount}'. Must be a valid number.",
                "amount", amount, "INVALID_NUMBER"
            )
    
    @staticmethod
    def validate_company_name(company_name: str) -> str:
        """Validate company name"""
        if not company_name:
            raise ValidationError("Company name is required", "company_name", company_name, "REQUIRED")
        
        company_name = company_name.strip()
        
        if len(company_name) < 2:
            raise ValidationError(
                "Company name must be at least 2 characters long",
                "company_name", company_name, "TOO_SHORT"
            )
        
        if len(company_name) > 100:
            raise ValidationError(
                "Company name cannot exceed 100 characters",
                "company_name", company_name, "TOO_LONG"
            )
        
        # Check for valid characters (letters, numbers, spaces, common punctuation)
        if not re.match(r'^[a-zA-Z0-9\s\-\.\,\&\'\"]+$', company_name):
            raise ValidationError(
                "Company name contains invalid characters",
                "company_name", company_name, "INVALID_CHARACTERS"
            )
        
        return company_name
    
    @staticmethod
    def validate_timeline(timeline: Union[str, int]) -> int:
        """Validate project timeline in months"""
        if timeline is None:
            raise ValidationError("Timeline is required", "timeline", timeline, "REQUIRED")
        
        try:
            timeline_months = int(timeline)
            
            if timeline_months < 1:
                raise ValidationError(
                    "Timeline must be at least 1 month",
                    "timeline", timeline, "TOO_SHORT"
                )
            
            if timeline_months > 120:  # 10 years
                raise ValidationError(
                    "Timeline cannot exceed 120 months (10 years)",
                    "timeline", timeline, "TOO_LONG"
                )
            
            return timeline_months
            
        except (ValueError, TypeError):
            raise ValidationError(
                f"Invalid timeline '{timeline}'. Must be a valid number of months.",
                "timeline", timeline, "INVALID_NUMBER"
            )
    
    @staticmethod
    def validate_roi_calculation_request(data: Dict) -> Dict:
        """Validate a complete ROI calculation request"""
        validated_data = {}
        errors = []
        
        try:
            # Required fields validation
            required_fields = ['company_size', 'project_type', 'target_industry']
            for field in required_fields:
                if field not in data:
                    errors.append(ValidationError(f"{field} is required", field, None, "REQUIRED"))
            
            if errors:
                raise ValidationError("Multiple validation errors", code="MULTIPLE_ERRORS")
            
            # Validate each field
            validated_data['company_size'] = APIValidator.validate_company_size(data['company_size'])
            validated_data['project_type'] = APIValidator.validate_project_type(data['project_type'])
            validated_data['target_industry'] = APIValidator.validate_industry(data['target_industry'])
            
            # Optional fields
            if 'current_industry' in data:
                validated_data['current_industry'] = APIValidator.validate_industry(data['current_industry'])
            else:
                validated_data['current_industry'] = validated_data['target_industry']
            
            if 'currency' in data:
                validated_data['currency'] = APIValidator.validate_currency(data['currency'])
            else:
                validated_data['currency'] = Config.DEFAULT_CURRENCY
            
            if 'company_name' in data:
                validated_data['company_name'] = APIValidator.validate_company_name(data['company_name'])
            else:
                validated_data['company_name'] = 'Your Company'
            
            if 'custom_investment' in data:
                validated_data['custom_investment'] = APIValidator.validate_investment_amount(
                    data['custom_investment'], validated_data['currency']
                )
            
            if 'custom_timeline' in data:
                validated_data['custom_timeline'] = APIValidator.validate_timeline(data['custom_timeline'])
            
            return validated_data
            
        except ValidationError as e:
            if e.code == "MULTIPLE_ERRORS":
                # Return all validation errors
                error_details = [error.to_dict() for error in errors]
                raise ValidationError(
                    "Multiple validation errors occurred",
                    details=error_details,
                    code="MULTIPLE_ERRORS"
                )
            else:
                raise

class DataSanitizer:
    """Data sanitization utilities"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = None, allow_special: bool = False) -> str:
        """Enhanced string sanitization"""
        if not isinstance(value, str):
            return str(value)
        
        # Remove control characters and normalize whitespace
        sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
        sanitized = re.sub(r'\s+', ' ', sanitized)
        sanitized = sanitized.strip()
        
        if not allow_special:
            # Remove potentially dangerous characters
            sanitized = re.sub(r'[<>"\']', '', sanitized)
            # Remove SQL injection patterns
            sanitized = re.sub(r'(union|select|insert|update|delete|drop|create|alter)\s', '', sanitized, flags=re.IGNORECASE)
        
        # Validate length
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        # Ensure minimum length for required fields
        if len(sanitized) == 0:
            raise ValidationError("Input cannot be empty after sanitization", "input", value, "EMPTY_AFTER_SANITIZATION")
        
        return sanitized
    
    @staticmethod
    def sanitize_company_name(value: str) -> str:
        """Specialized company name sanitization"""
        if not value:
            raise ValidationError("Company name is required", "company_name", value, "REQUIRED")
        
        # Allow letters, numbers, spaces, and common business characters
        sanitized = re.sub(r'[^a-zA-Z0-9\s\-\.\,\&\(\)]', '', value)
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        if len(sanitized) < 2:
            raise ValidationError("Company name too short after sanitization", "company_name", value, "TOO_SHORT")
        
        return sanitized[:100]  # Cap at 100 characters
    
    @staticmethod
    def sanitize_number(value: Union[str, int, float]) -> Union[int, float]:
        """Sanitize numeric input"""
        if isinstance(value, (int, float)):
            return value
        
        if isinstance(value, str):
            # Remove non-numeric characters except decimal point and minus
            cleaned = re.sub(r'[^\d.-]', '', value)
            try:
                if '.' in cleaned:
                    return float(cleaned)
                else:
                    return int(cleaned)
            except ValueError:
                raise ValidationError(f"Cannot convert '{value}' to number", "number", value, "INVALID_NUMBER")
        
        raise ValidationError(f"Invalid number type: {type(value)}", "number", value, "INVALID_TYPE")

def handle_validation_errors(f):
    """Decorator to handle validation errors consistently"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error in {f.__name__}: {e.message}")
            return {'error': True, 'validation_error': e.to_dict()}, 400
        except BusinessLogicError as e:
            logger.warning(f"Business logic error in {f.__name__}: {e.message}")
            return {'error': True, 'business_error': e.to_dict()}, 422
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}")
            return {
                'error': True, 
                'message': 'An unexpected error occurred',
                'details': str(e) if Config.DEBUG else None,
                'timestamp': datetime.utcnow().isoformat()
            }, 500
    
    return decorated_function

class BusinessValidator:
    """Business logic validation"""
    
    @staticmethod
    def validate_business_logic(company_size: str, project_type: str, industry: str, 
                              investment_amount: Decimal = None) -> bool:
        """Validate business logic constraints"""
        
        company_config = Config.COMPANY_SIZES[company_size]
        project_config = Config.PROJECT_TYPES[project_type]
        industry_config = Config.INDUSTRIES[industry]
        
        # Check if investment is within company size budget range
        if investment_amount:
            if investment_amount < company_config.min_budget:
                raise BusinessLogicError(
                    f"Investment amount is below typical budget range for {company_size} companies",
                    {
                        'min_budget': company_config.min_budget,
                        'max_budget': company_config.max_budget,
                        'investment': float(investment_amount)
                    }
                )
            
            if investment_amount > company_config.max_budget * 5:  # More flexibility for large investments
                raise BusinessLogicError(
                    f"Investment amount is significantly above typical budget range for {company_size} companies",
                    {
                        'min_budget': company_config.min_budget,
                        'max_budget': company_config.max_budget,
                        'investment': float(investment_amount),
                        'note': 'Consider selecting a larger company size or breaking into phases'
                    }
                )
        
        # Check industry-project compatibility
        high_risk_projects = ['blockchain_platform', 'ai_integration', 'crypto']
        if project_type in high_risk_projects and company_size == 'startup':
            if industry_config.risk_factor > 0.3:
                raise BusinessLogicError(
                    f"High-risk project type '{project_config.description}' in high-risk industry "
                    f"'{industry}' may not be suitable for startup companies",
                    {
                        'project_risk': project_config.risk_level,
                        'industry_risk': industry_config.risk_factor,
                        'recommendation': 'Consider lower-risk alternatives or seek additional funding'
                    }
                )
        
        return True

# Export validation utilities
__all__ = [
    'ValidationError',
    'BusinessLogicError', 
    'APIValidator',
    'DataSanitizer',
    'BusinessValidator',
    'handle_validation_errors'
]