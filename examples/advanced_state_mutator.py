"""This example demonstrates how to implement a custom state storage
using Redis and integrate it with Telegrinder's StateMutator.

The example implements a simple pizza ordering flow where the current
state of the user is stored in Redis between updates.

Requirements:
- Redis server
- `redis` Python package

Set the `REDIS_URL` environment variable to point to your Redis instance
before running the example.
"""

# pyright: reportGeneralTypeIssues=false

import os
import typing
from dataclasses import dataclass
from enum import StrEnum

import redis.asyncio as redis  # type: ignore
from kungfu import Nothing, Option, Some
from kungfu.library.monad.option import NOTHING

from telegrinder import API, Bot, CallbackQuery, Message, Token, configure_dotenv, setup_logger
from telegrinder.node import Payload, PayloadSerializer, Text, global_node, scalar_node
from telegrinder.rules import Command
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard
from telegrinder.tools.serialization.msgpack_ser import MsgPackSerializer
from telegrinder.tools.state_mutator import State, StateMutator, mutation
from telegrinder.tools.state_storage.abc import (
    ABCStateStorage,
    Key,
    StateData,
)

configure_dotenv()

logger = setup_logger()
api = API(Token.from_env())
bot = Bot(api)


# Implementation of a custom state storage using Redis
# by inheriting from ABCStateStorage
class PizzaStateStorage(ABCStateStorage[str]):
    # Key format: {storage_key}:{user_id}
    # storage_key is the "pizza" string that acts as an identifier
    # for this storage, separating its data from other data in the storage.
    KEY = "pizza:{user_id}"

    # Time-To-Live: state lifetime is 10 minutes.
    TTL = 60 * 10
    # After this time expires, Redis automatically removes the state
    # from the storage.

    def __init__(
        self,
        redis_client: redis.Redis,
        ttl: int = TTL,
    ) -> None:
        self.redis_client = redis_client
        self.ttl = ttl
        self.serializer = MsgPackSerializer(StateData[str])

    def key(self, user_id: int, /) -> str:
        return self.KEY.format(user_id=user_id)

    async def get(self, user_id: int) -> Option[StateData[str]]:
        # Get the state as a raw payload from the storage
        # using the pizza:{user_id} key.
        payload = await self.redis_client.get(name=self.key(user_id))

        # Redis was configured with decode_responses=True,
        # so we expect to receive a str here.
        # get() can also return None if there is no state
        # for the given key in the storage.
        if not isinstance(payload, str):
            return NOTHING

        # Deserialize the raw state into a Python StateData object.
        # StateData is a dataclass with two fields: key and payload.
        # key is the key of the state itself, used to identify it.
        # payload contains the raw data of the state.
        # .deserialize returns a successful result as `Ok(StateData(...))`.
        # Otherwise, it returns an error because the `ABCStateStorage`
        # interface requires `Option[StateData]`.
        # We need to convert `Result` into `Option` using `.cast(Some, Nothing)`.
        # `Ok` is converted to `Some`, while `Error` is converted to `Nothing`.
        return self.serializer.deserialize(payload).cast(Some, Nothing)

    async def delete(self, user_id: int) -> None:
        # Delete the state from the storage using the pizza:{user_id} key.
        await self.redis_client.delete(self.key(user_id))

    async def set(self, user_id: int, key: Key, payload: str) -> None:
        # Store the state using the pizza:{user_id} key.
        await self.redis_client.set(
            name=self.key(user_id),
            value=self.serializer.serialize(StateData(key, payload)),
            #                    ^ Serialize the Python StateData object into a raw
            #                      payload so it can be stored in the storage.
            ex=self.ttl,
            # ^ Set the Time-To-Live for the state.
            # Redis will automatically remove it when the TTL expires.
        )


# Alias for StateMutator.
# StateMutator[PizzaStateStorage] returns a StateMutator node
# that works exclusively with PizzaStateStorage.
# A type alias makes it more convenient to use.
type Mutator = StateMutator[PizzaStateStorage]


# Enum containing the state keys.
class PizzaOrder(StrEnum):
    CHOOSING_PIZZA = "choosing_pizza"
    CHOOSING_SIZE = "choosing_size"
    CHOOSING_DELIVERY = "choosing_delivery"
    WAITING_FOR_ADDRESS = "waiting_for_address"
    CONFIRMING = "confirming"


# Implementation of states by inheriting from the State class.
# State needs to know which StateMutator it should use
# to access and manage states.

# States must be dataclasses so they can be serialized
# into a raw payload and stored in the storage.

# StateMutator is specified for State as State[StateMutator].
# State itself is a node, so it can be used anywhere
# where nodes can be injected: handlers, rules, middlewares, etc.

# The state key is specified through the __state_key__ attribute.
# The key can be a str, int, or float.


@dataclass
class ChoosingPizza(State[Mutator]):  # Specify the StateMutator that works with PizzaStateStorage.
    # Define a state key.
    __state_key__ = PizzaOrder.CHOOSING_PIZZA

    # State mutation.
    # Mutations can be used to transition from one state to another.
    # In this case, we transition from ChoosingPizza to ChoosingSize.

    # The mutation decorator is defined on the ChoosingPizza method,
    # so it knows that the transition starts from ChoosingPizza
    # and goes to the state returned by the method: ChoosingSize.
    @mutation
    def choose_pizza(self, pizza: Pizza) -> ChoosingSize:
        return ChoosingSize(pizza)

    # This method can be called manually or by the mutator
    # when the state is set through the mutator.
    async def enter(self) -> typing.Self:
        # __user_id__ is an alias for self.__mutator__.user_id.
        # This property contains the user ID for whom this state was created.
        # It can be None when the mutator is not bound to the current state.
        if self.__user_id__ is not None:
            logger.info("User (id={}) is choosing a pizza!", self.__user_id__)

        return await super().enter()


@dataclass
class ChoosingSize(State[Mutator]):
    __state_key__ = PizzaOrder.CHOOSING_SIZE

    pizza: Pizza

    @mutation
    def choose_size(self, size: PizzaSize) -> ChoosingDelivery:
        return ChoosingDelivery(
            pizza=self.pizza,
            size=size,
        )


@dataclass
class ChoosingDelivery(State[Mutator]):
    __state_key__ = PizzaOrder.CHOOSING_DELIVERY

    pizza: Pizza
    size: PizzaSize

    @mutation
    def choose_delivery(
        self,
        delivery: DeliveryType,
    ) -> WaitingForAddress | Confirming:
        if delivery is DeliveryType.DELIVERY:
            return WaitingForAddress(
                pizza=self.pizza,
                size=self.size,
            )

        return Confirming(
            pizza=self.pizza,
            size=self.size,
            delivery=delivery,
            address=None,
        )


@dataclass
class WaitingForAddress(State[Mutator]):
    __state_key__ = PizzaOrder.WAITING_FOR_ADDRESS

    pizza: Pizza
    size: PizzaSize

    @mutation
    def set_address(self, address: str) -> Confirming:
        return Confirming(
            pizza=self.pizza,
            size=self.size,
            delivery=DeliveryType.DELIVERY,
            address=address,
        )


@dataclass
class Confirming(State[Mutator]):
    __state_key__ = PizzaOrder.CONFIRMING

    pizza: Pizza
    size: PizzaSize
    delivery: DeliveryType
    address: str | None

    # This method can be called manually or by the mutator
    # when the state is unset through the mutator.
    async def exit(self) -> None:
        if self.__user_id__ is not None:
            logger.info("Pizza order for user (id={}) has been confirmed!", self.__user_id__)

        await super().exit()


# Mutation defined as a function.
# This function can be called with a mutator passed to it.


# The state returned by this function will be automatically
# set through the provided mutator.
# The mutator will also call the state's .enter() method.
@mutation
def choose_pizza() -> ChoosingPizza:
    return ChoosingPizza()


# Enum helpers
class Pizza(StrEnum):
    PEPPERONI = "pepperoni"
    MARGHERITA = "margherita"
    FOUR_CHEESE = "four_cheese"
    HAWAIIAN = "hawaiian"


class PizzaSize(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class DeliveryType(StrEnum):
    DELIVERY = "delivery"
    PICKUP = "pickup"


# Static inline keyboards.
class ChoosePizzaKeyboard(InlineKeyboard, max_in_row=1):
    PEPPERONI = InlineButton("pepperoni", callback_data=Pizza.PEPPERONI)
    MARGHERITA = InlineButton("margherita", callback_data=Pizza.MARGHERITA)
    FOUR_CHEESE = InlineButton("four_cheese", callback_data=Pizza.FOUR_CHEESE)
    HAWAIIAN = InlineButton("hawaiian", callback_data=Pizza.HAWAIIAN)


class ChoosePizzaSizeKeyboard(InlineKeyboard, max_in_row=1):
    SMALL = InlineButton("small", callback_data=PizzaSize.SMALL)
    MEDIUM = InlineButton("medium", callback_data=PizzaSize.MEDIUM)
    LARGE = InlineButton("large", callback_data=PizzaSize.LARGE)


class ChooseDeliveryTypeKeyboard(InlineKeyboard, max_in_row=2):
    DELIVERY = InlineButton("delivery", callback_data=DeliveryType.DELIVERY)
    PICKUP = InlineButton("pickup", callback_data=DeliveryType.PICKUP)


# Global scalar node used to create a globally shared Redis instance.
# When the application shuts down, this node will be closed,
# and its context manager will safely close the Redis connection.
@global_node
@scalar_node[typing.Any]
class Redis:
    @classmethod
    async def __compose__(cls) -> typing.AsyncGenerator[redis.Redis]:
        async with (
            redis.Redis.from_url(
                url=os.environ["REDIS_URL"],  # URL of the Redis instance specified in the environment variable.
                # See: https://github.com/redis/lettuce/wiki/Redis-URI-and-connection-details
                protocol=2,  # See the Redis protocol specification: https://redis.io/docs/latest/develop/reference/protocol-spec/
                decode_responses=True,  # Decode Redis responses from bytes into strings.
            ) as client
        ):
            yield client


# The lifespan is used to initialize and configure resources
# that should be available while the bot is running.


# It can also receive nodes and internal injections as arguments,
# so dependencies can be initialized and injected directly
# into the lifespan.
@bot.lifespan
async def lifespan(
    redis_client: Redis,  # Get the redis.Redis instance through our Redis node.
) -> typing.AsyncGenerator[None]:
    # Set the global payload serializer so StateMutator uses
    # the serializer specified here to serialize the payload
    # stored in StateData.
    PayloadSerializer.set(PayloadSerializer(MsgPackSerializer))

    # Inject PizzaStateStorage globally for the entire application.

    # StateMutator can resolve the storage by the type specified in
    # StateMutator[<storage-class>].

    # Dependencies can also be injected directly through
    # bot.dispatch.injections.

    # This can be useful when different dispatchers need to work
    # with different storage implementations.

    bot.dispatch[PizzaStateStorage] = PizzaStateStorage(redis_client)  # type: ignore

    yield


# State handling.

# States can be injected into handlers and processed there.
# StateMutator is also a node, so it can be injected as well
# to set, transition, and delete states.
# Get the current state and process it.


@bot.on.message(Command("start"))
async def start_handler(message: Message, mutator: Mutator) -> None:
    await choose_pizza(mutator)
    await message.reply(
        text="🍕 Welcome to the pizzeria!\nChoose a pizza:",
        reply_markup=ChoosePizzaKeyboard.get_markup(),
    )


@bot.on.callback_query(
    ChoosePizzaKeyboard.PEPPERONI
    | ChoosePizzaKeyboard.HAWAIIAN
    | ChoosePizzaKeyboard.MARGHERITA
    | ChoosePizzaKeyboard.FOUR_CHEESE,
)
async def pizza_handler(
    cb: CallbackQuery,
    state: ChoosingPizza,
    payload: Payload,
) -> None:
    await state.choose_pizza(Pizza(payload))
    await cb.edit_text(
        text="🍕 Now choose the pizza size:",
        reply_markup=ChoosePizzaSizeKeyboard.get_markup(),
    )


@bot.on.callback_query(
    ChoosePizzaSizeKeyboard.SMALL | ChoosePizzaSizeKeyboard.MEDIUM | ChoosePizzaSizeKeyboard.LARGE,
)
async def size_handler(
    cb: CallbackQuery,
    state: ChoosingSize,
    payload: Payload,
) -> None:
    pizza_size = PizzaSize(payload)

    await state.choose_size(pizza_size)
    await cb.edit_text(
        text=f"📏 Size: {pizza_size.value}\n\nHow would you like to receive your order?",
        reply_markup=ChooseDeliveryTypeKeyboard.get_markup(),
    )


@bot.on.callback_query(
    ChooseDeliveryTypeKeyboard.DELIVERY | ChooseDeliveryTypeKeyboard.PICKUP,
)
async def delivery_handler(
    cb: CallbackQuery,
    state: ChoosingDelivery,
    payload: Payload,
) -> None:
    delivery = DeliveryType(payload)

    await state.choose_delivery(delivery)
    await cb.edit_text(
        text="Great! "
        + (
            "🛵 Please provide a delivery address:"
            if delivery is DeliveryType.DELIVERY
            else (f"Your order:\n🍕 Pizza: {state.pizza.value}\n📏 Size: {state.size.value}\n\nConfirm it: /confirm")
        ),
    )


@bot.on.message()
async def address_handler(waiting: WaitingForAddress, address: Text) -> str:
    await waiting.set_address(address)
    return "📍 Got it!\n\nConfirm it: /confirm"


@bot.on.message(Command("confirm"))
async def confirm_handler(state: Confirming) -> str:
    await state.exit()

    delivery = f"📍 Address: {state.address}" if state.delivery is DeliveryType.DELIVERY else "🏪 Pickup"

    return f"✅ Order placed!\n\n🍕 Pizza: {state.pizza.value}\n📏 Size: {state.size.value}\n{delivery}\n\nThank you! ❤️"


bot.run_forever()
