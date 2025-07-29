"""
Enhanced ROI Calculator with advanced financial modeling
Includes Monte Carlo simulations, sensitivity analysis, and precise calculations
"""

import random
import math
from decimal import Decimal, ROUND_HALF_UP

# Graceful numpy import for Termux compatibility
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️  NumPy not available - using simplified calculations (still accurate)")
    # Create a simple numpy substitute for basic operations
    class np:
        @staticmethod
        def exp(x):
            return math.exp(float(x))
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
from config import Config
from utils.validators import ValidationError, BusinessLogicError
from utils.analytics import AdvancedAnalyticsEngine

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
        self.analytics_engine = AdvancedAnalyticsEngine()
    
    def _get_config_value(self, config, key, default=None):
        """Helper to get value from dict or object config"""
        if isinstance(config, dict):
            return config.get(key, default)
        else:
            return getattr(config, key, default)
        
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
            base_cost = Decimal(str(self._get_config_value(project_config, 'base_cost', 100000)))
            company_multiplier = Decimal(str(self._get_config_value(company_config, 'cost_multiplier', 1.0)))
            industry_multiplier = Decimal('1.0') + Decimal(str(self._get_config_value(industry_config, 'volatility', 0.1)))
            
            # Simplified cost calculation for more reasonable estimates
            # Apply moderate company multiplier (reduced impact)
            company_factor = (company_multiplier - Decimal('1.0')) * Decimal('0.5') + Decimal('1.0')  # Reduce company impact by 50%
            
            # Apply minimal industry multiplier
            industry_factor = Decimal('1.0') + (industry_multiplier - Decimal('1.0')) * Decimal('0.3')  # Reduce industry impact by 70%
            
            # Calculate development cost with reduced multipliers
            development_cost = base_cost * company_factor * industry_factor
            
            # Simplified additional costs (much lower)
            infrastructure_cost = development_cost * Decimal('0.08')  # 8% of dev cost (reduced from 15%)
            maintenance_cost = development_cost * Decimal('0.12')    # 12% annual maintenance (reduced from 20%)
            
            # Minimal regulatory and risk buffers
            complexity_factor = Decimal('1.1') if self._get_config_value(project_config, 'complexity', 'Medium') == 'High' else Decimal('1.0')
            risk_factor = Decimal('1.05')  # Fixed 5% risk buffer
            
            # Total cost with much lower overhead
            total_cost = development_cost * complexity_factor * risk_factor + infrastructure_cost + maintenance_cost
            
            # Use custom investment if provided
            if custom_investment:
                total_cost = custom_investment
            
            # Convert to target currency
            total_cost_converted = self.convert_currency(total_cost, 'USD', currency)
            
            # Timeline calculation
            base_timeline = self._get_config_value(project_config, 'timeline', 6)
            if custom_timeline:
                timeline_months = custom_timeline
            else:
                # Adjust timeline based on company size and complexity
                size_factor = {'startup': 1.2, 'small': 1.0, 'medium': 0.9, 'large': 0.85, 'enterprise': 0.8}
                timeline_months = int(base_timeline * size_factor[company_size])
            
            # Calculate simple regulatory and risk costs for breakdown
            regulatory_cost = development_cost * Decimal('0.02')  # 2% regulatory cost
            risk_buffer = development_cost * Decimal('0.03')      # 3% risk buffer
            
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
                    'company': float(company_factor),
                    'industry': float(industry_factor),
                    'complexity': float(complexity_factor),
                    'risk': float(risk_factor)
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating project cost: {str(e)}")
            raise ValidationError(f"Failed to calculate project cost: {str(e)}")
    
    def calculate_enhanced_roi_projection(self, investment: Optional[Decimal], industry: str, 
                                        project_type: str, timeline_months: int,
                                        currency: str, company_size: str) -> ROIResult:
        """Calculate enhanced ROI with Monte Carlo simulation and advanced metrics"""
        
        try:
            industry_config = Config.INDUSTRIES[industry]
            project_config = Config.PROJECT_TYPES[project_type]
            company_config = Config.COMPANY_SIZES[company_size]
            
            # Handle optional investment: use estimated project cost if not provided
            if investment is None or investment == 0:
                investment = self.calculate_project_cost(company_size, project_type, industry, timeline_months)
                logger.info(f"Using estimated project cost: {investment}")
            
            # Base ROI calculation
            base_roi_multiplier = Decimal(str(self._get_config_value(project_config, 'roi_potential', 2.0)))
            growth_rate = Decimal(str(self._get_config_value(industry_config, 'growth_rate', 0.1)))
            
            # Realistic revenue calculation
            base_revenue = investment * base_roi_multiplier
            
            # Apply realistic growth over timeline (max 5 years of growth)
            max_growth_years = min(timeline_months / 12, 5)  # Cap at 5 years
            annual_growth_rate = min(growth_rate, 0.5)  # Cap growth at 50% annually
            
            # Use simple compound growth instead of exponential
            growth_multiplier = Decimal('1') + (Decimal(str(annual_growth_rate)) * Decimal(str(max_growth_years)))
            projected_revenue = base_revenue * growth_multiplier
            
            # Cap revenue at reasonable multiples of investment
            max_reasonable_revenue = investment * Decimal('10')  # Max 10x investment
            projected_revenue = min(projected_revenue, max_reasonable_revenue)
            
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
    
    def generate_business_intelligence(self, investment: Decimal, industry: str, project_type: str,
                                     company_size: str, timeline_months: int, roi_result: ROIResult):
        """Generate comprehensive business intelligence and analytics"""
        try:
            return self.analytics_engine.generate_comprehensive_analysis(
                investment=investment,
                industry=industry,
                project_type=project_type,
                company_size=company_size,
                timeline_months=timeline_months,
                roi_result=roi_result
            )
        except Exception as e:
            logger.error(f"Error generating business intelligence: {str(e)}")
            # Return a minimal analytics result if full analysis fails
            return None
    
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
        """Generate monthly cash flow projections with realistic timing"""
        cash_flows = [-investment]  # Initial investment as negative cash flow
        
        # More realistic revenue distribution - revenue grows gradually
        monthly_revenues = []
        total_s_curve_factor = Decimal('0')
        
        # First calculate all S-curve factors to normalize them
        s_curve_factors = []
        for month in range(1, timeline_months + 1):
            progress = month / timeline_months
            if NUMPY_AVAILABLE:
                try:
                    s_curve_factor = Decimal(str(1 / (1 + np.exp(-6 * (progress - 0.5)))))
                except:
                    s_curve_factor = Decimal(str(progress ** 0.5))  # Square root for gradual start
            else:
                try:
                    s_curve_factor = Decimal(str(1 / (1 + math.exp(-6 * (progress - 0.5)))))
                except:
                    # More realistic fallback - square root growth
                    s_curve_factor = Decimal(str(progress ** 0.5))
            s_curve_factors.append(s_curve_factor)
            total_s_curve_factor += s_curve_factor
        
        # Normalize and distribute revenue
        monthly_operating_cost = operating_costs / timeline_months
        for s_curve_factor in s_curve_factors:
            # Normalize the S-curve factor
            normalized_factor = s_curve_factor / total_s_curve_factor if total_s_curve_factor > 0 else Decimal(str(1 / timeline_months))
            monthly_revenue = total_revenue * normalized_factor
            net_monthly_flow = monthly_revenue - monthly_operating_cost
            cash_flows.append(net_monthly_flow)
        
        return cash_flows
    
    def _calculate_npv(self, cash_flows: List[Decimal], discount_rate: Decimal) -> Decimal:
        """Calculate Net Present Value with timeline-appropriate discount rate"""
        if len(cash_flows) <= 1:
            return Decimal('0')
            
        npv = Decimal('0')
        # Adjust discount rate based on project timeline
        timeline_months = len(cash_flows) - 1  # Subtract initial investment
        
        # For short-term projects (< 2 years), use lower discount rate
        if timeline_months <= 24:
            adjusted_discount_rate = discount_rate * Decimal('0.5')  # Use 4% instead of 8%
        else:
            adjusted_discount_rate = discount_rate
            
        monthly_discount_rate = adjusted_discount_rate / Decimal('12')
        
        for month, cash_flow in enumerate(cash_flows):
            if month == 0:
                # Initial investment doesn't need discounting
                npv += cash_flow
            else:
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
        
        # Risk factors should be between 0-1, then scaled to 100
        company_risk = Decimal(str(self._get_config_value(company_config, 'risk_multiplier', 0.2))) * Decimal('30')  # Max 30
        project_risk = Decimal(str(self._get_config_value(project_config, 'risk_level', 0.2))) * Decimal('40')   # Max 40
        industry_risk = Decimal(str(self._get_config_value(industry_config, 'risk_factor', 0.1))) * Decimal('20') # Max 20
        market_volatility = Decimal(str(self._get_config_value(industry_config, 'volatility', 0.1))) * Decimal('10') # Max 10
        
        total_risk_score = company_risk + project_risk + industry_risk + market_volatility
        
        # Ensure the score is within 0-100 range
        total_risk_score = min(total_risk_score, Decimal('100'))
        total_risk_score = max(total_risk_score, Decimal('0'))
        
        return total_risk_score.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    
    def _monte_carlo_simulation(self, investment: Decimal, industry: str, 
                               project_type: str, timeline_months: int,
                               company_size: str, simulations: int = 1000) -> Tuple[Decimal, Decimal]:
        """Run Monte Carlo simulation for confidence intervals"""
        
        industry_config = Config.INDUSTRIES[industry]
        project_config = Config.PROJECT_TYPES[project_type]
        
        results = []
        
        # Reduce simulations if numpy not available for faster computation
        if not NUMPY_AVAILABLE:
            simulations = min(100, simulations)
        
        for _ in range(simulations):
            # Add randomness to key parameters
            if NUMPY_AVAILABLE:
                growth_rate = self._get_config_value(industry_config, 'growth_rate', 0.1)
                volatility = self._get_config_value(industry_config, 'volatility', 0.1)
                roi_potential = self._get_config_value(project_config, 'roi_potential', 2.0)
                risk_level = self._get_config_value(project_config, 'risk_level', 0.2)
                
                random_growth = random.gauss(growth_rate, volatility * 0.3)
                random_roi = random.gauss(roi_potential, risk_level * 0.5)
                random_timeline = random.gauss(timeline_months, timeline_months * 0.1)
            else:
                # Simplified randomness for Termux compatibility
                growth_rate = self._get_config_value(industry_config, 'growth_rate', 0.1)
                volatility = self._get_config_value(industry_config, 'volatility', 0.1)
                roi_potential = self._get_config_value(project_config, 'roi_potential', 2.0)
                risk_level = self._get_config_value(project_config, 'risk_level', 0.2)
                
                volatility_factor = volatility * 0.3
                random_growth = growth_rate + random.uniform(-volatility_factor, volatility_factor)
                
                risk_factor = risk_level * 0.5
                random_roi = roi_potential + random.uniform(-risk_factor, risk_factor)
                
                timeline_factor = timeline_months * 0.1
                random_timeline = timeline_months + random.uniform(-timeline_factor, timeline_factor)
            
            # Ensure positive values
            random_growth = max(0, random_growth)
            random_roi = max(0.5, random_roi)
            random_timeline = max(6, random_timeline)
            
            # Calculate realistic ROI for this simulation
            base_revenue = investment * Decimal(str(random_roi))
            
            # Apply realistic growth (capped at 5 years and 50% annually)
            max_growth_years = min(random_timeline / 12, 5)
            capped_growth = min(random_growth, 0.5)
            growth_multiplier = Decimal('1') + (Decimal(str(capped_growth)) * Decimal(str(max_growth_years)))
            projected_revenue = base_revenue * growth_multiplier
            
            # Cap at reasonable multiples
            max_revenue = investment * Decimal('8')  # Max 8x investment for simulations
            projected_revenue = min(projected_revenue, max_revenue)
            
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
        base_growth_rate = self._get_config_value(industry_config, 'growth_rate', 0.1)
        for var in variations:
            modified_growth = base_growth_rate * (1 + var)
            modified_growth = max(0, modified_growth)
            # Create a temporary modified config
            modified_industry_config = dict(industry_config) if isinstance(industry_config, dict) else industry_config.__dict__.copy()
            modified_industry_config['growth_rate'] = modified_growth
            roi = self._calculate_base_roi(investment, modified_industry_config, project_config, timeline_months)
            growth_sensitivity.append(float(roi))
        sensitivity['growth_rate'] = growth_sensitivity
        
        # ROI potential sensitivity
        roi_sensitivity = []
        base_roi_potential = self._get_config_value(project_config, 'roi_potential', 2.0)
        for var in variations:
            modified_roi_potential = base_roi_potential * (1 + var)
            modified_roi_potential = max(0.5, modified_roi_potential)
            # Create a temporary modified config
            modified_project_config = dict(project_config) if isinstance(project_config, dict) else project_config.__dict__.copy()
            modified_project_config['roi_potential'] = modified_roi_potential
            roi = self._calculate_base_roi(investment, industry_config, modified_project_config, timeline_months)
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
        """Calculate realistic base ROI for sensitivity analysis"""
        roi_potential = self._get_config_value(project_config, 'roi_potential', 2.0)
        base_revenue = investment * Decimal(str(roi_potential))
        
        # Apply realistic growth caps
        max_growth_years = min(timeline_months / 12, 5)
        growth_rate = self._get_config_value(industry_config, 'growth_rate', 0.1)
        capped_growth = min(growth_rate, 0.5)
        growth_multiplier = Decimal('1') + (Decimal(str(capped_growth)) * Decimal(str(max_growth_years)))
        projected_revenue = base_revenue * growth_multiplier
        
        # Cap at reasonable multiples
        max_revenue = investment * Decimal('10')
        projected_revenue = min(projected_revenue, max_revenue)
        
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
        
        market_size = self._get_config_value(industry_config, 'market_size', 'Medium')
        market_info = market_size_values.get(market_size, market_size_values['Medium'])
        
        return {
            'market_size_usd': market_info['value'],
            'annual_growth_rate': f"{self._get_config_value(industry_config, 'growth_rate', 0.1) * 100:.1f}%",
            'risk_level': self._get_risk_level_description(self._get_config_value(industry_config, 'risk_factor', 0.1)),
            'volatility': f"{self._get_config_value(industry_config, 'volatility', 0.1) * 100:.1f}%",
            'regulatory_complexity': self._get_config_value(industry_config, 'regulatory_complexity', 'Medium'),
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
        growth_rate = self._get_config_value(industry_config, 'growth_rate', 0.1)
        risk_factor = self._get_config_value(industry_config, 'risk_factor', 0.1)
        volatility = self._get_config_value(industry_config, 'volatility', 0.1)
        score = (growth_rate * 50) - (risk_factor * 30) - (volatility * 20)
        
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
        regulatory_complexity = self._get_config_value(industry_config, 'regulatory_complexity', 'Medium')
        if regulatory_complexity == 'Very High':
            recommendations.append("📋 High regulatory complexity: Engage compliance experts early")
        
        volatility = self._get_config_value(industry_config, 'volatility', 0.1)
        if volatility > 0.3:
            recommendations.append("📈 High market volatility: Monitor market conditions closely")
        
        # Company size specific recommendations
        if company_size == 'startup':
            recommendations.append("🏢 Startup recommendation: Consider MVP approach and iterative development")
            recommendations.append("💡 Seek mentorship and advisory support")
        elif company_size == 'enterprise':
            recommendations.append("🏛️ Enterprise scale: Leverage existing infrastructure and partnerships")
            recommendations.append("🔄 Implement change management for smooth adoption")
        
        # Project type specific recommendations
        project_config = Config.PROJECT_TYPES.get(project_type, {})
        description = project_config.get('description', '') if isinstance(project_config, dict) else getattr(project_config, 'description', '')
        if 'AI' in description or 'Blockchain' in description:
            recommendations.append("🤖 Advanced technology: Ensure team has required expertise")
            recommendations.append("📚 Invest in training and knowledge transfer")
        
        return recommendations[:8]  # Limit to 8 most relevant recommendations