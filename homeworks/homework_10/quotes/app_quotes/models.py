from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=32, null=False)
    born_date = models.CharField(max_length=32, null=False)
    born_location = models.TextField(max_length=64, null=False)
    description = models.CharField(null=False)
    
    def __str__(self):
        return f"{self.fullname}"

class Tag(models.Model):
    tag = models.CharField(max_length=32, null=False, unique=True)

    def __str__(self):
        return f"{self.tag}"

class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    quote = models.TextField(null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote}"
