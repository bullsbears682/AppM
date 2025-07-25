"""
Advanced Analytics Engine for ROI Calculator
Provides realistic business insights, market analysis, and detailed reporting
"""

import math
import random
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from config import Config

@dataclass
class MarketAnalysis:
    """Market analysis and insights"""
    market_size: Decimal
    growth_rate: Decimal
    competition_level: str
    market_maturity: str
    seasonal_factors: Dict[str, Decimal]
    key_trends: List[str]
    opportunities: List[str]
    threats: List[str]

@dataclass
class CompetitiveAnalysis:
    """Competitive landscape analysis"""
    market_share_potential: Decimal
    competitive_advantage: str
    differentiation_score: Decimal
    pricing_power: str
    barriers_to_entry: List[str]
    competitive_threats: List[str]

@dataclass
class FinancialMetrics:
    """Enhanced financial metrics"""
    customer_acquisition_cost: Decimal
    lifetime_value: Decimal
    gross_margin: Decimal
    operating_margin: Decimal
    working_capital_needs: Decimal
    burn_rate: Decimal
    runway_months: int
    break_even_units: int

@dataclass
class RiskAnalysis:
    """Comprehensive risk analysis"""
    market_risk: Decimal
    execution_risk: Decimal
    financial_risk: Decimal
    regulatory_risk: Decimal
    technology_risk: Decimal
    overall_risk: Decimal
    risk_mitigation: List[str]
    contingency_plans: List[str]

@dataclass
class BusinessIntelligence:
    """Complete business intelligence package"""
    market_analysis: MarketAnalysis
    competitive_analysis: CompetitiveAnalysis
    financial_metrics: FinancialMetrics
    risk_analysis: RiskAnalysis
    success_probability: Decimal
    recommended_actions: List[str]
    kpi_targets: Dict[str, Any]
    milestones: List[Dict[str, Any]]

class AdvancedAnalyticsEngine:
    """Advanced analytics for realistic business insights"""
    
    def __init__(self):
        self.config = Config()
    
    def generate_comprehensive_analysis(self, 
                                      investment: Decimal,
                                      industry: str,
                                      project_type: str,
                                      company_size: str,
                                      timeline_months: int,
                                      roi_result: Any) -> BusinessIntelligence:
        """Generate comprehensive business intelligence"""
        
        # Market Analysis
        market_analysis = self._analyze_market(industry, investment, timeline_months)
        
        # Competitive Analysis
        competitive_analysis = self._analyze_competition(industry, project_type, company_size)
        
        # Financial Metrics
        financial_metrics = self._calculate_financial_metrics(
            investment, roi_result, industry, project_type
        )
        
        # Risk Analysis
        risk_analysis = self._analyze_risks(
            industry, project_type, company_size, investment
        )
        
        # Success Probability
        success_probability = self._calculate_success_probability(
            market_analysis, competitive_analysis, financial_metrics, risk_analysis
        )
        
        # Recommendations
        recommended_actions = self._generate_recommendations(
            market_analysis, competitive_analysis, financial_metrics, risk_analysis
        )
        
        # KPI Targets
        kpi_targets = self._set_kpi_targets(investment, roi_result, timeline_months)
        
        # Milestones
        milestones = self._create_milestone_plan(timeline_months, investment)
        
        return BusinessIntelligence(
            market_analysis=market_analysis,
            competitive_analysis=competitive_analysis,
            financial_metrics=financial_metrics,
            risk_analysis=risk_analysis,
            success_probability=success_probability,
            recommended_actions=recommended_actions,
            kpi_targets=kpi_targets,
            milestones=milestones
        )
    
    def _analyze_market(self, industry: str, investment: Decimal, timeline_months: int) -> MarketAnalysis:
        """Analyze market conditions and opportunities"""
        
        # Market size estimation based on industry
        market_sizes = {
            'technology': Decimal('500000000'),  # $500M
            'healthcare': Decimal('800000000'),  # $800M
            'finance': Decimal('300000000'),     # $300M
            'retail': Decimal('250000000'),      # $250M
            'manufacturing': Decimal('400000000'), # $400M
            'education': Decimal('150000000'),   # $150M
            'real_estate': Decimal('600000000'), # $600M
            'consulting': Decimal('200000000'),  # $200M
        }
        
        market_size = market_sizes.get(industry, Decimal('350000000'))
        
        # Growth rates by industry (realistic annual rates)
        growth_rates = {
            'technology': Decimal('0.12'),      # 12% 
            'healthcare': Decimal('0.08'),      # 8%
            'finance': Decimal('0.06'),         # 6%
            'retail': Decimal('0.04'),          # 4%
            'manufacturing': Decimal('0.05'),   # 5%
            'education': Decimal('0.07'),       # 7%
            'real_estate': Decimal('0.09'),     # 9%
            'consulting': Decimal('0.10'),      # 10%
        }
        
        growth_rate = growth_rates.get(industry, Decimal('0.07'))
        
        # Competition levels
        competition_levels = {
            'technology': 'High',
            'healthcare': 'Medium-High', 
            'finance': 'High',
            'retail': 'Very High',
            'manufacturing': 'Medium',
            'education': 'Medium',
            'real_estate': 'Medium-High',
            'consulting': 'High'
        }
        
        competition_level = competition_levels.get(industry, 'Medium')
        
        # Market maturity
        maturity_levels = {
            'technology': 'Emerging-Growth',
            'healthcare': 'Mature',
            'finance': 'Mature', 
            'retail': 'Mature',
            'manufacturing': 'Mature',
            'education': 'Growth',
            'real_estate': 'Mature',
            'consulting': 'Growth'
        }
        
        market_maturity = maturity_levels.get(industry, 'Growth')
        
        # Seasonal factors (monthly multipliers)
        seasonal_factors = self._get_seasonal_factors(industry)
        
        # Key trends, opportunities, and threats
        trends = self._get_market_trends(industry)
        opportunities = self._get_market_opportunities(industry, investment)
        threats = self._get_market_threats(industry)
        
        return MarketAnalysis(
            market_size=market_size,
            growth_rate=growth_rate,
            competition_level=competition_level,
            market_maturity=market_maturity,
            seasonal_factors=seasonal_factors,
            key_trends=trends,
            opportunities=opportunities,
            threats=threats
        )
    
    def _analyze_competition(self, industry: str, project_type: str, company_size: str) -> CompetitiveAnalysis:
        """Analyze competitive landscape"""
        
        # Market share potential based on company size and industry
        market_share_potentials = {
            'startup': {'technology': 0.5, 'healthcare': 0.3, 'finance': 0.2},
            'small': {'technology': 2.0, 'healthcare': 1.5, 'finance': 1.0},
            'medium': {'technology': 5.0, 'healthcare': 3.0, 'finance': 2.5},
            'large': {'technology': 10.0, 'healthcare': 8.0, 'finance': 6.0},
            'enterprise': {'technology': 15.0, 'healthcare': 12.0, 'finance': 10.0}
        }
        
        base_share = market_share_potentials.get(company_size, {}).get(industry, 2.0)
        market_share_potential = Decimal(str(base_share))
        
        # Competitive advantages by project type
        advantages = {
            'product_development': 'Innovation and first-mover advantage',
            'process_improvement': 'Operational efficiency and cost leadership',
            'market_expansion': 'Market penetration and customer relationships',
            'technology_upgrade': 'Technology differentiation and scalability',
            'cost_reduction': 'Cost structure optimization',
            'digital_transformation': 'Digital capabilities and agility'
        }
        
        competitive_advantage = advantages.get(project_type, 'Operational excellence')
        
        # Differentiation scores (1-10 scale)
        diff_scores = {
            'product_development': 8.5,
            'process_improvement': 6.0,
            'market_expansion': 7.0,
            'technology_upgrade': 8.0,
            'cost_reduction': 5.5,
            'digital_transformation': 9.0
        }
        
        differentiation_score = Decimal(str(diff_scores.get(project_type, 7.0)))
        
        # Pricing power
        pricing_powers = {
            'product_development': 'High',
            'technology_upgrade': 'Medium-High',
            'digital_transformation': 'High',
            'market_expansion': 'Medium',
            'process_improvement': 'Medium-Low',
            'cost_reduction': 'Low'
        }
        
        pricing_power = pricing_powers.get(project_type, 'Medium')
        
        # Barriers to entry and threats
        barriers = self._get_barriers_to_entry(industry, project_type)
        threats = self._get_competitive_threats(industry, company_size)
        
        return CompetitiveAnalysis(
            market_share_potential=market_share_potential,
            competitive_advantage=competitive_advantage,
            differentiation_score=differentiation_score,
            pricing_power=pricing_power,
            barriers_to_entry=barriers,
            competitive_threats=threats
        )
    
    def _calculate_financial_metrics(self, investment: Decimal, roi_result: Any, 
                                   industry: str, project_type: str) -> FinancialMetrics:
        """Calculate enhanced financial metrics"""
        
        # Customer Acquisition Cost (realistic ranges)
        cac_ranges = {
            'technology': (50, 500),
            'healthcare': (200, 1000),
            'finance': (300, 800),
            'retail': (20, 100),
            'consulting': (500, 2000)
        }
        
        cac_range = cac_ranges.get(industry, (100, 400))
        customer_acquisition_cost = Decimal(str(random.uniform(*cac_range)))
        
        # Customer Lifetime Value (3-5x CAC is healthy)
        ltv_multiplier = random.uniform(3.5, 6.0)
        lifetime_value = customer_acquisition_cost * Decimal(str(ltv_multiplier))
        
        # Gross margin by industry (realistic percentages)
        gross_margins = {
            'technology': random.uniform(70, 85),
            'healthcare': random.uniform(40, 60),
            'finance': random.uniform(60, 75),
            'retail': random.uniform(20, 40),
            'consulting': random.uniform(50, 70),
            'manufacturing': random.uniform(25, 45)
        }
        
        gross_margin = Decimal(str(gross_margins.get(industry, random.uniform(40, 60))))
        
        # Operating margin (typically 50-70% of gross margin)
        operating_margin = gross_margin * Decimal(str(random.uniform(0.5, 0.7)))
        
        # Working capital needs (% of revenue)
        wc_percentages = {
            'technology': random.uniform(5, 15),
            'manufacturing': random.uniform(15, 25),
            'retail': random.uniform(10, 20),
            'consulting': random.uniform(8, 15)
        }
        
        wc_percentage = wc_percentages.get(industry, random.uniform(8, 18))
        working_capital_needs = roi_result.projected_revenue * Decimal(str(wc_percentage / 100))
        
        # Monthly burn rate (for startups/small companies)
        monthly_burn_ranges = {
            'startup': (10000, 50000),
            'small': (25000, 100000),
            'medium': (50000, 250000),
            'large': (100000, 500000)
        }
        
        burn_rate = Decimal(str(random.uniform(20000, 80000)))  # Default range
        
        # Runway calculation
        cash_available = investment * Decimal('0.7')  # Assume 70% for operations
        runway_months = int(cash_available / burn_rate) if burn_rate > 0 else 24
        
        # Break-even units calculation
        unit_price = Decimal(str(random.uniform(50, 500)))  # Varies by industry
        unit_cost = unit_price * (Decimal('1') - gross_margin / Decimal('100'))
        unit_margin = unit_price - unit_cost
        fixed_costs = investment * Decimal('0.3')  # Assume 30% fixed costs
        break_even_units = int(fixed_costs / unit_margin) if unit_margin > 0 else 1000
        
        return FinancialMetrics(
            customer_acquisition_cost=customer_acquisition_cost.quantize(Decimal('0.01')),
            lifetime_value=lifetime_value.quantize(Decimal('0.01')),
            gross_margin=gross_margin.quantize(Decimal('0.1')),
            operating_margin=operating_margin.quantize(Decimal('0.1')),
            working_capital_needs=working_capital_needs.quantize(Decimal('0.01')),
            burn_rate=burn_rate.quantize(Decimal('0.01')),
            runway_months=runway_months,
            break_even_units=break_even_units
        )
    
    def _analyze_risks(self, industry: str, project_type: str, 
                      company_size: str, investment: Decimal) -> RiskAnalysis:
        """Comprehensive risk analysis"""
        
        # Risk scoring (0-100 scale)
        industry_risks = {
            'technology': {'market': 35, 'execution': 45, 'financial': 30, 'regulatory': 20, 'tech': 25},
            'healthcare': {'market': 25, 'execution': 35, 'financial': 40, 'regulatory': 70, 'tech': 30},
            'finance': {'market': 30, 'execution': 40, 'financial': 50, 'regulatory': 80, 'tech': 35},
            'retail': {'market': 50, 'execution': 30, 'financial': 45, 'regulatory': 25, 'tech': 20},
            'manufacturing': {'market': 40, 'execution': 35, 'financial': 45, 'regulatory': 45, 'tech': 30}
        }
        
        base_risks = industry_risks.get(industry, {'market': 35, 'execution': 40, 'financial': 40, 'regulatory': 35, 'tech': 30})
        
        # Adjust for company size (larger companies generally have lower execution risk)
        size_adjustments = {
            'startup': 1.3,
            'small': 1.1,
            'medium': 1.0,
            'large': 0.85,
            'enterprise': 0.7
        }
        
        size_factor = size_adjustments.get(company_size, 1.0)
        
        market_risk = Decimal(str(base_risks['market'] * size_factor))
        execution_risk = Decimal(str(base_risks['execution'] * size_factor))
        financial_risk = Decimal(str(base_risks['financial'] * size_factor))
        regulatory_risk = Decimal(str(base_risks['regulatory']))
        technology_risk = Decimal(str(base_risks['tech'] * size_factor))
        
        # Overall risk (weighted average)
        weights = [0.25, 0.30, 0.20, 0.15, 0.10]  # execution risk gets highest weight
        risks = [market_risk, execution_risk, financial_risk, regulatory_risk, technology_risk]
        overall_risk = sum(risk * Decimal(str(weight)) for risk, weight in zip(risks, weights))
        
        # Risk mitigation strategies
        mitigation = self._get_risk_mitigation(industry, project_type)
        contingency = self._get_contingency_plans(industry, project_type)
        
        return RiskAnalysis(
            market_risk=market_risk.quantize(Decimal('0.1')),
            execution_risk=execution_risk.quantize(Decimal('0.1')),
            financial_risk=financial_risk.quantize(Decimal('0.1')),
            regulatory_risk=regulatory_risk.quantize(Decimal('0.1')),
            technology_risk=technology_risk.quantize(Decimal('0.1')),
            overall_risk=overall_risk.quantize(Decimal('0.1')),
            risk_mitigation=mitigation,
            contingency_plans=contingency
        )
    
    def _calculate_success_probability(self, market: MarketAnalysis, competitive: CompetitiveAnalysis,
                                     financial: FinancialMetrics, risk: RiskAnalysis) -> Decimal:
        """Calculate realistic success probability"""
        
        # Base probability starts at 50%
        base_prob = 50.0
        
        # Market factors
        if market.growth_rate > Decimal('0.10'):
            base_prob += 10  # High growth market
        elif market.growth_rate < Decimal('0.03'):
            base_prob -= 10  # Slow growth market
            
        # Competition adjustment
        comp_adjustments = {
            'Low': 15,
            'Medium': 5,
            'Medium-High': -5,
            'High': -10,
            'Very High': -15
        }
        base_prob += comp_adjustments.get(market.competition_level, 0)
        
        # Financial health
        if financial.lifetime_value > financial.customer_acquisition_cost * Decimal('4'):
            base_prob += 15  # Healthy LTV/CAC ratio
        elif financial.lifetime_value < financial.customer_acquisition_cost * Decimal('3'):
            base_prob -= 10  # Poor unit economics
            
        # Risk adjustment
        risk_adjustment = float(risk.overall_risk) * -0.3  # Higher risk reduces probability
        base_prob += risk_adjustment
        
        # Differentiation bonus
        if competitive.differentiation_score > Decimal('7'):
            base_prob += 10
        elif competitive.differentiation_score < Decimal('5'):
            base_prob -= 5
            
        # Ensure probability is between 10% and 85%
        final_prob = max(10, min(85, base_prob))
        
        return Decimal(str(final_prob)).quantize(Decimal('0.1'))
    
    # Helper methods for generating realistic business data
    def _get_seasonal_factors(self, industry: str) -> Dict[str, Decimal]:
        """Get seasonal multipliers by month"""
        seasonal_patterns = {
            'retail': {
                'Q1': 0.8, 'Q2': 0.9, 'Q3': 1.0, 'Q4': 1.7  # Holiday boost
            },
            'technology': {
                'Q1': 1.1, 'Q2': 0.9, 'Q3': 0.8, 'Q4': 1.2  # End of year budgets
            },
            'consulting': {
                'Q1': 1.3, 'Q2': 1.0, 'Q3': 0.7, 'Q4': 1.0  # New year planning
            }
        }
        
        pattern = seasonal_patterns.get(industry, {'Q1': 1.0, 'Q2': 1.0, 'Q3': 1.0, 'Q4': 1.0})
        return {k: Decimal(str(v)) for k, v in pattern.items()}
    
    def _get_market_trends(self, industry: str) -> List[str]:
        """Get current market trends"""
        trends_by_industry = {
            'technology': [
                'AI and machine learning adoption',
                'Cloud-first infrastructure',
                'Remote work technologies',
                'Cybersecurity focus',
                'API-first development'
            ],
            'healthcare': [
                'Telemedicine growth',
                'Digital health records',
                'Personalized medicine',
                'Preventive care focus',
                'Healthcare AI applications'
            ],
            'finance': [
                'Digital banking transformation',
                'Cryptocurrency adoption',
                'RegTech solutions',
                'Open banking APIs',
                'ESG investing focus'
            ]
        }
        
        return trends_by_industry.get(industry, ['Digital transformation', 'Sustainability focus', 'Customer experience improvement'])
    
    def _get_market_opportunities(self, industry: str, investment: Decimal) -> List[str]:
        """Get market opportunities"""
        opportunities = [
            'Underserved customer segments',
            'Geographic expansion potential',
            'Product line extensions',
            'Strategic partnerships',
            'Technology integration opportunities'
        ]
        
        if investment > Decimal('1000000'):
            opportunities.append('Market consolidation opportunities')
            opportunities.append('Acquisition possibilities')
            
        return opportunities[:4]  # Return top 4
    
    def _get_market_threats(self, industry: str) -> List[str]:
        """Get market threats"""
        threat_map = {
            'technology': ['New competitor entry', 'Technology obsolescence', 'Talent shortage'],
            'healthcare': ['Regulatory changes', 'Compliance costs', 'Privacy concerns'],
            'finance': ['Economic volatility', 'Regulatory scrutiny', 'Fintech disruption'],
            'retail': ['E-commerce competition', 'Changing consumer behavior', 'Supply chain issues']
        }
        
        return threat_map.get(industry, ['Economic downturn', 'Increased competition', 'Regulatory changes'])
    
    def _get_barriers_to_entry(self, industry: str, project_type: str) -> List[str]:
        """Get barriers to entry"""
        barriers = {
            'technology': ['Technical expertise required', 'High R&D costs', 'Network effects'],
            'healthcare': ['Regulatory approval', 'Clinical trials', 'Safety requirements'],
            'finance': ['Regulatory compliance', 'Capital requirements', 'Trust and reputation']
        }
        
        return barriers.get(industry, ['Capital requirements', 'Regulatory compliance', 'Brand recognition'])
    
    def _get_competitive_threats(self, industry: str, company_size: str) -> List[str]:
        """Get competitive threats"""
        base_threats = ['Price competition', 'New market entrants', 'Technology disruption']
        
        if company_size in ['startup', 'small']:
            base_threats.extend(['Large competitor response', 'Resource limitations'])
        else:
            base_threats.extend(['Agile startup competition', 'Innovation lag'])
            
        return base_threats[:4]
    
    def _get_risk_mitigation(self, industry: str, project_type: str) -> List[str]:
        """Get risk mitigation strategies"""
        return [
            'Diversify revenue streams',
            'Build strategic partnerships',
            'Maintain cash reserves',
            'Implement agile development',
            'Regular market monitoring'
        ]
    
    def _get_contingency_plans(self, industry: str, project_type: str) -> List[str]:
        """Get contingency plans"""
        return [
            'Pivot to adjacent markets',
            'Adjust pricing strategy',
            'Reduce operational costs',
            'Seek additional funding',
            'Form strategic alliances'
        ]
    
    def _generate_recommendations(self, market: MarketAnalysis, competitive: CompetitiveAnalysis,
                                financial: FinancialMetrics, risk: RiskAnalysis) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Market-based recommendations
        if market.growth_rate > Decimal('0.10'):
            recommendations.append('Accelerate market entry to capture high growth opportunity')
        
        if market.competition_level in ['High', 'Very High']:
            recommendations.append('Focus on differentiation and unique value proposition')
        
        # Financial recommendations
        if financial.customer_acquisition_cost > financial.lifetime_value / Decimal('3'):
            recommendations.append('Optimize customer acquisition channels to reduce CAC')
        
        if financial.gross_margin < Decimal('40'):
            recommendations.append('Improve operational efficiency to increase margins')
        
        # Risk-based recommendations
        if risk.overall_risk > Decimal('60'):
            recommendations.append('Implement comprehensive risk management framework')
        
        if risk.execution_risk > Decimal('50'):
            recommendations.append('Strengthen project management and execution capabilities')
        
        # Competitive recommendations
        if competitive.differentiation_score < Decimal('6'):
            recommendations.append('Enhance product differentiation and competitive positioning')
        
        # Default recommendations if none added
        if not recommendations:
            recommendations = [
                'Monitor key performance indicators closely',
                'Build strong customer relationships',
                'Maintain financial discipline'
            ]
        
        return recommendations[:5]  # Return top 5
    
    def _set_kpi_targets(self, investment: Decimal, roi_result: Any, timeline_months: int) -> Dict[str, Any]:
        """Set realistic KPI targets"""
        return {
            'monthly_revenue_target': float(roi_result.projected_revenue / Decimal(str(timeline_months))),
            'customer_acquisition_target': random.randint(50, 500),
            'gross_margin_target': random.uniform(45, 75),
            'cash_burn_target': float(investment / Decimal(str(timeline_months * 2))),
            'market_share_target': random.uniform(0.5, 5.0),
            'roi_milestone': float(roi_result.roi_percentage * Decimal('0.5'))  # 50% of projected ROI
        }
    
    def _create_milestone_plan(self, timeline_months: int, investment: Decimal) -> List[Dict[str, Any]]:
        """Create realistic milestone plan"""
        milestones = []
        
        # Key milestones at different timeline points
        milestone_points = [0.25, 0.5, 0.75, 1.0]  # 25%, 50%, 75%, 100%
        milestone_names = ['MVP Launch', 'Market Validation', 'Scale Preparation', 'Full Launch']
        
        for i, (point, name) in enumerate(zip(milestone_points, milestone_names)):
            month = int(timeline_months * point)
            milestone = {
                'month': month,
                'name': name,
                'description': f'{name} - Key project milestone',
                'success_criteria': f'Achieve {int(point * 100)}% of project objectives',
                'budget_allocated': float(investment * Decimal(str(point * 0.3)))  # 30% budget distribution
            }
            milestones.append(milestone)
        
        return milestones