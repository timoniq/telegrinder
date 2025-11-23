from telegrinder import API, Dispatch, Telegrinder, Token, WaiterMachine
from telegrinder.modules import setup_logger

setup_logger()

dp = Dispatch()
bot = Telegrinder(API(Token.from_env()), dispatch=dp)
wm = WaiterMachine()
