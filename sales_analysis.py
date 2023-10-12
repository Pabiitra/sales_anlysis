# Import necessary library

import pandas as pd
import os
import matplotlib.pyplot as plt

### Task 1: Merge the 12 months of sales data into a single csv file

df = pd.read_csv('C:/Users/Shree/OneDrive/Desktop/sales/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv')
files = [file for file in os.listdir('C:/Users/Shree/OneDrive/Desktop/sales/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data')]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv('C:/Users/Shree/OneDrive/Desktop/sales/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/' + file)
    all_months_data = pd.concat([all_months_data, df])
    
# save this merge file in csv formate
all_months_data.to_csv('all_data.csv', index=False) 

### Read in updated dataframe

all_data = pd.read_csv('all_data.csv')   




### Clean up the data !

# Drop rows of NAN
nan_df = all_data[all_data.isna().any(axis=1)]
all_data = all_data.dropna(how='all')

# Find 'Or' and delete it
all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']

# Convert columns to the correct type
all_data['Quantity Ordered'] =pd.to_numeric(all_data['Quantity Ordered']) # Make int
all_data['Price Each'] = pd.to_numeric(all_data['Price Each']) # Make float


### Augment data with additional columns

# Task 2 : Add month column
all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int64') 

# Task 3: Add a sales column
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

# Add a city column
# let's use .apply()
def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2]

all_data['City'] = all_data['Purchase Address'].apply(lambda x:f'{get_city(x)} ({get_state(x)}')




### Question 1: What was the best month for sales ? How much was earned that month ?

results = all_data.groupby('Month').sum()

# visualisation
months = range(1, 13)

plt.bar(months, results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD  ($)')
plt.xlabel('Month number')
plt.show()




### Question 2: What city had the heightest number of sales
results = all_data.groupby('City').sum()

# Visualisation
cities = [city for city, df in all_data.groupby('City')]

plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation='vertical', size=5)
plt.ylabel('Sales in USD  ($)')
plt.xlabel('City name')
plt.show()




### Question 3: What time shold we display advertisements to maximize likelihood of customer's buying product ?
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])

all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute

# Visualisation
hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()

# My recomended is around 11am(11) or 7pm(19)






### Question 4: What products are mst often sold together ?
df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

df = df[['Order ID', 'Grouped']].drop_duplicates()

# Reference : counting-inique pairs of numbers into a python dictionary
from itertools import combinations
from collections import Counter
count = Counter()
for row in df['Grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key, value)





### Question 5: What product sold the most ? Why do you think it sold the most ?

product_group = all_data.groupby('Product')
Quantity_ordered = product_group.sum()['Quantity Ordered']

# Visualisation
products = [product for product, df in product_group]

plt.bar(products, Quantity_ordered)
plt.xticks(products, rotation='vertical', size=4)
plt.ylabel('# Ordered')
plt.xlabel('Product')
plt.show()

prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, Quantity_ordered)
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=6)

plt.show()











   