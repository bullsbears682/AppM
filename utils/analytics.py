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