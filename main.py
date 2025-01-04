import random
import csv
import os
from gui import start_gui
from dense_index import DenseIndex
from utils import generate_random_data


def perform_search_tests(dense_index_db, num_tests=15, output_csv='search_results.csv'):

    existing_keys = [item[0] for item in dense_index_db.index_list]
    if not existing_keys:
        print("No keys available for searching.")
        return

    num_existing = num_tests // 2
    num_non_existing = num_tests - num_existing

    test_existing = random.sample(existing_keys, min(num_existing, len(existing_keys)))

    # To ensure non-existing keys, find keys outside the current max range
    max_key = max(existing_keys) if existing_keys else 0
    test_non_existing = []
    while len(test_non_existing) < num_non_existing:
        k = random.randint(max_key + 1, max_key + num_tests * 10)
        if k not in existing_keys:
            test_non_existing.append(k)

    test_keys = test_existing + test_non_existing
    random.shuffle(test_keys)  # Shuffle to mix existing and non-existing keys

    results = []
    for key in test_keys:
        found, comparisons = dense_index_db.search_with_comparisons(key)
        results.append({
            'Search Key': key,
            'Comparisons': comparisons,
            'Found': 'Yes' if found else 'No'
        })

    avg_comparisons = sum(r['Comparisons'] for r in results) / len(results)

    print("\nSearch Performance Analysis:")
    print("{:<12} {:<12} {:<6}".format('Search Key', 'Comparisons', 'Found'))
    for r in results:
        print("{:<12} {:<12} {:<6}".format(r['Search Key'], r['Comparisons'], r['Found']))
    print(f"\nAverage Number of Comparisons: {avg_comparisons:.2f}")

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Search Key', 'Comparisons', 'Found']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)
        writer.writerow({'Search Key': 'Average', 'Comparisons': f"{avg_comparisons:.2f}", 'Found': ''})

    print(f"\nSearch Performance Analysis saved to {output_csv}")


def main():
    data_file = 'dense_index_db.pkl'

    if os.path.exists(data_file):
        dense_index_db = DenseIndex.load_from_disk(data_file)
    else:
        dense_index_db = DenseIndex()

        specific_keys = list(range(1, 101))

        # Generate 10,000 records, including specific keys
        random_records = generate_random_data(10000, specific_keys=specific_keys)
        for key, value in random_records:
            dense_index_db.insert(key, value)

        # Confirm insertion
        print(f"Inserted {len(random_records)} records")
        print(f"Primary Storage Size: {len(dense_index_db.primary_storage)}")
        print(f"Overflow Storage Size: {len(dense_index_db.overflow_mgr.overflow_storage)}")

        # Optionally, print specific keys to confirm
        print("Specific keys inserted:")
        for key in specific_keys:
            value = dense_index_db.search(key)
            print(f"Key: {key}, Value: {value}")

        dense_index_db.save_to_disk(data_file)

    perform_search_tests(dense_index_db, num_tests=15)

    start_gui(dense_index_db)


if __name__ == "__main__":
    main()
