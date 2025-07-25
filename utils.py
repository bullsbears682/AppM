#!/usr/bin/env python3
"""
Utility functions for Business ROI Calculator
Input validation, error handling, and helper functions
"""

import re
import logging
from functools import wraps
from datetime import datetime
from typing import Dict, Any, Optional, Union, List
from flask import jsonify, request
from config import VALIDATION_RULES, ERROR_MESSAGES, CURRENCIES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, field: str = None, code: str = None):
        super().__init__(message)
        self.message = message
        self.field = field
        self.code = code

class CalculationError(Exception):
    """Custom exception for calculation errors"""
    def __init__(self, message: str, details: str = None):
        super().__init__(message)
        self.message = message
        self.details = details

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """Validate that all required fields are present and not empty"""
    missing_fields = []
    
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == '':
            missing_fields.append(field)
    
    if missing_fields:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing_fields)}",
            field='general',
            code='missing_fields'
        )
    
    return True

def validate_company_name(company_name: str) -> bool:
    """Validate company name format and length"""
    if not company_name or not isinstance(company_name, str):
        raise ValidationError(
            ERROR_MESSAGES['missing_required_field'],
            field='company_name',
            code='required'
        )
    
    # Strip whitespace
    company_name = company_name.strip()
    
    # Check length
    rules = VALIDATION_RULES['company_name']
    if len(company_name) < rules['min_length'] or len(company_name) > rules['max_length']:
        raise ValidationError(
            ERROR_MESSAGES['invalid_company_name'],
            field='company_name',
            code='length'
        )
    
    # Check pattern
    if not re.match(rules['pattern'], company_name):
        raise ValidationError(
            ERROR_MESSAGES['invalid_company_name'],
            field='company_name',
            code='pattern'
        )
    
    return True

def validate_enum_field(value: str, field_name: str) -> bool:
    """Validate that a field value is in the allowed enum values"""
    if field_name not in VALIDATION_RULES:
        raise ValidationError(
            f"Unknown field: {field_name}",
            field=field_name,
            code='unknown_field'
        )
    
    allowed_values = VALIDATION_RULES[field_name]['allowed_values']
    
    if value not in allowed_values:
        raise ValidationError(
            f"Invalid value for {field_name}. Allowed values: {', '.join(allowed_values)}",
            field=field_name,
            code='invalid_enum'
        )
    
    return True

def validate_budget(budget: Union[int, float, str]) -> float:
    """Validate and convert budget to float"""
    try:
        budget_float = float(budget)
    except (ValueError, TypeError):
        raise ValidationError(
            "Budget must be a valid number",
            field='budget',
            code='invalid_type'
        )
    
    rules = VALIDATION_RULES['custom_budget']
    if budget_float < rules['min_value'] or budget_float > rules['max_value']:
        raise ValidationError(
            ERROR_MESSAGES['invalid_budget'],
            field='budget',
            code='out_of_range'
        )
    
    return budget_float

def validate_currency(currency: str) -> bool:
    """Validate currency code"""
    if currency not in CURRENCIES:
        raise ValidationError(
            f"Invalid currency code. Supported currencies: {', '.join(CURRENCIES.keys())}",
            field='currency',
            code='invalid_currency'
        )
    
    return True

def validate_roi_calculation_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Comprehensive validation for ROI calculation input"""
    try:
        # Required fields
        required_fields = ['company_name', 'company_size', 'current_industry', 'project_type', 'target_industry']
        validate_required_fields(data, required_fields)
        
        # Validate individual fields
        validate_company_name(data['company_name'])
        validate_enum_field(data['company_size'], 'company_size')
        validate_enum_field(data['current_industry'], 'industry')
        validate_enum_field(data['project_type'], 'project_type')
        validate_enum_field(data['target_industry'], 'industry')
        
        # Optional currency validation
        currency = data.get('currency', 'USD')
        validate_currency(currency)
        
        # Optional budget validation
        if 'custom_budget' in data and data['custom_budget']:
            data['custom_budget'] = validate_budget(data['custom_budget'])
        
        # Clean and normalize data
        cleaned_data = {
            'company_name': data['company_name'].strip(),
            'company_size': data['company_size'].lower(),
            'current_industry': data['current_industry'].lower(),
            'project_type': data['project_type'].lower(),
            'target_industry': data['target_industry'].lower(),
            'currency': currency.upper(),
            'custom_budget': data.get('custom_budget')
        }
        
        logger.info(f"Validation successful for company: {cleaned_data['company_name']}")
        return cleaned_data
        
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Unexpected validation error: {str(e)}")
        raise ValidationError(
            ERROR_MESSAGES['validation_error'],
            field='general',
            code='unexpected_error'
        )

def format_currency(amount: float, currency: str = 'USD', include_symbol: bool = True) -> str:
    """Format currency amount with proper symbol and decimal places"""
    try:
        currency_info = CURRENCIES.get(currency.upper(), CURRENCIES['USD'])
        decimal_places = currency_info['decimal_places']
        symbol = currency_info['symbol']
        
        # Format the number
        if decimal_places == 0:
            formatted_amount = f"{amount:,.0f}"
        else:
            formatted_amount = f"{amount:,.{decimal_places}f}"
        
        if include_symbol:
            return f"{symbol}{formatted_amount}"
        else:
            return formatted_amount
            
    except Exception as e:
        logger.error(f"Currency formatting error: {str(e)}")
        return f"${amount:,.2f}"  # Fallback to USD format

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 100.0 if new_value > 0 else 0.0
    
    return ((new_value - old_value) / old_value) * 100

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def clamp(value: float, min_value: float = None, max_value: float = None) -> float:
    """Clamp a value between min and max bounds"""
    if min_value is not None and value < min_value:
        return min_value
    if max_value is not None and value > max_value:
        return max_value
    return value

def get_risk_category(risk_score: float) -> str:
    """Convert numerical risk score to categorical description"""
    if risk_score <= 0.15:
        return 'Low'
    elif risk_score <= 0.25:
        return 'Medium'
    elif risk_score <= 0.35:
        return 'High'
    else:
        return 'Very High'

def get_complexity_score(complexity: str) -> float:
    """Convert complexity description to numerical score"""
    complexity_mapping = {
        'low': 0.2,
        'medium': 0.5,
        'high': 0.8,
        'very high': 1.0
    }
    return complexity_mapping.get(complexity.lower(), 0.5)

def handle_errors(f):
    """Decorator for consistent error handling in Flask routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"Validation error in {f.__name__}: {e.message}")
            return jsonify({
                'error': 'Validation Error',
                'message': e.message,
                'field': e.field,
                'code': e.code,
                'timestamp': datetime.now().isoformat()
            }), 400
        except CalculationError as e:
            logger.error(f"Calculation error in {f.__name__}: {e.message}")
            return jsonify({
                'error': 'Calculation Error',
                'message': e.message,
                'details': e.details,
                'timestamp': datetime.now().isoformat()
            }), 422
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}", exc_info=True)
            return jsonify({
                'error': 'Internal Server Error',
                'message': ERROR_MESSAGES['server_error'],
                'timestamp': datetime.now().isoformat()
            }), 500
    
    return decorated_function

def log_calculation_request():
    """Log incoming calculation requests for monitoring"""
    try:
        user_agent = request.headers.get('User-Agent', 'Unknown')
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        
        logger.info(f"ROI calculation request from {ip_address} using {user_agent}")
        
    except Exception as e:
        logger.error(f"Error logging request: {str(e)}")

def generate_calculation_id() -> str:
    """Generate unique ID for calculations"""
    from uuid import uuid4
    return str(uuid4())[:8]

def sanitize_input(input_str: str) -> str:
    """Sanitize string input to prevent basic injection attacks"""
    if not isinstance(input_str, str):
        return str(input_str)
    
    # Remove any HTML tags
    clean_str = re.sub(r'<[^>]*>', '', input_str)
    
    # Remove excessive whitespace
    clean_str = ' '.join(clean_str.split())
    
    return clean_str.strip()

def validate_positive_number(value: Union[int, float, str], field_name: str) -> float:
    """Validate that a value is a positive number"""
    try:
        num_value = float(value)
        if num_value <= 0:
            raise ValidationError(
                f"{field_name} must be a positive number",
                field=field_name,
                code='negative_value'
            )
        return num_value
    except (ValueError, TypeError):
        raise ValidationError(
            f"{field_name} must be a valid number",
            field=field_name,
            code='invalid_number'
        )

def get_market_confidence_level(volatility: float, growth_rate: float) -> str:
    """Calculate market confidence level based on volatility and growth"""
    confidence_score = (growth_rate * 2) - volatility
    
    if confidence_score >= 0.4:
        return 'Very High'
    elif confidence_score >= 0.2:
        return 'High'
    elif confidence_score >= 0.0:
        return 'Medium'
    elif confidence_score >= -0.2:
        return 'Low'
    else:
        return 'Very Low'

def calculate_compound_growth(initial_value: float, growth_rate: float, periods: int) -> float:
    """Calculate compound growth over multiple periods"""
    return initial_value * ((1 + growth_rate) ** periods)

def format_large_number(number: float, precision: int = 1) -> str:
    """Format large numbers with appropriate suffixes (K, M, B)"""
    if number < 1000:
        return f"{number:.{precision}f}"
    elif number < 1000000:
        return f"{number/1000:.{precision}f}K"
    elif number < 1000000000:
        return f"{number/1000000:.{precision}f}M"
    else:
        return f"{number/1000000000:.{precision}f}B"

def calculate_break_even_point(investment: float, monthly_return: float) -> int:
    """Calculate break-even point in months"""
    if monthly_return <= 0:
        return 999  # Never breaks even
    
    return max(1, int(investment / monthly_return))

def get_industry_benchmark(industry: str, metric: str) -> Optional[float]:
    """Get industry benchmark data for comparison"""
    # This would typically connect to a database or external API
    # For now, return None to indicate no benchmark available
    logger.info(f"Benchmark requested for {industry} - {metric}")
    return None

def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate date range format and logic"""
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        if start >= end:
            raise ValidationError(
                "End date must be after start date",
                field='date_range',
                code='invalid_range'
            )
        
        return True
    except ValueError:
        raise ValidationError(
            "Invalid date format. Use YYYY-MM-DD",
            field='date_range',
            code='invalid_format'
        )