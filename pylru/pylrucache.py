__author__ = 'elpablogrande'

class PyLRUCache:
    """
    Instances of PyLRUCache:
        hold the cache of data in a dictionary as key-value pairs
        Keep track of the rank of each key in the dictionary
        Set and get items in the cache and update rank accordingly
    PyLRUCache instance Variables/Objects:
        cache_size: Integer. Number of items cache can hold.
        rank_offset: Integer. Keeps track of order in which items are inserted, updated or accessed.
        cache_dict: Dictionary. Holds the data being contained in the LRU.
            Also contains the rank_offset at the time of last insert, read or update for the key.
        keymap: List. Holds dictionaries containing the key and rank offset of each item in the cache_dict.
            Always sorted by rank, so the dictionary at position 0 always represents the least recently used item.
            rank offset being stored here allows fast lookup of the ordinal position of any key in the keymap list.
    """

    cache_size = 0
    rank_offset = 0
    cache_dict = {}
    keymap = []

    def __init__(self, capacity):
        """
        Initializer method for cache object.
        :param capacity: capacity of cache (int).
        :return: void
        """
        self.cache_size = capacity

    def set_key(self, key, value):
        """
        Sets value for a given key and upserts key's value in the cache dictionary.
        :param key: Key to be added to the cache dictionary.
        :param value: Value for input key
        :return: 0 for OK
        """

        # increment rank offset
        self.rank_offset += 1

        # rank offset value of key, if it exists; defaults to current rank offset if not
        key_rank_offset = self.rank_offset
        key_is_new = False

        # Does the key exist?
        try:
            key_rank_offset = self.cache_dict[key]['rank_offset']
        except KeyError:
            # If not:
            #   Add the key to the dictionary
            key_is_new = True

        if key_is_new:
            if len(self.cache_dict) == self.cache_size:
                # If the dictionary is at capacity:
                #   Remove the item at the lowest rank
                #   Pop the lowest-ranked key reference from the rank keymap
                lowest_keymap = self.keymap[0]
                lowest_key = lowest_keymap['key']
                del self.cache_dict[lowest_key]
                self.keymap.pop(0)

        else:
            # If key exists:
            #   Find the existing key's ordinal position in the keymap and pop that item
            keymap_ordinal = self.find_keymap_ordinal(key_rank_offset, 0, len(self.keymap))
            self.keymap.pop(keymap_ordinal)

        # Insert the new keymap reference and upsert the key
        self.keymap.append({'key': key, 'rank_offset':self.rank_offset})
        self.cache_dict[key] = {'value': value, 'rank_offset': self.rank_offset}

        # debug
        #print(self.cache_dict)
        #print(self.keymap)

        return 0

    def get_key_value(self, key):
        """
        Returns value for key in the LRU cache dictionary if it exists.
        Updates use rank for key if exists
        :param key: key being searched.
        :return: Value for key if exists, or None
        """

        key_dict = {}
        # Find the key and its rank offset in the LRU dictionary. Return None if doesn't exist.
        try:
            key_dict = self.cache_dict[key]
        except KeyError:
            return None

        # Key exists:
        #   Increment rank offset
        self.rank_offset += 1

        #   Find its ordinal position in keymap and pop that item
        keymap_ordinal = self.find_keymap_ordinal(key_dict['rank_offset'], 0, len(self.keymap))
        self.keymap.pop(keymap_ordinal)

        #   Insert new item with rank offset for key in keymap
        self.keymap.append({'key': key, 'rank_offset': self.rank_offset})

        #   Update rank offset in cache dictionary
        key_dict['rank_offset'] = self.rank_offset
        self.cache_dict[key] = key_dict

        # debug
        #print(self.cache_dict)
        #print(self.keymap)

        # Return the key's value.
        return key_dict['value']

    def find_keymap_ordinal(self, offset, min_position, max_position):
        """
        Recursively finds the ordinal position of a key in the sorted keymap list based on the rank offset.
        Assumes it is being implemented correctly, i.e., it isn't equipped to handle an offset that doesn't exist.
        Also assumes that the keymap list is sorted by rank offset.
        :param offset: Integer. Rank offset value for the key being searched.
        :param min_position: Integer. Lowest ordinal position to consider.
        :param max_position: Integer. Highest ordinal position to consider.
        :return: integer ordinal position of item in keymap for offset.
        """

        # Find the ordinal halfway between the min and max positions
        check_ordinal = min_position + int((max_position - min_position) // 2)

        # Get its rank offset value
        rank_offset = self.keymap[check_ordinal]['rank_offset']

        if rank_offset == offset:
            # if it matches, we've found our ordinal. Return.
            return check_ordinal
        elif rank_offset < offset:
            # recurse high.
            return self.find_keymap_ordinal(offset, check_ordinal, max_position)
        else:
            # recurse low.
            return self.find_keymap_ordinal(offset, min_position, check_ordinal)
