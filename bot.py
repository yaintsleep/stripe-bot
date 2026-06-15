import asyncio
import logging
import os
import stripe
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web
from config import BOT_TOKEN, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stripe.api_key = STRIPE_SECRET_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Это тестовый бот для оплаты через Stripe.\n\n"
        "Нажми кнопку ниже, чтобы купить товар.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Купить за $5", callback_data="buy")]
        ])
    )

@dp.callback_query(F.data == "buy")
async def process_buy(callback: types.CallbackQuery):
    await callback.answer()
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Тестовый товар 🧪"},
                    "unit_amount": 500,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{BASE_URL}/cancel",
            metadata={"telegram_user_id": str(callback.from_user.id)},
        )
        await callback.message.answer(
            "✅ Ссылка для оплаты создана!\n\nПосле оплаты вернись сюда — бот пришлёт подтверждение.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url=session.url)]
            ])
        )
    except Exception as e:
        logger.error(f"Stripe error: {e}")
        await callback.message.answer("❌ Ошибка при создании сессии оплаты.")

async def stripe_webhook(request: web.Request) -> web.Response:
    payload = await request.read()
    sig_header = request.headers.get("Stripe-Signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        return web.Response(status=400, text="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("metadata", {}).get("telegram_user_id")
        amount = session.get("amount_total", 0) / 100
        currency = session.get("currency", "usd").upper()
        if user_id:
            try:
                await bot.send_message(
                    chat_id=int(user_id),
                    text=f"🎉 Оплата прошла успешно!\n\n💰 Сумма: {amount} {currency}\n📦 Товар: Тестовый товар 🧪\n✅ Спасибо за покупку!"
                )
            except Exception as e:
                logger.error(f"Failed to notify user {user_id}: {e}")
    return web.Response(status=200, text="OK")

async def success_page(request: web.Request) -> web.Response:
    return web.Response(content_type="text/html",
        text="<html><body><h2>✅ Оплата прошла! Вернись в Telegram.</h2></body></html>")

async def cancel_page(request: web.Request) -> web.Response:
    return web.Response(content_type="text/html",
        text="<html><body><h2>❌ Оплата отменена.</h2></body></html>")

async def main():
    app = web.Application()
    app.router.add_post("/webhook", stripe_webhook)
    app.router.add_get("/success", success_page)
    app.router.add_get("/cancel", cancel_page)

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"Webhook server started on port {port}")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
