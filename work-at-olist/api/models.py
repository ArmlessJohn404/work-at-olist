from django.db import models

# TODO: Implement Node as an "ltree" or "mtptt" make queries log(n)
class Node(models.Model):
    """
    Basic data structure for the database.
    Each node points to a parent in the tree. Those are the `categories`
    If the parent is `None`, then the node is at the `root` and is a `channel`
    `root` nodes are not shown
    """

    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True,
                               on_delete=models.CASCADE)

    class Meta:
        unique_together = (("name", "parent"))

    def __repr__(self):
        return self.branch
    __str__ = __repr__

    @property
    def parent_name(self):
        """
        Returns the parent node's name
        """
        return self.parent.name if isinstance(self.parent, Node) else 'root'

    def _branch(self):
        """
        Recursively gets the branch of the `Node`
        """
        if self.parent is not None:
            return self.parent._branch()+" / "+self.name
        else:
            return self.name

    @property
    def branch(self):
        """
        Returns the entire branch abobe this Node up to the root
        """
        branch = self._branch()
        return " / ".join(branch.split(" / ")[1:])

    def _tree(self, tree):
        """
        Recursively appends the `Node` to `tree` without the root (channel)
        """
        if self.parent is not None:
            tree.append(self.branch)
        for branch in self.node_set.all():
            branch._tree(tree)

    @property
    def tree(self):
        """
        Returns the entire tree below this `Node`
        """
        tree = []
        self._tree(tree)
        return str("\n".join(tree)).strip()

    def _find_category(self, category_list):
        category_name = category_list.pop(0)
        for new_node in self.node_set.all():
            if new_node.name == category_name:
                if category_list:
                    return new_node._find_category(category_list)
                else:
                    return new_node
        else:
            return

    def find_category(self, category_name):
        """
        Returns the category `Node` inside the instance tree
        """
        category_list = category_name.split(" / ")
        return self._find_category(category_list)
