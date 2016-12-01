from itertools import chain

from algo.tests.utils import timeit
from algo.tree.basetree import pretty_tree
from algo.tree.bstree import is_bstree
from algo.tree.rbtree import RBTree, RBNode, is_rbtree


def rbtree_from_nested_list(seq):
    serial = 0

    def create_root(seq):
        nonlocal serial

        if seq is None:
            return None
        if not isinstance(seq, (tuple, list)):
            seq = (seq,)
        assert 1 <= len(seq) <= 3

        color = seq[0]
        left = seq[1] if len(seq) >= 2 else None
        right = seq[2] if len(seq) == 3 else None

        node_left = create_root(left)
        node = RBNode(serial, color)
        serial += 1
        node.left = node_left
        node.right = create_root(right)
        return node

    root = create_root(seq)
    return RBTree(root)


def test_is_rbtree():
    R, B = RBNode.RED, RBNode.BLACK
    cases = (
        (True,  None),
        (True,  (B, None, None)),
        (False, (R, None, None)),
        (True,  (B,
                    R,
                    R,)),
        (True,  (B,
                    None,
                    R,)),
        (False, (B,
                    B,
                    None)),
        (True,  (B,
                    B,
                    B)),
        (False, (B,
                    (R,
                        B),
                    (R,
                        B),)),
        (False, (B,
                    (R,
                        R,
                        R),
                    R,)),
        (True,  (B,
                    B,
                    (R,
                        B,
                        B),)),
    )

    for ans, ques in cases:
        tree = rbtree_from_nested_list(ques)
        assert is_rbtree(tree) is ans


def test_pretty_tree():
    def process(string):
        return [ line.rstrip() for line in string.splitlines() if line.strip() ]

    R, B = RBNode.RED, RBNode.BLACK
    tree = rbtree_from_nested_list([B, B, [B, R, R]])
    ans = '''
       ■1
   ┌───┴───────┐
   ■0          ■3
 ┌─┴─┐     ┌───┴───┐
NIL NIL    □2      □4
         ┌─┴─┐   ┌─┴─┐
        NIL NIL NIL NIL'''

    output = pretty_tree(tree)
    assert process(output) == process(ans)

    tree = RBTree()
    tree.insert(+8601010086)
    ans = '''
■8601010086
   ┌─┴─┐
  NIL NIL'''

    output = pretty_tree(tree)
    assert process(output) == process(ans)


def gen_rbtree_by_insert(max_len):
    nums = []
    used = set()

    def recur(tree, count):
        nonlocal nums

        # exclude duplicated case
        key = tree.to_tuple()
        if key in used:
            return
        else:
            used.add(key)

        if not nums:
            new_nums = uniq_nums = [0]
        else:
            uniq_nums = sorted(set(nums))
            new_nums = [ (uniq_nums[i] + uniq_nums[i + 1]) / 2 for i in range(len(uniq_nums) - 1) ]
            new_nums.extend([min(nums) - 1, max(nums) + 1])

        for num in chain(new_nums, uniq_nums):
            nums.append(num)

            t = tree.deepcopy()
            t.insert(num)
            yield t, count
            if len(nums) < max_len:
                yield from recur(t, count + 1)

            nums.pop()

    yield from recur(RBTree(), 1)


@timeit('RBTree::insert()')
def test_rbtree_insert():
    for tree, count in gen_rbtree_by_insert(7):
        assert tree.count() == count
        assert is_rbtree(tree)
        assert is_bstree(tree)


@timeit('RBTree::remove()')
def test_rbtree_remove():
    def removed_one(arr, el):
        arr = arr.copy()
        arr.remove(el)
        return arr

    def test_remove(t):
        flatten = list(t.data_iter())
        for to_remove in sorted(set(flatten)):
            test_tree = t.deepcopy()
            removed_node = test_tree.remove(to_remove)
            assert removed_node.data == to_remove
            assert list(test_tree.data_iter()) == removed_one(flatten, to_remove)
            assert is_rbtree(test_tree)
            assert is_bstree(test_tree)

        test_tree = t.deepcopy()
        assert test_tree.remove(min(flatten, default=0) - 1) is None
        assert test_tree.remove(max(flatten, default=0) + 1) is None

    for tree, count in gen_rbtree_by_insert(7):
        test_remove(tree)