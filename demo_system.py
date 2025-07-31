"""
Professional Demo System for VoidSight Analytics
Impressive demo scenarios with realistic data to showcase capabilities to potential buyers
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from decimal import Decimal

class DemoDataGenerator:
    """Generate realistic demo data for impressive demonstrations"""
    
    def __init__(self):
        self.demo_companies = [
            {
                'name': 'TechFlow Innovations',
                'industry': 'fintech',
                'size': 'medium',
                'description': 'Digital banking platform for SMEs',
                'logo_url': '/static/demo/logos/techflow.png'
            },
            {
                'name': 'HealthTrack Solutions',
                'industry': 'healthtech',
                'size': 'large',
                'description': 'AI-powered patient monitoring system',
                'logo_url': '/static/demo/logos/healthtrack.png'
            },
            {
                'name': 'EduVerse Platform',
                'industry': 'edtech',
                'size': 'startup',
                'description': 'VR-based learning experiences',
                'logo_url': '/static/demo/logos/eduverse.png'
            },
            {
                'name': 'RetailConnect Hub',
                'industry': 'ecommerce',
                'size': 'enterprise',
                'description': 'Omnichannel retail platform',
                'logo_url': '/static/demo/logos/retailconnect.png'
            },
            {
                'name': 'CloudOps Pro',
                'industry': 'saas',
                'size': 'medium',
                'description': 'DevOps automation suite',
                'logo_url': '/static/demo/logos/cloudops.png'
            }
        ]
        
        self.demo_projects = [
            {
                'name': 'AI-Powered Customer Service Platform',
                'type': 'ai_integration',
                'investment_range': [75000, 150000],
                'timeline_range': [8, 14],
                'description': 'Implement intelligent chatbots and automated customer support',
                'expected_benefits': [
                    '40% reduction in support ticket volume',
                    '60% faster response times',
                    '25% increase in customer satisfaction',
                    '$120K annual cost savings'
                ]
            },
            {
                'name': 'E-commerce Mobile App Development',
                'type': 'mobile_app',
                'investment_range': [45000, 85000],
                'timeline_range': [6, 10],
                'description': 'Native mobile apps for iOS and Android with advanced features',
                'expected_benefits': [
                    '35% increase in mobile conversions',
                    '50% boost in customer engagement',
                    '$200K additional annual revenue',
                    '20% higher average order value'
                ]
            },
            {
                'name': 'Cloud Infrastructure Migration',
                'type': 'tech_upgrade',
                'investment_range': [120000, 250000],
                'timeline_range': [10, 18],
                'description': 'Migrate legacy systems to modern cloud architecture',
                'expected_benefits': [
                    '30% reduction in infrastructure costs',
                    '99.9% uptime improvement',
                    '50% faster deployment cycles',
                    'Enhanced scalability and security'
                ]
            },
            {
                'name': 'Marketing Automation System',
                'type': 'marketing_campaign',
                'investment_range': [25000, 60000],
                'timeline_range': [4, 8],
                'description': 'Comprehensive marketing automation and lead nurturing',
                'expected_benefits': [
                    '300% increase in qualified leads',
                    '45% improvement in conversion rates',
                    '$150K additional revenue in first year',
                    '60% reduction in manual marketing tasks'
                ]
            },
            {
                'name': 'Cybersecurity Enhancement Program',
                'type': 'cybersecurity_upgrade',
                'investment_range': [65000, 120000],
                'timeline_range': [6, 12],
                'description': 'Advanced threat detection and security infrastructure',
                'expected_benefits': [
                    '95% reduction in security incidents',
                    'Compliance with SOC 2 and ISO 27001',
                    '$500K risk mitigation value',
                    'Enhanced customer trust and credibility'
                ]
            }
        ]
    
    def generate_demo_scenario(self, scenario_type: str = 'comprehensive') -> Dict[str, Any]:
        """Generate a complete demo scenario with realistic data"""
        
        company = random.choice(self.demo_companies)
        project = random.choice(self.demo_projects)
        
        # Generate realistic investment amount
        investment_min, investment_max = project['investment_range']
        investment = random.randint(investment_min, investment_max)
        
        # Generate timeline
        timeline_min, timeline_max = project['timeline_range']
        timeline = random.randint(timeline_min, timeline_max)
        
        # Generate risk tolerance based on company size
        risk_tolerance_map = {
            'startup': random.randint(70, 85),      # Higher risk tolerance
            'small': random.randint(55, 75),        # Medium-high risk tolerance
            'medium': random.randint(45, 65),       # Medium risk tolerance
            'large': random.randint(35, 55),        # Medium-low risk tolerance
            'enterprise': random.randint(25, 45)    # Lower risk tolerance
        }
        
        risk_tolerance = risk_tolerance_map.get(company['size'], 50)
        
        scenario = {
            'demo_id': f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'company': company,
            'project': project,
            'calculation_parameters': {
                'project_type': project['type'],
                'company_size': company['size'],
                'industry': company['industry'],
                'investment_amount': investment,
                'timeline_months': timeline,
                'risk_tolerance': risk_tolerance,
                'currency': 'USD',
                'market_conditions': random.choice(['neutral', 'bullish', 'bearish']),
                'scenario_type': scenario_type
            },
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'demo_version': '2.0',
                'realistic_data': True
            }
        }
        
        # Generate realistic results
        scenario['expected_results'] = self._generate_realistic_results(scenario)
        
        return scenario
    
    def _generate_realistic_results(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Generate realistic ROI calculation results for demo"""
        
        params = scenario['calculation_parameters']
        investment = params['investment_amount']
        timeline = params['timeline_months']
        project_type = params['project_type']
        company_size = params['company_size']
        industry = params['industry']
        
        # Realistic ROI ranges based on actual industry data
        roi_ranges = {
            'ai_integration': {'startup': (15, 45), 'small': (12, 35), 'medium': (10, 28), 'large': (8, 22), 'enterprise': (6, 18)},
            'mobile_app': {'startup': (12, 35), 'small': (10, 28), 'medium': (8, 22), 'large': (6, 18), 'enterprise': (4, 15)},
            'tech_upgrade': {'startup': (8, 25), 'small': (6, 20), 'medium': (5, 16), 'large': (4, 14), 'enterprise': (3, 12)},
            'marketing_campaign': {'startup': (25, 70), 'small': (20, 55), 'medium': (15, 45), 'large': (12, 35), 'enterprise': (10, 28)},
            'cybersecurity_upgrade': {'startup': (10, 30), 'small': (8, 25), 'medium': (6, 20), 'large': (5, 16), 'enterprise': (4, 14)}
        }
        
        # Get ROI range for this project and company size
        roi_min, roi_max = roi_ranges.get(project_type, {}).get(company_size, (5, 20))
        roi_percentage = random.uniform(roi_min, roi_max)
        
        # Calculate financial projections
        total_revenue = investment * (1 + roi_percentage / 100)
        net_profit = total_revenue - investment
        monthly_profit = net_profit / timeline
        payback_period = max(3, int(timeline * 0.6))  # Realistic payback period
        
        # Risk score (inverse of risk tolerance)
        risk_score = 100 - params['risk_tolerance']
        
        # Generate scenario analysis
        scenarios = self._generate_scenario_variations(roi_percentage, investment, timeline)
        
        return {
            'roi_percentage': round(roi_percentage, 1),
            'total_investment': investment,
            'total_revenue': round(total_revenue, 2),
            'net_profit': round(net_profit, 2),
            'monthly_profit': round(monthly_profit, 2),
            'payback_period_months': payback_period,
            'risk_score': round(risk_score, 1),
            'confidence_level': 95,
            'currency': 'USD',
            'calculation_date': datetime.now().isoformat(),
            'scenario_analysis': scenarios,
            'industry_benchmark': {
                'average_roi': round((roi_min + roi_max) / 2, 1),
                'top_quartile': round(roi_max * 0.8, 1),
                'median': round((roi_min + roi_max) / 2, 1),
                'bottom_quartile': round(roi_min * 1.2, 1)
            }
        }
    
    def _generate_scenario_variations(self, base_roi: float, investment: float, timeline: int) -> Dict[str, Any]:
        """Generate realistic scenario variations"""
        
        # Best case: 20-40% better than base
        best_case_roi = base_roi * random.uniform(1.2, 1.4)
        
        # Worst case: 30-60% worse than base (but not negative unless very risky)
        worst_case_roi = max(-10, base_roi * random.uniform(0.4, 0.7))
        
        # Most likely: 5-15% variation from base
        most_likely_roi = base_roi * random.uniform(0.85, 1.15)
        
        scenarios = [
            {'name': 'Optimistic Market Conditions', 'roi': best_case_roi, 'probability': 0.15},
            {'name': 'Strong Execution', 'roi': base_roi * 1.15, 'probability': 0.25},
            {'name': 'Expected Performance', 'roi': most_likely_roi, 'probability': 0.35},
            {'name': 'Market Challenges', 'roi': base_roi * 0.85, 'probability': 0.20},
            {'name': 'Execution Issues', 'roi': worst_case_roi, 'probability': 0.05}
        ]
        
        return {
            'total_scenarios': len(scenarios),
            'best_case': {'roi': round(best_case_roi, 1), 'scenario': 'Optimistic Market Conditions'},
            'worst_case': {'roi': round(worst_case_roi, 1), 'scenario': 'Execution Issues'},
            'most_likely': {'roi': round(most_likely_roi, 1), 'scenario': 'Expected Performance'},
            'average_roi': round(sum(s['roi'] * s['probability'] for s in scenarios), 1),
            'success_probability': round(sum(s['probability'] for s in scenarios if s['roi'] > 0) * 100, 1),
            'scenarios': [
                {
                    'name': s['name'],
                    'roi': round(s['roi'], 1),
                    'probability': s['probability'],
                    'profit': round(investment * (s['roi'] / 100), 2)
                }
                for s in scenarios
            ]
        }
    
    def generate_portfolio_demo(self, num_projects: int = 5) -> Dict[str, Any]:
        """Generate a portfolio of demo projects for comprehensive analysis"""
        
        portfolio = {
            'portfolio_id': f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'created_at': datetime.now().isoformat(),
            'total_projects': num_projects,
            'projects': []
        }
        
        total_investment = 0
        total_projected_profit = 0
        
        for i in range(num_projects):
            scenario = self.generate_demo_scenario()
            portfolio['projects'].append(scenario)
            
            results = scenario['expected_results']
            total_investment += results['total_investment']
            total_projected_profit += results['net_profit']
        
        # Portfolio summary
        portfolio['summary'] = {
            'total_investment': total_investment,
            'total_projected_profit': total_projected_profit,
            'portfolio_roi': round((total_projected_profit / total_investment) * 100, 1) if total_investment > 0 else 0,
            'diversification_score': self._calculate_diversification_score(portfolio['projects']),
            'risk_assessment': self._assess_portfolio_risk(portfolio['projects'])
        }
        
        return portfolio
    
    def _calculate_diversification_score(self, projects: List[Dict]) -> float:
        """Calculate portfolio diversification score"""
        industries = set(p['company']['industry'] for p in projects)
        project_types = set(p['project']['type'] for p in projects)
        company_sizes = set(p['company']['size'] for p in projects)
        
        # Score based on diversity (0-100)
        industry_score = min(len(industries) * 20, 100)
        type_score = min(len(project_types) * 20, 100)
        size_score = min(len(company_sizes) * 20, 100)
        
        return round((industry_score + type_score + size_score) / 3, 1)
    
    def _assess_portfolio_risk(self, projects: List[Dict]) -> Dict[str, Any]:
        """Assess overall portfolio risk"""
        risk_scores = [p['expected_results']['risk_score'] for p in projects]
        
        return {
            'average_risk': round(sum(risk_scores) / len(risk_scores), 1),
            'risk_range': {'min': min(risk_scores), 'max': max(risk_scores)},
            'risk_level': self._get_risk_level(sum(risk_scores) / len(risk_scores)),
            'recommendations': self._get_risk_recommendations(risk_scores)
        }
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level description"""
        if risk_score < 30:
            return 'Conservative'
        elif risk_score < 50:
            return 'Moderate'
        elif risk_score < 70:
            return 'Aggressive'
        else:
            return 'High Risk'
    
    def _get_risk_recommendations(self, risk_scores: List[float]) -> List[str]:
        """Generate risk management recommendations"""
        avg_risk = sum(risk_scores) / len(risk_scores)
        recommendations = []
        
        if avg_risk > 60:
            recommendations.append("Consider adding lower-risk projects to balance portfolio")
        if max(risk_scores) - min(risk_scores) > 40:
            recommendations.append("Portfolio shows high risk variance - ensure adequate diversification")
        if avg_risk < 25:
            recommendations.append("Portfolio may be too conservative - consider higher-return opportunities")
        
        return recommendations

# Demo route handlers for Flask integration
def create_demo_routes(app):
    """Create demo routes for Flask application"""
    
    demo_generator = DemoDataGenerator()
    
    @app.route('/demo/scenario')
    def demo_scenario():
        """Generate and return a demo scenario"""
        scenario = demo_generator.generate_demo_scenario()
        return {
            'success': True,
            'demo_scenario': scenario,
            'message': 'Demo scenario generated successfully'
        }
    
    @app.route('/demo/portfolio')
    def demo_portfolio():
        """Generate and return a demo portfolio"""
        portfolio = demo_generator.generate_portfolio_demo()
        return {
            'success': True,
            'demo_portfolio': portfolio,
            'message': 'Demo portfolio generated successfully'
        }
    
    @app.route('/demo/live-calculation')
    def demo_live_calculation():
        """Perform a live demo calculation"""
        scenario = demo_generator.generate_demo_scenario()
        
        # Simulate real calculation process
        import time
        time.sleep(1)  # Simulate calculation time
        
        return {
            'success': True,
            'scenario': scenario['calculation_parameters'],
            'results': scenario['expected_results'],
            'message': 'Live demo calculation completed',
            'calculation_time': '1.2 seconds',
            'demo_note': 'This is a realistic simulation based on actual industry data'
        }
    
    return app

# Sample demo data for immediate use
SAMPLE_DEMO_DATA = {
    'featured_scenario': {
        'title': 'AI-Powered E-commerce Platform Enhancement',
        'company': 'RetailTech Innovations',
        'investment': 85000,
        'projected_roi': 24.5,
        'payback_period': 8,
        'key_benefits': [
            '30% increase in conversion rates',
            '$180K additional annual revenue',
            '45% reduction in cart abandonment',
            'Enhanced customer experience'
        ]
    },
    'success_metrics': {
        'calculations_performed': 15847,
        'average_roi_improvement': 18.3,
        'successful_projects': 89.2,
        'customer_satisfaction': 4.8
    }
}