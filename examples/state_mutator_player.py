from dataclasses import dataclass
import datetime

from telegrinder.tools.state_mutator import State, StateMutator, mutation
from telegrinder.rules import Command, Argument, Markup



@dataclass
class Stopped(State):
    @mutation
    def play(self, song: str, offset: datetime.timedelta = datetime.timedelta(0)) -> "Playing":
        return Playing(song, offset, datetime.datetime.now())


@dataclass
class Playing(State):
    song: str
    offset: datetime.timedelta
    started_at: datetime.datetime
    
    @mutation
    def stop(self) -> "Stopped":
        return Stopped()
    
    @mutation
    def pause(self) -> "Paused":
        return Paused(
            self.song,
            offset=datetime.datetime.now() - self.started_at - self.offset,
            stopped_at=datetime.datetime.now(),
        )


@dataclass
class Paused(State):
    song: str
    offset: datetime.timedelta
    stopped_at: datetime.datetime

    @mutation
    def stop(self) -> "Stopped":
        return Stopped()
    
    @mutation
    def play(self) -> "Playing":
        return Playing(
            self.song,
            offset=self.offset,
            started_at=datetime.datetime.now(),
        )


@mutation
def plug_in():
    print("You successfully plugged in your CD player")
    return Stopped()


from telegrinder import API, Bot, Token, setup_logger
from telegrinder.rules import Text

bot = Bot(API(Token.from_env()))
setup_logger(level="DEBUG")


@bot.on.message(Command("plug_in"))
async def plug_in_handler(mutator: StateMutator):
    await plug_in(mutator)
    return "Yes great, choose song with /play <song_name>"


@bot.on.message(Markup("/play <song_name>") | Markup("/play"))
async def play_song_handler(state: Stopped | Paused | Playing, song_name: str | None = None):
    match state:
        case Stopped():
            if song_name is None:
                return "You should choose song name"
            await state.play(song_name)
            return f"Started playing {song_name}"
        case Paused():
            if song_name is None:
                await state.play()
                return f"Continued playing {state.song}"
            else:
                previous_song = state.song
                state = await state.stop()
                await state.play(song_name)
                return f"Stopped paused {previous_song}, started playing {song_name}"
        case Playing():
            if song_name is None:
                return "💽🎵🎼🎶"
            else:
                previous_song = state.song
                state = await state.stop()
                await state.play(song_name)
                return f"Stopped playing {previous_song}, started playing {song_name}"


@bot.on.message(Command("stop"))
async def stop_handler(state: Playing | Paused):
    match state:
        case Playing():
            await state.stop()
            return f"Stopped playing {state.song} at {datetime.datetime.now() - state.started_at + state.offset}"
        case Paused():
            await state.stop()
            return f"Stopped playing {state.song} at {state.offset}"


@bot.on.message(Command("pause"))
async def pause_handler(state: Playing):
    new_state = await state.pause()
    return f"Paused {state.song} at {new_state.offset}"


bot.run_forever()
