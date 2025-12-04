
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_revenue_comparison_chart(file_path='carsFixed.csv', revenue_per_car=100):
    df = pd.read_csv(file_path)

    # --- Calculations from financial_analysis.py ---
    productivity = df.groupby(['shopID', 'boss'])['carsFixed'].mean().unstack()
    days_visited = df[df['boss'] == 1]['shopID'].value_counts().sort_index()
    total_days = len(df['observation'].unique())

    # Hypothetical optimal schedule
    optimal_schedule = {4: 0.4, 2: 0.4, 1: 0.1, 5: 0.1, 3: 0.0}

    # Current schedule revenue
    current_revenue = 0
    for shop_id in sorted(df['shopID'].unique()):
        days_present = days_visited.get(shop_id, 0)
        days_absent = 50 - days_present
        mean_cars_present = productivity.loc[shop_id, 1] if 1 in productivity.columns else 0
        mean_cars_absent = productivity.loc[shop_id, 0] if 0 in productivity.columns else 0
        current_revenue += (days_present * mean_cars_present + days_absent * mean_cars_absent) * revenue_per_car

    # Optimal schedule revenue
    optimal_revenue = 0
    for shop_id in sorted(df['shopID'].unique()):
        # total_days is 250, 5 shops, so 250 / 5 = 50 days per shop on average
        days_present_optimal = optimal_schedule.get(shop_id, 0) * 50 * 5 
        days_absent_optimal = 50 - days_present_optimal
        mean_cars_present = productivity.loc[shop_id, 1] if 1 in productivity.columns else 0
        mean_cars_absent = productivity.loc[shop_id, 0] if 0 in productivity.columns else 0
        optimal_revenue += (days_present_optimal * mean_cars_present + days_absent_optimal * mean_cars_absent) * revenue_per_car

    # --- Create Visualization ---
    scenarios = ['Current Schedule', 'Optimal Schedule']
    revenues = [current_revenue, optimal_revenue]

    plt.figure(figsize=(8, 6))
    bars = plt.bar(scenarios, revenues, color=['#80B1D3', '#FB8072'])
    
    plt.ylabel('Projected Annual Revenue ($)')
    plt.title('Projected Revenue: Current vs. Optimal Schedule')
    plt.ylim(0, max(revenues) * 1.15) 

    # Add revenue numbers on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + max(revenues)*0.02, f'${yval:,.0f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('revenue_scenarios.png', dpi=300)
    print("Successfully created 'revenue_scenarios.png'")

if __name__ == '__main__':
    generate_revenue_comparison_chart()
