from django.db import models

# TODO: Implement Node as an "ltree" or "mtptt" make queries log(n)
class Node(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        unique_together = (("name", "parent"))

    def __repr__(self):
        return self.tree

    @property
    def parent_name(self):
        return self.parent.name if isinstance(self.parent, Node) else 'root'

    @property
    def tree(self):
        if isinstance(self.parent, Node):
            return self.parent.tree+" / "+self.name
        return self.name
