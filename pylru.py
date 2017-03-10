__author__ = 'elpablogrande'
import pylru.PyLRUCache
import string

# PyLRU
# Main CLI execution script.
# Instantiates a PyLRUCache object and accesses its methods for setting and getting items.

# set up "enumeration" of acceptable commands
command_dictionary = {"SIZE": 0, "GET": 1, "SET": 2, "EXIT": 3}
my_cache = None

run_loop = True
print("PyLRU: Copyright (c) 2017 by Paul Anderson.")

while run_loop:

    # Parse command
    command_list = string.split(raw_input())
    #print(command_list)

    # validate command
    try:
        command_status = command_dictionary[command_list[0]]
    except KeyError:
        print("ERROR")
        continue

    if command_status == 0:
        # execute SIZE - Instantiates cache object.
        # Error if cache object already instantiated.
        if my_cache is not None:
            print("ERROR")
            continue

        # Validate input
        if len(command_list) > 2:
            print("ERROR")
            continue

        try:
            cache_size = int(command_list[1])
        except ValueError:
            print("ERROR")
            continue

        my_cache = pylru.PyLRUCache.PyLRUCache(int(cache_size))
        print("SIZE OK")

    elif command_status == 1:
        # execute GET
        # if cache size not set and cache object not instantiated, print error
        # Validate input
        if len(command_list) > 2:
            print("ERROR")
            continue

        try:
            value_for_key = my_cache.get_key_value(command_list[1])
        except (NameError, AttributeError, IndexError):
            print("ERROR")
            continue

        if value_for_key is None:
            print("NOT FOUND")
        else:
            print("GOT " + value_for_key)

    elif command_status == 2:
        # execute SET
        # if cache size not set and cache object not instantiated, print error

        # Validate input
        if len(command_list) > 3:
            print("ERROR")
            continue

        try:
            set_status = my_cache.set_key(command_list[1], command_list[2])
        except (NameError, AttributeError, IndexError):
            print("ERROR")
            continue

        print("SET OK")

    else:
        # Exit.
        run_loop = False
        break

