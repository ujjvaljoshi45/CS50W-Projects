from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import Flight, Passengers

# Create your views here.

def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request,flight_id):
    flight = Flight.objects.get(pk = flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passengers.objects.exclude(flights = flight).all()
    return render(request, "flights/flight.html", {
        "flight" : flight,
        "passengers" : passengers,
        "non_passengers" : non_passengers
    })

def book(request,flight_id):

    if request.POST:
        flight = Flight.objects.get(pk = flight_id)

        passenger_id = int(request.POST["passenger"])
        passenger = Passengers.objects.get(pk=passenger_id)
        passenger.flights.add(flight)

        return redirect("flight", flight_id)