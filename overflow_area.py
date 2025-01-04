class OverflowManager:
    def __init__(self):
        self.overflow_storage = {}  # key -> value

    def add_record(self, key, value):
        self.overflow_storage[key] = value

    def get_record(self, key):
        return self.overflow_storage.get(key, None)

    def exists(self, key):
        return key in self.overflow_storage

    def delete_record(self, key):
        self.overflow_storage.pop(key, None)

    def edit_record(self, key, new_value):
        if key in self.overflow_storage:
            self.overflow_storage[key] = new_value
