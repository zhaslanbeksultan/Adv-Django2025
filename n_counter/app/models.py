from django.contrib.auth.models import User
from django.db import models


class Food(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=250)
    carbs = models.FloatField(default=0)
    proteins = models.FloatField(default=0)
    fats = models.FloatField(default=0)
    calories = models.IntegerField(default=0)


class Consume(models.Model):
    food_consumed = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)