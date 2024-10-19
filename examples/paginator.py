import dataclasses
import datetime
import math

from telegrinder import API, CallbackQuery, Message, Telegrinder, Token
from telegrinder.rules import Text
from telegrinder.tools import Fetcher, Page, Paginator, PaginatorData

bot = Telegrinder(API(Token.from_env()))


@dataclasses.dataclass
class Transaction:
    id: int
    amount: int
    date: datetime.datetime
    comment: str

    def __repr__(self) -> str:
        datefmt = self.date.strftime("%d.%m")
        return f"🍙 {self.id} {self.amount}💰 ({datefmt})"

    @classmethod
    async def fetch(cls, id: int) -> "Transaction":
        return transactions_db[id - 1]


transactions_db = [
    Transaction(
        id=i + 1,
        amount=int((i + 2) * 5 / 2),
        date=datetime.datetime.now(),
        comment=f"Transaction number {i + 1}",
    )
    for i in range(16)
]


class TransactionFetcher(Fetcher[Transaction]):
    limit = 3

    async def get_page(self, n: int) -> Page[Transaction]:
        items = transactions_db[(n - 1) * self.limit : n * self.limit]
        return Page(math.ceil(len(transactions_db) / self.limit), n, items)


@bot.on.message(Text("/transactions"))
async def message_handler(message: Message) -> None:
    kb = await Paginator[Transaction, TransactionFetcher].get_keyboard()
    await message.answer("Shimi shimi yay transactions 💖", reply_markup=kb)


@bot.on.callback_query()
async def transaction_handler(
    cb: CallbackQuery,
    transaction: PaginatorData[Transaction, TransactionFetcher],
) -> None:
    await cb.edit_text(
        f"Transaction info: {transaction.id=}, {transaction.amount=}, {transaction.date=}, {transaction.comment=}",
    )


bot.run_forever()
