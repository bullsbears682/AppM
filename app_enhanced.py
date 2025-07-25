#!/usr/bin/env python3
"""
Enhanced Business ROI Calculator - Flask Application
Restructured with better error handling, validation, and organization
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from config import config, UI_CONSTANTS
from utils import (
    handle_errors, validate_roi_calculation_input, log_calculation_request,
    generate_calculation_id, format_currency, ValidationError, CalculationError
)
from models import EnhancedROICalculator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('roi_calculator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)
    
    # Initialize calculator
    calculator = EnhancedROICalculator()
    
    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 error: {request.url}")
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'timestamp': datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {str(error)}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'timestamp': datetime.now().isoformat()
        }), 500
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        return jsonify({
            'error': 'Validation Error',
            'message': error.message,
            'field': error.field,
            'code': error.code,
            'timestamp': datetime.now().isoformat()
        }), 400
    
    @app.errorhandler(CalculationError)
    def calculation_error(error):
        return jsonify({
            'error': 'Calculation Error',
            'message': error.message,
            'details': error.details,
            'timestamp': datetime.now().isoformat()
        }), 422
    
    # Routes
    @app.route('/')
    def index():
        """Main dashboard route"""
        try:
            logger.info("Dashboard accessed")
            return render_template('index_enhanced.html', 
                                 app_config=app.config,
                                 ui_constants=UI_CONSTANTS)
        except Exception as e:
            logger.error(f"Dashboard error: {str(e)}")
            return render_template('error.html', error="Dashboard unavailable"), 500
    
    @app.route('/api/calculate', methods=['POST'])
    @handle_errors
    def calculate_roi():
        """Enhanced ROI calculation endpoint with comprehensive validation"""
        try:
            # Log request for monitoring
            log_calculation_request()
            
            # Get and validate input data
            input_data = request.get_json()
            if not input_data:
                raise ValidationError("No data provided", field="request", code="empty_request")
            
            # Comprehensive validation
            validated_data = validate_roi_calculation_input(input_data)
            
            # Generate unique calculation ID
            calculation_id = generate_calculation_id()
            logger.info(f"Starting calculation {calculation_id} for {validated_data['company_name']}")
            
            # Calculate project cost
            project_cost = calculator.calculate_project_cost(
                company_size=validated_data['company_size'],
                project_type=validated_data['project_type'],
                industry=validated_data['target_industry'],
                currency=validated_data['currency'],
                custom_budget=validated_data.get('custom_budget')
            )
            
            # Calculate ROI projections
            roi_projections = calculator.calculate_enhanced_roi_projection(
                investment=project_cost.total_cost,
                industry=validated_data['target_industry'],
                project_type=validated_data['project_type'],
                timeline_months=project_cost.timeline_months,
                currency=validated_data['currency']
            )
            
            # Calculate risk assessment
            risk_assessment = calculator.calculate_comprehensive_risk_assessment(
                company_size=validated_data['company_size'],
                project_type=validated_data['project_type'],
                industry=validated_data['target_industry']
            )
            
            # Get market insights
            market_insights = calculator.get_enhanced_market_insights(
                industry=validated_data['target_industry']
            )
            
            # Prepare response
            response_data = {
                'calculation_id': calculation_id,
                'timestamp': datetime.now().isoformat(),
                'input_data': validated_data,
                'project_cost': {
                    'total_cost': project_cost.total_cost,
                    'total_cost_formatted': format_currency(project_cost.total_cost, validated_data['currency']),
                    'currency': project_cost.currency,
                    'currency_symbol': project_cost.currency_symbol,
                    'breakdown': project_cost.breakdown,
                    'timeline_months': project_cost.timeline_months,
                    'complexity': project_cost.complexity,
                    'confidence_interval': {
                        'lower': project_cost.confidence_interval[0],
                        'upper': project_cost.confidence_interval[1],
                        'lower_formatted': format_currency(project_cost.confidence_interval[0], validated_data['currency']),
                        'upper_formatted': format_currency(project_cost.confidence_interval[1], validated_data['currency'])
                    }
                },
                'roi_projections': {
                    scenario: {
                        'scenario': roi.scenario,
                        'annual_return': roi.annual_return,
                        'annual_return_formatted': format_currency(roi.annual_return, validated_data['currency']),
                        'total_roi': roi.total_roi,
                        'total_roi_formatted': format_currency(roi.total_roi, validated_data['currency']),
                        'roi_percentage': roi.roi_percentage,
                        'break_even_months': roi.break_even_months,
                        'probability': roi.probability,
                        'description': roi.description,
                        'net_present_value': roi.net_present_value,
                        'npv_formatted': format_currency(roi.net_present_value, validated_data['currency']),
                        'irr': roi.irr,
                        'payback_period': roi.payback_period
                    }
                    for scenario, roi in roi_projections.items()
                },
                'risk_assessment': {
                    'overall_risk': risk_assessment.overall_risk,
                    'risk_category': risk_assessment.risk_category,
                    'company_risk': risk_assessment.company_risk,
                    'project_risk': risk_assessment.project_risk,
                    'industry_risk': risk_assessment.industry_risk,
                    'market_volatility': risk_assessment.market_volatility,
                    'mitigation_strategies': risk_assessment.mitigation_strategies
                },
                'market_insights': {
                    'market_size': market_insights.market_size,
                    'growth_rate': market_insights.growth_rate,
                    'risk_level': market_insights.risk_level,
                    'volatility': market_insights.volatility,
                    'confidence_level': market_insights.confidence_level,
                    'regulatory_complexity': market_insights.regulatory_complexity,
                    'trends': market_insights.trends,
                    'opportunities': market_insights.opportunities,
                    'challenges': market_insights.challenges
                },
                'recommendations': generate_recommendations(validated_data, risk_assessment, market_insights)
            }
            
            logger.info(f"Calculation {calculation_id} completed successfully")
            return jsonify(response_data)
            
        except ValidationError:
            raise  # Re-raise validation errors
        except CalculationError:
            raise  # Re-raise calculation errors
        except Exception as e:
            logger.error(f"Unexpected error in calculate_roi: {str(e)}", exc_info=True)
            raise CalculationError(
                "Calculation failed due to unexpected error",
                f"Internal error during ROI calculation: {str(e)}"
            )
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': app.config['VERSION'],
            'app_name': app.config['APP_NAME']
        })
    
    @app.route('/api/config', methods=['GET'])
    def get_config():
        """Get client configuration data"""
        try:
            from config import COMPANY_SIZES, INDUSTRIES, PROJECT_TYPES, CURRENCIES
            
            return jsonify({
                'company_sizes': {
                    k: {
                        'description': v['description'],
                        'typical_revenue': v['typical_revenue']
                    }
                    for k, v in COMPANY_SIZES.items()
                },
                'industries': {
                    k: {
                        'description': v['description'],
                        'growth_rate': f"{v['growth_rate']*100:.1f}%",
                        'market_size': v['market_size']
                    }
                    for k, v in INDUSTRIES.items()
                },
                'project_types': {
                    k: {
                        'description': v['description'],
                        'complexity': v['complexity'],
                        'timeline': v['timeline'],
                        'required_skills': v['required_skills']
                    }
                    for k, v in PROJECT_TYPES.items()
                },
                'currencies': {
                    k: {
                        'name': v['name'],
                        'symbol': v['symbol']
                    }
                    for k, v in CURRENCIES.items()
                }
            })
            
        except Exception as e:
            logger.error(f"Config endpoint error: {str(e)}")
            return jsonify({'error': 'Configuration data unavailable'}), 500
    
    def generate_recommendations(data: dict, risk: object, market: object) -> list:
        """Generate personalized recommendations based on calculation results"""
        recommendations = []
        
        # Risk-based recommendations
        if risk.risk_category == 'High' or risk.risk_category == 'Very High':
            recommendations.append({
                'type': 'risk',
                'priority': 'high',
                'title': 'High Risk Project',
                'message': 'Consider implementing additional risk mitigation strategies',
                'actions': risk.mitigation_strategies[:3]
            })
        
        # Market-based recommendations
        if market.confidence_level in ['Very High', 'High']:
            recommendations.append({
                'type': 'market',
                'priority': 'medium',
                'title': 'Strong Market Opportunity',
                'message': f'The {data["target_industry"]} market shows strong growth potential',
                'actions': ['Consider accelerated timeline', 'Evaluate larger investment', 'Plan for scaling']
            })
        
        # Company size recommendations
        if data['company_size'] == 'startup':
            recommendations.append({
                'type': 'strategy',
                'priority': 'medium',
                'title': 'Startup Considerations',
                'message': 'Focus on MVP and iterative development',
                'actions': ['Start with core features', 'Plan phased rollout', 'Secure funding runway']
            })
        
        return recommendations
    
    return app

# Create app instance
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']
    
    logger.info(f"Starting Enhanced ROI Calculator on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )