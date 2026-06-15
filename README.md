# 🤖 Stripe Test Bot

Минимальный Telegram-бот для тестирования Stripe Checkout.

## 📦 Установка

```bash
pip install -r requirements.txt
```

## ⚙️ Настройка

Открой `config.py` и заполни все переменные:

### 1. BOT_TOKEN
- Зайди к [@BotFather](https://t.me/BotFather) → `/newbot`
- Скопируй токен

### 2. STRIPE_SECRET_KEY
- Stripe Dashboard → Developers → API keys
- Скопируй **Secret key** (начинается с `sk_test_...`)

### 3. BASE_URL + STRIPE_WEBHOOK_SECRET
Для теста используй **ngrok**:

```bash
# Установи ngrok: https://ngrok.com
ngrok http 8000
```

Скопируй HTTPS-URL (например `https://abc123.ngrok.io`) → вставь в `BASE_URL`.

Затем:
- Stripe Dashboard → Developers → Webhooks → **Add endpoint**
- URL: `https://abc123.ngrok.io/webhook`
- Events: выбери `checkout.session.completed`
- Скопируй **Signing secret** (whsec_...) → вставь в `STRIPE_WEBHOOK_SECRET`

## 🚀 Запуск

```bash
python bot.py
```

## 💳 Тестовая карта Stripe

При оплате используй:
- **Номер:** `4242 4242 4242 4242`
- **Дата:** любая в будущем (например `12/34`)
- **CVC:** любые 3 цифры
- **Имя/адрес:** любые

## 🔄 Поток работы

```
Пользователь /start
    → нажимает "Купить"
    → бот создаёт Stripe Checkout Session
    → пользователь переходит на страницу оплаты Stripe
    → вводит тестовую карту
    → Stripe отправляет webhook на /webhook
    → бот присылает подтверждение в Telegram
```
