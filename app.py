#!/usr/bin/env python3
"""
Business ROI Calculator - Modern Web Application
Helps companies calculate costs and ROI for business projects
"""

from flask import Flask, render_template, request, jsonify
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Business data and calculations
COMPANY_SIZES = {
    'startup': {'multiplier': 0.7, 'min_budget': 5000, 'max_budget': 100000},
    'small': {'multiplier': 1.0, 'min_budget': 25000, 'max_budget': 500000},
    'medium': {'multiplier': 1.5, 'min_budget': 100000, 'max_budget': 2000000},
    'enterprise': {'multiplier': 2.5, 'min_budget': 500000, 'max_budget': 10000000}
}

INDUSTRIES = {
    'fintech': {'growth_rate': 0.25, 'risk_factor': 0.15, 'market_size': 'Large'},
    'healthtech': {'growth_rate': 0.30, 'risk_factor': 0.20, 'market_size': 'Huge'},
    'edtech': {'growth_rate': 0.22, 'risk_factor': 0.12, 'market_size': 'Large'},
    'ecommerce': {'growth_rate': 0.18, 'risk_factor': 0.08, 'market_size': 'Massive'},
    'saas': {'growth_rate': 0.35, 'risk_factor': 0.18, 'market_size': 'Large'},
    'gaming': {'growth_rate': 0.20, 'risk_factor': 0.25, 'market_size': 'Medium'},
    'realEstate': {'growth_rate': 0.15, 'risk_factor': 0.10, 'market_size': 'Stable'},
    'foodBeverage': {'growth_rate': 0.12, 'risk_factor': 0.15, 'market_size': 'Medium'},
    'manufacturing': {'growth_rate': 0.10, 'risk_factor': 0.08, 'market_size': 'Large'},
    'logistics': {'growth_rate': 0.16, 'risk_factor': 0.12, 'market_size': 'Large'}
}

PROJECT_TYPES = {
    'product_development': {
        'base_cost': 150000, 'timeline': 12, 'roi_potential': 2.5,
        'description': 'New Product Development', 'complexity': 'High'
    },
    'digital_transformation': {
        'base_cost': 200000, 'timeline': 18, 'roi_potential': 3.0,
        'description': 'Digital Transformation', 'complexity': 'Very High'
    },
    'market_expansion': {
        'base_cost': 100000, 'timeline': 8, 'roi_potential': 2.0,
        'description': 'Market Expansion', 'complexity': 'Medium'
    },
    'tech_upgrade': {
        'base_cost': 80000, 'timeline': 6, 'roi_potential': 1.8,
        'description': 'Technology Upgrade', 'complexity': 'Medium'
    },
    'marketing_campaign': {
        'base_cost': 50000, 'timeline': 4, 'roi_potential': 1.5,
        'description': 'Marketing Campaign', 'complexity': 'Low'
    },
    'ecommerce_platform': {
        'base_cost': 120000, 'timeline': 10, 'roi_potential': 2.2,
        'description': 'E-commerce Platform', 'complexity': 'High'
    },
    'mobile_app': {
        'base_cost': 90000, 'timeline': 8, 'roi_potential': 2.0,
        'description': 'Mobile Application', 'complexity': 'High'
    },
    'ai_integration': {
        'base_cost': 180000, 'timeline': 14, 'roi_potential': 2.8,
        'description': 'AI Integration', 'complexity': 'Very High'
    }
}

class ROICalculator:
    def __init__(self):
        pass
    
    def calculate_project_cost(self, company_size, project_type, industry, custom_requirements=None):
        """Calculate realistic project costs based on multiple factors"""
        
        # Base calculations
        size_data = COMPANY_SIZES.get(company_size, COMPANY_SIZES['small'])
        project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        
        # Calculate base cost with size multiplier
        base_cost = project_data['base_cost'] * size_data['multiplier']
        
        # Industry complexity adjustment
        industry_multiplier = 1.0 + (industry_data['risk_factor'] * 0.5)
        adjusted_cost = base_cost * industry_multiplier
        
        # Add some realistic variance
        variance = random.uniform(0.85, 1.15)
        final_cost = int(adjusted_cost * variance)
        
        return {
            'total_cost': final_cost,
            'breakdown': {
                'development': int(final_cost * 0.6),
                'design': int(final_cost * 0.15),
                'testing': int(final_cost * 0.1),
                'deployment': int(final_cost * 0.05),
                'project_management': int(final_cost * 0.1)
            },
            'timeline_months': project_data['timeline'],
            'complexity': project_data['complexity']
        }
    
    def calculate_roi_projection(self, investment, industry, project_type, timeline_months):
        """Calculate ROI projections with realistic scenarios"""
        
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
        
        # Base ROI calculation
        base_roi = project_data['roi_potential']
        growth_rate = industry_data['growth_rate']
        
        # Calculate projections for different scenarios
        scenarios = {
            'conservative': {
                'multiplier': 0.7,
                'probability': 0.8,
                'description': 'Conservative estimate with market challenges'
            },
            'realistic': {
                'multiplier': 1.0,
                'probability': 0.6,
                'description': 'Most likely scenario based on market data'
            },
            'optimistic': {
                'multiplier': 1.4,
                'probability': 0.3,
                'description': 'Best case with optimal market conditions'
            }
        }
        
        projections = {}
        for scenario, data in scenarios.items():
            roi_multiplier = base_roi * data['multiplier']
            annual_return = investment * roi_multiplier * growth_rate
            
            projections[scenario] = {
                'annual_return': int(annual_return),
                'total_roi': int(annual_return * 3),  # 3-year projection
                'roi_percentage': int((roi_multiplier - 1) * 100),
                'break_even_months': max(6, int(timeline_months / roi_multiplier)),
                'probability': data['probability'],
                'description': data['description']
            }
        
        return projections
    
    def get_market_insights(self, industry):
        """Get market insights for the selected industry"""
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        
        insights = {
            'market_size': industry_data['market_size'],
            'growth_rate': f"{industry_data['growth_rate']*100:.0f}%",
            'risk_level': 'Low' if industry_data['risk_factor'] < 0.1 else 'Medium' if industry_data['risk_factor'] < 0.2 else 'High',
            'trends': self._get_industry_trends(industry),
            'opportunities': self._get_industry_opportunities(industry)
        }
        
        return insights
    
    def _get_industry_trends(self, industry):
        trends = {
            'fintech': ['Digital payments growth', 'Blockchain adoption', 'RegTech expansion'],
            'healthtech': ['Telemedicine boom', 'AI diagnostics', 'Wearable health devices'],
            'edtech': ['Remote learning', 'Personalized education', 'VR/AR in education'],
            'ecommerce': ['Mobile commerce', 'Social selling', 'Same-day delivery'],
            'saas': ['AI-powered tools', 'Industry-specific solutions', 'Integration platforms'],
            'gaming': ['Mobile gaming', 'Cloud gaming', 'NFT integration'],
            'realEstate': ['PropTech solutions', 'Virtual tours', 'Smart buildings'],
            'foodBeverage': ['Food delivery apps', 'Sustainable packaging', 'Ghost kitchens'],
            'manufacturing': ['Industry 4.0', 'IoT integration', 'Sustainable manufacturing'],
            'logistics': ['Last-mile delivery', 'Drone delivery', 'Supply chain optimization']
        }
        return trends.get(industry, ['Market digitization', 'Customer experience focus', 'Operational efficiency'])
    
    def _get_industry_opportunities(self, industry):
        opportunities = {
            'fintech': ['Emerging markets', 'SME banking', 'Crypto services'],
            'healthtech': ['Remote monitoring', 'Mental health apps', 'Elderly care tech'],
            'edtech': ['Corporate training', 'Skill development', 'Language learning'],
            'ecommerce': ['B2B marketplaces', 'Subscription models', 'International expansion'],
            'saas': ['Vertical solutions', 'API economy', 'No-code platforms'],
            'gaming': ['Esports platforms', 'Educational games', 'Fitness gaming'],
            'realEstate': ['Smart home tech', 'Co-living spaces', 'Real estate investment'],
            'foodBeverage': ['Plant-based alternatives', 'Meal kits', 'Food waste reduction'],
            'manufacturing': ['3D printing', 'Robotics', 'Green manufacturing'],
            'logistics': ['Cold chain logistics', 'Reverse logistics', 'Cross-border shipping']
        }
        return opportunities.get(industry, ['Digital innovation', 'Market expansion', 'Efficiency improvements'])

# Initialize calculator
calculator = ROICalculator()

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate_roi():
    """Calculate ROI based on user input"""
    try:
        data = request.json
        
        company_name = data.get('company_name', 'Your Company')
        company_size = data.get('company_size', 'small')
        current_industry = data.get('current_industry', 'saas')
        project_type = data.get('project_type', 'product_development')
        target_industry = data.get('target_industry', current_industry)
        budget_range = data.get('budget_range', 'medium')
        
        # Calculate project costs
        cost_analysis = calculator.calculate_project_cost(
            company_size, project_type, target_industry
        )
        
        # Calculate ROI projections
        roi_projections = calculator.calculate_roi_projection(
            cost_analysis['total_cost'], 
            target_industry, 
            project_type, 
            cost_analysis['timeline_months']
        )
        
        # Get market insights
        market_insights = calculator.get_market_insights(target_industry)
        
        # Compile response
        response = {
            'company_name': company_name,
            'project_summary': {
                'type': PROJECT_TYPES[project_type]['description'],
                'industry': target_industry.replace('_', ' ').title(),
                'timeline': f"{cost_analysis['timeline_months']} months",
                'complexity': cost_analysis['complexity']
            },
            'cost_analysis': cost_analysis,
            'roi_projections': roi_projections,
            'market_insights': market_insights,
            'recommendations': calculator._get_recommendations(company_size, project_type, target_industry),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/industries')
def get_industries():
    """Get available industries"""
    industries = []
    for key, value in INDUSTRIES.items():
        industries.append({
            'id': key,
            'name': key.replace('_', ' ').title(),
            'growth_rate': f"{value['growth_rate']*100:.0f}%",
            'market_size': value['market_size']
        })
    return jsonify(industries)

@app.route('/api/projects')
def get_projects():
    """Get available project types"""
    projects = []
    for key, value in PROJECT_TYPES.items():
        projects.append({
            'id': key,
            'name': value['description'],
            'complexity': value['complexity'],
            'timeline': f"{value['timeline']} months"
        })
    return jsonify(projects)

# Add recommendations method to calculator
def _get_recommendations(self, company_size, project_type, industry):
    """Generate personalized recommendations"""
    recommendations = []
    
    if company_size == 'startup':
        recommendations.append("Consider MVP approach to minimize initial investment")
        recommendations.append("Focus on core features first, expand later")
    elif company_size == 'enterprise':
        recommendations.append("Leverage existing infrastructure for cost savings")
        recommendations.append("Consider phased rollout across departments")
    
    if industry in ['fintech', 'healthtech']:
        recommendations.append("Budget extra for compliance and security requirements")
    
    if project_type == 'ai_integration':
        recommendations.append("Start with pilot program to validate AI use cases")
        recommendations.append("Ensure data quality before implementation")
    
    return recommendations

# Bind the method to the calculator instance
calculator._get_recommendations = _get_recommendations.__get__(calculator, ROICalculator)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)