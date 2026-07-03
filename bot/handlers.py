from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from config import ADMIN_ID
from database import add_request
from faq import FAQ_ANSWERS, FAQ_BUTTONS

NAME, PROJECT_TYPE, DESCRIPTION, CONTACT = range(4)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Оставить заявку", callback_data="new_request")],
        [InlineKeyboardButton("❓ Частые вопросы", callback_data="faq")],
        [InlineKeyboardButton("📞 Связаться с нами", callback_data="contacts")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Добро пожаловать!\n\n"
        "Мы создаём сайты и Telegram-боты под ключ.\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "new_request":
        await query.edit_message_text("Как вас зовут?")
        return NAME

    elif query.data == "faq":
        keyboard = []
        for text, key in FAQ_BUTTONS:
            keyboard.append([InlineKeyboardButton(text, callback_data=f"faq_{key}")])
        keyboard.append([InlineKeyboardButton("◀️ Назад", callback_data="back_to_menu")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Выберите вопрос:", reply_markup=reply_markup)

    elif query.data.startswith("faq_"):
        key = query.data[4:]
        answer = FAQ_ANSWERS.get(key, "Информация уточняется.")
        keyboard = [[InlineKeyboardButton("◀️ Назад к вопросам", callback_data="faq")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(answer, reply_markup=reply_markup)

    elif query.data == "contacts":
        text = (
            "Связаться с нами:\n\n"
            "Email: newgram@inbox.ru\n"
            "Telegram: @Horusum"
        )
        keyboard = [[InlineKeyboardButton("◀️ Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    elif query.data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("📝 Оставить заявку", callback_data="new_request")],
            [InlineKeyboardButton("❓ Частые вопросы", callback_data="faq")],
            [InlineKeyboardButton("📞 Связаться с нами", callback_data="contacts")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Мы создаём сайты и Telegram-боты под ключ.\nВыберите действие:",
            reply_markup=reply_markup
        )

    return ConversationHandler.END


async def name_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Какой проект вам нужен? (сайт / бот / другое)")
    return PROJECT_TYPE


async def project_type_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["project_type"] = update.message.text
    await update.message.reply_text("Опишите вашу задачу подробнее:")
    return DESCRIPTION


async def description_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["description"] = update.message.text
    await update.message.reply_text("Укажите контакт для связи (телефон, Telegram, email):")
    return CONTACT


async def contact_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    context.user_data["contact"] = update.message.text

    request_id = await add_request(
        user_id=user.id,
        username=user.username,
        name=context.user_data["name"],
        project_type=context.user_data["project_type"],
        description=context.user_data["description"],
        contact=context.user_data["contact"],
    )

    await update.message.reply_text(
        "Спасибо! Ваша заявка принята.\n"
        "Мы свяжемся с вами в ближайшее время для оценки стоимости и сроков."
    )

    admin_text = (
        f"🔔 Новая заявка #{request_id}\n\n"
        f"Имя: {context.user_data['name']}\n"
        f"Проект: {context.user_data['project_type']}\n"
        f"Описание: {context.user_data['description']}\n"
        f"Контакт: {context.user_data['contact']}\n"
        f"Username: @{user.username or 'нет'}"
    )

    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)
    except Exception:
        pass

    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Заявка отменена.")
    context.user_data.clear()
    return ConversationHandler.END
