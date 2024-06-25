#Data Manipulation
import pandas as pd

path_to_file = r'C:\Users\zheng\OneDrive - Louisiana State University\Documents\1 GSAPP\SMORGASBORD\Working with Spatial Data in Python\2015_Street_Tree_Census_-_Tree_Data.csv'
df = pd.read_csv(path_to_file)

# need to categorize the health conditions in different lists
# Create masks for each health condition
mask_good = df['health'] == 'Good'
mask_fair = df['health'] == 'Fair'
mask_poor = df['health'] == 'Poor'

good_tree_dbh = df.loc[mask_good, 'tree_dbh'].tolist()
fair_tree_dbh = df.loc[mask_fair, 'tree_dbh'].tolist()
poor_tree_dbh = df.loc[mask_poor, 'tree_dbh'].tolist()

# Output
print("Good health tree diameters:", good_tree_dbh[:10])
print("Fair health tree diameters:", fair_tree_dbh[:10])
print("Poor health tree diameters:", poor_tree_dbh[:10])