#!/usr/bin/env python3
"""
Business models and calculation logic for ROI Calculator
Enhanced with more accurate financial calculations
"""

import logging
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from config import COMPANY_SIZES, INDUSTRIES, PROJECT_TYPES, CURRENCIES
from utils import (
    CalculationError, format_currency, safe_divide, clamp, 
    get_risk_category, calculate_compound_growth, format_large_number,
    calculate_break_even_point, get_market_confidence_level
)

logger = logging.getLogger(__name__)

@dataclass
class ProjectCost:
    """Data class for project cost breakdown"""
    total_cost: float
    total_cost_usd: float
    currency: str
    currency_symbol: str
    breakdown: Dict[str, float]
    timeline_months: int
    complexity: str
    confidence_interval: Tuple[float, float]

@dataclass
class ROIScenario:
    """Data class for ROI scenario results"""
    scenario: str
    annual_return: float
    total_roi: float
    roi_percentage: float
    break_even_months: int
    probability: float
    description: str
    net_present_value: float
    irr: float
    payback_period: float

@dataclass
class MarketInsights:
    """Data class for market insights and analysis"""
    market_size: str
    growth_rate: str
    risk_level: str
    volatility: str
    confidence_level: str
    regulatory_complexity: str
    trends: List[str]
    opportunities: List[str]
    challenges: List[str]

@dataclass
class RiskAssessment:
    """Data class for comprehensive risk assessment"""
    overall_risk: float
    risk_category: str
    company_risk: float
    project_risk: float
    industry_risk: float
    market_volatility: float
    mitigation_strategies: List[str]

class EnhancedROICalculator:
    """Enhanced ROI Calculator with improved accuracy and financial modeling"""
    
    def __init__(self):
        self.discount_rate = 0.08  # 8% discount rate for NPV calculations
        self.risk_free_rate = 0.03  # 3% risk-free rate
        
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount between currencies with error handling"""
        try:
            if from_currency == to_currency:
                return amount
            
            from_rate = CURRENCIES.get(from_currency, {}).get('rate', 1.0)
            to_rate = CURRENCIES.get(to_currency, {}).get('rate', 1.0)
            
            # Convert to USD first, then to target currency
            usd_amount = amount / from_rate
            converted_amount = usd_amount * to_rate
            
            return converted_amount
            
        except Exception as e:
            logger.error(f"Currency conversion error: {str(e)}")
            raise CalculationError(
                "Currency conversion failed",
                f"Failed to convert {amount} from {from_currency} to {to_currency}"
            )
    
    def calculate_monte_carlo_variance(self, base_cost: float, volatility: float, iterations: int = 1000) -> Tuple[float, float]:
        """Calculate cost variance using Monte Carlo simulation"""
        try:
            # Generate random variations based on volatility
            variations = np.random.normal(1.0, volatility, iterations)
            costs = base_cost * variations
            
            # Calculate confidence interval (5th and 95th percentiles)
            lower_bound = np.percentile(costs, 5)
            upper_bound = np.percentile(costs, 95)
            
            return (lower_bound, upper_bound)
            
        except Exception as e:
            logger.warning(f"Monte Carlo calculation failed: {str(e)}")
            # Fallback to simple variance calculation
            variance = base_cost * volatility
            return (base_cost - variance, base_cost + variance)
    
    def calculate_project_cost(self, company_size: str, project_type: str, industry: str, 
                             currency: str = 'USD', custom_budget: Optional[float] = None) -> ProjectCost:
        """Calculate enhanced project cost with Monte Carlo simulation"""
        try:
            # Get base data
            size_data = COMPANY_SIZES.get(company_size, COMPANY_SIZES['small'])
            project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
            industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
            
            # Use custom budget if provided and valid
            if custom_budget and size_data['min_budget'] <= custom_budget <= size_data['max_budget']:
                base_cost = custom_budget
            else:
                base_cost = project_data['base_cost'] * size_data['multiplier']
            
            # Enhanced industry complexity adjustment
            regulatory_factor = self._get_regulatory_factor(industry_data.get('regulatory_complexity', 'Medium'))
            market_maturity_factor = self._get_market_maturity_factor(industry_data['market_size'])
            
            industry_multiplier = 1.0 + (industry_data['risk_factor'] * 0.4) + regulatory_factor + market_maturity_factor
            adjusted_cost = base_cost * industry_multiplier
            
            # Add realistic variance with improved modeling
            volatility = industry_data['volatility']
            market_conditions = np.random.uniform(0.9, 1.1)  # Market condition factor
            final_cost_usd = adjusted_cost * market_conditions
            
            # Calculate confidence interval
            confidence_interval = self.calculate_monte_carlo_variance(final_cost_usd, volatility)
            
            # Convert to requested currency
            final_cost = self.convert_currency(final_cost_usd, 'USD', currency)
            
            # Enhanced cost breakdown with more realistic proportions
            breakdown = self._calculate_detailed_breakdown(final_cost, project_type, industry)
            
            return ProjectCost(
                total_cost=int(final_cost),
                total_cost_usd=int(final_cost_usd),
                currency=currency,
                currency_symbol=CURRENCIES[currency]['symbol'],
                breakdown=breakdown,
                timeline_months=project_data['timeline'],
                complexity=project_data['complexity'],
                confidence_interval=(int(confidence_interval[0]), int(confidence_interval[1]))
            )
            
        except Exception as e:
            logger.error(f"Project cost calculation error: {str(e)}")
            raise CalculationError(
                "Failed to calculate project cost",
                f"Error in cost calculation for {project_type} project"
            )
    
    def _get_regulatory_factor(self, complexity: str) -> float:
        """Calculate regulatory complexity factor"""
        factors = {
            'Very High': 0.25,
            'High': 0.15,
            'Medium': 0.08,
            'Low': 0.03
        }
        return factors.get(complexity, 0.08)
    
    def _get_market_maturity_factor(self, market_size: str) -> float:
        """Calculate market maturity factor"""
        factors = {
            'Massive': -0.05,  # Mature markets have cost advantages
            'Huge': -0.03,
            'Large': 0.0,
            'Medium': 0.05,
            'Emerging': 0.15,  # New markets have higher costs
            'Volatile': 0.20,
            'Growing': 0.10,
            'Stable': -0.02,
            'Specialized': 0.12
        }
        return factors.get(market_size, 0.0)
    
    def _calculate_detailed_breakdown(self, total_cost: float, project_type: str, industry: str) -> Dict[str, float]:
        """Calculate detailed cost breakdown based on project type and industry"""
        # Base breakdown percentages
        base_breakdown = {
            'development': 0.50,
            'design': 0.12,
            'testing': 0.10,
            'deployment': 0.08,
            'project_management': 0.10,
            'compliance': 0.05,
            'training': 0.05
        }
        
        # Adjust based on project type
        if project_type in ['ai_integration', 'blockchain_platform']:
            base_breakdown['development'] = 0.60
            base_breakdown['testing'] = 0.15
            base_breakdown['compliance'] = 0.10
        elif project_type in ['marketing_campaign']:
            base_breakdown['development'] = 0.20
            base_breakdown['design'] = 0.30
            base_breakdown['deployment'] = 0.25
        elif project_type in ['digital_transformation']:
            base_breakdown['training'] = 0.15
            base_breakdown['project_management'] = 0.18
        
        # Adjust based on industry
        if industry in ['fintech', 'healthtech']:
            base_breakdown['compliance'] += 0.10
            base_breakdown['testing'] += 0.05
        
        # Normalize to ensure total is 100%
        total_percentage = sum(base_breakdown.values())
        normalized_breakdown = {k: v / total_percentage for k, v in base_breakdown.items()}
        
        # Calculate actual costs
        return {category: int(total_cost * percentage) 
                for category, percentage in normalized_breakdown.items()}
    
    def calculate_enhanced_roi_projection(self, investment: float, industry: str, project_type: str, 
                                        timeline_months: int, currency: str = 'USD') -> Dict[str, ROIScenario]:
        """Enhanced ROI projections with IRR, NPV, and advanced financial metrics"""
        try:
            industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
            project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
            
            # Enhanced base calculations
            base_roi = project_data['roi_potential']
            growth_rate = industry_data['growth_rate']
            volatility = industry_data['volatility']
            risk_factor = industry_data['risk_factor']
            
            # Calculate discount rate adjusted for industry risk
            adjusted_discount_rate = self.discount_rate + (risk_factor * 0.5)
            
            # Enhanced scenarios with more sophisticated modeling
            scenarios_data = {
                'pessimistic': {
                    'multiplier': max(0.3, 0.6 - (volatility * 0.3)),
                    'probability': 0.15,
                    'description': 'Worst case with significant market challenges and delays'
                },
                'conservative': {
                    'multiplier': max(0.5, 0.8 - (volatility * 0.15)),
                    'probability': 0.25,
                    'description': 'Conservative estimate accounting for typical market challenges'
                },
                'realistic': {
                    'multiplier': 1.0 + (growth_rate * 0.1),
                    'probability': 0.40,
                    'description': 'Most likely scenario based on current market conditions'
                },
                'optimistic': {
                    'multiplier': 1.4 + (growth_rate * 0.3),
                    'probability': 0.20,
                    'description': 'Best case with favorable market conditions and optimal execution'
                }
            }
            
            projections = {}
            investment_usd = investment if currency == 'USD' else self.convert_currency(investment, currency, 'USD')
            
            for scenario, data in scenarios_data.items():
                # Calculate ROI multiplier with enhanced logic
                roi_multiplier = max(0.1, base_roi * data['multiplier'])
                
                # Calculate returns with compound growth
                annual_return_usd = investment_usd * (roi_multiplier - 1) * growth_rate
                total_return_3yr = calculate_compound_growth(annual_return_usd, growth_rate, 3)
                
                # Convert back to requested currency
                annual_return = self.convert_currency(annual_return_usd, 'USD', currency)
                total_roi = self.convert_currency(total_return_3yr, 'USD', currency)
                
                # Calculate advanced financial metrics
                irr = self._calculate_irr(investment, annual_return, 3)
                npv = self._calculate_npv(investment, annual_return, 3, adjusted_discount_rate)
                payback_period = calculate_break_even_point(investment, annual_return / 12)
                
                projections[scenario] = ROIScenario(
                    scenario=scenario.title(),
                    annual_return=int(annual_return),
                    total_roi=int(total_roi),
                    roi_percentage=int((roi_multiplier - 1) * 100),
                    break_even_months=max(1, int(timeline_months / roi_multiplier)),
                    probability=data['probability'],
                    description=data['description'],
                    net_present_value=int(npv),
                    irr=irr,
                    payback_period=payback_period
                )
            
            return projections
            
        except Exception as e:
            logger.error(f"ROI projection calculation error: {str(e)}")
            raise CalculationError(
                "Failed to calculate ROI projections",
                f"Error in ROI calculation for {project_type} in {industry}"
            )
    
    def _calculate_irr(self, investment: float, annual_cash_flow: float, years: int) -> float:
        """Calculate Internal Rate of Return using Newton-Raphson method"""
        try:
            # Simple IRR approximation for annual cash flows
            if annual_cash_flow <= 0:
                return -100.0
            
            # Initial guess
            rate = 0.1
            
            for _ in range(100):  # Max iterations
                npv = -investment
                npv_derivative = 0
                
                for year in range(1, years + 1):
                    discount_factor = (1 + rate) ** year
                    npv += annual_cash_flow / discount_factor
                    npv_derivative -= year * annual_cash_flow / (discount_factor * (1 + rate))
                
                if abs(npv) < 0.01:  # Convergence
                    break
                
                if npv_derivative == 0:
                    break
                
                rate = rate - npv / npv_derivative
            
            return round(rate * 100, 2)
            
        except Exception:
            # Fallback calculation
            return round((annual_cash_flow / investment) * 100, 2)
    
    def _calculate_npv(self, investment: float, annual_cash_flow: float, years: int, discount_rate: float) -> float:
        """Calculate Net Present Value"""
        try:
            npv = -investment
            
            for year in range(1, years + 1):
                npv += annual_cash_flow / ((1 + discount_rate) ** year)
            
            return npv
            
        except Exception:
            return annual_cash_flow * years - investment
    
    def calculate_comprehensive_risk_assessment(self, company_size: str, project_type: str, industry: str) -> RiskAssessment:
        """Calculate comprehensive risk assessment with mitigation strategies"""
        try:
            size_data = COMPANY_SIZES.get(company_size, COMPANY_SIZES['small'])
            project_data = PROJECT_TYPES.get(project_type, PROJECT_TYPES['product_development'])
            industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
            
            # Individual risk components
            company_risk = size_data['risk_factor']
            project_risk = project_data['risk_level']
            industry_risk = industry_data['risk_factor']
            market_volatility = industry_data['volatility']
            
            # Weighted composite risk score
            overall_risk = (
                company_risk * 0.25 +
                project_risk * 0.35 +
                industry_risk * 0.25 +
                market_volatility * 0.15
            )
            
            # Generate mitigation strategies
            strategies = self._generate_mitigation_strategies(company_size, project_type, industry, overall_risk)
            
            return RiskAssessment(
                overall_risk=round(overall_risk, 3),
                risk_category=get_risk_category(overall_risk),
                company_risk=round(company_risk, 3),
                project_risk=round(project_risk, 3),
                industry_risk=round(industry_risk, 3),
                market_volatility=round(market_volatility, 3),
                mitigation_strategies=strategies
            )
            
        except Exception as e:
            logger.error(f"Risk assessment calculation error: {str(e)}")
            raise CalculationError(
                "Failed to calculate risk assessment",
                f"Error in risk calculation for {project_type}"
            )
    
    def _generate_mitigation_strategies(self, company_size: str, project_type: str, industry: str, risk_score: float) -> List[str]:
        """Generate contextual risk mitigation strategies"""
        strategies = []
        
        # Company size specific strategies
        if company_size == 'startup':
            strategies.extend([
                "Implement agile development methodology to reduce delivery risk",
                "Secure adequate funding runway before project start",
                "Consider phased implementation to manage cash flow"
            ])
        elif company_size == 'enterprise':
            strategies.extend([
                "Establish comprehensive change management program",
                "Leverage existing infrastructure and resources",
                "Implement robust governance and oversight processes"
            ])
        
        # Industry specific strategies
        if industry in ['fintech', 'healthtech']:
            strategies.extend([
                "Engage regulatory bodies early in the development process",
                "Implement comprehensive compliance monitoring",
                "Budget additional time and resources for regulatory approval"
            ])
        
        if industry in ['crypto', 'web3']:
            strategies.extend([
                "Monitor regulatory developments closely",
                "Implement robust security and audit procedures",
                "Consider geographic diversification of operations"
            ])
        
        # Project type specific strategies
        if project_type in ['ai_integration', 'data_analytics']:
            strategies.extend([
                "Ensure high-quality training data availability",
                "Implement bias detection and mitigation procedures",
                "Plan for model interpretability and explainability"
            ])
        
        # Risk level specific strategies
        if risk_score > 0.3:
            strategies.extend([
                "Consider purchasing project insurance",
                "Establish contingency budget of 20-30%",
                "Implement weekly risk review meetings"
            ])
        
        return strategies[:6]  # Limit to 6 most relevant strategies
    
    def get_enhanced_market_insights(self, industry: str) -> MarketInsights:
        """Get comprehensive market insights with enhanced analysis"""
        try:
            industry_data = INDUSTRIES.get(industry, INDUSTRIES['saas'])
            
            # Calculate confidence level
            confidence_level = get_market_confidence_level(
                industry_data['volatility'], 
                industry_data['growth_rate']
            )
            
            # Generate contextual insights
            trends = self._get_industry_trends(industry)
            opportunities = self._get_industry_opportunities(industry)
            challenges = self._get_industry_challenges(industry)
            
            return MarketInsights(
                market_size=industry_data['market_size'],
                growth_rate=f"{industry_data['growth_rate']*100:.1f}%",
                risk_level=get_risk_category(industry_data['risk_factor']),
                volatility=f"{industry_data['volatility']*100:.1f}%",
                confidence_level=confidence_level,
                regulatory_complexity=industry_data.get('regulatory_complexity', 'Medium'),
                trends=trends,
                opportunities=opportunities,
                challenges=challenges
            )
            
        except Exception as e:
            logger.error(f"Market insights calculation error: {str(e)}")
            raise CalculationError(
                "Failed to generate market insights",
                f"Error generating insights for {industry}"
            )
    
    def _get_industry_trends(self, industry: str) -> List[str]:
        """Get industry-specific trends"""
        trends_map = {
            'fintech': [
                "Open banking APIs driving innovation",
                "Increased focus on financial inclusion",
                "AI-powered fraud detection becoming standard",
                "Cryptocurrency integration in traditional finance"
            ],
            'healthtech': [
                "Telemedicine adoption accelerating post-pandemic",
                "AI diagnostic tools gaining regulatory approval",
                "Wearable health monitoring becoming mainstream",
                "Personalized medicine through genomics"
            ],
            'saas': [
                "Low-code/no-code platforms democratizing development",
                "API-first architecture becoming standard",
                "AI integration in business workflows",
                "Usage-based pricing models gaining popularity"
            ],
            'ecommerce': [
                "Social commerce integration expanding",
                "AR/VR try-before-buy experiences",
                "Sustainable packaging becoming priority",
                "Voice commerce adoption growing"
            ]
        }
        
        return trends_map.get(industry, [
            "Digital transformation accelerating",
            "Remote work driving technology adoption",
            "Sustainability becoming key differentiator",
            "Customer experience focus intensifying"
        ])
    
    def _get_industry_opportunities(self, industry: str) -> List[str]:
        """Get industry-specific opportunities"""
        opportunities_map = {
            'fintech': [
                "Underbanked populations in emerging markets",
                "SME lending gaps in traditional banking",
                "Carbon credit trading platforms"
            ],
            'healthtech': [
                "Mental health technology solutions",
                "Elderly care technology platforms",
                "Chronic disease management tools"
            ],
            'saas': [
                "Industry-specific vertical solutions",
                "Workflow automation tools",
                "Data analytics and business intelligence"
            ]
        }
        
        return opportunities_map.get(industry, [
            "Market consolidation creating opportunities",
            "Technology adoption in traditional sectors",
            "International expansion potential"
        ])
    
    def _get_industry_challenges(self, industry: str) -> List[str]:
        """Get industry-specific challenges"""
        challenges_map = {
            'fintech': [
                "Increasing regulatory scrutiny",
                "Cybersecurity threats and compliance costs",
                "Competition from traditional banks adopting tech"
            ],
            'healthtech': [
                "Complex regulatory approval processes",
                "Privacy and data security concerns",
                "Integration with legacy healthcare systems"
            ],
            'crypto': [
                "Regulatory uncertainty and changing laws",
                "Market volatility and investor sentiment",
                "Environmental concerns over energy usage"
            ]
        }
        
        return challenges_map.get(industry, [
            "Increasing competition and market saturation",
            "Talent acquisition and retention challenges",
            "Economic uncertainty affecting investment"
        ])