from django.db import models
from django import forms
import pCalc
# Create your models here.
class Card(models.Model):
    suit = models.CharField(max_length=1)
    rank = models.CharField(max_length=2)
    def __getSuit__(self):
        return self.suit
    def __getRank__(self):
        return self.rank
    def __str__(self):
        return self.rank + self.suit
    def makeCard(self, suit, rank):
        return Card(suit, rank)
class numPlayers(models.Model):
    numPlayers = models.IntegerField()
    def __getNumPlayers__(self):
        return self.numPlayers
    def __str__(self):
        return str(self.numPlayers)