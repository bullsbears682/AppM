#!/usr/bin/env python3

def simulate_calculation(investment, project_type='web_application', company_size='startup'):
    """Simulate the ROI calculation logic from the frontend"""
    
    # Investment size categories
    is_small = investment < 5000
    is_medium = investment < 50000
    
    # ROI ranges based on investment size (matching frontend logic)
    if is_small:
        roi_ranges = {
            'web_application': {'min': 20, 'max': 80},
            'ai_integration': {'min': 25, 'max': 100},
            'ecommerce_platform': {'min': 30, 'max': 90}
        }
    elif is_medium:
        roi_ranges = {
            'web_application': {'min': 12, 'max': 40},
            'ai_integration': {'min': 15, 'max': 50},
            'ecommerce_platform': {'min': 15, 'max': 45}
        }
    else:
        roi_ranges = {
            'web_application': {'min': 8, 'max': 25},
            'ai_integration': {'min': 12, 'max': 35},
            'ecommerce_platform': {'min': 10, 'max': 30}
        }
    
    # Get ROI range for project type
    roi_range = roi_ranges.get(project_type, {'min': 10, 'max': 30})
    base_roi = (roi_range['min'] + roi_range['max']) / 2  # Use average ROI
    
    # Calculate expected revenue
    expected_revenue = investment * (1 + base_roi / 100)
    
    # Project complexity multipliers (updated to match frontend)
    base_complexity_multipliers = {
        'web_application': 1.10,
        'ai_integration': 1.30,
        'ecommerce_platform': 1.15
    }
    
    # Scale complexity based on investment size
    investment_scale = 0.8 if investment < 10000 else 1.0 if investment < 100000 else 1.2
    complexity_multipliers = {}
    for key, value in base_complexity_multipliers.items():
        complexity_multipliers[key] = 1 + (value - 1) * investment_scale
    
    # Company size efficiency (updated to match frontend)
    efficiency_multipliers = {
        'startup': 0.95 if investment < 25000 else 1.05,
        'small': 1.02,
        'medium': 1.0,
        'large': 0.95,
        'enterprise': 0.90
    }
    
    complexity = complexity_multipliers.get(project_type, 1.25)
    efficiency = efficiency_multipliers.get(company_size, 1.0)
    actual_project_cost = investment * complexity * efficiency
    
    # Calculate gross profit
    gross_profit = expected_revenue - actual_project_cost
    
    # Operating costs as percentage of gross profit (updated to match frontend)
    base_operating_rates = {
        'web_application': 0.08,
        'ai_integration': 0.12,
        'ecommerce_platform': 0.09
    }
    
    # Lower operating costs for smaller investments
    operating_scale = 0.5 if investment < 10000 else 0.8 if investment < 50000 else 1.0
    operating_rate = base_operating_rates.get(project_type, 0.08) * operating_scale
    
    timeline = 12  # 12 months
    operating_costs = max(0, gross_profit) * operating_rate * (timeline / 12)
    
    # Tax rates (from frontend)
    tax_rates = {
        'startup': 0.15,
        'small': 0.20,
        'medium': 0.25,
        'large': 0.28,
        'enterprise': 0.30
    }
    
    tax_rate = tax_rates.get(company_size, 0.25)
    taxable_profit = max(0, gross_profit - operating_costs)
    taxes = taxable_profit * tax_rate
    
    # Final net profit
    net_profit = gross_profit - operating_costs - taxes
    
    return {
        'investment': investment,
        'expected_revenue': expected_revenue,
        'actual_cost': actual_project_cost,
        'gross_profit': gross_profit,
        'operating_costs': operating_costs,
        'taxes': taxes,
        'net_profit': net_profit,
        'roi_percentage': base_roi,
        'effective_roi': (net_profit / investment * 100) if investment > 0 else 0
    }

def main():
    # Test different investment amounts
    test_amounts = [1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
    project_types = ['web_application', 'ai_integration', 'ecommerce_platform']

    print('=== ROI CALCULATOR SCALING TEST ===')
    print()

    for project_type in project_types:
        print(f'--- {project_type.replace("_", " ").title()} ---')
        print(f'{"Investment":<12} {"Expected ROI":<12} {"Actual ROI":<12} {"Net Profit":<15} {"Revenue":<12} {"Costs":<12}')
        print('-' * 85)
        
        for amount in test_amounts:
            result = simulate_calculation(amount, project_type, 'startup')
            
            print(f'${amount:,}     {result["roi_percentage"]:.1f}%     {result["effective_roi"]:.1f}%     ${result["net_profit"]:,.0f}     ${result["expected_revenue"]:,.0f}     ${result["actual_cost"]:,.0f}')
        
        print()

    print('=== ANALYSIS BY INVESTMENT SIZE ===')
    print()

    # Analyze by investment categories
    small_investments = [amt for amt in test_amounts if amt < 5000]
    medium_investments = [amt for amt in test_amounts if 5000 <= amt < 50000]
    large_investments = [amt for amt in test_amounts if amt >= 50000]

    categories = [
        ('Small Investments (<$5K)', small_investments),
        ('Medium Investments ($5K-$50K)', medium_investments),
        ('Large Investments (>$50K)', large_investments)
    ]

    for category_name, amounts in categories:
        print(f'--- {category_name} ---')
        
        total_profit = 0
        total_investment = 0
        
        for amount in amounts:
            result = simulate_calculation(amount, 'web_application', 'startup')
            total_profit += result['net_profit']
            total_investment += amount
            
            profit_margin = (result['net_profit'] / result['expected_revenue'] * 100) if result['expected_revenue'] > 0 else 0
            print(f'${amount:,}: {result["effective_roi"]:.1f}% ROI, ${result["net_profit"]:,.0f} profit ({profit_margin:.1f}% margin)')
        
        avg_roi = (total_profit / total_investment * 100) if total_investment > 0 else 0
        print(f'Average ROI for category: {avg_roi:.1f}%')
        print()

    print('=== POTENTIAL ISSUES ANALYSIS ===')
    print()
    
    # Look for problematic patterns
    issues_found = []
    
    for amount in test_amounts:
        for project_type in project_types:
            result = simulate_calculation(amount, project_type, 'startup')
            
            # Check for impossible results
            if result['net_profit'] < -amount:  # Loss more than total investment
                issues_found.append(f'${amount:,} {project_type}: Loss ${result["net_profit"]:,.0f} > Investment')
            
            if result['effective_roi'] < -100:  # More than 100% loss
                issues_found.append(f'${amount:,} {project_type}: {result["effective_roi"]:.1f}% ROI (impossible loss)')
            
            if result['actual_cost'] > result['expected_revenue'] * 2:  # Costs more than 2x revenue
                issues_found.append(f'${amount:,} {project_type}: Costs ${result["actual_cost"]:,.0f} >> Revenue ${result["expected_revenue"]:,.0f}')
    
    if issues_found:
        print('ISSUES DETECTED:')
        for issue in issues_found[:10]:  # Show first 10 issues
            print(f'⚠️  {issue}')
        if len(issues_found) > 10:
            print(f'... and {len(issues_found) - 10} more issues')
    else:
        print('✅ No impossible results detected!')
    
    print()
    print('=== PROFITABILITY SUMMARY ===')
    
    profitable_count = 0
    total_tests = len(test_amounts) * len(project_types)
    
    for amount in test_amounts:
        for project_type in project_types:
            result = simulate_calculation(amount, project_type, 'startup')
            if result['net_profit'] > 0:
                profitable_count += 1
    
    print(f'Profitable scenarios: {profitable_count}/{total_tests} ({profitable_count/total_tests*100:.1f}%)')

if __name__ == '__main__':
    main()