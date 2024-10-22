import dataclasses
import math

from telegrinder import API, CallbackQuery, Message, Telegrinder, Token
from telegrinder.rules import Text
from telegrinder.tools import Page, Paginator, PaginatorItem

bot = Telegrinder(API(Token.from_env()))


@dataclasses.dataclass
class Admin:
    id: int
    full_name: str

    def __repr__(self) -> str:
        return f"🍙 ({self.id}) {self.full_name}"


class AdminPaginator(Paginator[Admin]):
    chat_id: int

    async def get_page(self, page_number: int) -> Page[Admin]:
        limit = 3
        admins = (await self.api.get_chat_administrators(chat_id=self.chat_id)).unwrap()
        max_page = math.ceil(len(admins) / limit)

        return Page(
            items=[
                Admin(id=admin.v.user.id, full_name=admin.v.user.full_name)
                for admin in admins[(page_number - 1) * max_page : page_number * max_page]
            ],
            max_page=max_page,
            page_number=page_number,
        )

    async def get_detail(self, id: int) -> Admin:
        member = (await self.api.get_chat_member(chat_id=self.chat_id, user_id=id)).unwrap()
        return Admin(id=member.v.user.id, full_name=member.v.user.full_name)


@bot.on.message(Text("/admins"))
async def message_handler(message: Message) -> None:
    kb = await AdminPaginator(message.api, message.chat_id).get_keyboard()
    await message.answer("Admins:", reply_markup=kb)


@bot.on.callback_query()
async def transaction_handler(
    cb: CallbackQuery,
    admin: PaginatorItem[Admin, AdminPaginator],
) -> None:
    await cb.edit_text(f"Admin: {admin.full_name} 🍙")


bot.run_forever()
