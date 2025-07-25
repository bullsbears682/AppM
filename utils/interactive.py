"""
Interactive Features for ROI Calculator
Scenario comparison, what-if analysis, and real-time adjustments
"""

from typing import Dict, List, Any, Tuple
from decimal import Decimal
import json
from datetime import datetime
from utils.calculator import EnhancedROICalculator
from utils.analytics import AdvancedAnalyticsEngine

class ScenarioManager:
    """Manage multiple ROI scenarios for comparison"""
    
    def __init__(self):
        self.calculator = EnhancedROICalculator()
        self.analytics = AdvancedAnalyticsEngine()
        self.scenarios = {}
    
    def create_scenario(self, scenario_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new scenario with given parameters"""
        
        # Calculate ROI for this scenario
        cost_analysis = self.calculator.calculate_project_cost(
            company_size=parameters['company_size'],
            project_type=parameters['project_type'],
            industry=parameters['industry'],
            currency=parameters['currency'],
            custom_investment=parameters.get('custom_investment'),
            custom_timeline=parameters.get('custom_timeline')
        )
        
        roi_result = self.calculator.calculate_enhanced_roi_projection(
            investment=cost_analysis['total_cost'],
            industry=parameters['industry'],
            project_type=parameters['project_type'],
            timeline_months=cost_analysis['timeline_months'],
            currency=parameters['currency'],
            company_size=parameters['company_size']
        )
        
        # Generate business intelligence
        business_intelligence = self.analytics.generate_comprehensive_analysis(
            investment=cost_analysis['total_cost'],
            industry=parameters['industry'],
            project_type=parameters['project_type'],
            company_size=parameters['company_size'],
            timeline_months=cost_analysis['timeline_months'],
            roi_result=roi_result
        )
        
        scenario_data = {
            'name': scenario_name,
            'parameters': parameters,
            'cost_analysis': cost_analysis,
            'roi_result': roi_result,
            'business_intelligence': business_intelligence,
            'created_at': datetime.now().isoformat()
        }
        
        self.scenarios[scenario_name] = scenario_data
        return scenario_data
    
    def compare_scenarios(self, scenario_names: List[str]) -> Dict[str, Any]:
        """Compare multiple scenarios side by side"""
        
        if not scenario_names:
            return {'error': 'No scenarios provided for comparison'}
        
        comparison = {
            'scenarios': [],
            'comparison_metrics': {},
            'recommendations': []
        }
        
        for name in scenario_names:
            if name in self.scenarios:
                scenario = self.scenarios[name]
                comparison['scenarios'].append({
                    'name': name,
                    'roi_percentage': float(scenario['roi_result'].roi_percentage),
                    'net_profit': float(scenario['roi_result'].net_profit),
                    'risk_score': float(scenario['roi_result'].risk_score),
                    'payback_period': scenario['roi_result'].payback_period_months,
                    'npv': float(scenario['roi_result'].npv),
                    'success_probability': float(scenario['business_intelligence'].success_probability) if scenario['business_intelligence'] else None,
                    'total_investment': float(scenario['cost_analysis']['total_cost'])
                })
        
        # Calculate comparison metrics
        comparison['comparison_metrics'] = self._calculate_comparison_metrics(comparison['scenarios'])
        comparison['recommendations'] = self._generate_comparison_recommendations(comparison['scenarios'])
        
        return comparison
    
    def _calculate_comparison_metrics(self, scenarios: List[Dict]) -> Dict[str, Any]:
        """Calculate metrics for scenario comparison"""
        
        if not scenarios:
            return {}
        
        roi_values = [s['roi_percentage'] for s in scenarios]
        risk_values = [s['risk_score'] for s in scenarios]
        investment_values = [s['total_investment'] for s in scenarios]
        
        return {
            'best_roi': {
                'scenario': max(scenarios, key=lambda x: x['roi_percentage'])['name'],
                'value': max(roi_values)
            },
            'lowest_risk': {
                'scenario': min(scenarios, key=lambda x: x['risk_score'])['name'],
                'value': min(risk_values)
            },
            'lowest_investment': {
                'scenario': min(scenarios, key=lambda x: x['total_investment'])['name'],
                'value': min(investment_values)
            },
            'best_risk_adjusted_return': self._calculate_best_risk_adjusted_return(scenarios),
            'average_roi': sum(roi_values) / len(roi_values),
            'roi_range': max(roi_values) - min(roi_values)
        }
    
    def _calculate_best_risk_adjusted_return(self, scenarios: List[Dict]) -> Dict[str, Any]:
        """Calculate risk-adjusted returns (Sharpe ratio style)"""
        
        best_ratio = -999
        best_scenario = None
        
        for scenario in scenarios:
            # Risk-adjusted return = ROI / Risk Score
            if scenario['risk_score'] > 0:
                ratio = scenario['roi_percentage'] / scenario['risk_score']
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_scenario = scenario['name']
        
        return {
            'scenario': best_scenario,
            'ratio': round(best_ratio, 2) if best_ratio > -999 else None
        }
    
    def _generate_comparison_recommendations(self, scenarios: List[Dict]) -> List[str]:
        """Generate recommendations based on scenario comparison"""
        
        recommendations = []
        
        if len(scenarios) < 2:
            return ['Need at least 2 scenarios for meaningful comparison']
        
        # Find best and worst scenarios
        best_roi = max(scenarios, key=lambda x: x['roi_percentage'])
        lowest_risk = min(scenarios, key=lambda x: x['risk_score'])
        
        # ROI recommendations
        if best_roi['roi_percentage'] > 20:
            recommendations.append(f"'{best_roi['name']}' offers exceptional ROI of {best_roi['roi_percentage']:.1f}% - highly recommended")
        elif best_roi['roi_percentage'] > 10:
            recommendations.append(f"'{best_roi['name']}' provides solid ROI of {best_roi['roi_percentage']:.1f}% - good investment option")
        
        # Risk recommendations
        if lowest_risk['risk_score'] < 30:
            recommendations.append(f"'{lowest_risk['name']}' offers the lowest risk profile at {lowest_risk['risk_score']:.1f}% - ideal for conservative investors")
        
        # Balance recommendations
        risk_adjusted = self._calculate_best_risk_adjusted_return(scenarios)
        if risk_adjusted['scenario']:
            recommendations.append(f"'{risk_adjusted['scenario']}' provides the best risk-adjusted return - optimal balance of return and risk")
        
        return recommendations

class WhatIfAnalyzer:
    """Perform what-if analysis on ROI parameters"""
    
    def __init__(self):
        self.calculator = EnhancedROICalculator()
    
    def analyze_investment_sensitivity(self, base_parameters: Dict[str, Any], 
                                     investment_range: Tuple[float, float], 
                                     steps: int = 10) -> Dict[str, Any]:
        """Analyze how ROI changes with different investment amounts"""
        
        min_investment, max_investment = investment_range
        step_size = (max_investment - min_investment) / (steps - 1)
        
        results = []
        
        for i in range(steps):
            investment_amount = min_investment + (i * step_size)
            
            # Calculate ROI for this investment level
            cost_analysis = self.calculator.calculate_project_cost(
                company_size=base_parameters['company_size'],
                project_type=base_parameters['project_type'],
                industry=base_parameters['industry'],
                currency=base_parameters['currency'],
                custom_investment=Decimal(str(investment_amount))
            )
            
            roi_result = self.calculator.calculate_enhanced_roi_projection(
                investment=cost_analysis['total_cost'],
                industry=base_parameters['industry'],
                project_type=base_parameters['project_type'],
                timeline_months=cost_analysis['timeline_months'],
                currency=base_parameters['currency'],
                company_size=base_parameters['company_size']
            )
            
            results.append({
                'investment': investment_amount,
                'roi_percentage': float(roi_result.roi_percentage),
                'net_profit': float(roi_result.net_profit),
                'risk_score': float(roi_result.risk_score),
                'payback_period': roi_result.payback_period_months
            })
        
        return {
            'analysis_type': 'investment_sensitivity',
            'base_parameters': base_parameters,
            'results': results,
            'insights': self._generate_sensitivity_insights(results, 'investment')
        }
    
    def analyze_timeline_sensitivity(self, base_parameters: Dict[str, Any],
                                   timeline_range: Tuple[int, int],
                                   steps: int = 8) -> Dict[str, Any]:
        """Analyze how ROI changes with different project timelines"""
        
        min_timeline, max_timeline = timeline_range
        step_size = (max_timeline - min_timeline) / (steps - 1)
        
        results = []
        
        for i in range(steps):
            timeline_months = int(min_timeline + (i * step_size))
            
            # Calculate ROI for this timeline
            cost_analysis = self.calculator.calculate_project_cost(
                company_size=base_parameters['company_size'],
                project_type=base_parameters['project_type'],
                industry=base_parameters['industry'],
                currency=base_parameters['currency'],
                custom_timeline=timeline_months
            )
            
            roi_result = self.calculator.calculate_enhanced_roi_projection(
                investment=cost_analysis['total_cost'],
                industry=base_parameters['industry'],
                project_type=base_parameters['project_type'],
                timeline_months=timeline_months,
                currency=base_parameters['currency'],
                company_size=base_parameters['company_size']
            )
            
            results.append({
                'timeline_months': timeline_months,
                'roi_percentage': float(roi_result.roi_percentage),
                'net_profit': float(roi_result.net_profit),
                'risk_score': float(roi_result.risk_score),
                'total_investment': float(cost_analysis['total_cost'])
            })
        
        return {
            'analysis_type': 'timeline_sensitivity',
            'base_parameters': base_parameters,
            'results': results,
            'insights': self._generate_sensitivity_insights(results, 'timeline')
        }
    
    def _generate_sensitivity_insights(self, results: List[Dict], analysis_type: str) -> List[str]:
        """Generate insights from sensitivity analysis"""
        
        insights = []
        
        if analysis_type == 'investment':
            # Find optimal investment level
            best_roi = max(results, key=lambda x: x['roi_percentage'])
            insights.append(f"Optimal ROI of {best_roi['roi_percentage']:.1f}% achieved at ${best_roi['investment']:,.0f} investment")
            
            # Check for diminishing returns
            roi_values = [r['roi_percentage'] for r in results]
            if len(roi_values) > 3:
                recent_trend = roi_values[-3:]
                if all(recent_trend[i] <= recent_trend[i-1] for i in range(1, len(recent_trend))):
                    insights.append("Warning: Diminishing returns observed at higher investment levels")
        
        elif analysis_type == 'timeline':
            # Find optimal timeline
            best_roi = max(results, key=lambda x: x['roi_percentage'])
            insights.append(f"Optimal timeline of {best_roi['timeline_months']} months for maximum ROI")
            
            # Check risk vs timeline relationship
            short_timeline = min(results, key=lambda x: x['timeline_months'])
            long_timeline = max(results, key=lambda x: x['timeline_months'])
            
            if short_timeline['risk_score'] > long_timeline['risk_score']:
                insights.append("Longer timelines generally reduce project risk")
        
        return insights

class RealTimeCalculator:
    """Real-time ROI calculation with parameter sliders"""
    
    def __init__(self):
        self.calculator = EnhancedROICalculator()
        self.current_parameters = {}
        self.calculation_history = []
    
    def update_parameter(self, parameter_name: str, value: Any) -> Dict[str, Any]:
        """Update a single parameter and recalculate ROI"""
        
        self.current_parameters[parameter_name] = value
        
        # Check if we have minimum required parameters
        required_params = ['company_size', 'project_type', 'industry', 'currency']
        if not all(param in self.current_parameters for param in required_params):
            return {'status': 'incomplete', 'missing_parameters': [p for p in required_params if p not in self.current_parameters]}
        
        # Calculate ROI with current parameters
        try:
            result = self._calculate_current_roi()
            
            # Store in history
            self.calculation_history.append({
                'timestamp': datetime.now().isoformat(),
                'parameters': self.current_parameters.copy(),
                'result': result
            })
            
            # Keep only last 10 calculations
            self.calculation_history = self.calculation_history[-10:]
            
            return {
                'status': 'success',
                'result': result,
                'parameter_updated': parameter_name,
                'calculation_id': len(self.calculation_history)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'parameter_updated': parameter_name
            }
    
    def _calculate_current_roi(self) -> Dict[str, Any]:
        """Calculate ROI with current parameters"""
        
        cost_analysis = self.calculator.calculate_project_cost(
            company_size=self.current_parameters['company_size'],
            project_type=self.current_parameters['project_type'],
            industry=self.current_parameters['industry'],
            currency=self.current_parameters['currency'],
            custom_investment=self.current_parameters.get('custom_investment'),
            custom_timeline=self.current_parameters.get('custom_timeline')
        )
        
        roi_result = self.calculator.calculate_enhanced_roi_projection(
            investment=cost_analysis['total_cost'],
            industry=self.current_parameters['industry'],
            project_type=self.current_parameters['project_type'],
            timeline_months=cost_analysis['timeline_months'],
            currency=self.current_parameters['currency'],
            company_size=self.current_parameters['company_size']
        )
        
        return {
            'roi_percentage': float(roi_result.roi_percentage),
            'net_profit': float(roi_result.net_profit),
            'total_investment': float(cost_analysis['total_cost']),
            'risk_score': float(roi_result.risk_score),
            'payback_period': roi_result.payback_period_months,
            'npv': float(roi_result.npv)
        }
    
    def get_parameter_impact(self, parameter_name: str, test_values: List[Any]) -> Dict[str, Any]:
        """Test impact of different values for a specific parameter"""
        
        if parameter_name not in self.current_parameters:
            return {'error': f'Parameter {parameter_name} not set in current calculation'}
        
        original_value = self.current_parameters[parameter_name]
        impacts = []
        
        for test_value in test_values:
            # Temporarily update parameter
            self.current_parameters[parameter_name] = test_value
            
            try:
                result = self._calculate_current_roi()
                impacts.append({
                    'parameter_value': test_value,
                    'roi_change': result['roi_percentage'] - self._get_baseline_roi(),
                    'roi_percentage': result['roi_percentage'],
                    'risk_change': result['risk_score'] - self._get_baseline_risk()
                })
            except Exception as e:
                impacts.append({
                    'parameter_value': test_value,
                    'error': str(e)
                })
        
        # Restore original value
        self.current_parameters[parameter_name] = original_value
        
        return {
            'parameter': parameter_name,
            'original_value': original_value,
            'impacts': impacts,
            'most_impactful': max(impacts, key=lambda x: abs(x.get('roi_change', 0))) if impacts else None
        }
    
    def _get_baseline_roi(self) -> float:
        """Get baseline ROI for comparison"""
        if self.calculation_history:
            return self.calculation_history[-1]['result']['roi_percentage']
        return 0.0
    
    def _get_baseline_risk(self) -> float:
        """Get baseline risk for comparison"""
        if self.calculation_history:
            return self.calculation_history[-1]['result']['risk_score']
        return 0.0