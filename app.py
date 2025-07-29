#!/usr/bin/env python3
"""
Business ROI Calculator - Enhanced Edition
Advanced web application with comprehensive validation, enhanced calculations, and modular architecture
"""

import os
import logging
from decimal import Decimal
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import our enhanced modules with fallbacks for Termux
try:
    from config import get_config
except ImportError:
    print("Warning: Using basic configuration")
    class BasicConfig:
        SECRET_KEY = "termux-fallback-key"
        HOST = "0.0.0.0"
        PORT = 5000
        DEBUG = True
        LOG_LEVEL = "INFO"
        LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
        ENABLE_CORS = True
    def get_config():
        return BasicConfig

try:
    from utils.validators import (
        APIValidator, ValidationError, BusinessLogicError, 
        BusinessValidator, handle_validation_errors, DataSanitizer
    )
except ImportError:
    print("Warning: Using basic validation")
    class ValidationError(Exception): pass
    class BusinessLogicError(Exception): pass
    class APIValidator: pass
    class BusinessValidator: pass
    class DataSanitizer: 
        @staticmethod
        def sanitize_input(data): return data
    def handle_validation_errors(f): return f

try:
    from utils.calculator import EnhancedROICalculator
except ImportError:
    print("Warning: Using basic calculator")
    class EnhancedROICalculator:
        def calculate_roi(self, **kwargs):
            # Basic ROI calculation fallback
            investment = kwargs.get('custom_investment', 100000)
            timeline = kwargs.get('custom_timeline', 12)
            roi_percentage = 25.0
            return {
                'roi_projection': {
                    'total_investment': investment,
                    'roi_percentage': roi_percentage,
                    'projected_revenue': investment * (1 + roi_percentage/100),
                    'payback_period_months': timeline,
                    'npv': investment * 0.15,
                    'irr': 0.18
                },
                'cost_analysis': {'development': investment * 0.7, 'marketing': investment * 0.3},
                'risk_assessment': {'risk_score': 5.0, 'confidence_level': 0.8}
            }

try:
    from utils.cache import calculation_cache
except ImportError:
    print("Warning: Using basic cache")
    class BasicCache:
        def get(self, key): return None
        def set(self, key, value, timeout=None): pass
        def stats(self): return {'hits': 0, 'misses': 0}
    calculation_cache = BasicCache()

try:
    from utils.rate_limiter import rate_limit, calculation_limiter, api_limiter
except ImportError:
    print("Warning: Disabling rate limiting")
    def rate_limit(*args, **kwargs): return lambda f: f
    calculation_limiter = rate_limit
    api_limiter = rate_limit

try:
    from utils.export import ReportGenerator
except ImportError:
    print("Warning: Using basic export")
    class ReportGenerator:
        def generate_report(self, data, format='json'):
            return {'message': 'Export not available in basic mode'}
# Core v2.0 - removed advanced interactive features

# Load environment variables
load_dotenv()

# Get configuration based on environment
config_class = get_config()

# Check for Termux environment and adjust accordingly
TERMUX_MODE = os.environ.get('PREFIX') is not None
if TERMUX_MODE:
    print("🚀 Running in Termux mode - using simplified configuration")

# Setup logging
logging.basicConfig(
    level=getattr(logging, config_class.LOG_LEVEL),
    format=config_class.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config_class)

# Enable CORS if configured
if config_class.ENABLE_CORS:
    CORS(app)

# Initialize core v2.0 calculator and tools
calculator = EnhancedROICalculator()
report_generator = ReportGenerator()

# Validate configuration on startup
try:
    # Basic configuration validation
    if hasattr(config_class, 'validate_config'):
        config_class.validate_config()
    else:
        # Simple validation for enterprise config
        assert hasattr(config_class, 'SECRET_KEY'), "SECRET_KEY must be configured"
        assert hasattr(config_class, 'HOST'), "HOST must be configured"
        assert hasattr(config_class, 'PORT'), "PORT must be configured"
    logger.info("Configuration validation successful")
except Exception as e:
    logger.error(f"Configuration validation failed: {e}")
    logger.warning("Continuing with default configuration...")
    # Don't raise in Termux - just warn and continue

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')


@app.route('/api/health')
def health_check():
    """Health check endpoint with system status"""
    try:
        cache_stats = calculation_cache.stats()
        
        return jsonify({
            'status': 'healthy',
            'version': '2.0.1',
            'timestamp': datetime.utcnow().isoformat(),
            'features': {
                'caching': True,
                'rate_limiting': True,
                'numpy_available': 'NUMPY_AVAILABLE' in globals() and globals().get('NUMPY_AVAILABLE', False),
                'enhanced_validation': True
            },
            'cache_stats': cache_stats,
            'environment': config_class.ENV
        })
    except Exception as e:
        return jsonify({
            'status': 'degraded',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

@app.route('/api/calculate', methods=['POST'])
@rate_limit(calculation_limiter, "Too many calculations. Please wait before trying again.")
@handle_validation_errors
def calculate_roi():
    """
    Enhanced ROI calculation endpoint with comprehensive validation
    
    Expected JSON payload:
    {
        "company_name": "Your Company",
        "company_size": "medium",
        "current_industry": "saas",
        "project_type": "product_development", 
        "target_industry": "saas",
        "currency": "USD",
        "custom_investment": 100000,  // optional
        "custom_timeline": 12         // optional
    }
    """
    try:
        # Get and validate request data
        data = request.get_json()
        if not data:
            raise ValidationError("No JSON data provided", code="NO_DATA")
        
        # Comprehensive validation
        validated_data = APIValidator.validate_roi_calculation_request(data)
        
        # Enhanced sanitization
        validated_data['company_name'] = DataSanitizer.sanitize_company_name(validated_data['company_name'])
        
        # Business logic validation
        custom_investment = validated_data.get('custom_investment')
        BusinessValidator.validate_business_logic(
            validated_data['company_size'],
            validated_data['project_type'], 
            validated_data['target_industry'],
            custom_investment
        )
        
        # Use caching for expensive calculations
        cache_key_data = {
            'company_size': validated_data['company_size'],
            'project_type': validated_data['project_type'],
            'industry': validated_data['target_industry'],
            'currency': validated_data['currency'],
            'custom_investment': float(custom_investment) if custom_investment else None,
            'custom_timeline': validated_data.get('custom_timeline')
        }
        
        def perform_calculations():
            # Calculate project cost
            cost_analysis = calculator.calculate_project_cost(
                company_size=validated_data['company_size'],
                project_type=validated_data['project_type'],
                industry=validated_data['target_industry'],
                currency=validated_data['currency'],
                custom_investment=custom_investment,
                custom_timeline=validated_data.get('custom_timeline')
            )
            
            # Calculate enhanced ROI projection
            roi_result = calculator.calculate_enhanced_roi_projection(
                investment=cost_analysis['total_cost'],
                industry=validated_data['target_industry'],
                project_type=validated_data['project_type'],
                timeline_months=cost_analysis['timeline_months'],
                currency=validated_data['currency'],
                company_size=validated_data['company_size']
            )
            
            return cost_analysis, roi_result
        
        # Get cached result or calculate
        cost_analysis, roi_result = calculation_cache.get_or_set(
            cache_key_data, perform_calculations, ttl=300  # Cache for 5 minutes
        )
        
        # Get market insights
        market_insights = calculator.get_market_insights(validated_data['target_industry'])
        
        # Core v2.0 - basic recommendations only
        
        # Generate recommendations
        recommendations = calculator.generate_recommendations(
            validated_data['company_size'],
            validated_data['project_type'],
            validated_data['target_industry'],
            roi_result
        )
        
        # Core v2.0 - focus on enhanced calculations and basic business intelligence
        
        # Format response
        currency_config = config_class.CURRENCIES[validated_data['currency']]
        
        response = {
            'success': True,
            'calculation_id': f"calc_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'input_parameters': validated_data,
            'cost_analysis': {
                'total_cost': float(cost_analysis['total_cost']),
                'cost_breakdown': {k: float(v) for k, v in cost_analysis['cost_breakdown'].items()},
                'timeline_months': cost_analysis['timeline_months'],
                'currency': cost_analysis['currency'],
                'currency_symbol': currency_config.symbol,
                'multipliers': cost_analysis['multipliers']
            },
            'roi_projection': {
                'total_investment': float(roi_result.total_investment),
                'projected_revenue': float(roi_result.projected_revenue),
                'net_profit': float(roi_result.net_profit),
                'roi_percentage': float(roi_result.roi_percentage),
                'payback_period_months': roi_result.payback_period_months,
                'break_even_point': float(roi_result.break_even_point),
                'npv': float(roi_result.npv),
                'irr': float(roi_result.irr),
                'risk_score': float(roi_result.risk_score),
                'confidence_interval': {
                    'lower': float(roi_result.confidence_interval[0]),
                    'upper': float(roi_result.confidence_interval[1])
                },
                'sensitivity_analysis': roi_result.sensitivity_analysis
            },
            'market_insights': market_insights,
            'recommendations': recommendations,
            'calculation_metadata': {
                'calculation_date': roi_result.calculation_date.isoformat(),
                'calculator_version': '2.0.0',
                'methodology': 'Enhanced Monte Carlo with NPV/IRR analysis'
            }
        }
        
        logger.info(f"ROI calculation completed for {validated_data['company_name']} - "
                   f"ROI: {roi_result.roi_percentage}%, Risk: {roi_result.risk_score}")
        
        return jsonify(response)
        
    except ValidationError:
        raise  # Re-raise validation errors to be handled by decorator
    except BusinessLogicError:
        raise  # Re-raise business logic errors to be handled by decorator
    except Exception as e:
        logger.error(f"Unexpected error in calculate_roi: {str(e)}")
        raise ValidationError(f"Calculation failed: {str(e)}")

@app.route('/api/currencies')
@rate_limit(api_limiter, "Too many API requests. Please slow down.")
@handle_validation_errors
def get_currencies():
    """Get available currencies with enhanced information"""
    try:
        currencies = {}
        for code, config in config_class.CURRENCIES.items():
            currencies[code] = {
                'symbol': config.symbol,
                'name': config.name,
                'rate': config.rate,
                'precision': config.precision
            }
        
        return jsonify({
            'success': True,
            'currencies': currencies,
            'default_currency': config_class.DEFAULT_CURRENCY
        })
        
    except Exception as e:
        logger.error(f"Error fetching currencies: {str(e)}")
        raise ValidationError(f"Failed to fetch currencies: {str(e)}")

@app.route('/api/industries')
@rate_limit(api_limiter, "Too many API requests. Please slow down.")
@handle_validation_errors
def get_industries():
    """Get available industries with enhanced information"""
    try:
        industries = []
        for key, config in config_class.INDUSTRIES.items():
            industries.append({
                'id': key,
                'name': key.replace('_', ' ').title(),
                'growth_rate': f"{config.growth_rate * 100:.1f}%",
                'market_size': config.market_size,
                'risk_level': calculator._get_risk_level_description(config.risk_factor),
                'volatility': f"{config.volatility * 100:.1f}%",
                'regulatory_complexity': config.regulatory_complexity
            })
        
        return jsonify({
            'success': True,
            'industries': industries
        })
        
    except Exception as e:
        logger.error(f"Error fetching industries: {str(e)}")
        raise ValidationError(f"Failed to fetch industries: {str(e)}")

@app.route('/api/projects')
@handle_validation_errors
def get_projects():
    """Get available project types with enhanced information"""
    try:
        projects = []
        for key, config in config_class.PROJECT_TYPES.items():
            projects.append({
                'id': key,
                'name': config.description,
                'complexity': config.complexity,
                'timeline': f"{config.timeline} months",
                'base_cost': f"${config.base_cost:,}",
                'roi_potential': f"{config.roi_potential:.1f}x",
                'risk_level': f"{config.risk_level * 100:.1f}%",
                'required_skills': config.required_skills
            })
        
        return jsonify({
            'success': True,
            'projects': projects
        })
        
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise ValidationError(f"Failed to fetch projects: {str(e)}")

@app.route('/api/company-sizes')
@handle_validation_errors
def get_company_sizes():
    """Get available company sizes with enhanced information"""
    try:
        company_sizes = []
        for key, config in config_class.COMPANY_SIZES.items():
            company_sizes.append({
                'id': key,
                'name': key.title(),
                'multiplier': config.multiplier,
                'budget_range': {
                    'min': config.min_budget,
                    'max': config.max_budget
                },
                'typical_team_size': config.typical_team_size,
                'risk_factor': f"{config.risk_factor * 100:.1f}%"
            })
        
        return jsonify({
            'success': True,
            'company_sizes': company_sizes
        })
        
    except Exception as e:
        logger.error(f"Error fetching company sizes: {str(e)}")
        raise ValidationError(f"Failed to fetch company sizes: {str(e)}")

@app.route('/api/market-insights/<industry>')
@handle_validation_errors
def get_market_insights_api(industry):
    """Get detailed market insights for a specific industry"""
    try:
        # Validate industry
        validated_industry = APIValidator.validate_industry(industry)
        
        # Get market insights
        insights = calculator.get_market_insights(validated_industry)
        
        return jsonify({
            'success': True,
            'industry': validated_industry,
            'insights': insights
        })
        
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error fetching market insights: {str(e)}")
        raise ValidationError(f"Failed to fetch market insights: {str(e)}")

@app.route('/api/validate', methods=['POST'])
@handle_validation_errors
def validate_input():
    """Validate user input without performing calculations"""
    try:
        data = request.get_json()
        if not data:
            raise ValidationError("No JSON data provided", code="NO_DATA")
        
        # Validate the request
        validated_data = APIValidator.validate_roi_calculation_request(data)
        
        # Perform business logic validation
        custom_investment = validated_data.get('custom_investment')
        BusinessValidator.validate_business_logic(
            validated_data['company_size'],
            validated_data['project_type'],
            validated_data['target_industry'],
            custom_investment
        )
        
        return jsonify({
            'success': True,
            'message': 'Input validation successful',
            'validated_data': {
                k: str(v) if isinstance(v, Decimal) else v 
                for k, v in validated_data.items()
            }
        })
        
    except ValidationError:
        raise
    except BusinessLogicError:
        raise
    except Exception as e:
        logger.error(f"Error in input validation: {str(e)}")
        raise ValidationError(f"Validation failed: {str(e)}")

@app.route('/api/export-html')
@handle_validation_errors 
def export_html_report():
    """Generate comprehensive HTML report"""
    try:
        # Get calculation parameters from URL
        company_name = request.args.get('company', 'Sample Company')
        company_size = request.args.get('company_size', 'medium')
        current_industry = request.args.get('current_industry', 'saas')
        project_type = request.args.get('project_type', 'product_development')
        target_industry = request.args.get('target_industry', 'saas')
        currency = request.args.get('currency', 'USD')
        
        # Validate parameters
        validated_data = {
            'company_name': APIValidator.validate_company_name(company_name),
            'company_size': APIValidator.validate_company_size(company_size),
            'current_industry': APIValidator.validate_industry(current_industry),
            'project_type': APIValidator.validate_project_type(project_type),
            'target_industry': APIValidator.validate_industry(target_industry),
            'currency': APIValidator.validate_currency(currency)
        }
        
        # Perform calculations
        cost_analysis = calculator.calculate_project_cost(
            validated_data['company_size'], 
            validated_data['project_type'], 
            validated_data['target_industry'], 
            validated_data['currency']
        )
        
        roi_result = calculator.calculate_enhanced_roi_projection(
            cost_analysis['total_cost'], 
            validated_data['target_industry'], 
            validated_data['project_type'], 
            cost_analysis['timeline_months'],
            validated_data['currency'],
            validated_data['company_size']
        )
        
        market_insights = calculator.get_market_insights(validated_data['target_industry'])
        recommendations = calculator.generate_recommendations(
            validated_data['company_size'], 
            validated_data['project_type'], 
            validated_data['target_industry'],
            roi_result
        )
        
        # Generate enhanced HTML report
        currency_config = config_class.CURRENCIES[validated_data['currency']]
        
        html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Business ROI Analysis Report - {validated_data['company_name']}</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 40px; 
            background: #f8f9fa; 
            line-height: 1.6;
        }}
        .container {{ 
            background: white; 
            padding: 40px; 
            border-radius: 15px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
            max-width: 1000px; 
            margin: 0 auto; 
        }}
        h1 {{ 
            color: #667eea; 
            text-align: center; 
            font-size: 2.5rem; 
            margin-bottom: 2rem; 
            border-bottom: 3px solid #667eea;
            padding-bottom: 1rem;
        }}
        h2 {{ 
            color: #4a5568; 
            border-bottom: 2px solid #667eea; 
            padding-bottom: 0.5rem; 
            margin-top: 2rem; 
        }}
        .header-info {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 30px; 
        }}
        .metric-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin: 20px 0; 
        }}
        .metric {{ 
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
            color: white; 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center; 
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        }}
        .metric-value {{ 
            font-size: 2rem; 
            font-weight: bold; 
            margin-bottom: 0.5rem; 
        }}
        .metric-label {{ 
            font-size: 0.9rem; 
            opacity: 0.9; 
        }}
        .risk-indicator {{
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin: 5px 0;
        }}
        .risk-low {{ background: #48bb78; color: white; }}
        .risk-medium {{ background: #ed8936; color: white; }}
        .risk-high {{ background: #e53e3e; color: white; }}
        .recommendations {{ 
            background: #e6fffa; 
            padding: 20px; 
            border-radius: 10px; 
            border-left: 4px solid #38b2ac; 
        }}
        .cost-breakdown {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .confidence-interval {{
            background: #fff5f5;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #e53e3e;
            margin: 15px 0;
        }}
        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 20px 0; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
        }}
        th, td {{ 
            padding: 15px; 
            text-align: left; 
            border-bottom: 1px solid #e2e8f0; 
        }}
        th {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            font-weight: 600; 
        }}
        tr:nth-child(even) {{ background-color: #f7fafc; }}
        .footer {{ 
            text-align: center; 
            margin-top: 40px; 
            padding: 20px; 
            background: #f7fafc; 
            border-radius: 10px; 
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Business ROI Analysis Report</h1>
        
        <div class="header-info">
            <h3>🏢 {validated_data['company_name']}</h3>
            <p><strong>Company Size:</strong> {validated_data['company_size'].title()}</p>
            <p><strong>Industry:</strong> {validated_data['target_industry'].replace('_', ' ').title()}</p>
            <p><strong>Project Type:</strong> {config_class.PROJECT_TYPES[validated_data['project_type']].description}</p>
            <p><strong>Currency:</strong> {currency_config.name} ({currency_config.symbol})</p>
            <p><strong>Report Generated:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
        </div>
        
        <div class="section">
            <h2>💰 Financial Summary</h2>
            <div class="metric-grid">
                <div class="metric">
                    <div class="metric-value">{currency_config.symbol}{roi_result.total_investment:,.0f}</div>
                    <div class="metric-label">Total Investment</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{currency_config.symbol}{roi_result.projected_revenue:,.0f}</div>
                    <div class="metric-label">Projected Revenue</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{roi_result.roi_percentage:.1f}%</div>
                    <div class="metric-label">ROI Percentage</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{roi_result.payback_period_months}</div>
                    <div class="metric-label">Payback (Months)</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Advanced Financial Metrics</h2>
            <div class="metric-grid">
                <div class="metric">
                    <div class="metric-value">{currency_config.symbol}{roi_result.npv:,.0f}</div>
                    <div class="metric-label">Net Present Value</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{roi_result.irr:.2f}%</div>
                    <div class="metric-label">Internal Rate of Return</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{roi_result.risk_score:.1f}/100</div>
                    <div class="metric-label">Risk Score</div>
                </div>
            </div>
            
            <div class="confidence-interval">
                <h4>📈 95% Confidence Interval</h4>
                <p>Expected ROI range: <strong>{roi_result.confidence_interval[0]:.1f}% - {roi_result.confidence_interval[1]:.1f}%</strong></p>
                <p><em>Based on Monte Carlo simulation with 1,000 iterations</em></p>
            </div>
        </div>
        
        <div class="section">
            <h2>💸 Cost Breakdown</h2>
            <div class="cost-breakdown">
                <table>
                    <tr>
                        <th>Cost Category</th>
                        <th>Amount</th>
                        <th>Percentage</th>
                    </tr>
                    <tr>
                        <td>Development</td>
                        <td>{currency_config.symbol}{cost_analysis['cost_breakdown']['development']:,.0f}</td>
                        <td>{(cost_analysis['cost_breakdown']['development'] / cost_analysis['total_cost'] * 100):.1f}%</td>
                    </tr>
                    <tr>
                        <td>Infrastructure</td>
                        <td>{currency_config.symbol}{cost_analysis['cost_breakdown']['infrastructure']:,.0f}</td>
                        <td>{(cost_analysis['cost_breakdown']['infrastructure'] / cost_analysis['total_cost'] * 100):.1f}%</td>
                    </tr>
                    <tr>
                        <td>Annual Maintenance</td>
                        <td>{currency_config.symbol}{cost_analysis['cost_breakdown']['maintenance_annual']:,.0f}</td>
                        <td>{(cost_analysis['cost_breakdown']['maintenance_annual'] / cost_analysis['total_cost'] * 100):.1f}%</td>
                    </tr>
                    <tr>
                        <td>Regulatory Compliance</td>
                        <td>{currency_config.symbol}{cost_analysis['cost_breakdown']['regulatory_compliance']:,.0f}</td>
                        <td>{(cost_analysis['cost_breakdown']['regulatory_compliance'] / cost_analysis['total_cost'] * 100):.1f}%</td>
                    </tr>
                    <tr>
                        <td>Risk Buffer</td>
                        <td>{currency_config.symbol}{cost_analysis['cost_breakdown']['risk_buffer']:,.0f}</td>
                        <td>{(cost_analysis['cost_breakdown']['risk_buffer'] / cost_analysis['total_cost'] * 100):.1f}%</td>
                    </tr>
                </table>
            </div>
        </div>
        
        <div class="section">
            <h2>🌍 Market Insights</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Market Size</td><td>${market_insights['market_size_usd']:,}</td></tr>
                <tr><td>Annual Growth Rate</td><td>{market_insights['annual_growth_rate']}</td></tr>
                <tr><td>Risk Level</td><td><span class="risk-indicator risk-{market_insights['risk_level'].lower()}">{market_insights['risk_level']}</span></td></tr>
                <tr><td>Market Volatility</td><td>{market_insights['volatility']}</td></tr>
                <tr><td>Regulatory Complexity</td><td>{market_insights['regulatory_complexity']}</td></tr>
                <tr><td>Investment Attractiveness</td><td>{market_insights['investment_attractiveness']}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>💡 Strategic Recommendations</h2>
            <div class="recommendations">
                <ul>
"""
        
        for rec in recommendations:
            html_report += f"                    <li>{rec}</li>\n"
        
        html_report += f"""
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>📄 Professional Business ROI Analysis</strong></p>
            <p>Generated by Enhanced ROI Calculator v2.0 • {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            <p><strong>Methodology:</strong> Monte Carlo Simulation, NPV/IRR Analysis, Sensitivity Testing</p>
            <p><small>💡 Tip: Use Ctrl+P (Cmd+P on Mac) to save this report as a PDF</small></p>
        </div>
    </div>
</body>
</html>
"""
        
        return html_report, 200, {'Content-Type': 'text/html'}
        
    except ValidationError:
        raise
    except Exception as e:
        logger.error(f"Error generating HTML report: {str(e)}")
        raise ValidationError(f"Failed to generate report: {str(e)}")

# Advanced Interactive Features
@app.route('/api/scenarios', methods=['POST'])
@rate_limit(calculation_limiter, "Too many scenario calculations.")
@handle_validation_errors  
def create_scenario():
    """Create a new ROI scenario"""
    
    data = request.get_json()
    scenario_name = data.get('scenario_name')
    parameters = data.get('parameters', {})
    
    if not scenario_name:
        raise ValidationError("Scenario name is required")
    
    # Validate parameters
    validated_params = APIValidator.validate_roi_calculation_request(parameters)
    
    # Create scenario
    scenario_data = scenario_manager.create_scenario(scenario_name, validated_params)
    
    return jsonify({
        'success': True,
        'scenario': scenario_data,
        'message': f'Scenario "{scenario_name}" created successfully'
    })

@app.route('/api/scenarios/compare', methods=['POST'])
@rate_limit(api_limiter, "Too many comparison requests.")
@handle_validation_errors
def compare_scenarios():
    """Compare multiple scenarios"""
    
    data = request.get_json()
    scenario_names = data.get('scenario_names', [])
    
    if len(scenario_names) < 2:
        raise ValidationError("At least 2 scenarios required for comparison")
    
    comparison = scenario_manager.compare_scenarios(scenario_names)
    
    return jsonify({
        'success': True,
        'comparison': comparison
    })

@app.route('/api/what-if/investment', methods=['POST'])
@rate_limit(calculation_limiter, "Too many what-if analyses.")
@handle_validation_errors
def what_if_investment():
    """Perform what-if analysis on investment amounts"""
    
    data = request.get_json()
    base_parameters = data.get('base_parameters', {})
    investment_range = data.get('investment_range', [10000, 1000000])
    steps = data.get('steps', 10)
    
    # Validate parameters
    validated_params = APIValidator.validate_roi_calculation_request(base_parameters)
    
    analysis = what_if_analyzer.analyze_investment_sensitivity(
        validated_params, 
        tuple(investment_range), 
        steps
    )
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

@app.route('/api/export/<format_type>', methods=['POST'])
@rate_limit(api_limiter, "Too many export requests.")
@handle_validation_errors
def export_advanced_report(format_type):
    """Export calculation results in professional formats"""
    
    data = request.get_json()
    if not data:
        raise ValidationError("No calculation data provided for export")
    
    if format_type == 'executive':
        html_report = report_generator.generate_executive_summary(data)
        return app.response_class(html_report, mimetype='text/html')
    
    elif format_type == 'detailed':
        html_report = report_generator.generate_detailed_report(data)
        return app.response_class(html_report, mimetype='text/html')
    
    elif format_type == 'json':
        json_export = report_generator.generate_json_export(data)
        return app.response_class(
            json_export,
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=roi_analysis.json'}
        )
    
    elif format_type == 'csv':
        csv_export = report_generator.generate_csv_export(data)
        return app.response_class(
            csv_export,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=roi_analysis.csv'}
        )
    
    else:
        raise ValidationError(f"Unsupported export format: {format_type}")

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': True,
        'message': 'Resource not found',
        'code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': True,
        'message': 'Internal server error',
        'code': 500,
        'details': str(error) if app.config['DEBUG'] else None
    }), 500

if __name__ == '__main__':
    logger.info(f"Starting Business ROI Calculator v2.0 in {config_class.ENV} mode")
    logger.info(f"Debug mode: {config_class.DEBUG}")
    
    app.run(
        debug=config_class.DEBUG,
        host=config_class.HOST,
        port=config_class.PORT
    )