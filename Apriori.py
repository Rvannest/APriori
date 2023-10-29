import time
from collections import defaultdict

# Initialize an empty list to store the baskets
baskets = []

# Specify the path to your data file
data_file_path = "C:\\Users\\R\\vscodework\\4250\\Project1\\retail.txt"

# Open and read the data file
with open(data_file_path, 'r') as file:
    for line in file:
        # Split the line into integers and create a basket
        single_basket = [int(item) for item in line.strip().split()]
        baskets.append(single_basket)

# Define the A-Priori function
def apriori(baskets, support_threshold):
    # Count singleton items
    singleton_counts = defaultdict(int)
    for basket in baskets:
        for item in basket:
            singleton_counts[item] += 1

    # Filter singletons that meet the support threshold
    frequent_singletons = {k for k, v in singleton_counts.items() if v >= support_threshold}

    # Counting the occurrence of each candidate pair
    pair_counts = defaultdict(int)
    for basket in baskets:
        basket_set = set(basket) & frequent_singletons  # Keep only frequent singletons
        for i, item_i in enumerate(basket_set):
            for item_j in list(basket_set)[i+1:]:  # Pairing item_i with all subsequent items in basket
                if item_i < item_j:
                    pair_counts[(item_i, item_j)] += 1
                else:
                    pair_counts[(item_j, item_i)] += 1

    # Get the frequent pairs
    frequent_pairs = {k for k, v in pair_counts.items() if v >= support_threshold}

    return frequent_pairs

# Define the chunks sizes and thresholds you want to test
chunk_sizes = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # e.g., 10%, 20%, 50%, 100% of the data
thresholds = [1, 5, 10]  # e.g., 1%, 5%, 10% thresholds

# Run the A-Priori algorithm for each combination of chunk size and threshold
for support_threshold_percentage in thresholds:
    for chunk_size in chunk_sizes:
        # Calculate the actual support threshold
        support_threshold = (len(baskets) * support_threshold_percentage) / 100
        
        # Select the chunk of the dataset to use
        baskets_chunk = baskets[:int(len(baskets) * chunk_size)]
        
        # Measure the execution time
        start_time = time.time()
        
        # Run the A-Priori algorithm on the selected chunk
        frequent_itemsets = apriori(baskets_chunk, support_threshold)
        
        # Calculate and print the execution time in milliseconds
        execution_time = (time.time() - start_time) * 1000
        print(f"Execution Time: {execution_time:.2f} ms with a chunk size of {chunk_size:.2f} and {support_threshold_percentage}% threshold")
        
        # Print the frequent itemsets
        print(f"Frequent Itemsets: {frequent_itemsets}\n")
