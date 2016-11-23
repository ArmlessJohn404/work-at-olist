from django.db import models

# TODO: Implement Node as an "ltree" or "mtptt" make queries log(n)
class Node(models.Model):
    """
    Basic data structure for the database.
    Each node points to a parent in the tree. Those are the `categories`
    If the parent is `None`, then the node is at the `root` and is a `channel`
    """

    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        unique_together = (("name", "parent"))

    def __repr__(self):
        return self.tree

    @property
    def parent_name(self):
        """
        Returns the parent node's name
        """
        return self.parent.name if isinstance(self.parent, Node) else 'root'

    @property
    def tree(self):
        """
        Returns the entire branch abobe the Node up to the root
        """
        if isinstance(self.parent, Node):
            return self.parent.tree+" / "+self.name
        return self.name
