from django.db import models


class Comment(models.Model):
    author = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return "%s : %s" % (self.author, self.text)
