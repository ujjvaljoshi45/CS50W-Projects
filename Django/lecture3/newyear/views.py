from calendar import month
from dataclasses import dataclass
from django.shortcuts import render
import datetime
# Create your views here.
def index(request):
    now = datetime.datetime.now()
    curr_month = now.month
    curr_day = now.date
    ans = "NO"
    if curr_day == 1 and curr_month == 1:
        ans = "YES"
    return render(request,"newyear/result.html",{
        "ans":ans
    })