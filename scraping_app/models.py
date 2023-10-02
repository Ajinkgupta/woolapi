from django.db import models

class CommodityData(models.Model):
    commodity_name = models.CharField(max_length=255)
    actual = models.FloatField()
    previous = models.FloatField()
    highest = models.FloatField()
    lowest = models.FloatField()
    dates = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    class Meta:
        app_label = 'scraping_app'  # Specify the app label here


    def __str__(self):
        return self.commodity_name
