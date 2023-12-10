import time
from collections import defaultdict

each_baskets = []

text_path = "C:\\Users\\R\\vscodework\\4250\\Project1\\retail.txt"

# chunks and thresholds
set_thresholds = [0.01, 0.05, 0.10]  #1%, 5%, 10% chunks
set_sizes_of_dataset = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]  #10%, 20%, 50%, 100% data


with open(text_path, 'r') as text:
    for line in text:
        create_singlebasket = [int(item) for item in line.strip().split()]
        each_baskets.append(create_singlebasket)


#A-Priori function
def apriori(each_baskets, supp_threshold):

    single_itemcount = defaultdict(int)
    for basket in each_baskets:
        for item in basket:
            single_itemcount[item] += 1

    #filter single if above threshold
    frequent_single_items = set()
    for k, v in single_itemcount.items():
        if v >= supp_threshold:
            frequent_single_items.add(k)

    #count pairs
    count_each_pairs = defaultdict(int)
    for basket in each_baskets:
        set_basket = set(basket) & frequent_single_items
        for i, item_i in enumerate(set_basket):
            for item_j in list(set_basket)[i+1:]:
                if item_i < item_j:
                    count_each_pairs[(item_i, item_j)] += 1
                else:
                    count_each_pairs[(item_j, item_i)] += 1

    #get frequent pairs
    frequent_pair_items = set()
    for k, v in count_each_pairs.items():
        if v >= supp_threshold:
            frequent_pair_items.add(k)

    return frequent_pair_items


#loop for thresholds and chunks
for support_percentage in set_thresholds:
    for chunk_size in set_sizes_of_dataset:
        
        supp_threshold = (len(each_baskets) * support_percentage)
        
        select_basket_chunk = each_baskets[:int(len(each_baskets) * chunk_size)]
        
        # measure time
        start_timer = time.time()
        
        find_frequent_itemsets = apriori(select_basket_chunk, supp_threshold)
        
        print(f"Frequent Itemsets: {find_frequent_itemsets}")

        execution_time = (time.time() - start_timer) * 1000
        print(f"Execution Time: {execution_time:.2f} ms --- Chunk size is {chunk_size:.2f} --- Support threshold is {support_percentage*100}%\n")
