from telegrinder import API, Dispatch, Telegrinder, Token
from telegrinder.modules import configure_dotenv, setup_logger

configure_dotenv()
setup_logger()

dp = Dispatch()
bot = Telegrinder(API(Token.from_env()), dispatch=dp)
