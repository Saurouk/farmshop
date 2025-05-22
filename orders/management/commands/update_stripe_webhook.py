import requests
from decouple import config
from django.core.management.base import BaseCommand

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
WEBHOOK_ID = config("STRIPE_WEBHOOK_ID")

def get_ngrok_url():
    try:
        res = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = res.json().get("tunnels", [])
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except Exception as e:
        print("❌ Erreur récupération URL Ngrok :", e)
    return None

def update_stripe_webhook(new_url):
    endpoint = f"https://api.stripe.com/v1/webhook_endpoints/{WEBHOOK_ID}"
    data = {"url": f"{new_url}/api/orders/stripe-webhook/"}
    headers = {
        "Authorization": f"Bearer {STRIPE_SECRET_KEY}"
    }
    res = requests.post(endpoint, data=data, headers=headers)
    if res.status_code == 200:
        print("✅ Webhook mis à jour :", data["url"])
    else:
        print("❌ Erreur mise à jour Stripe :", res.text)

class Command(BaseCommand):
    help = "Update Stripe webhook URL with current ngrok public URL"

    def handle(self, *args, **kwargs):
        ngrok_url = get_ngrok_url()
        if ngrok_url:
            update_stripe_webhook(ngrok_url)
        else:
            print("❌ Impossible de récupérer l'URL Ngrok")
