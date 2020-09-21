from django.db import models


class Flight(models.Model):
    date = models.DateField()
    flyFrom = models.CharField(max_length=10)
    flyTo = models.CharField(max_length=10)
    id_flight = models.TextField()
    token = models.TextField()
    price = models.IntegerField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.date}/{self.flyFrom}-{self.flyTo}"
