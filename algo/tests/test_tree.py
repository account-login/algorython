from algo.tests.utils import get_func_name, timed_test, gen_bst
from algo.tree import *
from algo.tree.basetree import *
from algo.tree.bstree import *


all_trees = (
    dict(tree=RBTree),
    dict(tree=AVLTree),
    dict(tree=Treap, is_random=True),
    dict(tree=RSTree, is_random=True),
)


def test_middle_iter():
    for iterator in (middle_iter, middle_iter_bystack, middle_iter_sm):
        with timed_test(get_func_name(iterator)):
            for root in gen_bst(4):
                count = BSTree(root).count()
                expanded = list(iterator(root))
                expanded_sorted = sorted(expanded, key=lambda n: n.data)
                assert len(expanded) == count \
                    and expanded_sorted == expanded == list(middle_iter(root)), \
                    ('{expanded}'.format_map(vars()), print_tree(BSTree(root)))


def test_repr_svg():
    def strip_space(s):
        return ''.join(ch for ch in s if not ch.isspace())

    for tree_type in (BSTree, RBTree, AVLTree, Treap, RSTree):
        tree = tree_type()
        for i in range(5):
            tree.insert(i)

        svg = tree._repr_svg_()
        assert strip_space(svg).startswith(strip_space('''
            <?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
             "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
            <!-- Generated by graphviz'''))


def test_pretty_tree():
    from algo.tree.rbtree import RBNode
    from algo.tests.test_rbtree import rbtree_from_nested_list

    def process(string):
        return [ line.rstrip() for line in string.splitlines() if line.strip() ]

    R, B = RBNode.RED, RBNode.BLACK
    tree = rbtree_from_nested_list([B, B, [B, R, R]])
    ans = '''
       ●1
   ┌───┴───────┐
   ●0          ●3
 ┌─┴─┐     ┌───┴───┐
NIL NIL    ○2      ○4
         ┌─┴─┐   ┌─┴─┐
        NIL NIL NIL NIL'''

    output = pretty_tree(tree)
    assert process(output) == process(ans)

    tree = RBTree()
    tree.insert(+8601010086)
    ans = '''
●8601010086
   ┌─┴─┐
  NIL NIL'''

    output = pretty_tree(tree)
    assert process(output) == process(ans)
