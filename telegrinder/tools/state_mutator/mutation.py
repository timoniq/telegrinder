import typing

from telegrinder.tools.aio import maybe_awaitable

if typing.TYPE_CHECKING:
    from telegrinder.node import State, StateMutator

    type AnyStorage = typing.Any

    class BoundMutation[**P, T, R](typing.Protocol):
        @staticmethod
        def __call__(self: T, *args: P.args, **kwargs: P.kwargs) -> typing.Coroutine[typing.Any, typing.Any, R] | R: ...

    class UnboundMutation[**P, R](typing.Protocol):
        def __call__(self, *args: P.args, **kwargs: P.kwargs) -> typing.Coroutine[typing.Any, typing.Any, R] | R: ...


class Mutation[
    ConstructMutation: typing.Callable[
        ...,
        typing.Coroutine[typing.Any, typing.Any, State[typing.Any]] | State[typing.Any],
    ],
    Into: State[typing.Any],
    From: State[typing.Any] | None,
]:
    construct_mutation: ConstructMutation
    from_state: From | None

    @typing.overload
    def __new__[**P, IntoState: State[typing.Any], FromState: State[typing.Any] | None](
        self, construct_mutation: BoundMutation[P, FromState, IntoState], /
    ) -> Mutation[BoundMutation[P, FromState, IntoState], IntoState, FromState]: ...

    @typing.overload
    def __new__[**P, IntoState: State[typing.Any]](
        self, construct_mutation: UnboundMutation[P, IntoState], /
    ) -> Mutation[UnboundMutation[P, IntoState], IntoState, None]: ...

    def __new__(cls, construct_mutation: typing.Any) -> Mutation[typing.Any, typing.Any, typing.Any]:
        instance = super().__new__(cls)
        instance.construct_mutation = construct_mutation
        instance.from_state = None
        return instance

    @typing.overload
    async def __call__[**P](
        self: Mutation[UnboundMutation[P, Into], Into, None],
        mutator: StateMutator[AnyStorage],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Into: ...

    @typing.overload
    async def __call__[**P](
        self: Mutation[BoundMutation[P, From, Into], Into, From],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> Into: ...

    async def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        mutator: StateMutator[AnyStorage]
        _args: list[typing.Any]
        from_state: State | None

        if self.from_state is not None:
            if self.from_state.__mutator__ is None:
                raise RuntimeError("State is not bound. Bind state with .bind(mutator) before mutating.")

            from_state, mutator, _args = self.from_state, self.from_state.__mutator__, [self.from_state, *args]
        elif args:
            mutator, *_args = args
            from_state = await mutator.get()
        else:
            raise RuntimeError("Mutator was not provided for mutating the state.")

        if from_state is not None:
            await from_state.exit()

        return await mutator.bind_state(await maybe_awaitable(self.construct_mutation(*_args, **kwargs))).enter()

    def __get__(self, instance: From, owner: typing.Any) -> typing.Self:
        if instance is None:
            return self

        bound = type(self)(self.construct_mutation)
        bound.from_state = instance
        return bound


mutation = Mutation


__all__ = ("mutation",)
