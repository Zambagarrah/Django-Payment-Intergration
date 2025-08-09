from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from payments.gateways.mpesa.stk_push import MpesaSTKPush
from django.http import JsonResponse
import os

def checkout(request):
    # Logic for handling the checkout process
    return render(request, 'payments/checkout.html')

def success(request):
    # Logic for handling successful payment
    return render(request, 'payments/success.html')

@csrf_exempt
def mpesa_checkout(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")

        mpesa = MpesaSTKPush(
            shortcode=os.getenv("MPESA_SHORTCODE"),
            passkey=os.getenv("MPESA_PASSKEY"),
            consumer_key=os.getenv("MPESA_CONSUMER_KEY"),
            consumer_secret=os.getenv("MPESA_CONSUMER_SECRET"),
            callback_url="https://yourdomain.com/api/mpesa/callback/"
        )

        result = mpesa.initiate_payment(phone, amount)
        return JsonResponse(result)

    return render(request, "mpesa_button.html")
