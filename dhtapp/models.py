from django.db import models

class Dht11(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temp: {self.temperature}, Humidité: {self.humidity}, Heure: {self.timestamp}"
