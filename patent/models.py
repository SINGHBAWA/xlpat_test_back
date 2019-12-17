from django.db import models


# Create your models here.
class Patent(models.Model):
    publication_number = models.CharField(max_length=100, unique=True)
    publication_page_url = models.CharField(max_length=1000)
    priority_date = models.DateField(max_length=100)
    publication_date = models.DateField(max_length=100)
    assignee = models.CharField(max_length=100)
    title = models.CharField(max_length=350)
    description = models.CharField(max_length=1500, null=True, blank=True)

    def __str__(self):
        return self.publication_number
