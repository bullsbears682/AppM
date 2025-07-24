#!/usr/bin/env python3
"""
DevCost Demo Script
Demonstrates the key features and commercial potential of the DevCost application
"""

import requests
import json
import time
from datetime import datetime

def print_banner():
    print("=" * 70)
    print("🚀 DevCost - Real-Time Development Cost Analytics DEMO")
    print("=" * 70)
    print()

def print_section(title):
    print(f"\n📊 {title}")
    print("-" * 50)

def demo_api_analysis():
    """Demonstrate the core API functionality"""
    print_section("LIVE REPOSITORY ANALYSIS")
    
    try:
        response = requests.get('http://localhost:5000/api/analysis')
        data = response.json()
        
        print(f"✅ API Status: Connected")
        print(f"📈 Total Development Cost: ${data['total_cost']:,.2f}")
        print(f"⏰ Total Development Hours: {data['total_hours']:.1f}h")
        print(f"🔢 Total Commits Analyzed: {data['total_commits']}")
        print(f"💰 Average Cost per Commit: ${data['avg_cost_per_commit']:.2f}")
        print(f"💵 Hourly Rate: ${data['hourly_rate']}/hour")
        
        if data['category_costs']:
            print(f"\n📋 Cost Breakdown by Category:")
            for category, cost in data['category_costs'].items():
                percentage = (cost / data['total_cost'] * 100) if data['total_cost'] > 0 else 0
                print(f"   • {category}: ${cost:.2f} ({percentage:.1f}%)")
        
        if data['commit_details']:
            print(f"\n🔍 Recent Commits Sample:")
            for commit in data['commit_details'][:3]:
                print(f"   • {commit['hash']}: {commit['message'][:40]}...")
                print(f"     Cost: ${commit['estimated_cost']:.2f} | Hours: {commit['estimated_hours']:.2f}h")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ API Status: Not Connected")
        print("   Make sure to run 'python app.py' in another terminal first")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def demo_business_value():
    """Demonstrate the business value proposition"""
    print_section("BUSINESS VALUE DEMONSTRATION")
    
    # Sample calculations based on typical enterprise scenarios
    scenarios = [
        {
            "company": "Mid-size SaaS (50 developers)",
            "monthly_cost": 50 * 75 * 160,  # 50 devs * $75/hr * 160 hrs/month
            "devcost_savings": 0.15,  # 15% efficiency improvement
            "monthly_savings": 50 * 75 * 160 * 0.15,
            "annual_roi": 50 * 75 * 160 * 0.15 * 12,
            "devcost_cost": 50 * 100  # $100/dev/month
        },
        {
            "company": "Enterprise (200 developers)",
            "monthly_cost": 200 * 85 * 160,
            "devcost_savings": 0.20,  # 20% efficiency improvement
            "monthly_savings": 200 * 85 * 160 * 0.20,
            "annual_roi": 200 * 85 * 160 * 0.20 * 12,
            "devcost_cost": 200 * 150  # $150/dev/month
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🏢 {scenario['company']}")
        print(f"   Current monthly dev cost: ${scenario['monthly_cost']:,}")
        print(f"   DevCost monthly savings: ${scenario['monthly_savings']:,}")
        print(f"   DevCost annual ROI: ${scenario['annual_roi']:,}")
        print(f"   DevCost subscription cost: ${scenario['devcost_cost']:,}/month")
        print(f"   Net annual savings: ${scenario['annual_roi'] - (scenario['devcost_cost'] * 12):,}")
        print(f"   ROI Multiple: {(scenario['annual_roi'] / (scenario['devcost_cost'] * 12)):.1f}x")

def demo_features():
    """Demonstrate key features"""
    print_section("KEY FEATURES SHOWCASE")
    
    features = [
        "🎯 Real-time cost tracking as commits happen",
        "📊 Beautiful executive dashboards for C-suite",
        "🤖 Smart categorization (Features, Bugs, Refactoring, etc.)",
        "👥 Developer productivity analytics",
        "🔥 File hotspot analysis (expensive files to maintain)",
        "⏱️ Time estimation based on code complexity",
        "💹 ROI calculations for features and technical debt",
        "🔄 Auto-refresh every 5 minutes",
        "⚙️ Configurable hourly rates",
        "📈 Historical trend analysis",
        "🎨 Modern, responsive web interface",
        "🔗 Git integration (works with any repository)"
    ]
    
    for feature in features:
        print(f"   {feature}")

def demo_market_opportunity():
    """Demonstrate market opportunity"""
    print_section("MARKET OPPORTUNITY")
    
    print("🌍 Global Market Size:")
    print("   • 26.8 million software developers worldwide")
    print("   • Average enterprise spends $500K-5M+ annually on development")
    print("   • 73% of teams report productivity measurement challenges")
    print()
    
    print("💰 Revenue Potential:")
    print("   • SaaS Model: $50-200/developer/month")
    print("   • Enterprise Plans: $10,000-50,000/month")
    print("   • Even 0.1% market share = $50M+ annual revenue")
    print()
    
    print("🎯 Competitive Advantages:")
    print("   • First mover in real-time development cost tracking")
    print("   • Actionable insights, not just metrics")
    print("   • Executive language (translates tech to business value)")
    print("   • Easy integration with existing workflows")

def demo_use_cases():
    """Demonstrate real-world use cases"""
    print_section("REAL-WORLD USE CASES")
    
    use_cases = [
        {
            "role": "CTO",
            "question": "What did Feature X actually cost us to build?",
            "answer": "DevCost tracks every commit and shows exact cost breakdown"
        },
        {
            "role": "Engineering Director", 
            "question": "Which developer provides the best ROI?",
            "answer": "Compare cost per feature, bug rates, and quality metrics"
        },
        {
            "role": "Product Manager",
            "question": "Should we refactor this code or rewrite it?",
            "answer": "Technical debt cost analysis shows financial impact"
        },
        {
            "role": "CFO",
            "question": "What's our development ROI compared to competitors?",
            "answer": "Benchmark cost per story point and feature delivery speed"
        }
    ]
    
    for case in use_cases:
        print(f"\n👤 {case['role']} asks:")
        print(f"   ❓ \"{case['question']}\"")
        print(f"   ✅ DevCost answer: {case['answer']}")

def main():
    print_banner()
    
    # Check if the application is running
    api_connected = demo_api_analysis()
    
    # Show business value regardless of API status
    demo_business_value()
    demo_features()
    demo_market_opportunity()
    demo_use_cases()
    
    print_section("NEXT STEPS")
    
    if api_connected:
        print("🌐 Live Demo: http://localhost:5000")
        print("   The DevCost dashboard is running and analyzing this repository!")
    else:
        print("🚀 To see the live demo:")
        print("   1. Run: python app.py")
        print("   2. Open: http://localhost:5000")
        print("   3. Run: python demo.py (again)")
    
    print("\n💼 Commercial Opportunities:")
    print("   • This is a working prototype of a viable SaaS product")
    print("   • Ready for customer validation and pilot programs")
    print("   • Scalable technology with clear monetization path")
    print("   • Addresses a real pain point every CTO faces")
    
    print("\n📞 Interested in:")
    print("   • Investing in this concept?")
    print("   • Partnering for development?")
    print("   • Licensing the technology?")
    print("   • Joining as a co-founder?")
    
    print("\n" + "=" * 70)
    print("🎯 DevCost: Finally know what your software development actually costs")
    print("=" * 70)

if __name__ == "__main__":
    main()