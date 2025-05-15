# telegram_bot.py

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters

from agent_kernel import (
    ridebuddy_agent, housescout_agent,
    errands_agent, cleaning_agent, custom_handler
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
SERVICES = {
    "driver": ("🚘 RideBuddy", ridebuddy_agent.run_agent),
    "housing": ("🏡 HouseScout", housescout_agent.run_agent),
    "errands": ("🚚 Errands & Deliveries", errands_agent.run_agent),
    "cleaning": ("🧹 House Cleaning", cleaning_agent.run_agent),
    "custom": ("🎉 Custom Request", custom_handler.handle_custom),
}

user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=key)] for key, (name, _) in SERVICES.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Please select a service:", reply_markup=reply_markup)

async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data
    user_id = query.from_user.id
    user_sessions[user_id] = {
        "service": SERVICES[key][1],
        "state": {}
    }
    await query.edit_message_text(f"{SERVICES[key][0]} selected! How can we help you?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        await update.message.reply_text("Please start with /start and choose a service.")
        return

    session = user_sessions[user_id]
    result = session["service"](update.message.text, session["state"])
    if isinstance(result, dict):
        user_sessions[user_id]["state"] = result.get("booking", {})
        await update.message.reply_text(result.get("question") or result.get("message"))
    else:
        await update.message.reply_text(result)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_selection))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
