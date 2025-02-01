def hash_horner(string: str, table_size: int, key: int) -> int:
    hash_result = 0
    for item in string:
        hash_result = (key * hash_result + ord(item)) % table_size
    hash_result = (hash_result * 2 + 1) % table_size
    return hash_result


def hash_function_string1(string: str, table_size: int) -> int:
    return hash_horner(string, table_size, table_size - 1)


def hash_function_string2(string: str, table_size: int) -> int:
    return hash_horner(string, table_size, table_size + 1)


class Node(object):
    def __init__(self, key, value, state=True):
        self.key = key
        self.value = value
        self.state = state

    def __str__(self):
        return f'({self.key}, {self.value}, {self.state})'


class Array(object):
    """
    Associative array implemented on a hash table with collision resolution using the double hashing method
    Provided the ability to access and change elements using self[key] construction
    There is a method that returns a list of keys to check for the presence of a key
    Methods for containing and iterating through an array are also implemented
    """
    __default_size = 8
    __rehash_size = 0.75

    def __init__(self, hash1=hash_function_string1, hash2=hash_function_string2):
        self.__buffer_size = self.__default_size  # size of array
        self.__size = 0  # number of not None elements
        self.__size_all_non_none = 0  # number of all elements
        self.__hash1 = hash1  # first hash function
        self.__hash2 = hash2  # second hash function
        self.__array = [None] * self.__buffer_size  # list of elements

    def __relocation(self):
        self.__size_all_non_none = 0
        self.__size = 0
        array = [None] * self.__buffer_size

        self.__array, array = array, self.__array

        for item in array:
            if item is not None and item.state == True:
                self.add(item.key, item.value)

    def __resize(self):
        past___buffer_size = self.__buffer_size
        self.__buffer_size *= 2
        self.__relocation()

    def __rehash(self):
        self.__relocation()

    def __hashing(self, key):
        try:
            h1 = self.__hash1(key, self.__buffer_size)
            h2 = self.__hash2(key, self.__buffer_size)
            return h1, h2
        except TypeError:
            raise TypeError("Invalid keys")

    def add(self, key, value):
        if self.__size + 1 > int(self.__rehash_size * self.__buffer_size):
            self.__resize()
        elif self.__size_all_non_none > 2 * self.__size:
            self.__rehash()

        h1, h2 = self.__hashing(key)

        i = 0
        first_deleted = -1  # first possible (deleted element) Node
        while self.__array[h1] is not None and i < self.__buffer_size:
            # element already in array
            if self.__array[h1].value == value and self.__array[h1].key and self.__array[h1].state:
                return False
            # changing an element using an existing key
            elif self.__array[h1].key == key:
                self.__array[h1].value = value
                return True
            # there is a place for element
            elif self.__array[h1].state == False and first_deleted == -1:
                first_deleted = h1
            h1 = (h1 + h2) % self.__buffer_size
            i = i + 1

        if first_deleted == -1:  # insertion new element
            self.__array[h1] = Node(key, value)
            self.__size_all_non_none += 1
        else:  # insertion element in deleted position
            self.__array[first_deleted].value = value
            self.__array[first_deleted].key = key
            self.__array[first_deleted].state = True

        self.__size += 1
        return True

    def find(self, key):
        h1, h2 = self.__hashing(key)

        i = 0
        while self.__array[h1] is not None and i < self.__buffer_size:
            if self.__array[h1].key == key and self.__array[h1].state == True:
                return self.__array[h1].value
            h1 = (h1 + h2) % self.__buffer_size
            i = i + 1

        return None

    def remove(self, key):
        h1, h2 = self.__hashing(key)

        i = 0
        while self.__array[h1] is not None and i < self.__buffer_size:
            if self.__array[h1].key == key and self.__array[h1].state == True:
                self.__array[h1].state = False
                self.__size -= 1
                return True
            h1 = (h1 + h2) % self.__buffer_size
            i = i + 1

        return False

    def __len__(self):
        return self.__size

    def keys(self):
        array = []

        for item in self.__array:
            if item is not None and item.state:
                array.append(item.key)

        return array

    def __contains__(self, item):
        if self.find(item):
            return True
        return False

    def __getitem__(self, item):
        return self.find(item)

    def __setitem__(self, key, value):
        return self.add(key, value)

    def __str__(self):
        array = []

        for item in self.__array:
            if item is not None:
                array.append(f'{item.key}: {item.value}')

        return '{' + ', '.join(array) + '}'

    def __iter__(self):  # iterating through an array returns a tuple (key, value)
        for item in self.__array:
            if item is not None:
                yield (item.key, item.value)

    def clear(self):
        self.__buffer_size = self.__default_size
        self.__size = 0
        self.__size_all_non_none = 0
        self.__array = [None] * self.__buffer_size