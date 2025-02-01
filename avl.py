class Node(object):

    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVL(object):
    """
    class implementing a self-balancing binary search tree
    implementing in-order, pre-order, past-order and bfs
    public wrapper methods for interaction are written for methods
    """

    def __init__(self):
        self.__root = None

    def __height(self, node: Node) -> int:
        if node is None:
            return 0
        return node.height

    def __balance_factor(self, node: Node) -> int:
        if node is None:
            return 0
        return self.__height(node.right) - self.__height(node.left)

    def __fix_height(self, node: Node) -> None:
        height_left = self.__height(node.left)
        height_right = self.__height(node.right)

        node.height = max(height_left, height_right) + 1

    def __right_rotate(self, node: Node) -> Node:
        left_child = node.left
        node.left = left_child.right
        left_child.right = node

        self.__fix_height(node)
        self.__fix_height(left_child)

        return left_child

    def __left_rotate(self, node: Node) -> Node:
        right_child = node.right
        node.right = right_child.left
        right_child.left = node

        self.__fix_height(node)
        self.__fix_height(right_child)

        return right_child

    def __balance(self, node: Node) -> Node:
        self.__fix_height(node)

        if self.__balance_factor(node) == 2:
            # big left rotation
            if self.__balance_factor(node.right) < 0:
                node.right = self.__right_rotate(node.right)

            return self.__left_rotate(node)

        elif self.__balance_factor(node) == -2:
            # big right rotation
            if self.__balance_factor(node.left) > 0:
                node.left = self.__left_rotate(node.left)

            return self.__right_rotate(node)

        return node

    def __insert(self, node: Node, data: int) -> Node:
        if node is None:
            return Node(data)
        if data < node.data:
            node.left = self.__insert(node.left, data)
        else:
            node.right = self.__insert(node.right, data)

        return self.__balance(node)

    def __find_min(self, node: Node) -> Node:
        if node.left is None:
            return node
        return self.__find_min(node.left)

    def __remove_min(self, node: Node) -> Node:
        if node.left is None:
            return node.right
        node.left = self.__remove_min(node.left)
        return self.__balance(node)

    def __remove(self, node: Node, data: int) -> Node:
        if node is None:
            return None

        if data < node.data:
            node.left = self.__remove(node.left, data)

        elif data > node.data:
            node.right = self.__remove(node.right, data)

        elif data == node.data:
            # the found node that requires deletion must be swapped with the leftmost node of the right subtree.
            # This node stores the previous value, in sorting order
            if node.right is None:
                return node.left
            node_min = self.__find_min(node.right)  # node with previous value
            node_min.right = self.__remove_min(node.right)  # link the right subtree with a node
            node_min.left = node.left  # link the left subtree with a node
            return self.__balance(node_min)

        return self.__balance(node)

    def insert(self, data: int) -> None:
        self.__root = self.__insert(self.__root, data)

    def remove(self, data: int) -> None:
        self.__root = self.__remove(self.__root, data)

    def __print_tree(self, node: Node, prefix="", is_left=True) -> None:
        if node is None:
            return

        self.__print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.data))
        self.__print_tree(node.left, prefix + ("    " if is_left else "│   "), True)

    def print_tree(self) -> None:
        self.__print_tree(self.__root)

    def bfs(self) -> list[int]:
        queue = []
        array = []

        queue.insert(0, self.__root)
        while len(queue) != 0:
            node = queue.pop()
            if node is not None:
                array.append(node.data)
                queue.insert(0, node.left)
                queue.insert(0, node.right)

        return array

    def __pre_order(self, node: Node, array: list[int]) -> None:
        if node is None:
            return

        array.append(node.data)

        self.__in_order(node.left, array)
        self.__in_order(node.right, array)

    def pre_order(self) -> list[int]:
        array = []
        self.__pre_order(self.__root, array)
        return array

    def __in_order(self, node: Node, array: list[int]) -> None:
        if node is None:
            return

        self.__in_order(node.left, array)

        array.append(node.data)

        self.__in_order(node.right, array)

    def in_order(self) -> list[int]:
        array = []
        self.__in_order(self.__root, array)
        return array

    def __post_order(self, node: Node, array: list[int]) -> None:
        if node is None:
            return

        self.__in_order(node.left, array)
        self.__in_order(node.right, array)

        array.append(node.data)

    def post_order(self) -> list[int]:
        array = []
        self.__post_order(self.__root, array)
        return array

    def __contains(self, node: Node, data: int) -> bool:
        if node is None:
            return False
        elif node.data == data:
            return True
        elif node.data < data:
            return self.__contains(node.right, data)
        else:
            return self.__contains(node.left, data)

    def contains(self, data: int) -> bool:
        return self.__contains(self.__root, data)

    def __len__(self) -> int:
        return len(self.in_order())

    def __contains__(self, item: int) -> bool:
        return self.__contains(self.__root, item)

    def clear(self):
        self.__root = None


def merge_tree(first_tree: AVL, second_tree: AVL) -> AVL:
    values1 = first_tree.in_order()
    values2 = second_tree.in_order()
    values = values1 + values2

    result_tree = AVL()

    for item in values:
        result_tree.insert(item)

    return result_tree


def split_tree(tree: AVL, value=None) -> (AVL, AVL):
    values = tree.in_order()

    if value is None:
        value = len(values) // 2
    else:
        value = values.index(value)
    first_tree, second_tree = AVL(), AVL()

    for item in values[:value]:
        first_tree.insert(item)
    for item in values[value:]:
        second_tree.insert(item)

    return first_tree, second_tree
