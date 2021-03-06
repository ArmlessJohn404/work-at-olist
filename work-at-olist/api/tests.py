from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import IntegrityError
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

    def test_if_cant_store_duplicate_nodes(self):
        parent = Node(name="parent")
        parent.save()
        node1 = Node(name="node_name", parent=parent)
        node1.save()
        with self.assertRaises(IntegrityError):
            node2 = Node(name="node_name", parent=parent)
            node2.save()

    def test_node_branch_property(self):
        parent = Node(name="parent", parent=None)
        node = Node(name="node_name", parent=parent)
        bro_node = Node(name="bro_node_name", parent=parent)
        s_node = Node(name="s_node_name", parent=node)
        bro_s_node = Node(name="bro_s_node_name", parent=node)
        branch = "{0} / {1}".format(node.name, s_node.name)
        self.assertEqual(s_node.branch, branch)

    def test_node_tree_property(self):
        parent = Node(name="parent", parent=None)
        parent.save()
        node = Node(name="node_name", parent=parent)
        node.save()
        bro_node = Node(name="bro_node_name", parent=parent)
        bro_node.save()
        s_node = Node(name="s_node_name", parent=node)
        s_node.save()
        bro_s_node = Node(name="bro_s_node_name", parent=node)
        bro_s_node.save()
        node_tree = ("node_name\n"
                     "node_name / s_node_name\n"
                     "node_name / bro_s_node_name")
        parent_tree = node_tree + "\nbro_node_name"
        self.assertEqual(parent.tree, parent_tree)
        self.assertEqual(node.tree, node_tree)

    def test_node_find_category_method(self):
        parent = Node(name="parent", parent=None)
        parent.save()
        node = Node(name="node_name", parent=parent)
        node.save()
        bro_node = Node(name="bro_node_name", parent=parent)
        bro_node.save()
        s_node = Node(name="s_node_name", parent=node)
        s_node.save()
        bro_s_node = Node(name="bro_s_node_name", parent=node)
        bro_s_node.save()
        s_bro_s_node = Node(name="s_bro_s_node_name", parent=s_node)
        bro_s_node.save()
        self.assertEqual(parent.find_category("node_name"), node)
        self.assertEqual(parent.find_category("node_name / s_node_name"),
                          s_node)
        self.assertEqual(parent.find_category("node_name / error"),
                          None)


class ImportcategoriesCommandTests(TestCase):

    def raise_importcategories(self, *args):
        with self.assertRaises(CommandError):
            call_command("importcategories", *args)

    def get_database_str(self):
        db_str = ""
        for node in Node.objects.all()[1:]:
            db_str += str(node)+"\n"
        return db_str

    def get_file_str(self, filename):
        file_str = ""
        for line in import_from_csv(filename)['category']:
            file_str += str(line+"\n")
        return file_str

    def test_importcategories_with_no_arguments(self):
        self.raise_importcategories()

    def test_importcategories_with_one_argument(self):
        self.raise_importcategories(["kitten"])

    def test_importcategories_three_arguments(self):
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
        file_str = self.get_file_str(TEST_FILE2)
        self.assertEqual(db_str, file_str)

    def test_importcategories_does_full_update(self):
        channel = "catTube"
        call_command("importcategories", channel, TEST_FILE1)
        call_command("importcategories", channel, TEST_FILE2)
        db_str = self.get_database_str()
        file_str = self.get_file_str(TEST_FILE2)
        self.assertEqual(db_str, file_str)

    def test_importcategories_on_two_channels(self):
        channel1 = "catTube"
        call_command("importcategories", channel1, TEST_FILE1)
        channel2 = "british bagels"
        call_command("importcategories", channel2, TEST_FILE2)
        db_str = self.get_database_str()
        file_str1 = self.get_file_str(TEST_FILE1)
        file_str2 = self.get_file_str(TEST_FILE2)
        # str1 and str2 concatenation must follow alphabetical order
        self.assertEqual(db_str, file_str1+"\n"+file_str2)


class ViewsTests(TestCase):

    def setUp(self):
        parent = Node(name="parent", parent=None)
        parent.save()
        other_parent = Node(name="other_parent", parent=None)
        other_parent.save()
        node = Node(name="node_name", parent=parent)
        node.save()
        bro_node = Node(name="bro_node_name", parent=parent)
        bro_node.save()
        s_node = Node(name="s_node_name", parent=node)
        s_node.save()
        bro_s_node = Node(name="bro_s_node_name", parent=node)
        bro_s_node.save()
        s_bro_s_node = Node(name="s_bro_s_node_name", parent=s_node)
        s_bro_s_node.save()

    def test_root_page(self):
        response = self.client.get("/")
        # print(response)

    def test_api_page(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work at Olist API")

    def test_channels_page(self):
        response = self.client.get("/api/?channels&preety")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "parent")
        self.assertContains(response, "other_parent")

    def test_channel_page(self):
        response = self.client.get("/api/?channel=parent&preety")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "node_name")
        self.assertContains(response, "s_bro_s_node_name")

    def test_category_page(self):
        response = self.client.get(
            "/api/?channel=parent&category=node_name / s_node_name&preety")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "node_name")
        self.assertContains(response, "s_bro_s_node_name")


class ApiTests(TestCase):
    def setUp(self):
        parent = Node(name="parent", parent=None)
        parent.save()
        other_parent = Node(name="other_parent", parent=None)
        other_parent.save()
        node = Node(name="node_name", parent=parent)
        node.save()
        bro_node = Node(name="bro_node_name", parent=parent)
        bro_node.save()
        s_node = Node(name="s_node_name", parent=node)
        s_node.save()
        bro_s_node = Node(name="bro_s_node_name", parent=node)
        bro_s_node.save()
        s_bro_s_node = Node(name="s_bro_s_node_name", parent=s_node)
        s_bro_s_node.save()

    def test_channels(self):
        response = self.client.get("/api/?channels")
        json = {"channels": ["parent", "other_parent"]}
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode("utf-8"), json)


    def test_channel(self):
        response = self.client.get("/api/?channel=parent")
        json = {
            "tree": [
                "node_name", "node_name / s_node_name",
                "node_name / s_node_name / s_bro_s_node_name",
                "node_name / bro_s_node_name", "bro_node_name"],
            "channel": "parent"}
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode("utf-8"), json)

    def test_channel_fail(self):
        response = self.client.get("/api/?channel=fail")
        self.assertEqual(response.status_code, 404)

    def test_category(self):
        response = self.client.get("/api/?channel=parent&category=node_name")
        json = {
            "category": "node_name",
            "tree": [
                "node_name",
                "node_name / s_node_name",
                "node_name / s_node_name / s_bro_s_node_name",
                "node_name / bro_s_node_name"
            ],
            "branch": "node_name",
            "channel": "parent"
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode("utf-8"), json)
        response = self.client.get(
            "/api/?channel=parent&category=node_name / s_node_name")
        json = {
            "branch": "node_name / s_node_name",
            "category": "node_name / s_node_name",
            "tree": [
                "node_name / s_node_name",
                "node_name / s_node_name / s_bro_s_node_name"
            ],
            "channel": "parent"
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode("utf-8"), json)

    def test_category_fail(self):
        response = self.client.get("/api/?channel=fail&category=node_name")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/api/?channel=parent&category=fail")
        self.assertEqual(response.status_code, 404)
