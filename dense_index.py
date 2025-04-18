import pickle
from overflow_area import OverflowManager

def uniform_binary_search(sorted_keys, target):
    """
    Performs a uniform binary search on a sorted list of keys.
    Args:
        sorted_keys (list): A list of keys sorted in ascending order.
        target: The key value to search for.
    Returns:
        tuple: (index, comparisons) if target is found, where index is the
               position in the list.
               (None, comparisons) if target is not found.
               'comparisons' is the number of comparisons made during the search.
    """
    low = 0
    high = len(sorted_keys) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if sorted_keys[mid] == target:
            return mid, comparisons
        elif sorted_keys[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None, comparisons

class DenseIndex:
    """
    Manages a dense index with primary storage and an overflow area.
    Index list stores tuples: (key, offset, location_type: 'primary'|'overflow').
    Primary storage simulates the main data file (in-memory dict).
    """
    MAX_PRIMARY_SIZE = 100

    def __init__(self):
        """Initializes an empty dense index structure."""
        self.index_list = []
        self.primary_storage = {}
        self.overflow_mgr = OverflowManager()

    def _find_index_pos(self, key):
         """
         Internal helper to find the index position of a key using binary search.
         Args: key: The key to search for in the index list.
         Returns: tuple (index, comparisons) or (None, comparisons)
         """
         keys_only = [item[0] for item in self.index_list]
         idx, comparisons = uniform_binary_search(keys_only, key)
         return idx, comparisons

    def search_with_comparisons(self, key):
        """
        Searches for a key using the index and overflow area.
        Checks overflow first, then performs binary search on the index.
        Args: key: The key to search for.
        Returns: tuple (value, comparisons) if found, (None, comparisons) if not found.
                 Comparisons count refers to the binary search on the index.
                 Returns 0 comparisons if found directly in overflow.
        """
        if self.overflow_mgr.exists(key):
             record = self.overflow_mgr.get_record(key)
             if record is not None:
                 return record, 0
             else:
                 return None, 0

        idx, comparisons = self._find_index_pos(key)

        if idx is None:
            return None, comparisons

        _, _, loc_type = self.index_list[idx]

        if loc_type == 'primary':
             value = self.primary_storage.get(key)
             return value, comparisons


        if loc_type == 'overflow':
            value = self.overflow_mgr.get_record(key)
            return value, comparisons # Value might be None if deleted from overflow

        return None, comparisons


    def insert(self, key, value):
        """
        Inserts a key-value pair. Checks for existence first.
        Adds to primary storage if space allows, otherwise to overflow.
        Updates the index list.
        Args:
            key: The key of the record to insert.
            value: The value of the record to insert.
        Returns: tuple (bool: success, str: message)
        """
        current_value, _ = self.search_with_comparisons(key)
        if current_value is not None:
            return False, f"Error: Key {key} already exists."

        if len(self.primary_storage) < self.MAX_PRIMARY_SIZE:
            self.primary_storage[key] = value
            self._insert_into_index(key, 0, 'primary')
            return True, f"Record (Key: {key}) inserted successfully into primary storage."
        else:
            self.overflow_mgr.add_record(key, value)
            self._insert_into_index(key, 0, 'overflow')
            return True, f"Record (Key: {key}) inserted successfully into overflow area."

    def delete(self, key):
        """
        Deletes a record by key. Removes from storage (primary/overflow) and index.
        Args: key: The key of the record to delete.
        Returns: tuple (bool: success, str: message)
        """
        current_value, _ = self.search_with_comparisons(key)
        if current_value is None:
            return False, f"Error: Record with key {key} not found."

        if self.overflow_mgr.exists(key):
            self.overflow_mgr.delete_record(key)

        if key in self.primary_storage:
             self.primary_storage.pop(key, None)

        idx, _ = self._find_index_pos(key)
        if idx is not None:
            self.index_list.pop(idx)
            return True, f"Record (Key: {key}) deleted successfully."
        else:
             # This case should ideally not happen if search found it earlier
             return False, f"Error: Key {key} found initially but failed to delete from index."


    def edit(self, key, new_value):
        """
        Edits the value of an existing record. Checks overflow first.
        Args:
            key: The key of the record to edit.
            new_value: The new value for the record.
        Returns: tuple (bool: success, str: message)
        """
        current_value, _ = self.search_with_comparisons(key)
        if current_value is None:
            return False, f"Error: Record with key {key} not found for editing."

        if self.overflow_mgr.exists(key):
            self.overflow_mgr.edit_record(key, new_value)
            return True, f"Record (Key: {key}) updated successfully in overflow area."
        elif key in self.primary_storage:
            self.primary_storage[key] = new_value
            return True, f"Record (Key: {key}) updated successfully in primary storage."
        else:
             return False, f"Error: Key {key} found initially but update failed (not in primary or overflow)."


    def _insert_into_index(self, key, offset, loc_type):
        """
        Inserts index entry (key, offset, loc_type) while maintaining sorted order by key.
        Uses linear search for insertion position for simplicity.
        Args:
            key: The key to insert.
            offset: The offset or pointer (currently unused, set to 0).
            loc_type (str): 'primary' or 'overflow'.
        """
        new_entry = (key, offset, loc_type)
        inserted = False
        for i, (k, _, _) in enumerate(self.index_list):
            if k > key:
                self.index_list.insert(i, new_entry)
                inserted = True
                break
        if not inserted:
            self.index_list.append(new_entry)

    def save_to_disk(self, filename='dense_index_db.pkl'):
        """
        Saves the entire DenseIndex object to disk using pickle.
        Args: filename (str): The name of the file to save to.
        """
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self, f)
            print(f"DenseIndex saved to {filename}.")
        except Exception as e:
            print(f"Error saving index to {filename}: {e}")


    @staticmethod
    def load_from_disk(filename='dense_index_db.pkl'):
        """
        Loads the DenseIndex object from disk.
        Args: filename (str): The name of the file to load from.
        Returns: DenseIndex object if successful, None otherwise.
        """
        try:
            with open(filename, 'rb') as f:
                dense_index = pickle.load(f)
            print(f"DenseIndex loaded from {filename}.")
            return dense_index
        except FileNotFoundError:
            print(f"Error: Data file {filename} not found. Creating new index.")
            return None
        except Exception as e:
            print(f"Error loading index from {filename}: {e}")
            return None

class OverflowManager:
    """Manages the overflow area using a dictionary."""
    def __init__(self):
        """Initializes an empty dictionary for overflow storage."""
        self.overflow_storage = {}

    def add_record(self, key, value):
        """Adds or updates a record in the overflow storage."""
        self.overflow_storage[key] = value

    def get_record(self, key):
        """
        Gets a record from overflow storage.
        Args: key: The key to retrieve.
        Returns: The value if key exists, None otherwise.
        """
        return self.overflow_storage.get(key, None)

    def exists(self, key):
        """
        Checks if a key exists in the overflow storage.
        Args: key: The key to check.
        Returns: True if the key exists, False otherwise.
        """
        return key in self.overflow_storage

    def delete_record(self, key):
        """
        Deletes a record from overflow storage if it exists.
        Args: key: The key to delete.
        """
        self.overflow_storage.pop(key, None)


    def edit_record(self, key, new_value):
        """
        Edits a record in overflow storage if it exists.
        Args:
            key: The key of the record to edit.
            new_value: The new value for the record.
        """
        if key in self.overflow_storage:
            self.overflow_storage[key] = new_value