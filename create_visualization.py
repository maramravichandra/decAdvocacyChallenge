
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
try:
    df = pd.read_csv('carsFixed.csv')
except FileNotFoundError:
    print("Error: 'carsFixed.csv' not found.")
    exit()

# Create the plot
plt.figure(figsize=(12, 8))
plot = sns.catplot(
    data=df,
    x='shopID',
    y='carsFixed',
    hue='boss',
    kind='bar',  # Use 'bar' to create a bar chart
    palette=['#80B1D3', '#FB8072'],
    legend_out=False
)

# Improve labels and title
plot.set_axis_labels("Shop ID", "Cars Fixed (Productivity)")
plot.fig.suptitle("Productivity by Shop and Boss Presence (All Data Points)", y=1.03)

# Adjust legend
plt.legend(title='Boss Present', loc='upper left', labels=['No', 'Yes'])

# Save the figure
try:
    plt.savefig('productivity_by_shop.png', dpi=300)
    print("Successfully created 'productivity_by_shop.png'")
except Exception as e:
    print(f"Error saving plot: {e}")

