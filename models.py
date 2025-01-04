class Record:
    """Basic record model with a unique key and some data."""
    def __init__(self, key, data):
        self.key = key
        self.data = data

    def __repr__(self):
        return f"Record(key={self.key}, data={self.data})"
