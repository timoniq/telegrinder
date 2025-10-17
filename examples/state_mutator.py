import dataclasses
from telegrinder.tools.state_mutator import mutation, State, StateMutator
import datetime


# State declaration


@dataclasses.dataclass
class AliveState(State):
    __description__ = "living"

    since: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)

    @mutation
    def die(self, reason: str) -> "DeadState":
        return DeadState(reason)


@dataclasses.dataclass
class DeadState(State):

    reason: str

    @mutation
    def resurrect(self) -> "AliveState":
        return AliveState()
    
    @property
    def __description__(self) -> str:
        return f"not living because you died of {self.reason}"


# primary mutations:

be_born = mutation(AliveState)

# or as function

@mutation
def login_as_ghost(silently: bool = False):
    if not silently:
        print("Ghost just logged in ~*_*~")
    return DeadState(reason="~*being a ghost*~")

# State use


from telegrinder import Bot, API, Token, setup_logger
from telegrinder.rules import Text


bot = Bot(API(Token.from_env()))
setup_logger(level="DEBUG")

@bot.on.message(Text("/die"))
async def die_handler(alive: AliveState):
    new = await alive.die("sadness")
    return f"You died because of {new.reason}"

@bot.on.message(Text("/resurrect"))
async def resurrect_handler(dead: DeadState):
    await dead.resurrect()
    return "You resurrected"

@bot.on.message(Text("/trick"))
async def trick_handler(mutator: StateMutator):
    # To inject mutation from any state: await AliveState().bind(mutator).die("oops")
    await (await be_born(mutator)).die("oops")
    return "Trick was unsuccessful"

@bot.on.message(Text("/song"))
async def sing_a_song_handler(state: AliveState):
    return f"You sing a song: la-lala so great to be living for {(datetime.datetime.now() - state.since).seconds} seconds"


@bot.on.message(Text("Gh0$T_рa$$w0rd"))
async def ghost_handler(m: StateMutator):
    await login_as_ghost(m, silently=True)
    return "~~~🎑♓️🐪❄️"


@bot.on.message()
async def in_state_handler(state: AliveState | DeadState):
    return f"You are {state.__description__}"

@bot.on.message(Text("/be_born"))
async def be_born_handler(mutator: StateMutator):
    await be_born(mutator)
    return "You were born"


@bot.on.message()
async def not_born_handler():
    return "You are not born"


bot.run_forever()
