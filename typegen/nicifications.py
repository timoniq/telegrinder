"""Code in this file is automatically parsed.
---
Nicifications are basically nice features for models which are included in auto-generate_noded models
The difference between nicifications and cure types is: cute types can borrow view runtime properties and have context api
(so they can implement model-specific methods).
Nicifications can only implement fields/methods/properties working only with model fields.
---
Type aliases are used to eliminate boilerplate code in annotations.
`TypeAliases.<TypeAlias>`
"""

import typing
from datetime import datetime
from functools import cached_property

from kungfu import Option, Sum
from msgspex import Model, is_none

from telegrinder.types import *

USED_IMPORTS = {
    "import typing",
    "from datetime import datetime",
    "from functools import cached_property",
    "from msgspex.tools import is_none",
}


class _Birthdate(Birthdate):
    @property
    def is_birthday(self) -> bool:
        """True, if today is a user's birthday."""
        now = datetime.now()
        return now.month == self.month and now.day == self.day

    @property
    def age(self) -> Option[int]:
        """Optional. Contains the user's age, if the user has a birth year specified."""
        return self.year.map(lambda year: ((datetime.now() - datetime(year, self.month, self.day)) // 365).days)


class _Chat(Chat):
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    @property
    def full_name(self) -> Option[str]:
        """Optional. Full name (`first_name` + `last_name`) of the
        other party in a `private` chat.
        """
        return self.first_name.map(lambda x: x + " " + self.last_name.unwrap_or(""))


class _ChatJoinRequest(ChatJoinRequest):
    @property
    def chat_id(self) -> int:
        """`chat_id` instead of `chat.id`."""
        return self.chat.id


class _ChatMemberUpdated(ChatMemberUpdated):
    @property
    def chat_id(self) -> int:
        """Alias `.chat_id` instead of `.chat.id`"""
        return self.chat.id


class _Message(Message):
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.message_id == other.message_id and self.chat_id == other.chat_id

    @cached_property
    def content_type(self) -> ContentType:
        """Type of content that the message contains."""
        for content in ContentType:
            if not is_none(getattr(self, content.value, None)):
                return content

        return ContentType.UNKNOWN

    @property
    def from_user(self) -> "User":
        """`from_user` instead of `from_.unwrap()`."""
        return self.from_.unwrap()

    @property
    def chat_id(self) -> int:
        """`chat_id` instead of `chat.id`."""
        return self.chat.id

    @property
    def chat_title(self) -> str:
        """Chat title, for `supergroups`, `channels` and `group` chats.
        Full name, for `private` chat.
        """
        return self.chat.full_name.unwrap() if self.chat.type == ChatType.PRIVATE else self.chat.title.unwrap()


class _User(User):
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.id == other.id

    @property
    def default_accent_color(self) -> DefaultAccentColor:
        """User's or bot's accent color (non-premium)."""
        return DefaultAccentColor(self.id % len(DefaultAccentColor))

    @property
    def full_name(self) -> str:
        """User's or bot's full name (`first_name` + `last_name`)."""
        return self.first_name + self.last_name.map(" ".__add__).unwrap_or("")


class _Update(Update):
    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.update_type == other.update_type

    @cached_property
    def update_type(self) -> UpdateType:
        """Incoming update type."""
        return UpdateType(next(iter(self.to_dict(exclude_fields={"update_id"}))))

    @cached_property
    def incoming_update(self) -> Model:
        """Incoming update."""
        return getattr(self, self.update_type.value).unwrap()


class _ReplyKeyboardMarkup(ReplyKeyboardMarkup):
    @property
    def empty_markup(self) -> ReplyKeyboardRemove:
        """Empty keyboard to remove the custom keyboard."""
        return ReplyKeyboardRemove(remove_keyboard=True, selective=self.selective.unwrap_or_none())


class _ManagedBotUpdated(ManagedBotUpdated):
    @property
    def user_id(self) -> int:
        """`user_id` instead of `user.id`."""
        return self.user.id


class TypeAliases:
    type RichTexts = typing.Annotated[list[RichText], list]
    type RichText = Sum[
        str,
        RichTextBold,
        RichTextItalic,
        RichTextUnderline,
        RichTextStrikethrough,
        RichTextSpoiler,
        RichTextDateTime,
        RichTextTextMention,
        RichTextSubscript,
        RichTextSuperscript,
        RichTextMarked,
        RichTextCode,
        RichTextCustomEmoji,
        RichTextMathematicalExpression,
        RichTextUrl,
        RichTextEmailAddress,
        RichTextPhoneNumber,
        RichTextBankCardNumber,
        RichTextMention,
        RichTextHashtag,
        RichTextCashtag,
        RichTextBotCommand,
        RichTextButton,
        RichTextAnchor,
        RichTextAnchorLink,
        RichTextReference,
        RichTextReferenceLink,
        RichTexts,
    ]
    type RichBlock = Sum[
        RichBlockParagraph,
        RichBlockSectionHeading,
        RichBlockPreformatted,
        RichBlockFooter,
        RichBlockDivider,
        RichBlockMathematicalExpression,
        RichBlockAnchor,
        RichBlockList,
        RichBlockBlockQuotation,
        RichBlockExpandableBlockQuotation,
        RichBlockPullQuotation,
        RichBlockCollage,
        RichBlockSlideshow,
        RichBlockTable,
        RichBlockDetails,
        RichBlockMap,
        RichBlockButtons,
        RichBlockAnimation,
        RichBlockAudio,
        RichBlockDocument,
        RichBlockPhoto,
        RichBlockVideo,
        RichBlockVoiceNote,
        RichBlockThinking,
    ]
    type InputRichBlock = Sum[
        InputRichBlockParagraph,
        InputRichBlockSectionHeading,
        InputRichBlockPreformatted,
        InputRichBlockFooter,
        InputRichBlockDivider,
        InputRichBlockMathematicalExpression,
        InputRichBlockAnchor,
        InputRichBlockList,
        InputRichBlockBlockQuotation,
        InputRichBlockExpandableBlockQuotation,
        InputRichBlockPullQuotation,
        InputRichBlockCollage,
        InputRichBlockSlideshow,
        InputRichBlockTable,
        InputRichBlockDetails,
        InputRichBlockMap,
        InputRichBlockButtons,
        InputRichBlockAnimation,
        InputRichBlockAudio,
        InputRichBlockDocument,
        InputRichBlockPhoto,
        InputRichBlockVideo,
        InputRichBlockVoiceNote,
        InputRichBlockThinking,
    ]
    type InputFileSource = Sum[str, InputFile]
    type InlineInputMessageContent = Sum[
        InputTextMessageContent,
        InputRichMessageContent,
        InputLocationMessageContent,
        InputVenueMessageContent,
        InputContactMessageContent,
        InputInvoiceMessageContent,
    ]
    type AccessibleMessage = Sum[Message, InaccessibleMessage]
    type ChatId = Sum[int, str]
    type BackgroundFill = Sum[
        BackgroundFillSolid,
        BackgroundFillGradient,
        BackgroundFillFreeformGradient,
    ]
    type ChatMember = Sum[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ]
    type Reaction = Sum[
        ReactionTypeEmoji,
        ReactionTypeCustomEmoji,
        ReactionTypePaid,
    ]
    type ChatBoostSource = Sum[
        ChatBoostSourcePremium,
        ChatBoostSourceGiftCode,
        ChatBoostSourceGiveaway,
    ]
    type TransactionPartner = Sum[
        TransactionPartnerUser,
        TransactionPartnerChat,
        TransactionPartnerAffiliateProgram,
        TransactionPartnerFragment,
        TransactionPartnerTelegramAds,
        TransactionPartnerTelegramApi,
        TransactionPartnerOther,
    ]
