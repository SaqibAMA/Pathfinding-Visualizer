# Python tree implementation

# simple node class
class Node:

    # constructor
    # top, bottom, left, and right denote the frontiers
    def __init__(self, top=None, bottom=None, left=None, right=None, g=None, h=None):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.g = g
        self.h = h


# simple tree implementation
class Tree:

    # constructor
    def __init__(self):
        self.root = None