import time
from collections import defaultdict

baskets = []

data_file_path = ""

with open(data_file_path, 'r') as file:
    for line in file:
        single_basket = [int(item) for item in line.strip().split()]
        baskets.append(single_basket)

# A-Priori function
def apriori(baskets, support_threshold):
    singleton_counts = defaultdict(int)
    for basket in baskets:
        for item in basket:
            singleton_counts[item] += 1

    frequent_singletons = {k for k, v in singleton_counts.items() if v >= support_threshold}

    pair_counts = defaultdict(int)
    for basket in baskets:
        basket_set = set(basket) & frequent_singletons
        for i, item_i in enumerate(basket_set):
            for item_j in list(basket_set)[i+1:]:
                if item_i < item_j:
                    pair_counts[(item_i, item_j)] += 1
                else:
                    pair_counts[(item_j, item_i)] += 1

    frequent_pairs = {k for k, v in pair_counts.items() if v >= support_threshold}

    return frequent_pairs

chunk_sizes = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  # 10%, 20%, 50%, 100% of the data
thresholds = [1, 5, 10]  # 1%, 5%, 10% thresholds

for support_threshold_percentage in thresholds:
    for chunk_size in chunk_sizes:
        support_threshold = (len(baskets) * support_threshold_percentage) / 100
        
        baskets_chunk = baskets[:int(len(baskets) * chunk_size)]
        
        start_time = time.time()
        
        frequent_itemsets = apriori(baskets_chunk, support_threshold)
        
        execution_time = (time.time() - start_time) * 1000
        print(f"Execution Time: {execution_time:.2f} ms with a chunk size of {chunk_size:.2f} and {support_threshold_percentage}% threshold")
        
        print(f"Frequent Itemsets: {frequent_itemsets}\n")
