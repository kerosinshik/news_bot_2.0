import logging
from typing import List, Dict, Any
from datetime import datetime, date
import requests
from bs4 import BeautifulSoup
from .database import add_event, get_today_events, clear_old_data

logger = logging.getLogger(__name__)

TECHMEME_EVENTS_URL = "https://www.techmeme.com/events"


def fetch_upcoming_events() -> List[Dict[str, Any]]:
    """
    Получает предстоящие события с сайта Techmeme.

    Returns:
        List[Dict[str, Any]]: Список словарей с информацией о событиях.
    """
    events = []
    try:
        response = requests.get(TECHMEME_EVENTS_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        event_elements = soup.select('.rhov')

        for event in event_elements:
            try:
                div_elements = event.find_all('div')
                if len(div_elements) >= 3:
                    date_str = div_elements[0].text.strip()
                    name = div_elements[1].text.strip()
                    location = div_elements[2].text.strip()

                    # Парсинг даты
                    date_parts = date_str.replace(',', '').split()
                    if len(date_parts) >= 2:
                        month = date_parts[0]
                        day = date_parts[1].split('-')[0]  # Берем только начальную дату
                        year = date_parts[2] if len(date_parts) > 2 else str(datetime.now().year)
                        event_date = datetime.strptime(f"{month} {day} {year}", '%b %d %Y').date()

                        # Создаем ключевые слова из названия и места проведения
                        keywords = set(word.lower() for word in (name + " " + location).split() if len(word) > 3)

                        events.append({
                            'name': name,
                            'date': event_date,
                            'keywords': list(keywords)
                        })
            except Exception as e:
                logger.error(f"Ошибка при обработке события: {e}")

        logger.info(f"Получено {len(events)} предстоящих событий")
    except Exception as e:
        logger.error(f"Ошибка при получении событий с {TECHMEME_EVENTS_URL}: {e}")

    return events


def update_events():
    """Обновляет базу данных событий."""
    logger.info("Начало обновления базы данных событий")

    # Очистка старых событий
    clear_old_data(days=1)  # Удаляем события, которые уже прошли

    # Получение новых событий
    new_events = fetch_upcoming_events()

    # Добавление новых событий в базу данных
    for event in new_events:
        add_event(event['name'], event['date'], event['keywords'])

    logger.info("Обновление базы данных событий завершено")


def get_relevant_events(article_content: str) -> List[Dict[str, Any]]:
    """
    Находит релевантные события для данной статьи.

    Args:
        article_content (str): Содержание статьи (заголовок + краткое содержание).

    Returns:
        List[Dict[str, Any]]: Список релевантных событий.
    """
    today_events = get_today_events()
    relevant_events = []

    for event in today_events:
        event_keywords = event[3].split(',')
        if any(keyword.lower() in article_content.lower() for keyword in event_keywords):
            relevant_events.append({
                'id': event[0],
                'name': event[1],
                'date': event[2],
                'keywords': event_keywords
            })

    return relevant_events


def generate_events_digest() -> str:
    """
    Генерирует дайджест предстоящих событий.

    Returns:
        str: Отформатированный текст дайджеста событий.
    """
    upcoming_events = fetch_upcoming_events()

    if not upcoming_events:
        return "На ближайшее время нет запланированных событий."

    digest = "📅 Предстоящие события в мире технологий:\n\n"

    for i, event in enumerate(upcoming_events[:10], 1):  # Ограничиваем 10 событиями
        digest += f"{i}. <b>{event['name']}</b>\n"
        digest += f"   📆 {event['date'].strftime('%d.%m.%Y')}\n"
        digest += f"   🔑 {', '.join(event['keywords'][:5])}\n\n"  # Ограничиваем 5 ключевыми словами

    digest += "\nСледите за обновлениями и не пропустите важные события! 🚀"

    return digest


if __name__ == "__main__":
    # Тестовый код для проверки работы модуля
    logging.basicConfig(level=logging.INFO)

    print("Обновление событий...")
    update_events()

    print("\nТекущие события:")
    today_events = get_today_events()
    for event in today_events:
        print(f"- {event[1]} ({event[2]})")

    print("\nПроверка релевантности:")
    test_article = "Конференция по искусственному интеллекту пройдет в следующем месяце"
    relevant = get_relevant_events(test_article)
    for event in relevant:
        print(f"- {event['name']} relevantрелевантно для статьи")

    print("\nГенерация дайджеста событий:")
    digest = generate_events_digest()
    print(digest)

    logger.info("Тестирование events.py завершено")