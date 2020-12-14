from django.db import models


class Location(models.Model):
    title = models.CharField(max_length=25)
    location_id = models.IntegerField()

    def __str__(self):
        return self.title


class Item(models.Model):
    query = models.CharField(max_length=20, verbose_name='Поисковый запрос')
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 related_name='items')

    def __str__(self):
        return self.query


class ItemHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='history')
    number = models.IntegerField()
    timestamp = models.IntegerField()

    def __str__(self):
        return self.item.query


class Ad(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name='ads')
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.title
