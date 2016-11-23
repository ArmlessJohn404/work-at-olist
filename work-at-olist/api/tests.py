from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from .management.commands.importcategories import Command as ImportCategories
from .models import Node
from rows import import_from_csv

TEST_FILE1 = "api/test/channel1.csv"
TEST_FILE2 = "api/test/channel2.csv"

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


class ImportcategoriesCommandTests(TestCase):

    def raise_importcategories(self, *args):
        with self.assertRaises(CommandError):
            call_command("importcategories", *args)

    def get_database_str(self):
        db_str = ""
        for node in Node.objects.all():
            db_str += str(node)+"\n"
        return db_str

    def get_file_str(self, filename, channel):
        file_str = channel+"\n"
        for line in import_from_csv(filename)['category']:
            file_str += "{0} / {1}\n".format(channel, line)
        return file_str

    def test_importcategories_with_no_arguments(self):
        self.raise_importcategories()

    def test_importcategories_with_one_argument(self):
        self.raise_importcategories(["kitten"])

    def test_importcategories_tree_arguments(self):
        self.raise_importcategories(["catTube", "kitten", "extra"])

    def test_importcategories_two_arguments(self):
        try:
            call_command("importcategories", "catTube", TEST_FILE2)
        except:
            self.fail("importcategories not recognizing the arguments")

    def test_importcategories_saves_on_database(self):
        channel = "catTube"
        call_command("importcategories", channel, TEST_FILE2)
        db_str = self.get_database_str()
        file_str = self.get_file_str(TEST_FILE2, channel)
        self.assertEquals(db_str, file_str)

    def test_importcategories_does_full_update(self):
        channel = "catTube"
        call_command("importcategories", channel, TEST_FILE1)
        call_command("importcategories", channel, TEST_FILE2)
        db_str = self.get_database_str()
        file_str = self.get_file_str(TEST_FILE2, channel)
        self.assertEquals(db_str, file_str)

    def test_importcategories_on_two_channels(self):
        channel1 = "catTube"
        call_command("importcategories", channel1, TEST_FILE1)
        channel2 = "british bagels"
        call_command("importcategories", channel2, TEST_FILE2)
        db_str = self.get_database_str()
        file_str1 = self.get_file_str(TEST_FILE1, channel1)
        file_str2 = self.get_file_str(TEST_FILE2, channel2)
        # str1 and str2 concatenation must follow alphabetical order
        self.assertEquals(db_str, file_str1+file_str2)
