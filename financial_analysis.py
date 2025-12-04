
import pandas as pd
import numpy as np

def analyze_financial_impact_and_confidence(file_path='carsFixed.csv', n_bootstraps=1000, revenue_per_car=100):
    df = pd.read_csv(file_path)

    # Financial Impact Analysis
    productivity = df.groupby(['shopID', 'boss'])['carsFixed'].mean().unstack()
    productivity['difference'] = productivity[1] - productivity[0]
    
    # Assuming Patrick works 5 days a week, 52 weeks a year = 260 days.
    # The data is for 250 days, which is close to a year of work days.
    # Let's assume Patrick can visit one shop each day.
    # An optimal schedule would be to prioritize shops with the highest productivity difference.
    
    # Get the number of days Patrick visited each shop in the dataset
    days_visited = df[df['boss'] == 1]['shopID'].value_counts().sort_index()
    
    # A simple optimal strategy: visit the top 2 shops (4 and 2) more often.
    # Let's say Patrick spends 40% of his time at Shop 4, 40% at Shop 2, and the remaining 20% distributed among other shops.
    # This is a hypothetical scenario to show the potential.
    optimal_schedule = {
        4: 0.4,
        2: 0.4,
        1: 0.1,
        5: 0.1,
        3: 0.0
    }
    
    # Calculate revenue for current and optimal schedules
    total_days = len(df['observation'].unique())
    
    # Current schedule revenue
    current_revenue = 0
    for shop_id in df['shopID'].unique():
        days_present = days_visited.get(shop_id, 0)
        days_absent = 50 - days_present  # Assuming 50 observations per shop
        
        mean_cars_present = productivity.loc[shop_id, 1]
        mean_cars_absent = productivity.loc[shop_id, 0]
        
        current_revenue += (days_present * mean_cars_present + days_absent * mean_cars_absent) * revenue_per_car
        
    # Optimal schedule revenue
    optimal_revenue = 0
    for shop_id in df['shopID'].unique():
        days_present = optimal_schedule.get(shop_id, 0) * total_days / 5 # Assuming 5 shops
        days_absent = 50 - days_present
        
        mean_cars_present = productivity.loc[shop_id, 1]
        mean_cars_absent = productivity.loc[shop_id, 0]
        
        optimal_revenue += (days_present * mean_cars_present + days_absent * mean_cars_absent) * revenue_per_car

    potential_revenue_increase = optimal_revenue - current_revenue

    # Confidence Analysis (Bootstrapping)
    bootstrap_results = []
    for i in range(n_bootstraps):
        # Sample with replacement from the original dataframe
        sample_df = df.sample(n=len(df), replace=True)
        
        # Calculate productivity difference for the sample
        sample_productivity = sample_df.groupby(['shopID', 'boss'])['carsFixed'].mean().unstack()
        sample_productivity['difference'] = sample_productivity[1] - sample_productivity[0]
        bootstrap_results.append(sample_productivity['difference'])

    bootstrap_df = pd.DataFrame(bootstrap_results)
    
    # Calculate confidence intervals
    confidence_intervals = bootstrap_df.quantile([0.025, 0.975]).T
    confidence_intervals.columns = ['lower_bound', 'upper_bound']
    
    return {
        "potential_revenue_increase": potential_revenue_increase,
        "confidence_intervals": confidence_intervals,
        "productivity_difference": productivity['difference']
    }

if __name__ == '__main__':
    analysis_results = analyze_financial_impact_and_confidence()
    print("Potential Revenue Increase:", analysis_results['potential_revenue_increase'])
    print("\nProductivity Difference:")
    print(analysis_results['productivity_difference'])
    print("\nConfidence Intervals:")
    print(analysis_results['confidence_intervals'])
