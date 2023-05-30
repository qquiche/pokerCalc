from django.shortcuts import render
from django.http import HttpResponse
from .models import Card, numPlayers
from pCalc import deck
import pCalc
# Create your views here.

def index(request):
    if request.method == 'POST':
        numPlayers = request.POST.get('numPlayers') 
        context = {'numPlayers': numPlayers, 'deck': deck}
        return calcInput(request, context)
    return render(request, 'pokerCalcApp/index.html')
def calcInput(request, context):
    return render(request, 'pokerCalcApp/calcInput.html', context)

