"""
Enhanced ROI Calculator with advanced financial modeling
Includes Monte Carlo simulations, sensitivity analysis, and precise calculations
"""

import random
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from config import Config
from utils.validators import ValidationError, BusinessLogicError

logger = logging.getLogger(__name__)

@dataclass
class ROIResult:
    """Comprehensive ROI calculation result"""
    total_investment: Decimal
    projected_revenue: Decimal
    net_profit: Decimal
    roi_percentage: Decimal
    payback_period_months: int
    break_even_point: Decimal
    npv: Decimal  # Net Present Value
    irr: Decimal  # Internal Rate of Return
    risk_score: Decimal
    confidence_interval: Tuple[Decimal, Decimal]
    sensitivity_analysis: Dict
    currency: str
    calculation_date: datetime

@dataclass 
class CashFlowProjection:
    """Monthly cash flow projection"""
    month: int
    revenue: Decimal
    costs: Decimal
    net_cash_flow: Decimal
    cumulative_cash_flow: Decimal

class EnhancedROICalculator:
    """Advanced ROI calculator with Monte Carlo simulations and enhanced accuracy"""
    
    def __init__(self):
        self.precision = Config.CALCULATION_PRECISION
        self.discount_rate = Decimal('0.08')  # 8% annual discount rate
        
    def convert_currency(self, amount: Decimal, from_currency: str, to_currency: str) -> Decimal:
        """Convert amount between currencies with enhanced precision"""
        if from_currency == to_currency:
            return amount
        
        from_config = Config.CURRENCIES[from_currency]
        to_config = Config.CURRENCIES[to_currency]
        
        # Convert to USD first, then to target currency
        usd_amount = amount / Decimal(str(from_config.rate))
        converted_amount = usd_amount * Decimal(str(to_config.rate))
        
        # Apply target currency precision
        precision = to_config.precision
        return converted_amount.quantize(Decimal('0.1') ** precision, rounding=ROUND_HALF_UP)
    
    def calculate_project_cost(self, company_size: str, project_type: str, 
                             industry: str, currency: str, 
                             custom_investment: Decimal = None,
                             custom_timeline: int = None) -> Dict:
        """Calculate comprehensive project cost with enhanced accuracy"""
        
        try:
            company_config = Config.COMPANY_SIZES[company_size]
            project_config = Config.PROJECT_TYPES[project_type]
            industry_config = Config.INDUSTRIES[industry]
            
            # Base cost calculation
            base_cost = Decimal(str(project_config.base_cost))
            company_multiplier = Decimal(str(company_config.multiplier))
            industry_multiplier = Decimal('1.0') + Decimal(str(industry_config.volatility))
            
            # Enhanced cost calculation with multiple factors
            adjusted_base_cost = base_cost * company_multiplier * industry_multiplier
            
            # Additional cost factors
            complexity_multiplier = self._get_complexity_multiplier(project_config.complexity)
            regulatory_multiplier = self._get_regulatory_multiplier(industry_config.regulatory_complexity)
            
            # Calculate components
            development_cost = adjusted_base_cost * complexity_multiplier
            infrastructure_cost = development_cost * Decimal('0.15')  # 15% of dev cost
            maintenance_cost = development_cost * Decimal('0.20')    # 20% annual maintenance
            regulatory_cost = development_cost * regulatory_multiplier
            
            # Risk buffer based on project and industry risk
            total_risk = Decimal(str(project_config.risk_level)) + Decimal(str(industry_config.risk_factor))
            risk_buffer = development_cost * total_risk * Decimal('0.5')
            
            # Total cost
            total_cost = development_cost + infrastructure_cost + maintenance_cost + regulatory_cost + risk_buffer
            
            # Use custom investment if provided
            if custom_investment:
                total_cost = custom_investment
            
            # Convert to target currency
            total_cost_converted = self.convert_currency(total_cost, 'USD', currency)
            
            # Timeline calculation
            base_timeline = project_config.timeline
            if custom_timeline:
                timeline_months = custom_timeline
            else:
                # Adjust timeline based on company size and complexity
                size_factor = {'startup': 1.2, 'small': 1.0, 'medium': 0.9, 'enterprise': 0.8}
                timeline_months = int(base_timeline * size_factor[company_size])
            
            return {
                'total_cost': total_cost_converted,
                'cost_breakdown': {
                    'development': self.convert_currency(development_cost, 'USD', currency),
                    'infrastructure': self.convert_currency(infrastructure_cost, 'USD', currency),
                    'maintenance_annual': self.convert_currency(maintenance_cost, 'USD', currency),
                    'regulatory_compliance': self.convert_currency(regulatory_cost, 'USD', currency),
                    'risk_buffer': self.convert_currency(risk_buffer, 'USD', currency)
                },
                'timeline_months': timeline_months,
                'currency': currency,
                'base_cost_usd': base_cost,
                'multipliers': {
                    'company': float(company_multiplier),
                    'industry': float(industry_multiplier),
                    'complexity': float(complexity_multiplier),
                    'regulatory': float(regulatory_multiplier)
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating project cost: {str(e)}")
            raise ValidationError(f"Failed to calculate project cost: {str(e)}")
    
    def calculate_enhanced_roi_projection(self, investment: Decimal, industry: str, 
                                        project_type: str, timeline_months: int,
                                        currency: str, company_size: str) -> ROIResult:
        """Calculate enhanced ROI with Monte Carlo simulation and advanced metrics"""
        
        try:
            industry_config = Config.INDUSTRIES[industry]
            project_config = Config.PROJECT_TYPES[project_type]
            company_config = Config.COMPANY_SIZES[company_size]
            
            # Base ROI calculation
            base_roi_multiplier = Decimal(str(project_config.roi_potential))
            growth_rate = Decimal(str(industry_config.growth_rate))
            
            # Enhanced revenue calculation
            base_revenue = investment * base_roi_multiplier
            
            # Apply growth compounding over timeline
            monthly_growth_rate = growth_rate / Decimal('12')
            compounded_multiplier = (Decimal('1') + monthly_growth_rate) ** timeline_months
            projected_revenue = base_revenue * compounded_multiplier
            
            # Calculate costs and profits
            operating_costs = projected_revenue * Decimal('0.30')  # 30% operating costs
            net_profit = projected_revenue - operating_costs - investment
            
            # ROI percentage
            roi_percentage = (net_profit / investment) * Decimal('100')
            
            # Advanced financial metrics
            cash_flows = self._generate_cash_flow_projections(
                investment, projected_revenue, timeline_months, operating_costs
            )
            
            npv = self._calculate_npv(cash_flows, self.discount_rate)
            irr = self._calculate_irr(cash_flows)
            payback_period = self._calculate_payback_period(cash_flows)
            
            # Risk assessment
            risk_score = self._calculate_comprehensive_risk_score(
                company_size, project_type, industry
            )
            
            # Monte Carlo simulation for confidence intervals
            confidence_interval = self._monte_carlo_simulation(
                investment, industry, project_type, timeline_months, company_size
            )
            
            # Sensitivity analysis
            sensitivity_analysis = self._sensitivity_analysis(
                investment, industry, project_type, timeline_months
            )
            
            return ROIResult(
                total_investment=investment,
                projected_revenue=projected_revenue,
                net_profit=net_profit,
                roi_percentage=roi_percentage,
                payback_period_months=payback_period,
                break_even_point=investment + operating_costs,
                npv=npv,
                irr=irr,
                risk_score=risk_score,
                confidence_interval=confidence_interval,
                sensitivity_analysis=sensitivity_analysis,
                currency=currency,
                calculation_date=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error calculating ROI projection: {str(e)}")
            raise ValidationError(f"Failed to calculate ROI projection: {str(e)}")
    
    def _get_complexity_multiplier(self, complexity: str) -> Decimal:
        """Get cost multiplier based on project complexity"""
        multipliers = {
            'Low': Decimal('0.8'),
            'Medium': Decimal('1.0'),
            'High': Decimal('1.3'),
            'Very High': Decimal('1.6')
        }
        return multipliers.get(complexity, Decimal('1.0'))
    
    def _get_regulatory_multiplier(self, regulatory_complexity: str) -> Decimal:
        """Get cost multiplier based on regulatory complexity"""
        multipliers = {
            'Low': Decimal('0.05'),
            'Medium': Decimal('0.10'),
            'High': Decimal('0.20'),
            'Very High': Decimal('0.35')
        }
        return multipliers.get(regulatory_complexity, Decimal('0.10'))
    
    def _generate_cash_flow_projections(self, investment: Decimal, total_revenue: Decimal,
                                      timeline_months: int, operating_costs: Decimal) -> List[Decimal]:
        """Generate monthly cash flow projections"""
        cash_flows = [-investment]  # Initial investment as negative cash flow
        
        # Distribute revenue over timeline with S-curve adoption
        monthly_revenues = []
        for month in range(1, timeline_months + 1):
            # S-curve: slow start, rapid growth, then plateau
            progress = month / timeline_months
            s_curve_factor = Decimal(str(1 / (1 + np.exp(-10 * (progress - 0.5)))))
            monthly_revenue = total_revenue * s_curve_factor / timeline_months
            monthly_revenues.append(monthly_revenue)
        
        # Calculate monthly cash flows
        monthly_operating_cost = operating_costs / timeline_months
        for monthly_revenue in monthly_revenues:
            net_monthly_flow = monthly_revenue - monthly_operating_cost
            cash_flows.append(net_monthly_flow)
        
        return cash_flows
    
    def _calculate_npv(self, cash_flows: List[Decimal], discount_rate: Decimal) -> Decimal:
        """Calculate Net Present Value"""
        npv = Decimal('0')
        monthly_discount_rate = discount_rate / Decimal('12')
        
        for month, cash_flow in enumerate(cash_flows):
            present_value = cash_flow / ((Decimal('1') + monthly_discount_rate) ** month)
            npv += present_value
        
        return npv.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def _calculate_irr(self, cash_flows: List[Decimal]) -> Decimal:
        """Calculate Internal Rate of Return using Newton-Raphson method"""
        # Simplified IRR calculation
        # In production, use a more sophisticated algorithm
        if len(cash_flows) < 2:
            return Decimal('0')
        
        # Initial guess
        rate = Decimal('0.10')  # 10%
        
        for _ in range(100):  # Max iterations
            npv = Decimal('0')
            npv_derivative = Decimal('0')
            
            for month, cash_flow in enumerate(cash_flows):
                factor = (Decimal('1') + rate) ** month
                npv += cash_flow / factor
                if month > 0:
                    npv_derivative -= month * cash_flow / (factor * (Decimal('1') + rate))
            
            if abs(npv) < Decimal('0.01'):
                break
            
            if npv_derivative == 0:
                break
                
            rate = rate - npv / npv_derivative
        
        return (rate * Decimal('12')).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    
    def _calculate_payback_period(self, cash_flows: List[Decimal]) -> int:
        """Calculate payback period in months"""
        cumulative_cash_flow = Decimal('0')
        
        for month, cash_flow in enumerate(cash_flows):
            cumulative_cash_flow += cash_flow
            if cumulative_cash_flow >= 0:
                return month
        
        return len(cash_flows)  # If never breaks even
    
    def _calculate_comprehensive_risk_score(self, company_size: str, project_type: str, 
                                          industry: str) -> Decimal:
        """Calculate comprehensive risk score (0-100)"""
        company_config = Config.COMPANY_SIZES[company_size]
        project_config = Config.PROJECT_TYPES[project_type]
        industry_config = Config.INDUSTRIES[industry]
        
        # Weight different risk factors
        company_risk = Decimal(str(company_config.risk_factor)) * Decimal('30')
        project_risk = Decimal(str(project_config.risk_level)) * Decimal('40')
        industry_risk = Decimal(str(industry_config.risk_factor)) * Decimal('20')
        market_volatility = Decimal(str(industry_config.volatility)) * Decimal('10')
        
        total_risk_score = company_risk + project_risk + industry_risk + market_volatility
        
        return (total_risk_score * Decimal('100')).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    
    def _monte_carlo_simulation(self, investment: Decimal, industry: str, 
                               project_type: str, timeline_months: int,
                               company_size: str, simulations: int = 1000) -> Tuple[Decimal, Decimal]:
        """Run Monte Carlo simulation for confidence intervals"""
        
        industry_config = Config.INDUSTRIES[industry]
        project_config = Config.PROJECT_TYPES[project_type]
        
        results = []
        
        for _ in range(simulations):
            # Add randomness to key parameters
            random_growth = random.gauss(industry_config.growth_rate, industry_config.volatility * 0.3)
            random_roi = random.gauss(project_config.roi_potential, project_config.risk_level * 0.5)
            random_timeline = random.gauss(timeline_months, timeline_months * 0.1)
            
            # Ensure positive values
            random_growth = max(0, random_growth)
            random_roi = max(0.5, random_roi)
            random_timeline = max(6, random_timeline)
            
            # Calculate ROI for this simulation
            base_revenue = investment * Decimal(str(random_roi))
            monthly_growth = Decimal(str(random_growth)) / Decimal('12')
            compounded = (Decimal('1') + monthly_growth) ** int(random_timeline)
            projected_revenue = base_revenue * compounded
            
            operating_costs = projected_revenue * Decimal('0.30')
            net_profit = projected_revenue - operating_costs - investment
            roi_percentage = (net_profit / investment) * Decimal('100')
            
            results.append(float(roi_percentage))
        
        # Calculate 95% confidence interval
        results.sort()
        lower_index = int(0.025 * len(results))
        upper_index = int(0.975 * len(results))
        
        lower_bound = Decimal(str(results[lower_index])).quantize(Decimal('0.1'))
        upper_bound = Decimal(str(results[upper_index])).quantize(Decimal('0.1'))
        
        return (lower_bound, upper_bound)
    
    def _sensitivity_analysis(self, investment: Decimal, industry: str,
                            project_type: str, timeline_months: int) -> Dict:
        """Perform sensitivity analysis on key parameters"""
        
        industry_config = Config.INDUSTRIES[industry]
        project_config = Config.PROJECT_TYPES[project_type]
        
        base_roi = self._calculate_base_roi(investment, industry_config, project_config, timeline_months)
        
        # Test parameter variations
        variations = [-0.2, -0.1, 0, 0.1, 0.2]  # ±20%, ±10%, baseline
        sensitivity = {}
        
        # Growth rate sensitivity
        growth_sensitivity = []
        for var in variations:
            modified_growth = industry_config.growth_rate * (1 + var)
            modified_config = industry_config
            modified_config.growth_rate = max(0, modified_growth)
            roi = self._calculate_base_roi(investment, modified_config, project_config, timeline_months)
            growth_sensitivity.append(float(roi))
        sensitivity['growth_rate'] = growth_sensitivity
        
        # ROI potential sensitivity
        roi_sensitivity = []
        for var in variations:
            modified_roi_potential = project_config.roi_potential * (1 + var)
            modified_config = project_config
            modified_config.roi_potential = max(0.5, modified_roi_potential)
            roi = self._calculate_base_roi(investment, industry_config, modified_config, timeline_months)
            roi_sensitivity.append(float(roi))
        sensitivity['roi_potential'] = roi_sensitivity
        
        # Timeline sensitivity
        timeline_sensitivity = []
        for var in variations:
            modified_timeline = int(timeline_months * (1 + var))
            modified_timeline = max(1, modified_timeline)
            roi = self._calculate_base_roi(investment, industry_config, project_config, modified_timeline)
            timeline_sensitivity.append(float(roi))
        sensitivity['timeline'] = timeline_sensitivity
        
        return sensitivity
    
    def _calculate_base_roi(self, investment: Decimal, industry_config, project_config, timeline_months: int) -> Decimal:
        """Calculate base ROI for sensitivity analysis"""
        base_revenue = investment * Decimal(str(project_config.roi_potential))
        monthly_growth = Decimal(str(industry_config.growth_rate)) / Decimal('12')
        compounded = (Decimal('1') + monthly_growth) ** timeline_months
        projected_revenue = base_revenue * compounded
        
        operating_costs = projected_revenue * Decimal('0.30')
        net_profit = projected_revenue - operating_costs - investment
        roi_percentage = (net_profit / investment) * Decimal('100')
        
        return roi_percentage.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    
    def get_market_insights(self, industry: str) -> Dict:
        """Get enhanced market insights with trends and predictions"""
        industry_config = Config.INDUSTRIES[industry]
        
        # Market size mapping
        market_size_values = {
            'Small': {'value': 1000000000, 'growth_potential': 'Limited'},
            'Medium': {'value': 10000000000, 'growth_potential': 'Moderate'},
            'Large': {'value': 100000000000, 'growth_potential': 'High'},
            'Huge': {'value': 500000000000, 'growth_potential': 'Very High'},
            'Massive': {'value': 1000000000000, 'growth_potential': 'Explosive'},
            'Stable': {'value': 50000000000, 'growth_potential': 'Steady'},
            'Volatile': {'value': 20000000000, 'growth_potential': 'Unpredictable'},
            'Emerging': {'value': 5000000000, 'growth_potential': 'Very High'},
            'Growing': {'value': 15000000000, 'growth_potential': 'High'},
            'Expanding': {'value': 30000000000, 'growth_potential': 'High'},
            'Specialized': {'value': 8000000000, 'growth_potential': 'Moderate'}
        }
        
        market_info = market_size_values.get(industry_config.market_size, market_size_values['Medium'])
        
        return {
            'market_size_usd': market_info['value'],
            'annual_growth_rate': f"{industry_config.growth_rate * 100:.1f}%",
            'risk_level': self._get_risk_level_description(industry_config.risk_factor),
            'volatility': f"{industry_config.volatility * 100:.1f}%",
            'regulatory_complexity': industry_config.regulatory_complexity,
            'growth_potential': market_info['growth_potential'],
            'key_trends': self._get_industry_trends(industry),
            'investment_attractiveness': self._calculate_investment_attractiveness(industry_config)
        }
    
    def _get_risk_level_description(self, risk_factor: float) -> str:
        """Convert risk factor to description"""
        if risk_factor <= 0.1:
            return 'Low'
        elif risk_factor <= 0.2:
            return 'Medium'
        elif risk_factor <= 0.3:
            return 'High'
        else:
            return 'Very High'
    
    def _get_industry_trends(self, industry: str) -> List[str]:
        """Get current industry trends"""
        trends = {
            'fintech': ['Digital banking growth', 'Cryptocurrency adoption', 'RegTech solutions'],
            'healthtech': ['Telemedicine expansion', 'AI diagnostics', 'Personalized medicine'],
            'edtech': ['Remote learning platforms', 'AI tutoring', 'Micro-credentials'],
            'ecommerce': ['Social commerce', 'Voice shopping', 'Sustainable packaging'],
            'saas': ['API-first architecture', 'No-code platforms', 'AI integration'],
            'gaming': ['Cloud gaming', 'Mobile gaming growth', 'VR/AR adoption'],
            'crypto': ['DeFi protocols', 'NFT marketplaces', 'Institutional adoption'],
            'web3': ['Decentralized identity', 'DAOs', 'Metaverse development'],
            'sustainability': ['Carbon trading', 'Green technology', 'Circular economy']
        }
        return trends.get(industry, ['Innovation acceleration', 'Digital transformation', 'Market expansion'])
    
    def _calculate_investment_attractiveness(self, industry_config) -> str:
        """Calculate overall investment attractiveness"""
        score = (industry_config.growth_rate * 50) - (industry_config.risk_factor * 30) - (industry_config.volatility * 20)
        
        if score >= 15:
            return 'Highly Attractive'
        elif score >= 10:
            return 'Attractive'
        elif score >= 5:
            return 'Moderately Attractive'
        else:
            return 'Cautionary'
    
    def generate_recommendations(self, company_size: str, project_type: str, 
                               industry: str, roi_result: ROIResult) -> List[str]:
        """Generate enhanced personalized recommendations"""
        recommendations = []
        
        # Risk-based recommendations
        if roi_result.risk_score > 70:
            recommendations.append("⚠️ High-risk project: Consider implementing risk mitigation strategies")
            recommendations.append("📊 Conduct thorough market research before proceeding")
        elif roi_result.risk_score > 50:
            recommendations.append("⚖️ Moderate risk: Develop contingency plans")
        
        # ROI-based recommendations
        if roi_result.roi_percentage > 200:
            recommendations.append("🚀 Exceptional ROI potential: Consider accelerating timeline")
        elif roi_result.roi_percentage > 100:
            recommendations.append("💰 Strong ROI potential: Good investment opportunity")
        elif roi_result.roi_percentage < 50:
            recommendations.append("📉 Lower ROI: Consider cost optimization strategies")
        
        # Payback period recommendations
        if roi_result.payback_period_months > 24:
            recommendations.append("⏰ Long payback period: Ensure sufficient cash flow")
        elif roi_result.payback_period_months < 12:
            recommendations.append("⚡ Quick payback: Excellent cash flow characteristics")
        
        # Industry-specific recommendations
        industry_config = Config.INDUSTRIES[industry]
        if industry_config.regulatory_complexity == 'Very High':
            recommendations.append("📋 High regulatory complexity: Engage compliance experts early")
        
        if industry_config.volatility > 0.3:
            recommendations.append("📈 High market volatility: Monitor market conditions closely")
        
        # Company size specific recommendations
        if company_size == 'startup':
            recommendations.append("🏢 Startup recommendation: Consider MVP approach and iterative development")
            recommendations.append("💡 Seek mentorship and advisory support")
        elif company_size == 'enterprise':
            recommendations.append("🏛️ Enterprise scale: Leverage existing infrastructure and partnerships")
            recommendations.append("🔄 Implement change management for smooth adoption")
        
        # Project type specific recommendations
        project_config = Config.PROJECT_TYPES[project_type]
        if 'AI' in project_config.description or 'Blockchain' in project_config.description:
            recommendations.append("🤖 Advanced technology: Ensure team has required expertise")
            recommendations.append("📚 Invest in training and knowledge transfer")
        
        return recommendations[:8]  # Limit to 8 most relevant recommendations