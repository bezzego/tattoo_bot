# Экспортируем тексты так, чтобы в коде работало: from app import texts
from .texts import ru as texts  # теперь texts.MENU_CALCULATE и т.п. доступны
