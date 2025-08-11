from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from payments.gateways.mpesa.stk_push import MpesaSTKPush
from django.http import JsonResponse
from django.conf import settings


def checkout(request):
    # Logic for handling the checkout process
    return render(request, 'payments/checkout.html')


def success(request):
    # Logic for handling successful payment
    return render(request, 'payments/success.html')


def normalize_phone(phone):
    phone = phone.strip()
    if phone.startswith("07"):
        return "254" + phone[1:]
    elif phone.startswith("+254"):
        return phone[1:]
    elif phone.startswith("254"):
        return phone
    else:
        raise ValueError("Invalid phone format")


@csrf_exempt
def mpesa_checkout(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")

        try:
            normalized_phone = normalize_phone(phone)
        except ValueError:
            return JsonResponse({"error": "Invalid phone format"}, status=400)

        mpesa = MpesaSTKPush(
            shortcode=settings.MPESA_SHORTCODE,
            passkey=settings.MPESA_PASSKEY,
            consumer_key=settings.MPESA_CONSUMER_KEY,
            consumer_secret=settings.MPESA_CONSUMER_SECRET,
            callback_url="https://yourdomain.com/api/mpesa/callback/"
        )

        result = mpesa.initiate_payment(normalized_phone, amount)
        return JsonResponse(result)

    return render(request, "mpesa_button.html")
