from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from database import get_stats, get_recent_requests, get_request


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    stats = await get_stats()
    text = (
        f"📊 Статистика заявок\n\n"
        f"Всего: {stats['total']}\n"
        f"За сегодня: {stats['today']}\n"
        f"За неделю: {stats['week']}\n"
        f"За месяц: {stats['month']}"
    )
    await update.message.reply_text(text)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    limit = 10
    if context.args:
        try:
            limit = int(context.args[0])
        except ValueError:
            limit = 10

    requests = await get_recent_requests(limit)

    if not requests:
        await update.message.reply_text("Заявок пока нет.")
        return

    text = f"📋 Последние {len(requests)} заявок:\n\n"
    for req in requests:
        text += f"#{req['id']} | {req['name']} | {req['project_type']} | {req['created_at']}\n"

    await update.message.reply_text(text)


async def read_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("Использование: /read <id>")
        return

    try:
        request_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID должен быть числом.")
        return

    req = await get_request(request_id)
    if not req:
        await update.message.reply_text(f"Заявка #{request_id} не найдена.")
        return

    text = (
        f"📝 Заявка #{req['id']}\n\n"
        f"Имя: {req['name']}\n"
        f"Тип проекта: {req['project_type']}\n"
        f"Описание: {req['description']}\n"
        f"Контакт: {req['contact']}\n"
        f"Username: @{req['username'] or 'нет'}\n"
        f"Дата: {req['created_at']}"
    )
    await update.message.reply_text(text)
