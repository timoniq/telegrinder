from telegrinder import API, Dispatch, Telegrinder, Token, WaiterMachine

dp = Dispatch()
bot = Telegrinder(API(Token.from_env()), dispatch=dp)
wm = WaiterMachine(dp)
