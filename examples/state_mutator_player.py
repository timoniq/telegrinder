import datetime
import enum
import typing
from dataclasses import dataclass

from telegrinder import API, Bot, Token, logger, setup_logger
from telegrinder.rules import Argument, Command
from telegrinder.tools.state_mutator import State, StateMutator, mutation

setup_logger(level="DEBUG")
bot = Bot(API(Token.from_env()))


type Plugged = Stopped


@mutation
async def plug_in() -> Plugged:
    logger.debug("You successfully plugged in your CD player")
    return Stopped()


class StateType(enum.Enum):
    STOPPED = enum.auto()
    PLAYING = enum.auto()
    PAUSED = enum.auto()


@dataclass
class Stopped(State):
    __type__: typing.ClassVar[typing.Literal[StateType.STOPPED]] = StateType.STOPPED

    @mutation
    def play(self, song: str, offset: datetime.timedelta = datetime.timedelta(0)) -> "Playing":
        return Playing(song, offset, datetime.datetime.now())


@dataclass
class Playing(State):
    __type__: typing.ClassVar[typing.Literal[StateType.PLAYING]] = StateType.PLAYING

    song: str
    offset: datetime.timedelta
    started_at: datetime.datetime

    @mutation
    def stop(self) -> "Stopped":
        return Stopped()

    @mutation
    def pause(self) -> "Paused":
        offset = datetime.datetime.now() - self.started_at
        return Paused(
            self.song,
            offset=(offset - self.offset) if self.offset <= datetime.timedelta(0) else offset + self.offset,
            stopped_at=datetime.datetime.now(),
        )


@dataclass
class Paused(State):
    __type__: typing.ClassVar[typing.Literal[StateType.PAUSED]] = StateType.PAUSED

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


@bot.on.message(Command("plug_in"))
async def plug_in_handler(mutator: StateMutator) -> str:
    await plug_in(mutator)
    return "Yes great, choose song with /play <song_name>"


@bot.on.message(Command("play", Argument("song_name", optional=True)))
async def play_song_handler(
    state: Stopped | Paused | Playing,
    song_name: str | None = None,
) -> str:
    match state:
        case Stopped():
            if song_name is None:
                return "You should choose song name"

            await state.play(song_name)
            return f"Started playing {song_name}"
        case Paused() | Playing():
            if song_name is not None:
                previous_song = state.song
                state = await state.stop()
                await state.play(song_name)
                return f"Stopped paused {previous_song}, started playing {song_name}"

            if state.__type__ is StateType.PLAYING:
                return "💽🎵🎼🎶"

            await state.play()
            return f"Continued playing {state.song}"


@bot.on.message(Command("stop"))
async def stop_handler(state: Playing | Paused) -> str:
    match state:
        case Playing():
            await state.stop()
            return f"Stopped playing {state.song} at {datetime.datetime.now() - state.started_at + state.offset}"
        case Paused():
            await state.stop()
            return f"Stopped playing {state.song} at {state.offset}"


@bot.on.message(Command("pause"))
async def pause_handler(state: Playing) -> str:
    new_state = await state.pause()
    return f"Paused {state.song} at {new_state.offset}"


bot.run_forever()
