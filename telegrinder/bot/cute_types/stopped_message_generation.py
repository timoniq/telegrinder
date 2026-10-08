from telegrinder.bot.cute_types.base import BaseCute
from telegrinder.types.objects import MessageGenerationStopped


class MessageGenerationStoppedCute(BaseCute[MessageGenerationStopped], MessageGenerationStopped, kw_only=True):
    pass


__all__ = ("MessageGenerationStoppedCute",)
