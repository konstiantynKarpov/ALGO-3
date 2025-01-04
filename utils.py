import random
import string


def generate_random_data(num_records=100, str_len=8, specific_keys=None):
    """
    Generates a list of (key, value) pairs.
    Keys are unique integers, values are random strings.
    Optionally includes specific keys.

    :param num_records: Total number of records to generate.
    :param str_len: Length of the random string for each record.
    :param specific_keys: A list of keys to include in the generated data.
    :return: List of tuples containing (key, value).
    """
    records = []
    used_keys = set()

    # Include specific keys first
    if specific_keys:
        for key in specific_keys:
            if key not in used_keys and len(records) < num_records:
                val = ''.join(random.choices(string.ascii_letters + string.digits, k=str_len))
                records.append((key, val))
                used_keys.add(key)

    # Generate remaining random records
    while len(records) < num_records:
        k = random.randint(1, 9999999)
        if k not in used_keys:
            used_keys.add(k)
            val = ''.join(random.choices(string.ascii_letters + string.digits, k=str_len))
            records.append((k, val))

    return records
