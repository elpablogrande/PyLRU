# PyLRU
Scalable LRU algorithm in Python 2.7

To run: 
`python pylru.py`

To extend, import 

#How it works:

The purpose of the design is to manage rank quickly and at any scale, avoiding any scans of the entire cache.

Instances of the class **PyLRUCache** manage a LRU cache of the size specified in the class's \__init__ method. There are two main data structures governing the cache: 

**dictionary *cache_dict*:**

Each key in this dictionary literally represents an item in the cache. Each key holds a dictionary containing two variables:

*value:* The value attributed to the key.

*rank_offset:* An integer; the value of the PyLRUCache instance variable rank_offset at the time the item was inserted, updated or read, which gets incremented each time an item is inserted, updated or read. *rank\_offset* represents the *cardinal* rank of each record.

**list *keymap*:**

Each object in this list (a dictionary) also represents an item in the cache; its position in the cache determines its *ordinal* rank according to least recent use, 0 being least recent. Its purpose is to provide a lookup of the rank of any given key without having to scan each record in *cache_dict.* Each record in *keymap*  contains the following two variables:

*key:* The item's key in *cache_dict*

*rank_offset:* The item's rank_offset as stored in *cache\_dict* - The important thing to know is that items in *keymap* are always sorted by this value.

The purpose of *keymap* is to provide a lookup for any given key by either its LRU rank or its *rank_offset* value. 

For example:

If a call to the *set_key* method for a distinct new key results in an overflow of the cache: 

1. it will simply look up the key for the item in keymap position 0
2. Identify the lowest-ranked item in *cache_dict* from this key, and delete it
3.  Pop the item at positon 0 from *keymap*; item at position 1 moves to position 0
4. Append records to *cache_dict* and *keymap* for the new key.

In cases of a read or update to a given existing key:

1. It finds the key's *rank_offset* variable from *cache_dict*, which stores the order of operations upon items *independently* from 
2. Looks up the ordinal position of the key in the *keymap* using the *rank_offset* value using the recursive *find\_keymap_ordinal* method
3. Pops the item at this location from *keymap* and re-inserts it, thus resetting its ordinal rank - Along with its updated *rank_offset* value.
4. Updates the *rank_offset* and/or value for the key in *cache_dict*

#Assumptions
(the mother of all F*ups, but time is limited...)

My main assumption here is that Python doesn't perform a full scan when looking up a key in a dictionary, but instead has a fast algorithm. I'll be looking into this. The intention of this design was to take advantage of the key-lookup capabilities of Python dictionaries and the FIFO capabilities of Python lists. It works, but does it scale? Stay tuned.

Also assuming all future implementation goes according to design; e.g., nobody extending this writes code that inserts records into *keymap* in the incorrect order. I didn't take the time to build in fail-safes.