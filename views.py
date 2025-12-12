import requests
from django.conf import settings
from django.shortcuts import render, redirect

def donate(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        email = request.POST["email"]
        name = request.POST["name"]

        payload = {
            "tx_ref": "donation-12345",
            "amount": amount,
            "currency": "UGX",
            "redirect_url": "http://localhost:8000/payment-success",
            "payment_options": "card,mobilemoneyuganda",
            "customer": {
                "email": email,
                "name": name,
            },
            "customizations": {
                "title": "Charity Donation",
                "description": "Support our cause",
            }
        }

        headers = {
            "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.flutterwave.com/v3/payments",
            json=payload,
            headers=headers
        )

        link = response.json()["data"]["link"]
        return redirect(link)

    return render(request, "donate.html")