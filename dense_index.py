import pickle
from uniform_binary import uniform_binary_search
from overflow_area import OverflowManager

class DenseIndex:
    """
    The DenseIndex manages:
    1) A sorted list of (key, offset, location_type) for quick searching.
       location_type can be 'primary' or 'overflow'.
    2) An in-memory "primary" structure (dict) that simulates the primary file.
    3) An overflow manager for extra records.
    """

    MAX_PRIMARY_SIZE = 100  # Example threshold for deciding "full" primary

    def __init__(self):
        self.index_list = []
        self.primary_storage = {}
        self.overflow_mgr = OverflowManager()

    def search(self, key):
        """Search via the dense index. Returns the found value or None."""
        result = uniform_binary_search([item[0] for item in self.index_list], key)
        if result is None:
            return None

        idx, _ = result
        _, _, loc_type = self.index_list[idx]

        if loc_type == 'primary':
            return self.primary_storage.get(key, None)
        else:
            return self.overflow_mgr.get_record(key)

    def search_with_comparisons(self, key):
        """
        Searches for a key and returns a tuple of (value, comparisons).
        """
        sorted_keys = [item[0] for item in self.index_list]
        idx, comparisons = uniform_binary_search(sorted_keys, key)
        if idx is None:
            return None, comparisons

        _, _, loc_type = self.index_list[idx]
        if loc_type == 'primary':
            return self.primary_storage.get(key, None), comparisons
        else:
            return self.overflow_mgr.get_record(key), comparisons

    def insert(self, key, value):
        if key in self.primary_storage or self.overflow_mgr.exists(key):
            print(f"Key {key} already exists. Skipping insertion.")
            return

        if len(self.primary_storage) < self.MAX_PRIMARY_SIZE:
            self.primary_storage[key] = value
            self._insert_into_index(key, 0, 'primary')
            print(f"Inserted key {key} into primary storage.")
        else:
            self.overflow_mgr.add_record(key, value)
            self._insert_into_index(key, 0, 'overflow')
            print(f"Inserted key {key} into overflow area.")

    def delete(self, key):
        idx = uniform_binary_search([item[0] for item in self.index_list], key)
        if idx is None:
            return False

        _, _, loc_type = self.index_list[idx]
        if loc_type == 'primary':
            self.primary_storage.pop(key, None)
        else:
            self.overflow_mgr.delete_record(key)

        self.index_list.pop(idx)
        print(f"Deleted key {key} from {loc_type} storage.")
        return True

    def edit(self, key, new_value):
        found = self.search(key)
        if found is None:
            return False
        if key in self.primary_storage:
            self.primary_storage[key] = new_value
            print(f"Edited key {key} in primary storage.")
        else:
            self.overflow_mgr.edit_record(key, new_value)
            print(f"Edited key {key} in overflow storage.")
        return True

    def _insert_into_index(self, key, offset, loc_type):
        new_entry = (key, offset, loc_type)
        inserted = False
        for i, (k, off, loc) in enumerate(self.index_list):
            if k > key:
                self.index_list.insert(i, new_entry)
                inserted = True
                break
        if not inserted:
            self.index_list.append(new_entry)

    def save_to_disk(self, filename='dense_index_db.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print(f"DenseIndex saved to {filename}.")

    @staticmethod
    def load_from_disk(filename='dense_index_db.pkl'):
        with open(filename, 'rb') as f:
            dense_index = pickle.load(f)
        print(f"DenseIndex loaded from {filename}.")
        return dense_index
