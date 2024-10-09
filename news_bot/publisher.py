import logging
from typing import Dict, Any, Optional
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from .database import add_published_article, log_post_stats
from .utils import escape_html
from config import TELEGRAM_CHANNEL_ID, category_emoji

logger = logging.getLogger(__name__)


def publish_to_telegram(bot: telebot.TeleBot, article: Dict[str, Any], channel_id: str = TELEGRAM_CHANNEL_ID) -> \
Optional[int]:
    """
    Публикует статью в Telegram канал.

    Args:
        bot (telebot.TeleBot): Инстанс бота Telegram.
        article (Dict[str, Any]): Словарь с данными статьи.
        channel_id (str): ID канала Telegram для публикации.

    Returns:
        Optional[int]: ID сообщения в Telegram, если публикация успешна, иначе None.
    """
    try:
        message = format_message(article)

        result = bot.send_message(
            channel_id,
            message,
            parse_mode='HTML',
            disable_web_page_preview=False,
        )

        logger.info(f"Статья успешно опубликована: {article['title']}")

        # Логируем статистику поста
        log_post_stats(result.message_id, datetime.now())

        # Добавляем статью в базу данных опубликованных
        add_published_article(article['id'], article['title'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        return result.message_id
    except Exception as e:
        logger.error(f"Ошибка при публикации статьи {article['title']}: {e}")
        return None


def format_message(article: Dict[str, Any]) -> str:
    """
    Форматирует сообщение для публикации в Telegram.

    Args:
        article (Dict[str, Any]): Словарь с данными статьи.

    Returns:
        str: Отформатированное сообщение.
    """
    emoji_for_category: str = category_emoji.get(article['category'], "🧪")
    category_tag = f"#{article['category'].upper()}"

    message = f"{emoji_for_category} {category_tag}\n\n"
    message += f"<b>{escape_html(article['title'])}</b>\n\n"
    message += f"{escape_html(article['summary'])}\n\n"
    message += f"<a href='{article['link']}'>Читать полностью</a>"

    return message


def create_article_keyboard(article: Dict[str, Any]) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопками для статьи.

    Args:
        article (Dict[str, Any]): Словарь с данными статьи.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Читать полностью", url=article['link']))
    keyboard.row(
        InlineKeyboardButton("👍", callback_data=f"like_{article['id']}"),
        InlineKeyboardButton("👎", callback_data=f"dislike_{article['id']}")
    )
    return keyboard


def publish_digest(bot: telebot.TeleBot, digest_text: str, channel_id: str = TELEGRAM_CHANNEL_ID) -> Optional[int]:
    """
    Публикует дайджест в Telegram канал.

    Args:
        bot (telebot.TeleBot): Инстанс бота Telegram.
        digest_text (str): Текст дайджеста.
        channel_id (str): ID канала Telegram для публикации.

    Returns:
        Optional[int]: ID сообщения в Telegram, если публикация успешна, иначе None.
    """
    try:
        result = bot.send_message(
            channel_id,
            digest_text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
        logger.info("Дайджест успешно опубликован")
        return result.message_id
    except Exception as e:
        logger.error(f"Ошибка при публикации дайджеста: {e}")
        return None


def update_post_stats(bot: telebot.TeleBot, message_id: int, channel_id: str = TELEGRAM_CHANNEL_ID):
    """
    Обновляет статистику поста.

    Args:
        bot (telebot.TeleBot): Инстанс бота Telegram.
        message_id (int): ID сообщения в Telegram.
        channel_id (str): ID канала Telegram.
    """
    try:
        message = bot.get_message(chat_id=channel_id, message_id=message_id)
        views = message.views if hasattr(message, 'views') else 0
        forwards = message.forward_count if hasattr(message, 'forward_count') else 0

        # Обновляем статистику в базе данных
        log_post_stats(message_id, views=views, forwards=forwards)
        logger.info(f"Статистика обновлена для поста {message_id}: просмотры - {views}, пересылки - {forwards}")
    except Exception as e:
        logger.error(f"Ошибка при обновлении статистики поста {message_id}: {e}")


if __name__ == "__main__":
    # Тестовый код для проверки работы модуля
    logging.basicConfig(level=logging.INFO)

    from telebot import TeleBot
    from config import TELEGRAM_BOT_TOKEN

    bot = TeleBot(TELEGRAM_BOT_TOKEN)

    test_article = {
        'id': '1',
        'title': 'Тестовая новость',
        'summary': 'Это тестовая новость для проверки работы publisher.py',
        'link': 'http://example.com',
        'category': 'технологии',
        'is_breaking': False
    }

    result = publish_to_telegram(bot, test_article)
    if result:
        print(f"Тестовая статья опубликована, ID сообщения: {result}")
    else:
        print("Не удалось опубликовать тестовую статью")