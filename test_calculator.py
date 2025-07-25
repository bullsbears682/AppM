#!/usr/bin/env python3

try:
    from utils.calculator import EnhancedROICalculator
    from decimal import Decimal
    
    calc = EnhancedROICalculator()
    print('✅ Calculator import successful')
    
    # Test with valid parameters
    result = calc.calculate_enhanced_roi_projection(
        investment=Decimal('10000'),
        industry='saas',
        project_type='product_development', 
        timeline_months=12,
        currency='USD',
        company_size='startup'
    )
    print('✅ Basic calculation successful')
    print(f'ROI: {result.roi_percentage}%')
    print(f'Projected Revenue: {result.projected_revenue}')
    print(f'Net Profit: {result.net_profit}')
    print(f'NPV: {result.npv}')
    print(f'IRR: {result.irr}')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()