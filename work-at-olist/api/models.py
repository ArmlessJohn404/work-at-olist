from django.db import models

# TODO: Implement Node as an "ltree" or "mtptt" make queries log(n)
class Node(models.Model):
    """
    Basic data structure for the database.
    Each node points to a parent in the tree. Those are the `categories`
    If the parent is `None`, then the node is at the `root` and is a `channel`
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

    @property
    def branch(self):
        """
        Returns the entire branch abobe this Node up to the root
        """
        if isinstance(self.parent, Node):
            return self.parent.branch+" / "+self.name
        return self.name

    def _tree(self, tree):
        """
        Recursively appends the `Node` to `tree` without the root (channel)
        """
        if self.parent is not None:
            tree.append(" / ".join(self.branch.split(" / ")[1:]))
        for branch in self.node_set.all():
            branch._tree(tree)

    @property
    def tree(self):
        """
        Returns the entire tree below this `Node`
        """
        tree = []
        self._tree(tree)
        return str("\n".join(tree))
