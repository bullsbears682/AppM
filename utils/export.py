"""
Advanced Export System for ROI Calculator
Generates professional reports in multiple formats
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from decimal import Decimal
from dataclasses import asdict
import base64

class ReportGenerator:
    """Generate professional business reports"""
    
    def __init__(self):
        self.report_templates = {
            'executive': 'Executive Summary Report',
            'detailed': 'Detailed Analysis Report', 
            'financial': 'Financial Projections Report',
            'investor': 'Investor Presentation Report'
        }
    
    def generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generate executive summary HTML report"""
        
        roi = data['roi_projection']
        cost = data['cost_analysis']
        bi = data.get('business_intelligence', {})
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Executive Summary - ROI Analysis</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
                .executive-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                .metric-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .metric-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
                .metric-label {{ color: #666; margin-top: 5px; }}
                .risk-low {{ color: #28a745; }}
                .risk-medium {{ color: #ffc107; }}
                .risk-high {{ color: #dc3545; }}
                .recommendation {{ background: #e8f5e8; border-left: 4px solid #28a745; padding: 15px; margin: 10px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Executive Summary</h1>
                <h2>{data['input_parameters']['company_name']}</h2>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div class="executive-grid">
                <div class="metric-card">
                    <div class="metric-value">{roi['roi_percentage']:.1f}%</div>
                    <div class="metric-label">Return on Investment</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">${roi['net_profit']:,.0f}</div>
                    <div class="metric-label">Net Profit Projection</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">{roi['payback_period_months']} months</div>
                    <div class="metric-label">Payback Period</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-value">${roi['npv']:,.0f}</div>
                    <div class="metric-label">Net Present Value</div>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <h3>📊 Key Insights</h3>
                <div class="recommendation">
                    <strong>Investment Recommendation:</strong> 
                    {'RECOMMENDED' if float(roi['roi_percentage']) > 15 else 'REQUIRES REVIEW' if float(roi['roi_percentage']) > 5 else 'NOT RECOMMENDED'}
                </div>
                
                <div class="recommendation">
                    <strong>Risk Assessment:</strong>
                    <span class="{'risk-low' if float(roi['risk_score']) < 30 else 'risk-medium' if float(roi['risk_score']) < 60 else 'risk-high'}">
                        {self._get_risk_level(float(roi['risk_score']))}
                    </span>
                </div>
                
                {'<div class="recommendation"><strong>Success Probability:</strong> ' + str(bi.get('success_probability', 'N/A')) + '%</div>' if bi else ''}
            </div>
            
            <div class="footer">
                <p>Generated by ROI Calculator v2.1 | Advanced Business Intelligence Platform</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def generate_detailed_report(self, data: Dict[str, Any]) -> str:
        """Generate comprehensive detailed report"""
        
        roi = data['roi_projection']
        cost = data['cost_analysis']
        bi = data.get('business_intelligence', {})
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Detailed ROI Analysis Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
                .header {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; border-radius: 15px; }}
                .section {{ margin: 30px 0; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
                .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
                .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
                .metric {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
                .metric-value {{ font-size: 1.5em; font-weight: bold; color: #4facfe; }}
                .chart-placeholder {{ height: 300px; background: #f8f9fa; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #666; }}
                .table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
                .table th, .table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                .table th {{ background: #f8f9fa; font-weight: bold; }}
                .risk-breakdown {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
                .risk-item {{ padding: 15px; border-radius: 8px; }}
                .risk-low {{ background: #d4edda; color: #155724; }}
                .risk-medium {{ background: #fff3cd; color: #856404; }}
                .risk-high {{ background: #f8d7da; color: #721c24; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Detailed ROI Analysis Report</h1>
                <h2>{data['input_parameters']['company_name']}</h2>
                <p>{data['input_parameters']['project_type'].replace('_', ' ').title()} Project</p>
                <p>Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <!-- Financial Overview -->
            <div class="section">
                <h2>💰 Financial Overview</h2>
                <div class="grid-3">
                    <div class="metric">
                        <div class="metric-value">${cost['total_cost']:,.0f}</div>
                        <div>Total Investment</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${roi['projected_revenue']:,.0f}</div>
                        <div>Projected Revenue</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{roi['roi_percentage']:.1f}%</div>
                        <div>ROI Percentage</div>
                    </div>
                </div>
                
                <h3>💼 Cost Breakdown</h3>
                <table class="table">
                    <thead>
                        <tr><th>Cost Category</th><th>Amount</th><th>Percentage</th></tr>
                    </thead>
                    <tbody>
                        {self._generate_cost_table_rows(cost['cost_breakdown'], cost['total_cost'])}
                    </tbody>
                </table>
            </div>
            
            <!-- Advanced Metrics -->
            <div class="section">
                <h2>📈 Advanced Financial Metrics</h2>
                <div class="grid-2">
                    <div>
                        <h4>Investment Returns</h4>
                        <div class="metric">
                            <div class="metric-value">${roi['npv']:,.0f}</div>
                            <div>Net Present Value</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{roi['irr']:.1f}%</div>
                            <div>Internal Rate of Return</div>
                        </div>
                    </div>
                    <div>
                        <h4>Timeline & Risk</h4>
                        <div class="metric">
                            <div class="metric-value">{roi['payback_period_months']} months</div>
                            <div>Payback Period</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{roi['risk_score']:.1f}%</div>
                            <div>Risk Score</div>
                        </div>
                    </div>
                </div>
            </div>
            
            {self._generate_business_intelligence_section(bi) if bi else ''}
            
            <!-- Risk Analysis -->
            <div class="section">
                <h2>🛡️ Risk Assessment</h2>
                <div class="risk-breakdown">
                    {self._generate_risk_breakdown(bi.get('risk_analysis', {})) if bi else self._generate_basic_risk_assessment(roi['risk_score'])}
                </div>
            </div>
            
            <!-- Recommendations -->
            <div class="section">
                <h2>🎯 Strategic Recommendations</h2>
                {self._generate_recommendations_section(data.get('recommendations', []), bi)}
            </div>
            
            <div style="text-align: center; margin-top: 40px; color: #666; border-top: 1px solid #ddd; padding-top: 20px;">
                <p><strong>ROI Calculator v2.1</strong> | Advanced Business Intelligence Platform</p>
                <p>This report was generated using Monte Carlo simulations and advanced financial modeling</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def generate_json_export(self, data: Dict[str, Any]) -> str:
        """Generate JSON export for API integration"""
        export_data = {
            'export_info': {
                'generated_at': datetime.now().isoformat(),
                'version': '2.1.0',
                'format': 'json',
                'calculator': 'ROI Calculator Advanced'
            },
            'company_info': data['input_parameters'],
            'financial_analysis': data['roi_projection'],
            'cost_analysis': data['cost_analysis'],
            'business_intelligence': data.get('business_intelligence'),
            'market_insights': data.get('market_insights'),
            'recommendations': data.get('recommendations', [])
        }
        
        return json.dumps(export_data, indent=2, default=str)
    
    def generate_csv_export(self, data: Dict[str, Any]) -> str:
        """Generate CSV export for spreadsheet analysis"""
        roi = data['roi_projection']
        cost = data['cost_analysis']
        
        csv_content = "Metric,Value,Unit\n"
        csv_content += f"Company Name,{data['input_parameters']['company_name']},text\n"
        csv_content += f"Project Type,{data['input_parameters']['project_type']},text\n"
        csv_content += f"Total Investment,{cost['total_cost']},currency\n"
        csv_content += f"Projected Revenue,{roi['projected_revenue']},currency\n"
        csv_content += f"Net Profit,{roi['net_profit']},currency\n"
        csv_content += f"ROI Percentage,{roi['roi_percentage']},percentage\n"
        csv_content += f"Payback Period,{roi['payback_period_months']},months\n"
        csv_content += f"NPV,{roi['npv']},currency\n"
        csv_content += f"IRR,{roi['irr']},percentage\n"
        csv_content += f"Risk Score,{roi['risk_score']},percentage\n"
        csv_content += f"Generated At,{datetime.now().isoformat()},datetime\n"
        
        return csv_content
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level description"""
        if risk_score <= 25:
            return "Low Risk"
        elif risk_score <= 45:
            return "Low-Moderate Risk"
        elif risk_score <= 65:
            return "Moderate Risk"
        elif risk_score <= 80:
            return "Moderate-High Risk"
        else:
            return "High Risk"
    
    def _generate_cost_table_rows(self, cost_breakdown: Dict, total_cost: float) -> str:
        """Generate cost breakdown table rows"""
        rows = ""
        for category, amount in cost_breakdown.items():
            percentage = (float(amount) / float(total_cost)) * 100
            rows += f"<tr><td>{category.replace('_', ' ').title()}</td><td>${float(amount):,.0f}</td><td>{percentage:.1f}%</td></tr>"
        return rows
    
    def _generate_business_intelligence_section(self, bi: Dict) -> str:
        """Generate business intelligence section"""
        if not bi:
            return ""
            
        return f"""
        <div class="section">
            <h2>🧠 Business Intelligence</h2>
            <div class="grid-2">
                <div>
                    <h4>Market Analysis</h4>
                    <div class="metric">
                        <div class="metric-value">${bi['market_analysis']['market_size'] / 1000000:.0f}M</div>
                        <div>Market Size</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{bi['market_analysis']['growth_rate'] * 100:.1f}%</div>
                        <div>Annual Growth Rate</div>
                    </div>
                </div>
                <div>
                    <h4>Success Metrics</h4>
                    <div class="metric">
                        <div class="metric-value">{bi['success_probability']:.1f}%</div>
                        <div>Success Probability</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{bi['competitive_analysis']['market_share_potential']:.1f}%</div>
                        <div>Market Share Potential</div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _generate_risk_breakdown(self, risk_analysis: Dict) -> str:
        """Generate detailed risk breakdown"""
        if not risk_analysis:
            return ""
            
        risks = [
            ('Market Risk', risk_analysis.get('market_risk', 0)),
            ('Execution Risk', risk_analysis.get('execution_risk', 0)),
            ('Financial Risk', risk_analysis.get('financial_risk', 0)),
            ('Regulatory Risk', risk_analysis.get('regulatory_risk', 0)),
            ('Technology Risk', risk_analysis.get('technology_risk', 0))
        ]
        
        html = ""
        for risk_name, risk_value in risks:
            risk_class = 'risk-low' if risk_value < 30 else 'risk-medium' if risk_value < 60 else 'risk-high'
            html += f'<div class="risk-item {risk_class}"><strong>{risk_name}</strong><br>{risk_value:.1f}%</div>'
        
        return html
    
    def _generate_basic_risk_assessment(self, risk_score: float) -> str:
        """Generate basic risk assessment when detailed analysis not available"""
        risk_class = 'risk-low' if risk_score < 30 else 'risk-medium' if risk_score < 60 else 'risk-high'
        return f'<div class="risk-item {risk_class}"><strong>Overall Risk Score</strong><br>{risk_score:.1f}%</div>'
    
    def _generate_recommendations_section(self, recommendations: list, bi: Dict) -> str:
        """Generate recommendations section"""
        html = "<ul>"
        
        if bi and bi.get('recommended_actions'):
            for rec in bi['recommended_actions']:
                html += f"<li style='margin: 10px 0; padding: 10px; background: #e8f5e8; border-radius: 5px;'>{rec}</li>"
        else:
            for rec in recommendations:
                html += f"<li style='margin: 10px 0; padding: 10px; background: #e8f5e8; border-radius: 5px;'>{rec}</li>"
        
        html += "</ul>"
        return html