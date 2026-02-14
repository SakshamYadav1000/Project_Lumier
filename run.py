from main import Lumier
from menu_handler import handler_menu

assistant = Lumier("Lumier")
assistant.welcome_user()
handler_menu(assistant)