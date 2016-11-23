from django.core.management.base import BaseCommand, CommandError
from rows import import_from_csv
from ...models import Node


class Command(BaseCommand):
    help = "import channel's categories from a CSV: importcategories"

    def add_arguments(self, parser):
        parser.add_argument('channel', nargs=1, type=str)
        parser.add_argument('filename', nargs=1, type=str)

    def handle(self, *args, **options):
        channel = options['channel'][0]
        filename = options['filename'][0]
        data = import_from_csv(filename)

        # Full update mode: Delete all channel's references
        # Just remove those lines if I misunderstood this
        if Node.objects.filter(name=channel, parent=None):
            root = Node.objects.get(name=channel, parent=None)
            self.del_tree(root)

        # Add to DB
        for category in data['category']:
            self.add_tree([channel]+category.split(' / '))
        print(Node.objects.all())

    def add_tree(self, tree, parent=None):
        """
        Recursively adds the tree to the database.
        args:
            `tree` is a list of the tree to be added
            `parent` is a `Node` instance of the current node
                to attach the tree
        """
        if tree:
            current = tree.pop(0).strip()
            if not Node.objects.filter(name=current, parent=parent):
                new = Node(name=current, parent=parent)
                new.save()
            else:
                new = Node.objects.get(name=current, parent=parent)
            self.add_tree(tree, new)

    def del_tree(self, node):
        """
        Recursively deletes the tree
        """
        for branch in Node.objects.filter(parent=node):
            self.del_tree(branch)
        node.delete()