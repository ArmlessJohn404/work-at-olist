from django.test import TestCase
from .models import Node


class NodeClassTests(TestCase):

    def test_node_stores_its_name(self):
        node = Node(name="node_name")
        self.assertIs(node.name, "node_name")

    def test_node_stores_its_parent(self):
        parent = Node(name="parent")
        node = Node(name="node_name", parent=parent)
        self.assertIs(parent, node.parent)

    def test_node_parent_name_method(self):
        parent = Node(name="parent")
        node = Node(name="node_name", parent=parent)
        self.assertIs(node.parent_name, parent.name)

    def test_node_tree_method(self):
        parent = Node(name="parent")
        node = Node(name="node_name", parent=parent)
        bro_node = Node(name="bro_node_name", parent=parent)
        sub_node = Node(name="sub_node_name", parent=node)
        bro_sub_node = Node(name="bro_sub_node_name", parent=node)
        tree = "{0} / {1} / {2}".format(parent.name, node.name, sub_node.name)
        self.assertEquals(sub_node.tree, tree)
