import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# RSS фиды
RSS_FEEDS = [
    'https://techcrunch.com/feed/',
    'https://www.wired.com/feed/rss',
    'https://www.theverge.com/rss/index.xml',
    'https://venturebeat.com/feed/',
    'https://artificialintelligence-news.com/feed/',
    'https://feeds.feedburner.com/TheHackersNews',
    'https://www.nature.com/nature.rss',
    'https://www.sciencedaily.com/rss/computers_math.xml',
    'http://www.ixbt.com/export/news.rss',
    'https://mashable.com/feeds/rss/all',
    'https://gizmodo.com/feed'
]

# Настройки публикации
ARTICLES_PER_FEED = 10
PUBLISH_INTERVAL = 1  # Интервал проверки в минутах
DELAY_BETWEEN_POSTS = 60  # секунд
MIN_PUBLICATION_INTERVAL = 3  # минимальный интервал между публикациями в минутах
MAX_PUBLICATIONS_PER_HOUR = 20  # Максимальное количество публикаций в час

MIN_INTEREST_SCORE = 1.5  # Минимальный балл интереса для публикации
PUBLICATION_DELAY_INCREASE = 30  # Увеличение задержки в минутах при отсутствии интересных новостей

# Настройки перевода
TARGET_LANGUAGE = 'ru'
SUMMARY_LENGTH = 200  # символов

# Настройки для срочных новостей
BREAKING_NEWS_KEYWORDS = [
    "breaking", "срочно", "just announced", "world first", "revolutionary",
    "game-changing", "major acquisition", "critical vulnerability"
]
PRIORITY_SOURCES = [
    "techcrunch.com", "wired.com", "theverge.com", "artificialintelligence-news.com"
]
MAX_BREAKING_NEWS_PER_HOUR = 3

# Словарь категорий и эмодзи
category_emoji = {
    "технологии": "💻",
    "инновации": "💡",
    "научный_прорыв": "🔭",
    "ии_и_нейросети": "🧠",
    "блокчейн": "⛓️",
    "кибербезопасность": "🛡️",
    "робототехника": "🦿",
    "vr_ar": "🥽",
    "интернет_вещей": "🌐",
    "5g": "📡",
    "биотехнологии": "🧬",
    "нанотехнологии": "🔬",
    "зеленые_технологии": "🌱",
    "космос": "🛸",
    "стартапы": "🆙",
    "инвестиции": "💹",
    "патенты": "📜",
    "научные_публикации": "🧪",
    "энергетика": "🗼",
    "медицина": "🩺",
    "транспорт": "🚄",
    "образование": "🎓",
    "финтех": "💲",
    "криптовалюты": "🪙",
    "геймификация": "🎮",
    "мобильные_устройства": "📱"
}

# Приоритетные категории
PRIORITY_CATEGORIES = [
    "инновации",
    "научные_публикации",
    "ии_и_нейросети",
    "кибербезопасность",
    "робототехника",
    "мобильные_устройства"
]

# Обновленные веса категорий
category_weights = {
    "технологии": 2.0,
    "инновации": 2.2,
    "научный_прорыв": 2.1,
    "ии_и_нейросети": 2.5,
    "блокчейн": 1.5,
    "кибербезопасность": 2.0,
    "робототехника": 2.2,
    "vr_ar": 1.8,
    "интернет_вещей": 1.7,
    "5g": 1.8,
    "биотехнологии": 1.9,
    "нанотехнологии": 1.8,
    "зеленые_технологии": 1.7,
    "космос": 2.1,
    "стартапы": 1.5,
    "инвестиции": 1.3,
    "патенты": 1.4,
    "научные_публикации": 1.9,
    "энергетика": 1.6,
    "медицина": 1.7,
    "транспорт": 1.5,
    "образование": 1.4,
    "финтех": 1.5,
    "криптовалюты": 1.4,
    "геймификация": 1.3,
    "мобильные_устройства": 1.7
}

# Параметры для выбора статей
TOP_ARTICLES_PERCENTAGE = 0.7
DIVERSITY_PERCENTAGE = 0.3


# Словарь категорий и ключевых слов
category_keywords = {
    "технологии": ["технология", "технологический", "tech", "technology", "hardware", "software", "гаджет", "девайс", "цифровой", "электроника"],
    "инновации": ["инновация", "инновационный", "innovation", "новшество", "прорыв", "революционный", "передовой", "новаторский", "pioneering"],
    "научный_прорыв": ["breakthrough", "discovery", "прорыв", "научный", "эксперимент", "гипотеза", "теория", "феномен", "закономерность", "scientific"],
    "ии_и_нейросети": ["искусственный интеллект", "artificial intelligence", "AI assistant", "AI safety", "AI system", "AI algorithm", "AI-powered", "AI-driven", "нейросеть", "machine learning", "deep learning", "neural network", "нейронная сеть", "машинное обучение", "глубокое обучение", "чат-бот AI", "AI image recognition", "AI распознавание образов", "AI модель", "AI model",],
    "блокчейн": ["blockchain", "блокчейн", "distributed ledger", "smart contract", "криптография", "децентрализация", "токен", "майнинг", "хеширование", "консенсус", "распределенный реестр", "умный контракт"],
    "кибербезопасность": ["cybersecurity", "кибербезопасность", "hacking", "encryption", "firewall", "защита данных", "информационная безопасность", "антивирус", "шифрование", "брандмауэр", "уязвимость", "киберугроза"],
    "робототехника": ["robotics", "робототехника", "robot", "робот", "механизация"],
    "vr_ar": ["virtual reality", "виртуальная реальность", "augmented reality", "дополненная реальность", "mixed reality", "смешанная реальность", "иммерсивные технологии"],
    "интернет_вещей": ["iot", "internet of things", "интернет вещей", "smart home", "умный дом", "connected devices", "подключенные устройства", "сенсоры", "датчики", "автоматизация", "m2m", "machine-to-machine"],
    "связь_и_5g": ["5g", "5джи", "network", "connectivity", "wireless", "мобильная связь", "сеть пятого поколения", "высокоскоростной интернет", "беспроводные технологии", "телекоммуникации", "спектр частот", "low latency"],
    "биотехнологии": ["biotech", "биотехнологии", "genetic", "genome", "биоинженерия", "генная инженерия", "клонирование", "стволовые клетки", "биоинформатика", "секвенирование", "генетически модифицированный", "биомедицина"],
    "нанотехнологии": ["nanotech", "нанотехнологии", "nanoscale", "наночастицы", "наноматериалы", "нанороботы", "наноэлектроника", "нанотрубки", "наноструктуры", "квантовые точки", "нанолитография", "наномедицина"],
    "зеленые_технологии": ["green tech", "зеленые технологии", "pollution", "renewable", "возобновляемые источники", "sustainability", "устойчивое развитие", "эко", "чистая энергия", "экологичный", "переработка", "энергоэффективность", "carbon footprint"],
    "космос": ["space", "космос", "спутник", "марс", "луна", "астрономия", "космонавтика", "ракета", "орбита", "галактика", "космический корабль", "телескоп"],
    "стартапы": ["startup", "стартап", "venture", "венчурный", "entrepreneur", "предприниматель", "инновационный бизнес", "масштабирование", "акселератор", "инкубатор", "единорог", "питч"],
    "инвестиции": ["investment", "инвестиции", "funding", "финансирование", "venture capital", "венчурный капитал", "angel investor", "бизнес-ангел", "crowdfunding", "краудфандинг", "ipo", "первичное размещение"],
    "патенты": ["patent", "патент", "intellectual property", "интеллектуальная собственность", "invention", "изобретение", "trademark", "торговая марка", "copyright", "авторское право", "лицензирование", "патентование"],
    "научные_публикации": ["research paper", "научная статья", "journal", "научный журнал", "scientific article", "научная публикация", "peer review", "рецензирование", "citation", "цитирование", "impact factor", "индекс цитирования"],
    "энергетика": ["energy", "энергетика", "power", "электроэнергия", "electricity", "электричество", "nuclear", "ядерная энергия", "solar", "солнечная энергия", "wind power", "ветроэнергетика"],
    "медицина": ["medicine", "медицина", "health", "здравоохранение", "symptom", "pharmaceutical", "фармацевтика", "therapy", "терапия", "diagnosis", "диагностика", "vaccine", "вакцина", "clinical trial", "клинические испытания"],
    "транспорт": ["transport", "транспорт", "бензиновый мотор", "vehicle", "транспортное средство", "autonomous", "беспилотный", "electric car", "электромобиль", "hyperloop", "гиперлуп", "smart city", "умный город", "logistics", "логистика"],
    "образование": ["education", "образование", "learning", "обучение", "school", "школа", "university", "университет", "e-learning", "дистанционное обучение", "mooc", "онлайн-курсы", "edtech", "образовательные технологии"],
    "финтех": ["fintech", "финтех", "banking", "банкинг", "payment", "платежи", "financial technology", "финансовые технологии", "digital wallet", "электронный кошелек", "mobile banking", "мобильный банкинг", "insurtech", "страховые технологии"],
    "криптовалюты": ["crypto", "крипто", "bitcoin", "биткоин", "ethereum", "эфириум", "blockchain", "блокчейн", "mining", "майнинг", "wallet", "кошелек", "exchange", "биржа", "token", "токен"],
    "геймификация": ["gamification", "геймификация", "serious games", "обучающие игры", "игрофикация", "game-based learning", "игровое обучение", "simulation", "симуляция", "virtual world", "виртуальный мир", "game mechanics", "игровые механики"],
    "мобильные_устройства": ["smartphone", "смартфон", "tablet", "планшет", "smartwatch", "умные часы", "wearable", "носимые устройства", "mobile device", "мобильное устройство", "app", "приложение", "mobile os", "мобильная ос", "iphone", "samsung galaxy", "AirPods"]
}

# Черный список ключевых слов
BLACKLIST_KEYWORDS = [
    "скидка", "распродажа", "Prime Day", "Black Friday", "Cyber Monday",
    "сэкономить", "дешевле", "акция", "уценка", "бесплатно",
    "купить", "продажа", "цена снижена", "специальное предложение",
    "скидок", "выгодная цена", "выгодное предложение", "экономия"
]

# Загрузка конфиденциальных данных из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# Проверка наличия необходимых переменных окружения
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в файле .env")
if not TELEGRAM_CHANNEL_ID:
    raise ValueError("TELEGRAM_CHANNEL_ID не найден в файле .env")
if not ADMIN_CHAT_ID:
    raise ValueError("ADMIN_CHAT_ID не найден в файле .env")