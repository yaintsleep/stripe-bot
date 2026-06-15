import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8948138574:AAFUTfG1kSXGEbodVnbiQ4MnNm8lVCvsOvg")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "sk_test_51TeGBKLvTXQUxbv28tSHuSZY3l36YUfi1aJR3aimXNvm0UbzpfI3fbbMYH5IEeIfE2XqlOGzxxT6QOw34CydJT7b00tbR6MgMq")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_QkHl2MyqwuSYpAEsLn1Yuhva3XEKbXVi")
BASE_URL = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
if BASE_URL and not BASE_URL.startswith("http"):
    BASE_URL = "https://" + BASE_URL
PORT = int(os.environ.get("PORT", 8000))
