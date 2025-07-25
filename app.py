#!/usr/bin/env python3
"""
Business ROI Calculator - Simplified Mobile Version
Advanced web application with multi-currency and HTML reports
"""

from flask import Flask, render_template, request, jsonify
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Enhanced business data and calculations
COMPANY_SIZES = {
    'startup': {'multiplier': 0.7, 'min_budget': 5000, 'max_budget': 100000, 'risk_factor': 0.3},
    'small': {'multiplier': 1.0, 'min_budget': 25000, 'max_budget': 500000, 'risk_factor': 0.2},
    'medium': {'multiplier': 1.5, 'min_budget': 100000, 'max_budget': 2000000, 'risk_factor': 0.15},
    'enterprise': {'multiplier': 2.5, 'min_budget': 500000, 'max_budget': 10000000, 'risk_factor': 0.1}
}

INDUSTRIES = {
    'fintech': {'growth_rate': 0.25, 'risk_factor': 0.15, 'market_size': 'Large', 'volatility': 0.2},
    'healthtech': {'growth_rate': 0.30, 'risk_factor': 0.20, 'market_size': 'Huge', 'volatility': 0.15},
    'edtech': {'growth_rate': 0.22, 'risk_factor': 0.12, 'market_size': 'Large', 'volatility': 0.18},
    'ecommerce': {'growth_rate': 0.18, 'risk_factor': 0.08, 'market_size': 'Massive', 'volatility': 0.12},
    'saas': {'growth_rate': 0.35, 'risk_factor': 0.18, 'market_size': 'Large', 'volatility': 0.22},
    'gaming': {'growth_rate': 0.20, 'risk_factor': 0.25, 'market_size': 'Medium', 'volatility': 0.3},
    'realEstate': {'growth_rate': 0.15, 'risk_factor': 0.10, 'market_size': 'Stable', 'volatility': 0.08},
    'foodBeverage': {'growth_rate': 0.12, 'risk_factor': 0.15, 'market_size': 'Medium', 'volatility': 0.1},
    'manufacturing': {'growth_rate': 0.10, 'risk_factor': 0.08, 'market_size': 'Large', 'volatility': 0.06},
    'logistics': {'growth_rate': 0.16, 'risk_factor': 0.12, 'market_size': 'Large', 'volatility': 0.14},
    'crypto': {'growth_rate': 0.45, 'risk_factor': 0.40, 'market_size': 'Volatile', 'volatility': 0.5},
    'nft': {'growth_rate': 0.35, 'risk_factor': 0.45, 'market_size': 'Emerging', 'volatility': 0.6},
    'web3': {'growth_rate': 0.40, 'risk_factor': 0.35, 'market_size': 'Growing', 'volatility': 0.4},
    'sustainability': {'growth_rate': 0.28, 'risk_factor': 0.18, 'market_size': 'Expanding', 'volatility': 0.16},
    'biotech': {'growth_rate': 0.32, 'risk_factor': 0.25, 'market_size': 'Specialized', 'volatility': 0.28}
}

# Enhanced project types
PROJECT_TYPES = {
    'product_development': {
        'base_cost': 150000, 'timeline': 12, 'roi_potential': 2.5,
        'description': 'New Product Development', 'complexity': 'High', 'risk_level': 0.2
    },
    'digital_transformation': {
        'base_cost': 200000, 'timeline': 18, 'roi_potential': 3.0,
        'description': 'Digital Transformation', 'complexity': 'Very High', 'risk_level': 0.15
    },
    'market_expansion': {
        'base_cost': 100000, 'timeline': 8, 'roi_potential': 2.0,
        'description': 'Market Expansion', 'complexity': 'Medium', 'risk_level': 0.18
    },
    'tech_upgrade': {
        'base_cost': 80000, 'timeline': 6, 'roi_potential': 1.8,
        'description': 'Technology Upgrade', 'complexity': 'Medium', 'risk_level': 0.12
    },
    'marketing_campaign': {
        'base_cost': 50000, 'timeline': 4, 'roi_potential': 1.5,
        'description': 'Marketing Campaign', 'complexity': 'Low', 'risk_level': 0.15
    },
    'ecommerce_platform': {
        'base_cost': 120000, 'timeline': 10, 'roi_potential': 2.2,
        'description': 'E-commerce Platform', 'complexity': 'High', 'risk_level': 0.16
    },
    'mobile_app': {
        'base_cost': 90000, 'timeline': 8, 'roi_potential': 2.0,
        'description': 'Mobile Application', 'complexity': 'High', 'risk_level': 0.18
    },
    'ai_integration': {
        'base_cost': 180000, 'timeline': 14, 'roi_potential': 2.8,
        'description': 'AI Integration', 'complexity': 'Very High', 'risk_level': 0.22
    },
    'blockchain_platform': {
        'base_cost': 250000, 'timeline': 16, 'roi_potential': 3.5,
        'description': 'Blockchain Platform', 'complexity': 'Very High', 'risk_level': 0.35
    },
    'iot_solution': {
        'base_cost': 160000, 'timeline': 12, 'roi_potential': 2.3,
        'description': 'IoT Solution', 'complexity': 'High', 'risk_level': 0.20
    },
    'data_analytics': {
        'base_cost': 140000, 'timeline': 10, 'roi_potential': 2.4,
        'description': 'Data Analytics Platform', 'complexity': 'High', 'risk_level': 0.17
    },
    'subscription_service': {
        'base_cost': 75000, 'timeline': 6, 'roi_potential': 2.1,
        'description': 'Subscription Service', 'complexity': 'Medium', 'risk_level': 0.14
    },
    'automation_system': {
        'base_cost': 110000, 'timeline': 9, 'roi_potential': 2.6,
        'description': 'Automation System', 'complexity': 'High', 'risk_level': 0.13
    },
    'cybersecurity_upgrade': {
        'base_cost': 95000, 'timeline': 7, 'roi_potential': 1.9,
        'description': 'Cybersecurity Upgrade', 'complexity': 'Medium', 'risk_level': 0.08
    },
    'cloud_migration': {
        'base_cost': 130000, 'timeline': 11, 'roi_potential': 2.2,
        'description': 'Cloud Migration', 'complexity': 'High', 'risk_level': 0.11
    }
}

# Currency exchange rates (simplified - in production, use real-time API)
CURRENCIES = {
    'USD': {'symbol': '$', 'rate': 1.0, 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'rate': 0.85, 'name': 'Euro'},
    'GBP': {'symbol': '£', 'rate': 0.73, 'name': 'British Pound'},
    'JPY': {'symbol': '¥', 'rate': 110.0, 'name': 'Japanese Yen'},
    'CAD': {'symbol': 'C$', 'rate': 1.25, 'name': 'Canadian Dollar'},
    'AUD': {'symbol': 'A$', 'rate': 1.35, 'name': 'Australian Dollar'},
    'CHF': {'symbol': 'CHF', 'rate': 0.92, 'name': 'Swiss Franc'},
    'CNY': {'symbol': '¥', 'rate': 6.45, 'name': 'Chinese Yuan'},
    'INR': {'symbol': '₹', 'rate': 74.5, 'name': 'Indian Rupee'},
    'BRL': {'symbol': 'R$', 'rate': 5.2, 'name': 'Brazilian Real'}
}

class EnhancedROICalculator:
    def __init__(self):
        pass
    
    def convert_currency(self, amount, from_currency, to_currency):
        """Convert amount between currencies"""
        if from_currency == to_currency:
            return amount
        
        # Convert to USD first, then to target currency
        usd_amount = amount / CURRENCIES[from_currency]['rate']
        converted_amount = usd_amount * CURRENCIES[to_currency]['rate']
        
        return converted_amount
    
    def calculate_risk_assessment(self, company_size, project_type, industry):
        """Calculate comprehensive risk assessment"""
        size_data = COMPANY_SIZES.get(company_size, COMPANY_SIZES['small'])
        project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        
        # Base risk factors
        company_risk = size_data['risk_factor']
        project_risk = project_data['risk_level']
        industry_risk = industry_data['risk_factor']
        market_volatility = industry_data['volatility']
        
        # Calculate composite risk score
        overall_risk = (company_risk * 0.3 + project_risk * 0.4 + industry_risk * 0.2 + market_volatility * 0.1)
        
        # Risk categories
        if overall_risk <= 0.15:
            risk_category = 'Low'
            risk_color = '#00ff88'
        elif overall_risk <= 0.25:
            risk_category = 'Medium'
            risk_color = '#ffaa00'
        else:
            risk_category = 'High'
            risk_color = '#ff4757'
        
        return {
            'overall_risk': round(overall_risk, 3),
            'risk_category': risk_category,
            'risk_color': risk_color,
            'risk_factors': {
                'company_size_risk': round(company_risk, 3),
                'project_complexity_risk': round(project_risk, 3),
                'industry_risk': round(industry_risk, 3),
                'market_volatility': round(market_volatility, 3)
            },
            'risk_mitigation': self._get_risk_mitigation_strategies(overall_risk, project_type, industry)
        }
    
    def _get_risk_mitigation_strategies(self, risk_level, project_type, industry):
        """Get risk mitigation strategies"""
        strategies = []
        
        if risk_level > 0.25:
            strategies.append("Consider phased implementation to reduce upfront investment")
            strategies.append("Establish clear success metrics and exit criteria")
            strategies.append("Allocate 20-30% contingency budget")
        
        if project_type in ['blockchain_platform', 'ai_integration', 'crypto']:
            strategies.append("Invest in specialized expertise and training")
            strategies.append("Stay updated with regulatory changes")
        
        if industry in ['crypto', 'nft', 'gaming']:
            strategies.append("Diversify market exposure")
            strategies.append("Monitor market trends closely")
        
        strategies.append("Regular progress reviews and milestone assessments")
        strategies.append("Maintain flexible project scope and timeline")
        
        return strategies
    
    def calculate_project_cost(self, company_size, project_type, industry, currency='USD', custom_requirements=None):
        """Enhanced cost calculation with currency support"""
        
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
        final_cost_usd = int(adjusted_cost * variance)
        
        # Convert to requested currency
        final_cost = self.convert_currency(final_cost_usd, 'USD', currency)
        
        return {
            'total_cost': int(final_cost),
            'total_cost_usd': final_cost_usd,
            'currency': currency,
            'currency_symbol': CURRENCIES[currency]['symbol'],
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
    
    def calculate_roi_projection(self, investment, industry, project_type, timeline_months, currency='USD'):
        """Enhanced ROI projections with risk-adjusted scenarios"""
        
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
        
        # Base ROI calculation
        base_roi = project_data['roi_potential']
        growth_rate = industry_data['growth_rate']
        volatility = industry_data['volatility']
        
        # Enhanced scenarios with risk adjustment
        scenarios = {
            'pessimistic': {
                'multiplier': 0.6 - (volatility * 0.2),
                'probability': 0.2,
                'description': 'Worst case with significant market challenges'
            },
            'conservative': {
                'multiplier': 0.8 - (volatility * 0.1),
                'probability': 0.3,
                'description': 'Conservative estimate with market challenges'
            },
            'realistic': {
                'multiplier': 1.0,
                'probability': 0.4,
                'description': 'Most likely scenario based on market data'
            },
            'optimistic': {
                'multiplier': 1.3 + (growth_rate * 0.2),
                'probability': 0.1,
                'description': 'Best case with optimal market conditions'
            }
        }
        
        projections = {}
        investment_usd = investment if currency == 'USD' else self.convert_currency(investment, currency, 'USD')
        
        for scenario, data in scenarios.items():
            roi_multiplier = max(0.1, base_roi * data['multiplier'])  # Ensure positive ROI
            annual_return_usd = investment_usd * roi_multiplier * growth_rate
            
            # Convert back to requested currency
            annual_return = self.convert_currency(annual_return_usd, 'USD', currency)
            total_roi = annual_return * 3  # 3-year projection
            
            projections[scenario] = {
                'annual_return': int(annual_return),
                'total_roi': int(total_roi),
                'roi_percentage': int((roi_multiplier - 1) * 100),
                'break_even_months': max(3, int(timeline_months / roi_multiplier)),
                'probability': data['probability'],
                'description': data['description'],
                'net_present_value': int(total_roi - investment)
            }
        
        return projections
    
    def get_market_insights(self, industry):
        """Enhanced market insights"""
        industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
        
        insights = {
            'market_size': industry_data['market_size'],
            'growth_rate': f"{industry_data['growth_rate']*100:.0f}%",
            'risk_level': 'Low' if industry_data['risk_factor'] < 0.1 else 'Medium' if industry_data['risk_factor'] < 0.2 else 'High',
            'volatility': f"{industry_data['volatility']*100:.0f}%",
            'trends': self._get_industry_trends(industry),
            'opportunities': self._get_industry_opportunities(industry),
            'challenges': self._get_industry_challenges(industry)
        }
        
        return insights
    
    def _get_industry_trends(self, industry):
        trends = {
            'fintech': ['Digital payments growth', 'Blockchain adoption', 'RegTech expansion', 'Open banking APIs'],
            'healthtech': ['Telemedicine boom', 'AI diagnostics', 'Wearable health devices', 'Personalized medicine'],
            'edtech': ['Remote learning', 'Personalized education', 'VR/AR in education', 'Microlearning platforms'],
            'ecommerce': ['Mobile commerce', 'Social selling', 'Same-day delivery', 'Voice commerce'],
            'saas': ['AI-powered tools', 'Industry-specific solutions', 'Integration platforms', 'No-code/low-code'],
            'gaming': ['Mobile gaming', 'Cloud gaming', 'NFT integration', 'Metaverse development'],
            'crypto': ['DeFi protocols', 'NFT marketplaces', 'Layer 2 solutions', 'Central bank digital currencies'],
            'web3': ['Decentralized apps', 'DAOs', 'Metaverse platforms', 'Blockchain interoperability'],
            'sustainability': ['Carbon tracking', 'Renewable energy tech', 'Circular economy', 'ESG reporting']
        }
        return trends.get(industry, ['Market digitization', 'Customer experience focus', 'Operational efficiency'])
    
    def _get_industry_opportunities(self, industry):
        opportunities = {
            'fintech': ['Emerging markets', 'SME banking', 'Crypto services', 'Embedded finance'],
            'healthtech': ['Remote monitoring', 'Mental health apps', 'Elderly care tech', 'Precision medicine'],
            'crypto': ['Institutional adoption', 'DeFi yield farming', 'NFT utilities', 'Cross-chain bridges'],
            'web3': ['Creator economy', 'Decentralized identity', 'Web3 gaming', 'Social tokens']
        }
        return opportunities.get(industry, ['Digital innovation', 'Market expansion', 'Efficiency improvements'])
    
    def _get_industry_challenges(self, industry):
        challenges = {
            'fintech': ['Regulatory compliance', 'Security concerns', 'Competition from big tech'],
            'crypto': ['Regulatory uncertainty', 'Market volatility', 'Scalability issues'],
            'web3': ['User adoption', 'Technical complexity', 'Environmental concerns'],
            'gaming': ['Market saturation', 'Platform dependencies', 'User acquisition costs']
        }
        return challenges.get(industry, ['Market competition', 'Technology changes', 'Economic uncertainty'])

# Initialize calculator
calculator = EnhancedROICalculator()

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html', currencies=CURRENCIES)

@app.route('/api/calculate', methods=['POST'])
def calculate_roi():
    """Enhanced ROI calculation API"""
    try:
        data = request.json
        
        company_name = data.get('company_name', 'Your Company')
        company_size = data.get('company_size', 'small')
        current_industry = data.get('current_industry', 'saas')
        project_type = data.get('project_type', 'product_development')
        target_industry = data.get('target_industry', current_industry)
        currency = data.get('currency', 'USD')
        
        # Calculate project costs
        cost_analysis = calculator.calculate_project_cost(
            company_size, project_type, target_industry, currency
        )
        
        # Calculate ROI projections
        roi_projections = calculator.calculate_roi_projection(
            cost_analysis['total_cost'], 
            target_industry, 
            project_type, 
            cost_analysis['timeline_months'],
            currency
        )
        
        # Get market insights
        market_insights = calculator.get_market_insights(target_industry)
        
        # Calculate risk assessment
        risk_assessment = calculator.calculate_risk_assessment(
            company_size, project_type, target_industry
        )
        
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
            'risk_assessment': risk_assessment,
            'recommendations': calculator._get_recommendations(company_size, project_type, target_industry),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/currencies')
def get_currencies():
    """Get available currencies"""
    return jsonify(CURRENCIES)

@app.route('/api/industries')
def get_industries():
    """Get available industries"""
    industries = []
    for key, value in INDUSTRIES.items():
        industries.append({
            'id': key,
            'name': key.replace('_', ' ').title(),
            'growth_rate': f"{value['growth_rate']*100:.0f}%",
            'market_size': value['market_size'],
            'risk_level': 'Low' if value['risk_factor'] < 0.1 else 'Medium' if value['risk_factor'] < 0.2 else 'High'
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
            'timeline': f"{value['timeline']} months",
            'base_cost': f"${value['base_cost']:,}"
        })
    return jsonify(projects)

@app.route('/api/export-html')
def export_html_report():
    """Generate HTML report for current calculation"""
    try:
        # Get calculation parameters from URL
        company_name = request.args.get('company', 'Sample Company')
        company_size = request.args.get('company_size', 'medium')
        current_industry = request.args.get('current_industry', 'saas')
        project_type = request.args.get('project_type', 'product_development')
        target_industry = request.args.get('target_industry', 'saas')
        currency = request.args.get('currency', 'USD')
        
        # Perform actual calculations
        cost_analysis = calculator.calculate_project_cost(
            company_size, project_type, target_industry, currency
        )
        
        roi_projections = calculator.calculate_roi_projection(
            cost_analysis['total_cost'], 
            target_industry, 
            project_type, 
            cost_analysis['timeline_months'],
            currency
        )
        
        market_insights = calculator.get_market_insights(target_industry)
        risk_assessment = calculator.calculate_risk_assessment(company_size, project_type, target_industry)
        recommendations = calculator._get_recommendations(company_size, project_type, target_industry)
        
        # Generate HTML report with actual data
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Business ROI Analysis Report - {company_name}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f8f9fa; }}
                .container {{ background: white; padding: 40px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); max-width: 1000px; margin: 0 auto; }}
                h1 {{ color: #667eea; text-align: center; font-size: 2.5rem; margin-bottom: 2rem; }}
                h2 {{ color: #4a5568; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem; margin-top: 2rem; }}
                .header-info {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
                .section {{ margin: 30px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
                th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
                th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: 600; }}
                tr:nth-child(even) {{ background-color: #f7fafc; }}
                .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
                .metric {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                .metric-value {{ font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem; }}
                .metric-label {{ font-size: 0.9rem; opacity: 0.9; }}
                .risk-{risk_assessment['risk_category'].lower()} {{ 
                    color: {risk_assessment['risk_color']}; 
                    font-weight: bold; 
                    padding: 5px 15px; 
                    border-radius: 20px; 
                    background: rgba(255,255,255,0.1); 
                    display: inline-block; 
                }}
                .recommendations {{ background: #e6fffa; padding: 20px; border-radius: 10px; border-left: 4px solid #38b2ac; }}
                .recommendations ul {{ margin: 0; padding-left: 20px; }}
                .recommendations li {{ margin: 10px 0; line-height: 1.6; }}
                .footer {{ text-align: center; margin-top: 40px; padding: 20px; background: #f7fafc; border-radius: 10px; }}
                @media print {{ body {{ margin: 0; }} .container {{ box-shadow: none; }} }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Business ROI Analysis Report</h1>
                
                <div class="header-info">
                    <h2 style="color: white; border: none; margin: 0;">Project Overview</h2>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 15px;">
                        <div><strong>Company:</strong> {company_name}</div>
                        <div><strong>Project:</strong> {PROJECT_TYPES[project_type]['description']}</div>
                        <div><strong>Industry:</strong> {target_industry.replace('_', ' ').title()}</div>
                        <div><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                        <div><strong>Currency:</strong> {CURRENCIES[currency]['symbol']} {currency}</div>
                        <div><strong>Timeline:</strong> {cost_analysis['timeline_months']} months</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>💰 Cost Analysis</h2>
                    <div class="metric-grid">
                        <div class="metric">
                            <div class="metric-value">{CURRENCIES[currency]['symbol']}{cost_analysis['total_cost']:,}</div>
                            <div class="metric-label">Total Project Cost</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{cost_analysis['timeline_months']}</div>
                            <div class="metric-label">Months Timeline</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{cost_analysis['complexity']}</div>
                            <div class="metric-label">Complexity Level</div>
                        </div>
                    </div>
                    
                    <table>
                        <tr><th>Cost Component</th><th>Amount</th><th>Percentage</th></tr>
                        <tr><td>Development</td><td>{CURRENCIES[currency]['symbol']}{cost_analysis['breakdown']['development']:,}</td><td>60%</td></tr>
                        <tr><td>Design</td><td>{CURRENCIES[currency]['symbol']}{cost_analysis['breakdown']['design']:,}</td><td>15%</td></tr>
                        <tr><td>Testing & QA</td><td>{CURRENCIES[currency]['symbol']}{cost_analysis['breakdown']['testing']:,}</td><td>10%</td></tr>
                        <tr><td>Deployment</td><td>{CURRENCIES[currency]['symbol']}{cost_analysis['breakdown']['deployment']:,}</td><td>5%</td></tr>
                        <tr><td>Project Management</td><td>{CURRENCIES[currency]['symbol']}{cost_analysis['breakdown']['project_management']:,}</td><td>10%</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>📈 ROI Projections (3-Year Outlook)</h2>
                    <table>
                        <tr><th>Scenario</th><th>ROI %</th><th>Annual Return</th><th>Total 3-Year ROI</th><th>Break-even</th><th>Probability</th></tr>
        """
        
        for scenario, data in roi_projections.items():
            html_report += f"""
                        <tr>
                            <td><strong>{scenario.title()}</strong><br><small>{data['description']}</small></td>
                            <td><strong>{data['roi_percentage']}%</strong></td>
                            <td>{CURRENCIES[currency]['symbol']}{data['annual_return']:,}</td>
                            <td>{CURRENCIES[currency]['symbol']}{data['total_roi']:,}</td>
                            <td>{data['break_even_months']} months</td>
                            <td>{int(data['probability'] * 100)}%</td>
                        </tr>
            """
        
        html_report += f"""
                    </table>
                </div>
                
                <div class="section">
                    <h2>⚖️ Risk Assessment</h2>
                    <p>Overall Risk Level: <span class="risk-{risk_assessment['risk_category'].lower()}">{risk_assessment['risk_category']}</span></p>
                    <p><strong>Risk Score:</strong> {risk_assessment['overall_risk']:.3f} out of 1.0</p>
                    
                    <div class="metric-grid">
                        <div class="metric">
                            <div class="metric-value">{risk_assessment['risk_factors']['company_size_risk']:.1%}</div>
                            <div class="metric-label">Company Size Risk</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{risk_assessment['risk_factors']['project_complexity_risk']:.1%}</div>
                            <div class="metric-label">Project Complexity</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{risk_assessment['risk_factors']['industry_risk']:.1%}</div>
                            <div class="metric-label">Industry Risk</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{risk_assessment['risk_factors']['market_volatility']:.1%}</div>
                            <div class="metric-label">Market Volatility</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🌍 Market Insights</h2>
                    <table>
                        <tr><th>Market Factor</th><th>Value</th></tr>
                        <tr><td>Market Size</td><td>{market_insights['market_size']}</td></tr>
                        <tr><td>Growth Rate</td><td>{market_insights['growth_rate']}</td></tr>
                        <tr><td>Risk Level</td><td>{market_insights['risk_level']}</td></tr>
                        <tr><td>Volatility</td><td>{market_insights['volatility']}</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>💡 Strategic Recommendations</h2>
                    <div class="recommendations">
                        <ul>
        """
        
        for rec in recommendations:
            html_report += f"<li>{rec}</li>"
        
        html_report += f"""
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p><strong>📄 Professional Business ROI Analysis</strong></p>
                    <p>Generated by Enhanced ROI Calculator • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><small>💡 Tip: Use Ctrl+P (Cmd+P on Mac) to save this report as a PDF</small></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_report, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add recommendations method to calculator
def _get_recommendations(self, company_size, project_type, industry):
    """Generate enhanced personalized recommendations"""
    recommendations = []
    
    if company_size == 'startup':
        recommendations.append("Consider MVP approach to minimize initial investment")
        recommendations.append("Focus on core features first, expand later")
        recommendations.append("Seek angel investors or venture capital for funding")
    elif company_size == 'enterprise':
        recommendations.append("Leverage existing infrastructure for cost savings")
        recommendations.append("Consider phased rollout across departments")
        recommendations.append("Implement comprehensive change management")
    
    if industry in ['fintech', 'healthtech']:
        recommendations.append("Budget extra for compliance and security requirements")
        recommendations.append("Engage with regulatory bodies early in the process")
    
    if industry in ['crypto', 'nft', 'web3']:
        recommendations.append("Stay updated with rapidly changing regulations")
        recommendations.append("Consider market volatility in financial planning")
        recommendations.append("Build strong community engagement strategies")
    
    if project_type == 'ai_integration':
        recommendations.append("Start with pilot program to validate AI use cases")
        recommendations.append("Ensure data quality before implementation")
        recommendations.append("Invest in AI ethics and bias mitigation")
    
    if project_type == 'blockchain_platform':
        recommendations.append("Choose the right blockchain network for your needs")
        recommendations.append("Plan for scalability from the beginning")
        recommendations.append("Consider environmental impact and sustainability")
    
    recommendations.append("Establish clear KPIs and success metrics")
    recommendations.append("Plan for ongoing maintenance and updates")
    
    return recommendations

# Bind the method to the calculator instance
calculator._get_recommendations = _get_recommendations.__get__(calculator, EnhancedROICalculator)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)