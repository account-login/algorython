from algo.tree.basetree import BaseNode, BaseTree, rotate_left, rotate_right


def avl_height_of(node):
    """
    :type node: AVLNode
    """
    if node is None:
        return 0
    else:
        return node.height


def is_avltree(tree):
    """
    :type tree: AVLTree
    """
    def check(node, parent):
        height = avl_height_of(node)
        if height == 0:
            return True

        l, r = avl_height_of(node.left), avl_height_of(node.right)
        if max(l, r) - min(l, r) > 1:
            return False

        if max(l, r) + 1 != height:
            return False

        if parent is not None:
            if node is parent.left:
                if r > l:
                    return False
            else:
                assert node is parent.right
                if l > r:
                    return False

        return check(node.left, node) and check(node.right, node)

    return check(tree.root, None)


def avl_rotate_left(node):
    """
    :type node: AVLNode
    """
    assert avl_height_of(node.right) > avl_height_of(node.left)
    node = rotate_left(node)
    node.left.height = max(avl_height_of(node.left.right), avl_height_of(node.left.left)) + 1
    node.height = max(avl_height_of(node.right), avl_height_of(node.left)) + 1
    return node


def avl_rotate_right(node):
    """
    :type node: AVLNode
    """
    assert avl_height_of(node.left) > avl_height_of(node.right)
    node = rotate_right(node)
    node.right.height = max(avl_height_of(node.right.left), avl_height_of(node.right.right)) + 1
    node.height = max(avl_height_of(node.left), avl_height_of(node.right)) + 1
    return node


class AVLNode(BaseNode):
    __slots__ = ('height',)

    def __init__(self, data):
        super().__init__(data)
        self.height = 1

    def deepcopy(self):
        ret = super().deepcopy()
        ret.height = self.height
        return ret


class AVLTree(BaseTree):
    __slots__ = ()
    node_type = AVLNode

    def insert(self, data):
        if self.root is None:
            self.root = self.node_type(data)
            return self.root

        stack = [self.root]
        while stack[-1] is not None:
            if data < stack[-1].data:
                stack.append(stack[-1].left)
            else:
                stack.append(stack[-1].right)
        stack.pop()     # pop None

        def fix(node):
            try:
                p = stack.pop()
            except IndexError:
                return

            if node is p.left:
                if avl_height_of(node.left) < avl_height_of(node.right):
                    #       p             p
                    #      / \           / \
                    # (n) *   ?     (n) *   ?
                    #    / \           / \
                    #   2   *   ==>   *   2
                    #      / \       / \
                    #     1   2     2   1
                    p.left = node = avl_rotate_left(p.left)
                assert avl_height_of(node.left) > avl_height_of(node.right)

                left_height, right_height = avl_height_of(p.left), avl_height_of(p.right)
                if left_height == right_height:
                    #     p
                    #    / \
                    #   n   3
                    #  / \
                    # 2   1
                    return
                elif left_height == right_height + 1:
                    #     p
                    #    / \
                    #   n   2
                    #  / \
                    # 2   1
                    p.height += 1
                    fix(p)
                else:
                    #     p           n
                    #    / \         / \
                    #   n   1  ==>  2   p
                    #  / \             / \
                    # 2   1           1   1
                    assert left_height == right_height + 2
                    assert avl_height_of(node.left) \
                        == avl_height_of(node.right) + 1 \
                        == avl_height_of(p.right) + 1
                    new_p = avl_rotate_right(p)
                    self.set_child(p, new_p, stack=stack)
            else:
                assert node is p.right
                if avl_height_of(node.right) < avl_height_of(node.left):
                    p.right = node = avl_rotate_right(p.right)
                assert avl_height_of(node.right) > avl_height_of(node.left)

                right_height, left_height = avl_height_of(p.right), avl_height_of(p.left)
                if right_height == left_height:
                    return
                elif right_height == left_height + 1:
                    p.height += 1
                    fix(p)
                else:
                    assert right_height == left_height + 2
                    assert avl_height_of(node.right) \
                        == avl_height_of(node.left) + 1 \
                        == avl_height_of(p.left) + 1
                    new_p = avl_rotate_left(p)
                    self.set_child(p, new_p, stack=stack)

        cur = stack.pop()
        new_node = self.node_type(data)
        if data < cur.data:
            cur.left = new_node
        else:
            cur.right = new_node

        if cur.left is None or cur.right is None:
            cur.height += 1
            fix(cur)

        return new_node