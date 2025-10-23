from __future__ import annotations

import typing

from telegrinder.tools.aio import maybe_awaitable

if typing.TYPE_CHECKING:
    from telegrinder.node.state_mutator import State, StateMutator

    class BoundMethod[**P, T, R](typing.Protocol):
        @staticmethod
        def __call__(
            self: T, *args: P.args, **kwargs: P.kwargs
        ) -> typing.Coroutine[typing.Any, typing.Any, R] | R: ...

    @typing.runtime_checkable
    class NotBoundFunction[**P, R](typing.Protocol):
        def __call__(
            self, *args: P.args, **kwargs: P.kwargs
        ) -> typing.Coroutine[typing.Any, typing.Any, R] | R: ...


class mutation[**P, IntoState: State, BoundState: State | None]:  # noqa: N801
    from_state: State | None

    @typing.overload
    def __init__(
        self: mutation[P, IntoState, BoundState],  # type: ignore
        construct_mutation: BoundMethod[P, BoundState, IntoState],
    ) -> None: ...

    @typing.overload
    def __init__(
        self: mutation[P, IntoState, None],  # type: ignore
        construct_mutation: NotBoundFunction[P, IntoState],
    ) -> None: ...

    def __init__(
        self,
        construct_mutation: typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, IntoState] | IntoState],
    ) -> None:
        self.construct_mutation = construct_mutation
        self.from_state = None

    @typing.overload
    async def __call__(
        self: mutation[P, IntoState, None],
        mutator: StateMutator,
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> IntoState: ...

    @typing.overload
    async def __call__(
        self: mutation[P, IntoState, State],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> IntoState: ...

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> IntoState:
        mutator: StateMutator

        if self.from_state is not None:
            if self.from_state.__mutator__ is None:
                raise RuntimeError("State is not bound. Bind state with .bind(mutator) before mutating")

            await self.from_state.exit()

            new_state = await maybe_awaitable(self.construct_mutation(self.from_state, *args, **kwargs))
            mutator = self.from_state.__mutator__
        else:
            mutator, args = args[0], args[1:]

            if (state := await mutator.get()) is not None:
                await state.exit()

            new_state = await maybe_awaitable(self.construct_mutation(*args, **kwargs))

        new_state.bind(mutator)
        await new_state.enter()

        return new_state

    def __get__(self, instance: State, owner: typing.Any) -> typing.Self:
        if instance is not None:
            self.from_state = instance
        return self


__all__ = ("mutation",)
