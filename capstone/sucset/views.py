from django.views.generic import View
from django.shortcuts import render
from .models import Fullplot, Subplots

def main(request):

    # temp = Finance.objects.only("Name")
    table = Fullplot.objects.all()
    rec = Fullplot.objects.values("recommend").last()["recommend"].split(",")
    subplots = Subplots.objects.all()
    print(rec)
    # good = Temp.objects.values('Good')
    # bad = Temp.objects.values('Bad')
    # rec = Temp.objects.values('Recommend').last()
    context = {
        "table":table,
        "rec":rec,
        "sub":subplots
        # 'date':date,
        # 'good':good,
        # 'bad':bad,
        # 'rec':rec,
    }
    return render(request,'sucset/sucset.html',context)