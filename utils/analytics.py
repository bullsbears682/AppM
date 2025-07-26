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
    market_size: float
    growth_rate: float
    competition_level: str
    market_maturity: str
    seasonal_factors: Dict[str, float]
    key_trends: List[str]
    opportunities: List[str]
    threats: List[str]

@dataclass
class CompetitiveAnalysis:
    """Competitive landscape analysis"""
    market_share_potential: float
    competitive_advantage: str
    differentiation_score: float
    pricing_power: str
    barriers_to_entry: List[str]
    competitive_threats: List[str]

@dataclass
class FinancialMetrics:
    """Enhanced financial metrics"""
    customer_acquisition_cost: float
    lifetime_value: float
    gross_margin: float
    operating_margin: float
    working_capital_needs: float
    burn_rate: float
    runway_months: int
    break_even_units: int

@dataclass
class RiskAnalysis:
    """Comprehensive risk analysis"""
    market_risk: float
    execution_risk: float
    financial_risk: float
    regulatory_risk: float
    technology_risk: float
    overall_risk: float
    risk_mitigation: List[str]
    contingency_plans: List[str]

@dataclass
class BusinessIntelligence:
    """Complete business intelligence package"""
    market_analysis: MarketAnalysis
    competitive_analysis: CompetitiveAnalysis
    financial_metrics: FinancialMetrics
    risk_analysis: RiskAnalysis
    success_probability: float
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
            market_analysis, competitive_analysis, financial_metrics, risk_analysis,
            industry, project_type, company_size, investment, timeline_months
        )
        
        # KPI Targets
        kpi_targets = self._set_kpi_targets(investment, roi_result, timeline_months,
                        industry, project_type, company_size)
        
        # Milestones
        milestones = self._create_milestone_plan(timeline_months, investment, industry, project_type, company_size)
        
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
    
    def generate_ai_powered_insights(self, investment: Decimal, industry: str, project_type: str,
                                   company_size: str, timeline_months: int, roi_result: Any,
                                   market_analysis: MarketAnalysis, competitive_analysis: CompetitiveAnalysis,
                                   financial_metrics: FinancialMetrics, risk_analysis: RiskAnalysis) -> Dict[str, Any]:
        """Generate AI-powered business insights using advanced analytics"""
        
        # Predictive Analytics
        future_scenarios = self._generate_future_scenarios(
            investment, industry, project_type, timeline_months, roi_result
        )
        
        # Market Intelligence
        market_intelligence = self._analyze_market_intelligence(
            industry, market_analysis, competitive_analysis
        )
        
        # Success Probability Matrix
        success_matrix = self._calculate_success_probability_matrix(
            financial_metrics, risk_analysis, market_analysis
        )
        
        # Investment Optimization Recommendations
        optimization_insights = self._generate_investment_optimization(
            investment, financial_metrics, risk_analysis, timeline_months
        )
        
        # Competitive Intelligence
        competitive_intelligence = self._analyze_competitive_landscape(
            industry, competitive_analysis, financial_metrics
        )
        
        # Financial Health Score
        financial_health_score = self._calculate_financial_health_score(
            financial_metrics, risk_analysis, float(roi_result.roi_percentage)
        )
        
        return {
            'future_scenarios': future_scenarios,
            'market_intelligence': market_intelligence,
            'success_matrix': success_matrix,
            'optimization_insights': optimization_insights,
            'competitive_intelligence': competitive_intelligence,
            'financial_health_score': financial_health_score,
            'predictive_alerts': self._generate_predictive_alerts(
                financial_metrics, risk_analysis, market_analysis
            )
        }
    
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
            market_size=float(market_size),
            growth_rate=float(growth_rate),
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
            market_share_potential=float(market_share_potential),
            competitive_advantage=competitive_advantage,
            differentiation_score=float(differentiation_score),
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
            customer_acquisition_cost=float(customer_acquisition_cost.quantize(Decimal('0.01'))),
            lifetime_value=float(lifetime_value.quantize(Decimal('0.01'))),
            gross_margin=float(gross_margin.quantize(Decimal('0.1'))),
            operating_margin=float(operating_margin.quantize(Decimal('0.1'))),
            working_capital_needs=float(working_capital_needs.quantize(Decimal('0.01'))),
            burn_rate=float(burn_rate.quantize(Decimal('0.01'))),
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
            market_risk=float(market_risk.quantize(Decimal('0.1'))),
            execution_risk=float(execution_risk.quantize(Decimal('0.1'))),
            financial_risk=float(financial_risk.quantize(Decimal('0.1'))),
            regulatory_risk=float(regulatory_risk.quantize(Decimal('0.1'))),
            technology_risk=float(technology_risk.quantize(Decimal('0.1'))),
            overall_risk=float(overall_risk.quantize(Decimal('0.1'))),
            risk_mitigation=mitigation,
            contingency_plans=contingency
        )
    
    def _calculate_success_probability(self, market: MarketAnalysis, competitive: CompetitiveAnalysis,
                                     financial: FinancialMetrics, risk: RiskAnalysis) -> float:
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
        if financial.lifetime_value > financial.customer_acquisition_cost * 4:
            base_prob += 15  # Healthy LTV/CAC ratio
        elif financial.lifetime_value < financial.customer_acquisition_cost * 3:
            base_prob -= 10  # Poor unit economics
            
        # Risk adjustment
        risk_adjustment = risk.overall_risk * -0.3  # Higher risk reduces probability
        base_prob += risk_adjustment
        
        # Differentiation bonus
        if competitive.differentiation_score > 7:
            base_prob += 10
        elif competitive.differentiation_score < 5:
            base_prob -= 5
            
        # Ensure probability is between 10% and 85%
        final_prob = max(10, min(85, base_prob))
        
        return float(Decimal(str(final_prob)).quantize(Decimal('0.1')))
    
    # Helper methods for generating realistic business data
    def _get_seasonal_factors(self, industry: str) -> Dict[str, float]:
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
        return pattern  # Already floats, no need for Decimal conversion
    
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
                                financial: FinancialMetrics, risk: RiskAnalysis, industry: str = None,
                                project_type: str = None, company_size: str = None, 
                                investment: Decimal = None, timeline_months: int = None) -> List[str]:
        """Generate dynamic, context-specific actionable recommendations"""
        recommendations = []
        
        # Industry-specific strategic recommendations
        industry_strategies = {
            'fintech': {
                'high_priority': ['Ensure regulatory compliance from day one', 'Implement enterprise-grade security'],
                'growth': ['Partner with traditional financial institutions', 'Focus on customer trust and transparency'],
                'risk': ['Maintain regulatory buffer in budget', 'Establish compliance monitoring systems']
            },
            'healthtech': {
                'high_priority': ['Prioritize patient data security', 'Obtain necessary medical certifications'],
                'growth': ['Build relationships with healthcare providers', 'Focus on clinical validation'],
                'risk': ['Plan for extended regulatory approval timelines', 'Maintain patient safety protocols']
            },
            'saas': {
                'high_priority': ['Focus on product-market fit', 'Build scalable infrastructure'],
                'growth': ['Implement strong customer success programs', 'Optimize for recurring revenue'],
                'risk': ['Monitor customer churn closely', 'Maintain competitive feature development']
            },
            'ecommerce': {
                'high_priority': ['Optimize conversion funnel', 'Build efficient logistics network'],
                'growth': ['Implement personalization engines', 'Expand payment options'],
                'risk': ['Monitor customer acquisition costs', 'Maintain inventory turnover efficiency']
            }
        }
        
        # Project type specific tactical recommendations
        project_tactics = {
            'product_development': {
                'execution': ['Implement agile development methodologies', 'Establish user feedback loops'],
                'market': ['Validate features through customer interviews', 'Build minimum viable product first'],
                'scaling': ['Plan for technical debt management', 'Design for scalability from start']
            },
            'digital_transformation': {
                'execution': ['Ensure comprehensive staff training', 'Phase implementation to minimize disruption'],
                'market': ['Communicate transformation benefits clearly', 'Measure efficiency gains continuously'],
                'scaling': ['Build change management capabilities', 'Establish digital excellence centers']
            },
            'market_expansion': {
                'execution': ['Conduct thorough market research', 'Adapt offerings to local preferences'],
                'market': ['Build local partnerships strategically', 'Understand regulatory differences'],
                'scaling': ['Develop scalable market entry processes', 'Create regional management structures']
            }
        }
        
        # Company size specific operational recommendations
        size_operations = {
            'startup': {
                'resource': ['Prioritize revenue-generating activities', 'Maintain lean operations'],
                'talent': ['Focus on multi-skilled team members', 'Establish advisor network'],
                'funding': ['Prepare for multiple funding rounds', 'Maintain detailed financial tracking']
            },
            'small': {
                'resource': ['Implement efficient project management systems', 'Automate routine processes'],
                'talent': ['Invest in employee development', 'Build specialized roles gradually'],
                'funding': ['Optimize cash flow management', 'Plan for sustainable growth']
            },
            'enterprise': {
                'resource': ['Leverage existing infrastructure synergies', 'Implement enterprise governance'],
                'talent': ['Utilize internal expertise networks', 'Establish cross-functional teams'],
                'funding': ['Align with strategic portfolio objectives', 'Ensure adequate resource allocation']
            }
        }
        
        # Get context-specific recommendations
        industry_config = industry_strategies.get(industry, industry_strategies.get('saas', {}))
        project_config = project_tactics.get(project_type, project_tactics.get('product_development', {}))
        size_config = size_operations.get(company_size, size_operations.get('small', {}))
        
        # Priority-based recommendation selection
        priority_recommendations = []
        
        # High-priority industry recommendations
        if industry_config.get('high_priority'):
            priority_recommendations.extend(industry_config['high_priority'][:2])
        
        # Critical risk-based recommendations
        if risk.overall_risk > Decimal('70'):
            priority_recommendations.append('Implement comprehensive risk mitigation framework immediately')
            if industry_config.get('risk'):
                priority_recommendations.extend(industry_config['risk'][:1])
        elif risk.overall_risk > Decimal('50'):
            if industry_config.get('risk'):
                priority_recommendations.extend(industry_config['risk'][:1])
        
        # Financial health recommendations
        if financial.customer_acquisition_cost > financial.lifetime_value / 2:
            priority_recommendations.append('Urgently optimize customer acquisition channels to improve LTV/CAC ratio')
        elif financial.customer_acquisition_cost > financial.lifetime_value / 3:
            priority_recommendations.append('Optimize customer acquisition channels to reduce CAC')
        
        if financial.gross_margin < 30:
            priority_recommendations.append('Critical: Improve operational efficiency to achieve sustainable margins')
        elif financial.gross_margin < 40:
            priority_recommendations.append('Improve operational efficiency to increase margins')
        
        # Market opportunity recommendations
        if market.growth_rate > 0.15:
            if industry_config.get('growth'):
                priority_recommendations.extend(industry_config['growth'][:1])
            priority_recommendations.append('Accelerate market entry to capture exceptional growth opportunity')
        elif market.growth_rate > 0.10:
            priority_recommendations.append('Capitalize on strong market growth through focused expansion')
        
        # Competitive positioning
        if competitive.differentiation_score < 5:
            priority_recommendations.append('Urgently enhance product differentiation and competitive positioning')
        elif competitive.differentiation_score < 7:
            priority_recommendations.append('Strengthen unique value proposition and competitive advantages')
        
        # Execution and operational recommendations
        if project_config.get('execution'):
            priority_recommendations.extend(project_config['execution'][:1])
        
        if size_config.get('resource'):
            priority_recommendations.extend(size_config['resource'][:1])
        
        # Timeline and investment specific recommendations
        if timeline_months and timeline_months < 18:
            priority_recommendations.append('Focus on rapid execution and quick wins given tight timeline')
        elif timeline_months and timeline_months > 36:
            priority_recommendations.append('Implement phased approach with clear intermediate milestones')
        
        if investment:
            investment_float = float(investment)
            if investment_float < 100000:
                priority_recommendations.append('Maximize ROI through lean startup methodology and MVP approach')
            elif investment_float > 1000000:
                priority_recommendations.append('Leverage significant investment for competitive advantages and market leadership')
        
        # Remove duplicates while preserving order
        unique_recommendations = []
        seen = set()
        for rec in priority_recommendations:
            if rec not in seen:
                unique_recommendations.append(rec)
                seen.add(rec)
        
        # Ensure we have enough recommendations
        if len(unique_recommendations) < 3:
            # Add context-appropriate fallback recommendations
            fallback_recs = [
                f'Focus on {industry} industry best practices and compliance',
                f'Implement {project_type} specific methodologies and frameworks',
                f'Leverage {company_size} company advantages for competitive positioning'
            ]
            for rec in fallback_recs:
                if rec not in seen and len(unique_recommendations) < 5:
                    unique_recommendations.append(rec)
        
        return unique_recommendations[:5]  # Return top 5 recommendations
    
    def _set_kpi_targets(self, investment: Decimal, roi_result: Any, timeline_months: int,
                        industry: str = None, project_type: str = None, company_size: str = None) -> Dict[str, Any]:
        """Set realistic, context-specific KPI targets"""
        
        # Industry benchmarks for key metrics
        industry_benchmarks = {
            'saas': {
                'customer_acquisition_multiplier': 2.5, 'gross_margin_range': (60, 80),
                'monthly_growth_rate': 0.15, 'churn_target': 5.0
            },
            'fintech': {
                'customer_acquisition_multiplier': 1.8, 'gross_margin_range': (45, 65),
                'monthly_growth_rate': 0.12, 'churn_target': 3.0
            },
            'healthtech': {
                'customer_acquisition_multiplier': 1.2, 'gross_margin_range': (50, 70),
                'monthly_growth_rate': 0.08, 'churn_target': 2.0
            },
            'ecommerce': {
                'customer_acquisition_multiplier': 3.0, 'gross_margin_range': (25, 45),
                'monthly_growth_rate': 0.20, 'churn_target': 8.0
            }
        }
        
        # Company size factors for scaling targets
        size_factors = {
            'startup': {'scale_factor': 0.5, 'growth_ambition': 1.5, 'risk_tolerance': 1.3},
            'small': {'scale_factor': 0.8, 'growth_ambition': 1.2, 'risk_tolerance': 1.1},
            'medium': {'scale_factor': 1.0, 'growth_ambition': 1.0, 'risk_tolerance': 1.0},
            'large': {'scale_factor': 1.5, 'growth_ambition': 0.8, 'risk_tolerance': 0.8},
            'enterprise': {'scale_factor': 2.0, 'growth_ambition': 0.6, 'risk_tolerance': 0.7}
        }
        
        # Project type specific KPI focus
        project_kpis = {
            'product_development': {
                'primary_kpis': ['user_adoption', 'feature_completion', 'customer_satisfaction'],
                'revenue_timing': 0.6  # Revenue expected at 60% of timeline
            },
            'market_expansion': {
                'primary_kpis': ['market_penetration', 'customer_acquisition', 'regional_revenue'],
                'revenue_timing': 0.4  # Revenue expected at 40% of timeline
            },
            'digital_transformation': {
                'primary_kpis': ['process_efficiency', 'cost_savings', 'user_adoption'],
                'revenue_timing': 0.8  # Revenue expected at 80% of timeline (efficiency gains)
            },
            'ai_integration': {
                'primary_kpis': ['model_accuracy', 'automation_rate', 'efficiency_gains'],
                'revenue_timing': 0.7  # Revenue expected at 70% of timeline
            }
        }
        
        # Get context configurations
        industry_config = industry_benchmarks.get(industry, industry_benchmarks['saas'])
        size_config = size_factors.get(company_size, size_factors['medium'])
        project_config = project_kpis.get(project_type, project_kpis['product_development'])
        
        # Calculate context-specific targets
        monthly_revenue_target = float(roi_result.projected_revenue / Decimal(str(timeline_months)))
        
        # Customer acquisition target based on industry and size
        base_customers = int(float(investment) / 1000 * industry_config['customer_acquisition_multiplier'])
        customer_acquisition_target = int(base_customers * size_config['scale_factor'])
        
        # Gross margin target based on industry benchmarks
        margin_range = industry_config['gross_margin_range']
        gross_margin_target = margin_range[0] + (margin_range[1] - margin_range[0]) * size_config['growth_ambition']
        
        # Cash burn target based on company size and risk tolerance
        optimal_burn_months = 18 * size_config['risk_tolerance']  # Runway consideration
        cash_burn_target = float(investment / Decimal(str(optimal_burn_months)))
        
        # Market share target based on industry and company size
        base_market_share = {
            'startup': 0.1, 'small': 0.5, 'medium': 2.0, 'large': 5.0, 'enterprise': 10.0
        }
        market_share_target = base_market_share.get(company_size, 2.0) * industry_config['monthly_growth_rate'] * 10
        
        # ROI milestone based on project timing and risk
        roi_milestone_timing = project_config['revenue_timing']
        roi_milestone = float(roi_result.roi_percentage * Decimal(str(roi_milestone_timing)))
        
        return {
            'monthly_revenue_target': monthly_revenue_target,
            'customer_acquisition_target': customer_acquisition_target,
            'gross_margin_target': gross_margin_target,
            'cash_burn_target': cash_burn_target,
            'market_share_target': market_share_target,
            'roi_milestone': roi_milestone,
            'primary_focus_areas': project_config['primary_kpis'],
            'industry_benchmark_margin': f"{margin_range[0]}-{margin_range[1]}%",
            'target_customer_churn': industry_config['churn_target'],
            'monthly_growth_rate_target': industry_config['monthly_growth_rate'] * 100
        }
    
    def _create_milestone_plan(self, timeline_months: int, investment: Decimal, industry: str = None, 
                              project_type: str = None, company_size: str = None) -> List[Dict[str, Any]]:
        """Create dynamic, project-specific milestone plan"""
        milestones = []
        
        # Industry-specific milestone frameworks
        industry_milestones = {
            'fintech': {
                'phases': ['Regulatory Compliance', 'MVP Development', 'Security Audit', 'Market Launch'],
                'focus': ['compliance', 'security', 'user_acquisition', 'scaling']
            },
            'healthtech': {
                'phases': ['Research & Development', 'Clinical Validation', 'Regulatory Approval', 'Commercial Launch'],
                'focus': ['research', 'validation', 'approval', 'adoption']
            },
            'saas': {
                'phases': ['Product Development', 'Beta Testing', 'Customer Acquisition', 'Revenue Scaling'],
                'focus': ['development', 'testing', 'growth', 'expansion']
            },
            'ecommerce': {
                'phases': ['Platform Development', 'Inventory Setup', 'Marketing Launch', 'Customer Retention'],
                'focus': ['platform', 'operations', 'marketing', 'loyalty']
            },
            'manufacturing': {
                'phases': ['Production Setup', 'Quality Control', 'Distribution Network', 'Market Penetration'],
                'focus': ['production', 'quality', 'logistics', 'sales']
            }
        }
        
        # Project type specific success criteria
        project_criteria = {
            'product_development': {
                'metrics': ['feature completion', 'user feedback score', 'market readiness', 'revenue generation'],
                'kpis': ['development velocity', 'quality metrics', 'customer satisfaction', 'market penetration']
            },
            'digital_transformation': {
                'metrics': ['system integration', 'user adoption', 'efficiency gains', 'cost savings'],
                'kpis': ['automation rate', 'user training', 'process optimization', 'ROI achievement']
            },
            'market_expansion': {
                'metrics': ['market research', 'local partnerships', 'customer acquisition', 'revenue growth'],
                'kpis': ['market share', 'customer base', 'revenue per market', 'expansion efficiency']
            },
            'ai_integration': {
                'metrics': ['AI model development', 'integration testing', 'performance optimization', 'deployment'],
                'kpis': ['model accuracy', 'system performance', 'user adoption', 'efficiency gains']
            }
        }
        
        # Company size influences milestone complexity and budget allocation
        size_factors = {
            'startup': {'complexity': 0.7, 'budget_ratio': [0.4, 0.3, 0.2, 0.1], 'risk_buffer': 0.3},
            'small': {'complexity': 0.8, 'budget_ratio': [0.3, 0.3, 0.25, 0.15], 'risk_buffer': 0.25},
            'medium': {'complexity': 1.0, 'budget_ratio': [0.25, 0.3, 0.3, 0.15], 'risk_buffer': 0.2},
            'large': {'complexity': 1.2, 'budget_ratio': [0.2, 0.3, 0.35, 0.15], 'risk_buffer': 0.15},
            'enterprise': {'complexity': 1.5, 'budget_ratio': [0.15, 0.25, 0.4, 0.2], 'risk_buffer': 0.1}
        }
        
        # Get context-specific configurations
        industry_config = industry_milestones.get(industry, industry_milestones['saas'])
        project_config = project_criteria.get(project_type, project_criteria['product_development'])
        size_config = size_factors.get(company_size, size_factors['medium'])
        
        # Dynamic milestone timing based on project complexity
        base_points = [0.25, 0.5, 0.75, 1.0]
        if size_config['complexity'] > 1.0:
            # More complex projects need earlier checkpoints
            milestone_points = [0.2, 0.45, 0.7, 1.0]
        else:
            milestone_points = base_points
        
        milestone_names = industry_config['phases']
        milestone_focus = industry_config['focus']
        success_metrics = project_config['metrics']
        kpi_areas = project_config['kpis']
        
        for i, (point, name, focus, metric, kpi) in enumerate(zip(
            milestone_points, milestone_names, milestone_focus, success_metrics, kpi_areas)):
            
            month = max(1, int(timeline_months * point))
            
            # Dynamic success criteria based on context
            success_criteria = self._generate_success_criteria(focus, metric, kpi, point, industry, project_type)
            
            # Dynamic budget allocation
            budget_allocated = float(investment * Decimal(str(size_config['budget_ratio'][i])))
            
            # Context-specific descriptions
            description = self._generate_milestone_description(name, focus, industry, project_type, company_size)
            
            milestone = {
                'month': month,
                'name': name,
                'description': description,
                'success_criteria': success_criteria,
                'budget_allocated': budget_allocated,
                'focus_area': focus,
                'key_metrics': [metric, kpi],
                'risk_level': self._calculate_milestone_risk(point, size_config['risk_buffer']),
                'deliverables': self._generate_deliverables(focus, project_type, industry)
            }
            milestones.append(milestone)
        
        return milestones
    
    def _generate_success_criteria(self, focus: str, metric: str, kpi: str, completion: float, 
                                 industry: str, project_type: str) -> str:
        """Generate specific success criteria for each milestone"""
        completion_pct = int(completion * 100)
        
        criteria_templates = {
            'development': f'Complete {completion_pct}% of {metric} with {kpi} meeting quality standards',
            'testing': f'Achieve {completion_pct}% {metric} coverage with {kpi} validation',
            'compliance': f'Obtain {completion_pct}% regulatory compliance for {metric}',
            'marketing': f'Reach {completion_pct}% of target {metric} through {kpi} optimization',
            'scaling': f'Scale {metric} to {completion_pct}% capacity with sustainable {kpi}',
            'research': f'Complete {completion_pct}% of {metric} research with validated {kpi}',
            'validation': f'Validate {completion_pct}% of {metric} hypotheses through {kpi} testing',
            'security': f'Implement {completion_pct}% of {metric} security measures with {kpi} compliance'
        }
        
        return criteria_templates.get(focus, f'Achieve {completion_pct}% completion of {metric} objectives')
    
    def _generate_milestone_description(self, name: str, focus: str, industry: str, 
                                      project_type: str, company_size: str) -> str:
        """Generate context-specific milestone descriptions"""
        
        # Industry-specific contexts
        industry_contexts = {
            'fintech': 'financial services compliance and security',
            'healthtech': 'healthcare regulations and patient safety',
            'saas': 'software scalability and user experience',
            'ecommerce': 'customer journey and conversion optimization',
            'manufacturing': 'production efficiency and quality control'
        }
        
        # Project type specific activities
        project_activities = {
            'product_development': 'innovative product features and market fit',
            'digital_transformation': 'digital process automation and efficiency',
            'market_expansion': 'new market penetration and customer acquisition',
            'ai_integration': 'AI capabilities and intelligent automation'
        }
        
        context = industry_contexts.get(industry, 'business objectives')
        activity = project_activities.get(project_type, 'strategic goals')
        
        return f'{name} milestone focusing on {context} while advancing {activity}'
    
    def _calculate_milestone_risk(self, completion: float, base_risk: float) -> str:
        """Calculate risk level for each milestone"""
        # Early milestones are typically higher risk
        risk_multiplier = 1.5 - completion  # Higher risk for earlier milestones
        total_risk = base_risk * risk_multiplier
        
        if total_risk < 0.2:
            return 'Low'
        elif total_risk < 0.4:
            return 'Medium'
        else:
            return 'High'
    
    def _generate_deliverables(self, focus: str, project_type: str, industry: str) -> List[str]:
        """Generate specific deliverables for each milestone"""
        
        deliverable_matrix = {
            ('development', 'product_development', 'saas'): [
                'Core feature implementation', 'API documentation', 'Testing framework'
            ],
            ('testing', 'product_development', 'saas'): [
                'Beta user feedback', 'Performance benchmarks', 'Security audit results'
            ],
            ('compliance', 'fintech', 'product_development'): [
                'Regulatory compliance documentation', 'Security certificates', 'Audit reports'
            ],
            ('marketing', 'market_expansion', 'ecommerce'): [
                'Market research report', 'Customer acquisition strategy', 'Brand positioning'
            ]
        }
        
        # Try specific combination first, then fallback to generic
        key = (focus, project_type, industry)
        if key in deliverable_matrix:
            return deliverable_matrix[key]
        
        # Generic deliverables based on focus
        generic_deliverables = {
            'development': ['Technical specifications', 'Development milestones', 'Quality metrics'],
            'testing': ['Test results', 'User feedback', 'Performance data'],
            'compliance': ['Compliance documentation', 'Certification status', 'Risk assessment'],
            'marketing': ['Marketing materials', 'Customer insights', 'Campaign metrics'],
            'scaling': ['Scalability plan', 'Resource allocation', 'Growth metrics']
        }
        
        return generic_deliverables.get(focus, ['Project deliverables', 'Progress report', 'Next phase planning'])
    
    def _generate_future_scenarios(self, investment: Decimal, industry: str, 
                                 project_type: str, timeline_months: int, roi_result: Any) -> Dict[str, Any]:
        """Generate predictive future scenarios"""
        
        base_revenue = float(roi_result.projected_revenue)
        base_roi = float(roi_result.roi_percentage)
        
        # Scenario modeling
        scenarios = {
            'optimistic': {
                'probability': 25,
                'revenue_multiplier': 1.4,
                'roi_boost': 15,
                'description': 'Market conditions exceed expectations',
                'key_drivers': ['Strong market adoption', 'Competitor delays', 'Economic growth']
            },
            'realistic': {
                'probability': 50,
                'revenue_multiplier': 1.0,
                'roi_boost': 0,
                'description': 'Expected market performance',
                'key_drivers': ['Normal market conditions', 'Planned execution', 'Stable economy']
            },
            'pessimistic': {
                'probability': 25,
                'revenue_multiplier': 0.7,
                'roi_boost': -10,
                'description': 'Market challenges and setbacks',
                'key_drivers': ['Market saturation', 'Increased competition', 'Economic headwinds']
            }
        }
        
        # Calculate scenario outcomes
        for scenario_name, scenario in scenarios.items():
            scenario['projected_revenue'] = base_revenue * scenario['revenue_multiplier']
            scenario['projected_roi'] = max(0, base_roi + scenario['roi_boost'])
            scenario['investment_recovery_months'] = self._calculate_recovery_time(
                float(investment), scenario['projected_revenue'], timeline_months
            )
        
        return {
            'scenarios': scenarios,
            'recommended_strategy': self._recommend_strategy_based_on_scenarios(scenarios),
            'risk_mitigation_timeline': self._generate_risk_timeline(timeline_months)
        }
    
    def _analyze_market_intelligence(self, industry: str, market_analysis: MarketAnalysis,
                                   competitive_analysis: CompetitiveAnalysis) -> Dict[str, Any]:
        """Advanced market intelligence analysis"""
        
        # Market maturity analysis
        maturity_insights = {
            'Growth': {
                'opportunity_score': 85,
                'entry_difficulty': 'Medium',
                'recommended_approach': 'Aggressive expansion',
                'key_strategies': ['First-mover advantage', 'Rapid scaling', 'Market education']
            },
            'Mature': {
                'opportunity_score': 60,
                'entry_difficulty': 'High',
                'recommended_approach': 'Differentiation focus',
                'key_strategies': ['Niche targeting', 'Innovation', 'Customer loyalty']
            },
            'Declining': {
                'opportunity_score': 30,
                'entry_difficulty': 'Low',
                'recommended_approach': 'Cost leadership',
                'key_strategies': ['Efficiency optimization', 'Consolidation', 'Exit strategy']
            }
        }
        
        current_maturity = maturity_insights.get(market_analysis.market_maturity, 
                                               maturity_insights['Growth'])
        
        # Competitive landscape scoring
        competition_impact = {
            'Low': {'threat_level': 20, 'market_share_potential': 15},
            'Medium': {'threat_level': 50, 'market_share_potential': 8},
            'High': {'threat_level': 80, 'market_share_potential': 3},
            'Very High': {'threat_level': 95, 'market_share_potential': 1}
        }
        
        comp_impact = competition_impact.get(market_analysis.competition_level,
                                           competition_impact['Medium'])
        
        return {
            'market_maturity_insights': current_maturity,
            'competitive_pressure': comp_impact,
            'market_timing_score': self._calculate_market_timing_score(
                market_analysis.growth_rate, market_analysis.competition_level
            ),
            'entry_barriers': self._analyze_entry_barriers(industry, competitive_analysis),
            'market_dynamics': self._analyze_market_dynamics(market_analysis)
        }
    
    def _calculate_success_probability_matrix(self, financial_metrics: FinancialMetrics,
                                            risk_analysis: RiskAnalysis, market_analysis: MarketAnalysis) -> Dict[str, Any]:
        """Calculate multi-dimensional success probability"""
        
        # Financial strength assessment
        financial_score = self._score_financial_strength(financial_metrics)
        
        # Risk tolerance assessment
        risk_score = 100 - risk_analysis.overall_risk
        
        # Market opportunity assessment
        market_score = market_analysis.growth_rate * 100
        
        # Weighted success probability
        weights = {'financial': 0.4, 'risk': 0.3, 'market': 0.3}
        overall_score = (
            financial_score * weights['financial'] +
            risk_score * weights['risk'] +
            market_score * weights['market']
        )
        
        # Success probability tiers
        if overall_score >= 80:
            tier = 'Excellent'
            confidence = 'Very High'
        elif overall_score >= 65:
            tier = 'Good'
            confidence = 'High'
        elif overall_score >= 50:
            tier = 'Fair'
            confidence = 'Medium'
        elif overall_score >= 35:
            tier = 'Poor'
            confidence = 'Low'
        else:
            tier = 'Critical'
            confidence = 'Very Low'
        
        return {
            'overall_score': round(overall_score, 1),
            'tier': tier,
            'confidence_level': confidence,
            'component_scores': {
                'financial_strength': round(financial_score, 1),
                'risk_management': round(risk_score, 1),
                'market_opportunity': round(market_score, 1)
            },
            'improvement_recommendations': self._generate_improvement_recommendations(
                financial_score, risk_score, market_score
            )
        }
    
    def _generate_investment_optimization(self, investment: Decimal, financial_metrics: FinancialMetrics,
                                        risk_analysis: RiskAnalysis, timeline_months: int) -> Dict[str, Any]:
        """Generate investment optimization insights"""
        
        current_runway = financial_metrics.runway_months
        optimal_runway = max(12, timeline_months * 1.5)  # 1.5x project timeline
        
        # Investment adequacy analysis
        if current_runway < optimal_runway:
            adequacy = 'Insufficient'
            additional_needed = (optimal_runway - current_runway) * financial_metrics.burn_rate
            recommendation = f'Consider additional ${additional_needed:,.0f} funding'
        elif current_runway > optimal_runway * 2:
            adequacy = 'Excess'
            excess_amount = (current_runway - optimal_runway) * financial_metrics.burn_rate
            recommendation = f'${excess_amount:,.0f} could be allocated to growth initiatives'
        else:
            adequacy = 'Optimal'
            recommendation = 'Investment level is well-balanced for project goals'
        
        # ROI optimization opportunities
        roi_optimization = []
        
        # CAC optimization
        if financial_metrics.lifetime_value / financial_metrics.customer_acquisition_cost < 3:
            roi_optimization.append({
                'area': 'Customer Acquisition',
                'impact': 'High',
                'recommendation': 'Optimize acquisition channels to improve LTV/CAC ratio',
                'potential_improvement': '15-30% ROI increase'
            })
        
        # Operational efficiency
        if financial_metrics.gross_margin < 50:
            roi_optimization.append({
                'area': 'Operational Efficiency',
                'impact': 'Medium',
                'recommendation': 'Streamline operations to improve gross margins',
                'potential_improvement': '10-20% ROI increase'
            })
        
        return {
            'investment_adequacy': adequacy,
            'runway_analysis': {
                'current_months': current_runway,
                'optimal_months': optimal_runway,
                'recommendation': recommendation
            },
            'roi_optimization_opportunities': roi_optimization,
            'capital_allocation_suggestions': self._suggest_capital_allocation(
                float(investment), financial_metrics, timeline_months
            )
        }
    
    def _suggest_capital_allocation(self, investment: float, financial_metrics: FinancialMetrics, 
                                   timeline_months: int) -> Dict[str, Any]:
         """Suggest optimal capital allocation based on financial metrics"""
         
         # Basic allocation framework
         allocations = {
             'product_development': 0.40,  # 40% for core product
             'marketing_sales': 0.25,      # 25% for customer acquisition
             'operations': 0.20,           # 20% for operations
             'contingency': 0.15           # 15% buffer
         }
         
         # Adjust based on financial health
         if financial_metrics.customer_acquisition_cost > financial_metrics.lifetime_value / 3:
             # Poor CAC, reduce marketing spend
             allocations['marketing_sales'] = 0.15
             allocations['product_development'] = 0.45
             allocations['operations'] = 0.25
         
         if financial_metrics.runway_months < 12:
             # Low runway, increase contingency
             allocations['contingency'] = 0.25
             allocations['product_development'] = 0.35
             allocations['marketing_sales'] = 0.20
         
         # Calculate dollar amounts
         dollar_allocations = {
             category: investment * percentage 
             for category, percentage in allocations.items()
         }
         
         return {
             'percentages': allocations,
             'dollar_amounts': dollar_allocations,
             'recommendations': self._generate_allocation_recommendations(allocations)
         }
     
     def _generate_allocation_recommendations(self, allocations: Dict[str, float]) -> List[str]:
         """Generate recommendations based on capital allocation"""
         recommendations = []
         
         if allocations['product_development'] > 0.45:
             recommendations.append('High product investment - focus on rapid development and innovation')
         
         if allocations['marketing_sales'] < 0.20:
             recommendations.append('Conservative marketing spend - optimize for efficiency over growth')
         
         if allocations['contingency'] > 0.20:
             recommendations.append('High contingency allocation - indicates higher risk profile')
         
         return recommendations
     
     def _analyze_competitive_landscape(self, industry: str, competitive_analysis: CompetitiveAnalysis,
                                       financial_metrics: FinancialMetrics) -> Dict[str, Any]:
         """Analyze competitive landscape in detail"""
         
         # Competitive positioning
         positioning = {
             'market_position': 'Challenger' if competitive_analysis.differentiation_score < 7 else 'Leader',
             'competitive_moat': 'Strong' if competitive_analysis.differentiation_score > 8 else 'Developing',
             'pricing_strategy': competitive_analysis.pricing_power,
             'differentiation_strength': competitive_analysis.differentiation_score
         }
         
         # Threat assessment
         threat_level = 'High' if len(competitive_analysis.competitive_threats) > 3 else 'Medium'
         
         # Opportunity assessment
         opportunities = len(competitive_analysis.barriers_to_entry)
         opportunity_score = min(100, opportunities * 20)
         
         return {
             'positioning': positioning,
             'threat_assessment': {
                 'level': threat_level,
                 'threats': competitive_analysis.competitive_threats,
                 'mitigation_required': len(competitive_analysis.competitive_threats) > 2
             },
             'opportunity_score': opportunity_score,
             'strategic_recommendations': self._generate_competitive_recommendations(
                 competitive_analysis, financial_metrics
             )
         }
     
     def _generate_competitive_recommendations(self, competitive_analysis: CompetitiveAnalysis,
                                             financial_metrics: FinancialMetrics) -> List[str]:
         """Generate competitive strategy recommendations"""
         recommendations = []
         
         if competitive_analysis.differentiation_score < 6:
             recommendations.append('Focus on product differentiation and unique value proposition')
         
         if competitive_analysis.pricing_power == 'Low':
             recommendations.append('Implement cost leadership strategy or find pricing premium opportunities')
         
         if financial_metrics.customer_acquisition_cost > financial_metrics.lifetime_value / 3:
             recommendations.append('Optimize customer acquisition to compete more effectively')
         
         return recommendations
    
    def _calculate_financial_health_score(self, financial_metrics: FinancialMetrics,
                                        risk_analysis: RiskAnalysis, roi_percentage: float) -> Dict[str, Any]:
        """Calculate comprehensive financial health score"""
        
        # Individual component scores (0-100)
        scores = {}
        
        # Liquidity score
        runway_score = min(100, (financial_metrics.runway_months / 24) * 100)
        scores['liquidity'] = runway_score
        
        # Profitability score
        margin_score = min(100, financial_metrics.gross_margin * 2)  # Assuming 50% is max good margin
        scores['profitability'] = margin_score
        
        # Efficiency score
        ltv_cac_ratio = financial_metrics.lifetime_value / financial_metrics.customer_acquisition_cost
        efficiency_score = min(100, (ltv_cac_ratio / 5) * 100)  # 5x LTV/CAC is excellent
        scores['efficiency'] = efficiency_score
        
        # Growth potential score
        roi_score = min(100, max(0, roi_percentage * 2))  # 50% ROI = 100 score
        scores['growth_potential'] = roi_score
        
        # Risk management score
        risk_score = 100 - risk_analysis.overall_risk
        scores['risk_management'] = risk_score
        
        # Overall weighted score
        weights = {
            'liquidity': 0.25,
            'profitability': 0.25,
            'efficiency': 0.20,
            'growth_potential': 0.20,
            'risk_management': 0.10
        }
        
        overall_score = sum(scores[key] * weights[key] for key in scores)
        
        # Health grade
        if overall_score >= 85:
            grade = 'A+'
            status = 'Excellent'
        elif overall_score >= 75:
            grade = 'A'
            status = 'Very Good'
        elif overall_score >= 65:
            grade = 'B+'
            status = 'Good'
        elif overall_score >= 55:
            grade = 'B'
            status = 'Fair'
        elif overall_score >= 45:
            grade = 'C'
            status = 'Below Average'
        else:
            grade = 'D'
            status = 'Poor'
        
        return {
            'overall_score': round(overall_score, 1),
            'grade': grade,
            'status': status,
            'component_scores': {k: round(v, 1) for k, v in scores.items()},
            'strengths': self._identify_financial_strengths(scores),
            'weaknesses': self._identify_financial_weaknesses(scores),
            'improvement_priority': self._prioritize_financial_improvements(scores)
        }
    
    def _score_financial_strength(self, financial_metrics: FinancialMetrics) -> float:
        """Score financial strength (0-100)"""
        # This is a simplified scoring, in a real system, this would be more complex
        # based on multiple financial ratios and historical data.
        liquidity_score = min(100, (financial_metrics.runway_months / 24) * 100) # Runway
        profitability_score = min(100, financial_metrics.gross_margin * 2) # Gross Margin
        efficiency_score = min(100, (financial_metrics.lifetime_value / financial_metrics.customer_acquisition_cost) * 100) # LTV/CAC
        
        # Weighted average
        return (liquidity_score * 0.3 + profitability_score * 0.3 + efficiency_score * 0.4)
    
    def _identify_financial_strengths(self, scores: Dict[str, float]) -> List[str]:
        """Identify strengths based on component scores"""
        strengths = []
        if scores['liquidity'] >= 80:
            strengths.append('Strong liquidity position')
        if scores['profitability'] >= 80:
            strengths.append('High profitability')
        if scores['efficiency'] >= 80:
            strengths.append('Excellent LTV/CAC ratio')
        if scores['growth_potential'] >= 80:
            strengths.append('High growth potential')
        if scores['risk_management'] >= 80:
            strengths.append('Strong risk management')
        return strengths
    
    def _identify_financial_weaknesses(self, scores: Dict[str, float]) -> List[str]:
        """Identify weaknesses based on component scores"""
        weaknesses = []
        if scores['liquidity'] < 50:
            weaknesses.append('Limited runway')
        if scores['profitability'] < 50:
            weaknesses.append('Low gross margins')
        if scores['efficiency'] < 50:
            weaknesses.append('Poor LTV/CAC ratio')
        if scores['growth_potential'] < 50:
            weaknesses.append('Limited growth potential')
        if scores['risk_management'] < 50:
            weaknesses.append('Weak risk management')
        return weaknesses
    
    def _prioritize_financial_improvements(self, scores: Dict[str, float]) -> List[str]:
        """Prioritize areas for improvement based on component scores"""
        improvements = []
        if scores['liquidity'] < 70:
            improvements.append('Focus on improving runway')
        if scores['profitability'] < 70:
            improvements.append('Improve operational efficiency')
        if scores['efficiency'] < 70:
            improvements.append('Optimize customer acquisition channels')
        if scores['growth_potential'] < 70:
            improvements.append('Invest in growth initiatives')
        if scores['risk_management'] < 70:
            improvements.append('Enhance risk management framework')
        return improvements
    
    def _generate_improvement_recommendations(self, financial_score: float, risk_score: float, market_score: float) -> List[str]:
        """Generate specific recommendations for improving component scores"""
        recommendations = []
        
        if financial_score < 70:
            recommendations.append('Focus on improving financial metrics (liquidity, profitability, efficiency)')
        if risk_score < 70:
            recommendations.append('Enhance risk management and contingency planning')
        if market_score < 70:
            recommendations.append('Accelerate market entry and customer acquisition')
            
        return recommendations
    
    def _generate_predictive_alerts(self, financial_metrics: FinancialMetrics, risk_analysis: RiskAnalysis,
                                   market_analysis: MarketAnalysis) -> List[str]:
        """Generate predictive alerts based on current metrics and trends"""
        alerts = []
        
        # Liquidity alert
        if financial_metrics.runway_months < 12:
            alerts.append('High risk: Projected runway is less than 12 months. Consider additional funding.')
        elif financial_metrics.runway_months < 24:
            alerts.append('Medium risk: Projected runway is less than 24 months. Monitor cash flow closely.')
            
        # Profitability alert
        if financial_metrics.gross_margin < 40:
            alerts.append('High risk: Gross margin is below 40%. Optimize operational efficiency.')
        elif financial_metrics.gross_margin < 50:
            alerts.append('Medium risk: Gross margin is below 50%. Consider cost reduction strategies.')
            
        # Efficiency alert
        if financial_metrics.lifetime_value / financial_metrics.customer_acquisition_cost < 3:
            alerts.append('High risk: LTV/CAC ratio is less than 3. Optimize customer acquisition channels.')
        elif financial_metrics.lifetime_value / financial_metrics.customer_acquisition_cost < 5:
            alerts.append('Medium risk: LTV/CAC ratio is less than 5. Consider customer retention strategies.')
            
        # Growth potential alert
        if market_analysis.growth_rate < 0.05:
            alerts.append('High risk: Market growth rate is below 5%. Focus on market penetration and expansion.')
        elif market_analysis.growth_rate < 0.10:
            alerts.append('Medium risk: Market growth rate is below 10%. Accelerate market entry.')
            
        # Risk alert
        if risk_analysis.overall_risk > 70:
            alerts.append('High risk: Overall risk score is above 70. Implement comprehensive risk mitigation.')
        elif risk_analysis.overall_risk > 50:
            alerts.append('Medium risk: Overall risk score is above 50. Monitor risk indicators.')
            
        return alerts
    
    def _calculate_recovery_time(self, initial_investment: float, revenue: float, timeline_months: int) -> int:
        """Calculate the number of months needed to recover initial investment based on revenue."""
        if revenue <= 0:
            return float('inf') # Cannot recover if no revenue
        return int(initial_investment / revenue * timeline_months)
    
    def _recommend_strategy_based_on_scenarios(self, scenarios: Dict[str, Any]) -> str:
        """Recommend a strategy based on future scenarios."""
        optimistic_prob = scenarios['optimistic']['probability']
        realistic_prob = scenarios['realistic']['probability']
        pessimistic_prob = scenarios['pessimistic']['probability']
        
        if optimistic_prob > realistic_prob and optimistic_prob > pessimistic_prob:
            return 'Aggressive Growth Strategy'
        elif realistic_prob > optimistic_prob and realistic_prob > pessimistic_prob:
            return 'Balanced Growth Strategy'
        else:
            return 'Defensive Growth Strategy'
    
    def _generate_risk_timeline(self, timeline_months: int) -> Dict[str, Any]:
        """Generate a timeline for risk mitigation."""
        risk_mitigation_timeline = {}
        current_month = 0
        
        # High-risk mitigation (e.g., regulatory approval, security audits)
        if timeline_months > 12:
            risk_mitigation_timeline['Regulatory Approval'] = 12
            risk_mitigation_timeline['Security Audit'] = 18
            current_month = 18
            
        # Medium-risk mitigation (e.g., customer acquisition, operational efficiency)
        if timeline_months > 24:
            risk_mitigation_timeline['Customer Acquisition'] = 24
            risk_mitigation_timeline['Operational Efficiency'] = 30
            current_month = 30
            
        # Low-risk mitigation (e.g., technology upgrades, market education)
        if timeline_months > 36:
            risk_mitigation_timeline['Technology Upgrade'] = 36
            risk_mitigation_timeline['Market Education'] = 42
            current_month = 42
            
        return risk_mitigation_timeline
    
    def _calculate_market_timing_score(self, growth_rate: float, competition_level: str) -> float:
        """Score market timing based on growth rate and competition."""
        # This is a simplified scoring, in a real system, this would be more complex
        # based on market trends, macroeconomic indicators, and specific industry factors.
        
        if growth_rate > 0.15 and competition_level == 'Low':
            return 90 # Excellent timing for high growth in low competition
        elif growth_rate > 0.10 and competition_level == 'Medium':
            return 80 # Good timing for moderate growth in medium competition
        elif growth_rate > 0.05 and competition_level == 'High':
            return 70 # Fair timing for low growth in high competition
        else:
            return 50 # Poor timing
    
    def _analyze_entry_barriers(self, industry: str, competitive_analysis: CompetitiveAnalysis) -> Dict[str, Any]:
        """Analyze barriers to entry for a specific industry."""
        barriers = {
            'technology': {
                'high_cost': 'High R&D costs, infrastructure requirements, and network effects',
                'regulatory': 'Stringent regulatory approvals, compliance costs, and security requirements',
                'brand': 'Strong brand recognition, trust, and customer loyalty'
            },
            'healthcare': {
                'regulatory': 'Extensive clinical trials, regulatory approvals, and safety requirements',
                'trust': 'Patient trust, data privacy, and HIPAA compliance',
                'capital': 'High capital requirements, regulatory compliance, and trust'
            },
            'finance': {
                'regulatory': 'Stringent regulatory compliance, capital requirements, and trust',
                'competition': 'High competition, established players, and network effects',
                'trust': 'Customer trust, data security, and regulatory buffer'
            },
            'retail': {
                'competition': 'High competition, established players, and network effects',
                'trust': 'Customer trust, data security, and regulatory buffer',
                'capital': 'High capital requirements, operational costs, and trust'
            },
            'manufacturing': {
                'regulatory': 'Stringent safety, quality, and environmental regulations',
                'trust': 'Supplier trust, quality standards, and regulatory compliance',
                'capital': 'High capital requirements, operational costs, and trust'
            },
            'education': {
                'regulatory': 'Stringent accreditation, compliance, and safety requirements',
                'trust': 'Student trust, data privacy, and regulatory buffer',
                'capital': 'High capital requirements, operational costs, and trust'
            },
            'real_estate': {
                'regulatory': 'Stringent licensing, zoning, and compliance requirements',
                'trust': 'Customer trust, data security, and regulatory buffer',
                'capital': 'High capital requirements, operational costs, and trust'
            },
            'consulting': {
                'regulatory': 'Stringent professional service regulations, compliance, and trust',
                'trust': 'Client trust, data security, and regulatory buffer',
                'capital': 'High capital requirements, operational costs, and trust'
            }
        }
        
        return barriers.get(industry, barriers['technology'])
    
    def _analyze_market_dynamics(self, market_analysis: MarketAnalysis) -> Dict[str, Any]:
        """Analyze market dynamics and trends."""
        dynamics = {
            'growth_rate': market_analysis.growth_rate,
            'competition_level': market_analysis.competition_level,
            'market_maturity': market_analysis.market_maturity,
            'seasonal_factors': market_analysis.seasonal_factors,
            'key_trends': market_analysis.key_trends,
            'opportunities': market_analysis.opportunities,
            'threats': market_analysis.threats
        }
        return dynamics