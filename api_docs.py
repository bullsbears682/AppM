"""
Professional API Documentation for VoidSight Analytics
Enterprise-grade API documentation with Swagger/OpenAPI integration
"""

from flask import Blueprint
from flask_restx import Api, Resource, fields, Namespace
from functools import wraps
from werkzeug.exceptions import ValidationError

# Create API documentation blueprint
api_bp = Blueprint('api_docs', __name__)

# Initialize Flask-RESTx API with professional configuration
api = Api(
    api_bp,
    version='2.0',
    title='VoidSight Analytics API',
    description='''
    **Enterprise ROI Intelligence Platform API**
    
    Professional RESTful API for business ROI calculations, scenario analysis, and financial modeling.
    
    ## Features
    - 🎯 Advanced ROI calculations with industry benchmarks
    - 📊 Monte Carlo simulations and risk analysis  
    - 🏢 Multi-industry and company size support
    - 💰 14+ currency support including cryptocurrency
    - 📈 Professional report generation (PDF, Excel, PowerPoint)
    - 🔐 Enterprise authentication and authorization
    - ⚡ High-performance calculations with caching
    
    ## Authentication
    All endpoints require JWT authentication. Include your token in the Authorization header:
    ```
    Authorization: Bearer <your_jwt_token>
    ```
    
    ## Rate Limits
    - Free tier: 100 requests/hour
    - Professional: 1,000 requests/hour  
    - Enterprise: 10,000 requests/hour
    
    ## Support
    - Documentation: https://docs.voidsight.com
    - Support: support@voidsight.com
    - Status: https://status.voidsight.com
    ''',
    doc='/docs/',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    },
    security='Bearer'
)

# Define namespaces for organized documentation
calculations_ns = Namespace('calculations', description='ROI calculation operations')
scenarios_ns = Namespace('scenarios', description='Scenario analysis and what-if modeling')
reports_ns = Namespace('reports', description='Professional report generation')
auth_ns = Namespace('auth', description='Authentication and user management')
analytics_ns = Namespace('analytics', description='Advanced analytics and insights')

api.add_namespace(calculations_ns, path='/api/calculations')
api.add_namespace(scenarios_ns, path='/api/scenarios')
api.add_namespace(reports_ns, path='/api/reports')
api.add_namespace(auth_ns, path='/api/auth')
api.add_namespace(analytics_ns, path='/api/analytics')

# Define data models for request/response documentation
roi_calculation_request = api.model('ROICalculationRequest', {
    'project_type': fields.String(required=True, description='Type of project', 
                                 enum=['ecommerce_platform', 'mobile_app', 'ai_integration', 'marketing_campaign', 
                                      'product_development', 'tech_upgrade', 'automation_system', 'cybersecurity_upgrade']),
    'company_size': fields.String(required=True, description='Company size category',
                                enum=['startup', 'small', 'medium', 'large', 'enterprise']),
    'industry': fields.String(required=True, description='Target industry',
                            enum=['fintech', 'healthtech', 'edtech', 'ecommerce', 'saas', 'gaming', 
                                 'realestate', 'foodbeverage', 'manufacturing', 'logistics']),
    'investment_amount': fields.Float(required=True, description='Initial investment amount', min=1000, max=100000000),
    'timeline_months': fields.Integer(required=True, description='Project timeline in months', min=1, max=120),
    'risk_tolerance': fields.Integer(required=False, description='Risk tolerance (0-100)', min=0, max=100, default=50),
    'currency': fields.String(required=False, description='Currency code', default='USD',
                            enum=['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'INR', 'KRW', 'SGD', 'HKD', 'BTC', 'ETH']),
    'market_conditions': fields.String(required=False, description='Current market conditions', 
                                     enum=['bullish', 'neutral', 'bearish'], default='neutral'),
    'custom_parameters': fields.Raw(required=False, description='Additional custom parameters')
})

roi_calculation_response = api.model('ROICalculationResponse', {
    'success': fields.Boolean(description='Request success status'),
    'roi_percentage': fields.Float(description='Calculated ROI percentage'),
    'total_investment': fields.Float(description='Total investment amount'),
    'projected_revenue': fields.Float(description='Projected revenue'),
    'net_profit': fields.Float(description='Net profit amount'),
    'payback_period_months': fields.Integer(description='Payback period in months'),
    'break_even_point': fields.Float(description='Break-even point'),
    'risk_score': fields.Float(description='Risk assessment score (0-100)'),
    'confidence_level': fields.Float(description='Confidence level percentage'),
    'currency': fields.String(description='Currency code'),
    'calculation_date': fields.DateTime(description='Calculation timestamp'),
    'scenario_analysis': fields.Raw(description='Detailed scenario analysis results'),
    'cash_flow_projection': fields.List(fields.Raw, description='Monthly cash flow projections'),
    'sensitivity_analysis': fields.Raw(description='Sensitivity analysis results')
})

scenario_analysis_request = api.model('ScenarioAnalysisRequest', {
    'base_parameters': fields.Nested(roi_calculation_request, required=True, description='Base calculation parameters'),
    'scenario_type': fields.String(required=True, description='Type of scenario analysis',
                                 enum=['monte_carlo', 'sensitivity', 'stress_test', 'what_if']),
    'iterations': fields.Integer(required=False, description='Number of Monte Carlo iterations', min=1000, max=100000, default=10000),
    'confidence_levels': fields.List(fields.Float, required=False, description='Confidence levels for analysis', default=[0.9, 0.95, 0.99]),
    'variable_ranges': fields.Raw(required=False, description='Ranges for variable sensitivity analysis')
})

report_generation_request = api.model('ReportGenerationRequest', {
    'calculation_results': fields.Raw(required=True, description='ROI calculation results to include in report'),
    'report_type': fields.String(required=True, description='Type of report to generate',
                                enum=['executive_summary', 'detailed_analysis', 'investor_presentation', 'technical_report']),
    'format': fields.String(required=True, description='Output format',
                          enum=['pdf', 'excel', 'powerpoint', 'html', 'json']),
    'branding': fields.Raw(required=False, description='Custom branding options'),
    'include_charts': fields.Boolean(required=False, description='Include visualization charts', default=True),
    'include_raw_data': fields.Boolean(required=False, description='Include raw calculation data', default=False)
})

auth_login_request = api.model('AuthLoginRequest', {
    'email': fields.String(required=True, description='User email address'),
    'password': fields.String(required=True, description='User password'),
    'remember_me': fields.Boolean(required=False, description='Remember login session', default=False)
})

auth_response = api.model('AuthResponse', {
    'success': fields.Boolean(description='Authentication success status'),
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'expires_in': fields.Integer(description='Token expiration time in seconds'),
    'user_info': fields.Raw(description='User profile information'),
    'subscription_tier': fields.String(description='User subscription tier')
})

error_response = api.model('ErrorResponse', {
    'success': fields.Boolean(description='Request success status', default=False),
    'error': fields.String(description='Error type'),
    'message': fields.String(description='Human-readable error message'),
    'code': fields.Integer(description='HTTP status code'),
    'details': fields.Raw(description='Additional error details'),
    'timestamp': fields.DateTime(description='Error timestamp')
})

# Authentication decorator for documentation
def require_auth(f):
    """Decorator to mark endpoints as requiring authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

# ROI Calculations Namespace
@calculations_ns.route('/roi')
class ROICalculation(Resource):
    @calculations_ns.doc('calculate_roi')
    @calculations_ns.expect(roi_calculation_request)
    @calculations_ns.marshal_with(roi_calculation_response)
    @calculations_ns.response(200, 'Success', roi_calculation_response)
    @calculations_ns.response(400, 'Validation Error', error_response)
    @calculations_ns.response(401, 'Unauthorized', error_response)
    @calculations_ns.response(429, 'Rate Limit Exceeded', error_response)
    @require_auth
    def post(self):
        """
        **Calculate ROI with Advanced Financial Modeling**
        
        Performs comprehensive ROI analysis using industry benchmarks, risk assessment, 
        and advanced financial modeling techniques.
        
        **Features:**
        - Real industry data and benchmarks
        - Monte Carlo risk simulations  
        - Currency conversion support
        - Company size and industry adjustments
        - Sensitivity analysis
        - Cash flow projections
        
        **Example Request:**
        ```json
        {
            "project_type": "ecommerce_platform",
            "company_size": "medium", 
            "industry": "retail",
            "investment_amount": 50000,
            "timeline_months": 12,
            "risk_tolerance": 60,
            "currency": "USD"
        }
        ```
        """
        pass

@calculations_ns.route('/batch')
class BatchROICalculation(Resource):
    @calculations_ns.doc('batch_calculate_roi')
    @calculations_ns.expect([roi_calculation_request])
    @calculations_ns.marshal_with([roi_calculation_response])
    @require_auth
    def post(self):
        """
        **Batch ROI Calculations**
        
        Calculate ROI for multiple projects simultaneously. Useful for portfolio analysis
        and comparing multiple investment opportunities.
        
        **Limits:**
        - Free tier: 5 calculations per batch
        - Professional: 25 calculations per batch
        - Enterprise: 100 calculations per batch
        """
        pass

# Scenario Analysis Namespace
@scenarios_ns.route('/monte-carlo')
class MonteCarloAnalysis(Resource):
    @scenarios_ns.doc('monte_carlo_analysis')
    @scenarios_ns.expect(scenario_analysis_request)
    @scenarios_ns.marshal_with(roi_calculation_response)
    @require_auth
    def post(self):
        """
        **Monte Carlo Scenario Analysis**
        
        Advanced probabilistic analysis using Monte Carlo simulations to model
        uncertainty and risk in ROI projections.
        
        **Features:**
        - Configurable iteration count (1,000 - 100,000)
        - Multiple confidence intervals
        - Risk distribution analysis
        - Stress testing scenarios
        """
        pass

@scenarios_ns.route('/sensitivity')
class SensitivityAnalysis(Resource):
    @scenarios_ns.doc('sensitivity_analysis')
    @scenarios_ns.expect(scenario_analysis_request)
    @require_auth
    def post(self):
        """
        **Sensitivity Analysis**
        
        Analyze how changes in key variables affect ROI outcomes.
        Identifies the most critical factors for project success.
        """
        pass

@scenarios_ns.route('/what-if')
class WhatIfAnalysis(Resource):
    @scenarios_ns.doc('what_if_analysis')
    @scenarios_ns.expect(scenario_analysis_request)
    @require_auth
    def post(self):
        """
        **What-If Analysis**
        
        Explore different scenarios by varying investment amounts,
        timelines, and market conditions.
        """
        pass

# Reports Namespace
@reports_ns.route('/generate')
class ReportGeneration(Resource):
    @reports_ns.doc('generate_report')
    @reports_ns.expect(report_generation_request)
    @require_auth
    def post(self):
        """
        **Generate Professional Reports**
        
        Create professionally formatted reports in multiple formats
        including PDF, Excel, and PowerPoint presentations.
        
        **Report Types:**
        - Executive Summary: High-level overview for stakeholders
        - Detailed Analysis: Complete technical analysis
        - Investor Presentation: Pitch-ready presentation
        - Technical Report: Full methodology and calculations
        """
        pass

@reports_ns.route('/templates')
class ReportTemplates(Resource):
    @reports_ns.doc('list_report_templates')
    @require_auth
    def get(self):
        """
        **List Available Report Templates**
        
        Get a list of available report templates and customization options.
        """
        pass

# Authentication Namespace
@auth_ns.route('/login')
class AuthLogin(Resource):
    @auth_ns.doc('user_login')
    @auth_ns.expect(auth_login_request)
    @auth_ns.marshal_with(auth_response)
    @auth_ns.response(200, 'Login successful', auth_response)
    @auth_ns.response(401, 'Invalid credentials', error_response)
    def post(self):
        """
        **User Authentication**
        
        Authenticate user and receive JWT tokens for API access.
        """
        pass

@auth_ns.route('/refresh')
class AuthRefresh(Resource):
    @auth_ns.doc('refresh_token')
    @auth_ns.marshal_with(auth_response)
    @require_auth
    def post(self):
        """
        **Refresh Access Token**
        
        Refresh expired access token using refresh token.
        """
        pass

@auth_ns.route('/profile')
class UserProfile(Resource):
    @auth_ns.doc('get_user_profile')
    @require_auth
    def get(self):
        """
        **Get User Profile**
        
        Retrieve current user profile and subscription information.
        """
        pass

# Analytics Namespace
@analytics_ns.route('/dashboard')
class AnalyticsDashboard(Resource):
    @analytics_ns.doc('analytics_dashboard')
    @require_auth
    def get(self):
        """
        **Analytics Dashboard Data**
        
        Get aggregated analytics and insights for dashboard display.
        """
        pass

@analytics_ns.route('/usage')
class UsageAnalytics(Resource):
    @analytics_ns.doc('usage_analytics')
    @require_auth
    def get(self):
        """
        **Usage Analytics**
        
        Get API usage statistics and billing information.
        """
        pass

# Error handlers for API documentation
@api.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handle validation errors"""
    return {'message': str(error)}, 400

@api.errorhandler(Exception)
def handle_exception(error):
    """Handle general exceptions"""
    return {'message': 'Internal server error'}, 500

def init_api_docs(app):
    """Initialize API documentation with the Flask app"""
    app.register_blueprint(api_bp, url_prefix='/api/v2')
    return api