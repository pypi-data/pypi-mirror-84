class LeetCodeObject:
    @property
    def attr(self):
        return ", ".join("{}: {}".format(k, getattr(self, k)) for k in self.__dict__.keys())

    def __str__(self):
        return self.__class__.__name__ + "{" + "{}".format(self.attr) + "}"


class ListNode(LeetCodeObject):
    """����ڵ�(ListNode)"""

    def __init__(self, val):
        self.val = val
        self.next = None


class TreeNode(LeetCodeObject):
    """�������ڵ�(TreeNode)"""

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Node(LeetCodeObject):
    """���ڵ�(Node)"""

    def __init__(self, val=None, children=None):
        if children is None:
            children = []
        self.val = val
        self.children = children