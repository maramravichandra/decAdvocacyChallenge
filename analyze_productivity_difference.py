
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('carsFixed.csv')

# Calculate mean productivity for each shop with and without the boss
productivity = df.groupby(['shopID', 'boss'])['carsFixed'].mean().unstack()

# Calculate the difference in productivity
productivity['difference'] = productivity[1] - productivity[0]

# Sort by the difference
sorted_shops = productivity.sort_values(by='difference', ascending=False)

print("Productivity difference (Patrick's presence - No one's presence):")
print(sorted_shops['difference'])

# Create the plot
plt.figure(figsize=(12, 8))
sns.barplot(x=sorted_shops.index, y=sorted_shops['difference'], palette='vlag')

# Improve labels and title
plt.xlabel("Shop")
plt.ylabel("Change in Productivity (Cars Fixed)")
plt.title("Impact of Patrick's Presence on Shop Productivity")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()


# Save the figure
plt.savefig('productivity_difference.png', dpi=300)
print("Successfully created 'productivity_difference.png'")
