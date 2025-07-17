from fntypes.result import Error, Ok

from telegrinder import API, ChatJoinRequest, Telegrinder, Token
from telegrinder.modules import logger
from telegrinder.rules import HasInviteLink, IsUser

bot = Telegrinder(API(Token.from_env()))

class Paginator:
    def get_page(self, page_number: int):
        ...


from telegrinder.node import Source


class PageManager:
    def get_page_keyboard(self):
        ...
    
    def get_page_text(self):
        ...

    def send_page(self, src: Source):
        ...


class NextPage(Rule):
    def __init__(self, page_manager: PageManager):
        ...


class PrevPage(Rule):
    ...


@bot.on.message()
async def show_me_page():
    await PageManager()