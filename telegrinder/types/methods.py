import typing
from .constructors import *
from telegrinder.tools import Result
from telegrinder.api.error import APIError

if typing.TYPE_CHECKING:
    from telegrinder.api.abc import ABCAPI

X = typing.TypeVar("X")


class APIMethods:
    def __init__(self, api: "ABCAPI"):
        self.api = api

    @staticmethod
    def get_params(loc: dict) -> dict:
        n = {k: v for k, v in loc.items() if k not in ("self", "other") and v is not None}
        n.update(loc['other'])
        return n

    @staticmethod
    def get_response(r: dict) -> dict:
        if 'json' in r: r['json_'] = r['json']
        return r

    async def invoke_after_msg(
        self,
        msg_id: typing.Optional[int] = None,
        query: typing.Optional[X] = None,
        **other
    ) -> Result['X', APIError]:
        result = await self.api.request("invokeAfterMsg", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=X(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def invoke_after_msgs(
        self,
        msg_ids: typing.Optional[typing.List[int]] = None,
        query: typing.Optional[X] = None,
        **other
    ) -> Result['X', APIError]:
        result = await self.api.request("invokeAfterMsgs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=X(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_code(
        self,
        phone_number: typing.Optional[str] = None,
        api_id: typing.Optional[int] = None,
        api_hash: typing.Optional[str] = None,
        settings: typing.Optional['CodeSettings'] = None,
        **other
    ) -> Result['SentCode', APIError]:
        result = await self.api.request("sendCode", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentCode(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def sign_up(
        self,
        phone_number: typing.Optional[str] = None,
        phone_code_hash: typing.Optional[str] = None,
        first_name: typing.Optional[str] = None,
        last_name: typing.Optional[str] = None,
        **other
    ) -> Result['Authorization', APIError]:
        result = await self.api.request("signUp", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Authorization(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def sign_in(
        self,
        phone_number: typing.Optional[str] = None,
        phone_code_hash: typing.Optional[str] = None,
        phone_code: typing.Optional[str] = None,
        **other
    ) -> Result['Authorization', APIError]:
        result = await self.api.request("signIn", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Authorization(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def log_out(
        self,
        **other
    ) -> Result['LoggedOut', APIError]:
        result = await self.api.request("logOut", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=LoggedOut(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def reset_authorizations(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetAuthorizations", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def export_authorization(
        self,
        dc_id: typing.Optional[int] = None,
        **other
    ) -> Result['ExportedAuthorization', APIError]:
        result = await self.api.request("exportAuthorization", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ExportedAuthorization(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def import_authorization(
        self,
        id: typing.Optional[int] = None,
        bytes: typing.Optional[bytes] = None,
        **other
    ) -> Result['Authorization', APIError]:
        result = await self.api.request("importAuthorization", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Authorization(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def bind_temp_auth_key(
        self,
        perm_auth_key_id: typing.Optional[int] = None,
        nonce: typing.Optional[int] = None,
        expires_at: typing.Optional[int] = None,
        encrypted_message: typing.Optional[bytes] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("bindTempAuthKey", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def register_device(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        no_muted: typing.Optional[bool] = None,
        token_type: typing.Optional[int] = None,
        token: typing.Optional[str] = None,
        app_sandbox: typing.Optional[bool] = None,
        secret: typing.Optional[bytes] = None,
        other_uids: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("registerDevice", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def unregister_device(
        self,
        token_type: typing.Optional[int] = None,
        token: typing.Optional[str] = None,
        other_uids: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("unregisterDevice", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def update_notify_settings(
        self,
        peer: typing.Optional['InputNotifyPeer'] = None,
        settings: typing.Optional['InputPeerNotifySettings'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("updateNotifySettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_notify_settings(
        self,
        peer: typing.Optional['InputNotifyPeer'] = None,
        **other
    ) -> Result['PeerNotifySettings', APIError]:
        result = await self.api.request("getNotifySettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PeerNotifySettings(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def reset_notify_settings(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetNotifySettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def update_profile(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        first_name: typing.Optional[str] = None,
        last_name: typing.Optional[str] = None,
        about: typing.Optional[str] = None,
        **other
    ) -> Result['User', APIError]:
        result = await self.api.request("updateProfile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=User(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def update_status(
        self,
        offline: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("updateStatus", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_wall_papers(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['WallPapers', APIError]:
        result = await self.api.request("getWallPapers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=WallPapers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def report_peer(
        self,
        peer: typing.Optional['InputPeer'] = None,
        reason: typing.Optional['ReportReason'] = None,
        message: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("reportPeer", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_users(
        self,
        id: typing.Optional[typing.List['InputUser']] = None,
        **other
    ) -> Result[typing.List['User'], APIError]:
        result = await self.api.request("getUsers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_full_user(
        self,
        id: typing.Optional['InputUser'] = None,
        **other
    ) -> Result['UserFull', APIError]:
        result = await self.api.request("getFullUser", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=UserFull(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_contact_i_ds(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result[typing.List[int], APIError]:
        result = await self.api.request("getContactIDs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_statuses(
        self,
        **other
    ) -> Result[typing.List['ContactStatus'], APIError]:
        result = await self.api.request("getStatuses", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_contacts(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Contacts', APIError]:
        result = await self.api.request("getContacts", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Contacts(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def import_contacts(
        self,
        contacts: typing.Optional[typing.List['InputContact']] = None,
        **other
    ) -> Result['ImportedContacts', APIError]:
        result = await self.api.request("importContacts", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ImportedContacts(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_contacts(
        self,
        id: typing.Optional[typing.List['InputUser']] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("deleteContacts", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_by_phones(
        self,
        phones: typing.Optional[typing.List[str]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteByPhones", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def block(
        self,
        id: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("block", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def unblock(
        self,
        id: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("unblock", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_blocked(
        self,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['Blocked', APIError]:
        result = await self.api.request("getBlocked", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Blocked(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_messages(
        self,
        id: typing.Optional[typing.List['InputMessage']] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_dialogs(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        exclude_pinned: typing.Optional[bool] = None,
        folder_id: typing.Optional[int] = None,
        offset_date: typing.Optional[int] = None,
        offset_id: typing.Optional[int] = None,
        offset_peer: typing.Optional['InputPeer'] = None,
        limit: typing.Optional[int] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Dialogs', APIError]:
        result = await self.api.request("getDialogs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Dialogs(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_history(
        self,
        peer: typing.Optional['InputPeer'] = None,
        offset_id: typing.Optional[int] = None,
        offset_date: typing.Optional[int] = None,
        add_offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        max_id: typing.Optional[int] = None,
        min_id: typing.Optional[int] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def search(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        peer: typing.Optional['InputPeer'] = None,
        q: typing.Optional[str] = None,
        from_id: typing.Optional['InputPeer'] = None,
        top_msg_id: typing.Optional[int] = None,
        filter: typing.Optional['MessagesFilter'] = None,
        min_date: typing.Optional[int] = None,
        max_date: typing.Optional[int] = None,
        offset_id: typing.Optional[int] = None,
        add_offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        max_id: typing.Optional[int] = None,
        min_id: typing.Optional[int] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("search", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def read_history(
        self,
        peer: typing.Optional['InputPeer'] = None,
        max_id: typing.Optional[int] = None,
        **other
    ) -> Result['AffectedMessages', APIError]:
        result = await self.api.request("readHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedMessages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_history(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        just_clear: typing.Optional[bool] = None,
        revoke: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        max_id: typing.Optional[int] = None,
        min_date: typing.Optional[int] = None,
        max_date: typing.Optional[int] = None,
        **other
    ) -> Result['AffectedHistory', APIError]:
        result = await self.api.request("deleteHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedHistory(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_messages(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        revoke: typing.Optional[bool] = None,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['AffectedMessages', APIError]:
        result = await self.api.request("deleteMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedMessages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def received_messages(
        self,
        max_id: typing.Optional[int] = None,
        **other
    ) -> Result[typing.List['ReceivedNotifyMessage'], APIError]:
        result = await self.api.request("receivedMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_typing(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        peer: typing.Optional['InputPeer'] = None,
        top_msg_id: typing.Optional[int] = None,
        action: typing.Optional['SendMessageAction'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setTyping", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_message(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        no_webpage: typing.Optional[bool] = None,
        silent: typing.Optional[bool] = None,
        background: typing.Optional[bool] = None,
        clear_draft: typing.Optional[bool] = None,
        noforwards: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        reply_to_msg_id: typing.Optional[int] = None,
        message: typing.Optional[str] = None,
        random_id: typing.Optional[int] = None,
        reply_markup: typing.Optional['ReplyMarkup'] = None,
        entities: typing.Optional[typing.List['MessageEntity']] = None,
        schedule_date: typing.Optional[int] = None,
        send_as: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("sendMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_media(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        silent: typing.Optional[bool] = None,
        background: typing.Optional[bool] = None,
        clear_draft: typing.Optional[bool] = None,
        noforwards: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        reply_to_msg_id: typing.Optional[int] = None,
        media: typing.Optional['InputMedia'] = None,
        message: typing.Optional[str] = None,
        random_id: typing.Optional[int] = None,
        reply_markup: typing.Optional['ReplyMarkup'] = None,
        entities: typing.Optional[typing.List['MessageEntity']] = None,
        schedule_date: typing.Optional[int] = None,
        send_as: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("sendMedia", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def forward_messages(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        silent: typing.Optional[bool] = None,
        background: typing.Optional[bool] = None,
        with_my_score: typing.Optional[bool] = None,
        drop_author: typing.Optional[bool] = None,
        drop_media_captions: typing.Optional[bool] = None,
        noforwards: typing.Optional[bool] = None,
        from_peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[typing.List[int]] = None,
        random_id: typing.Optional[typing.List[int]] = None,
        to_peer: typing.Optional['InputPeer'] = None,
        schedule_date: typing.Optional[int] = None,
        send_as: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("forwardMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def report_spam(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("reportSpam", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_peer_settings(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['PeerSettings', APIError]:
        result = await self.api.request("getPeerSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PeerSettings(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def report(
        self,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[typing.List[int]] = None,
        reason: typing.Optional['ReportReason'] = None,
        message: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("report", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_chats(
        self,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['Chats', APIError]:
        result = await self.api.request("getChats", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Chats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_full_chat(
        self,
        chat_id: typing.Optional[int] = None,
        **other
    ) -> Result['ChatFull', APIError]:
        result = await self.api.request("getFullChat", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChatFull(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_chat_title(
        self,
        chat_id: typing.Optional[int] = None,
        title: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editChatTitle", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_chat_photo(
        self,
        chat_id: typing.Optional[int] = None,
        photo: typing.Optional['InputChatPhoto'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editChatPhoto", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def add_chat_user(
        self,
        chat_id: typing.Optional[int] = None,
        user_id: typing.Optional['InputUser'] = None,
        fwd_limit: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("addChatUser", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_chat_user(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        revoke_history: typing.Optional[bool] = None,
        chat_id: typing.Optional[int] = None,
        user_id: typing.Optional['InputUser'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("deleteChatUser", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def create_chat(
        self,
        users: typing.Optional[typing.List['InputUser']] = None,
        title: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("createChat", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_state(
        self,
        **other
    ) -> Result['State', APIError]:
        result = await self.api.request("getState", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=State(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_difference(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        pts: typing.Optional[int] = None,
        pts_total_limit: typing.Optional[int] = None,
        date: typing.Optional[int] = None,
        qts: typing.Optional[int] = None,
        **other
    ) -> Result['Difference', APIError]:
        result = await self.api.request("getDifference", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Difference(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def update_profile_photo(
        self,
        id: typing.Optional['InputPhoto'] = None,
        **other
    ) -> Result['Photo', APIError]:
        result = await self.api.request("updateProfilePhoto", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Photo(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def upload_profile_photo(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        file: typing.Optional['InputFile'] = None,
        video: typing.Optional['InputFile'] = None,
        video_start_ts: typing.Optional[float] = None,
        **other
    ) -> Result['Photo', APIError]:
        result = await self.api.request("uploadProfilePhoto", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Photo(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_photos(
        self,
        id: typing.Optional[typing.List['InputPhoto']] = None,
        **other
    ) -> Result[typing.List[int], APIError]:
        result = await self.api.request("deletePhotos", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def save_file_part(
        self,
        file_id: typing.Optional[int] = None,
        file_part: typing.Optional[int] = None,
        bytes: typing.Optional[bytes] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveFilePart", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_file(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        precise: typing.Optional[bool] = None,
        cdn_supported: typing.Optional[bool] = None,
        location: typing.Optional['InputFileLocation'] = None,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['File', APIError]:
        result = await self.api.request("getFile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=File(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_config(
        self,
        **other
    ) -> Result['Config', APIError]:
        result = await self.api.request("getConfig", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Config(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_nearest_dc(
        self,
        **other
    ) -> Result['NearestDc', APIError]:
        result = await self.api.request("getNearestDc", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=NearestDc(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_app_update(
        self,
        source: typing.Optional[str] = None,
        **other
    ) -> Result['AppUpdate', APIError]:
        result = await self.api.request("getAppUpdate", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AppUpdate(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_invite_text(
        self,
        **other
    ) -> Result['InviteText', APIError]:
        result = await self.api.request("getInviteText", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=InviteText(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_user_photos(
        self,
        user_id: typing.Optional['InputUser'] = None,
        offset: typing.Optional[int] = None,
        max_id: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['Photos', APIError]:
        result = await self.api.request("getUserPhotos", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Photos(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_dh_config(
        self,
        version: typing.Optional[int] = None,
        random_length: typing.Optional[int] = None,
        **other
    ) -> Result['DhConfig', APIError]:
        result = await self.api.request("getDhConfig", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=DhConfig(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def request_encryption(
        self,
        user_id: typing.Optional['InputUser'] = None,
        random_id: typing.Optional[int] = None,
        g_a: typing.Optional[bytes] = None,
        **other
    ) -> Result['EncryptedChat', APIError]:
        result = await self.api.request("requestEncryption", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=EncryptedChat(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def accept_encryption(
        self,
        peer: typing.Optional['InputEncryptedChat'] = None,
        g_b: typing.Optional[bytes] = None,
        key_fingerprint: typing.Optional[int] = None,
        **other
    ) -> Result['EncryptedChat', APIError]:
        result = await self.api.request("acceptEncryption", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=EncryptedChat(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def discard_encryption(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        delete_history: typing.Optional[bool] = None,
        chat_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("discardEncryption", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_encrypted_typing(
        self,
        peer: typing.Optional['InputEncryptedChat'] = None,
        typing: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setEncryptedTyping", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def read_encrypted_history(
        self,
        peer: typing.Optional['InputEncryptedChat'] = None,
        max_date: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("readEncryptedHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_encrypted(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        silent: typing.Optional[bool] = None,
        peer: typing.Optional['InputEncryptedChat'] = None,
        random_id: typing.Optional[int] = None,
        data: typing.Optional[bytes] = None,
        **other
    ) -> Result['SentEncryptedMessage', APIError]:
        result = await self.api.request("sendEncrypted", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentEncryptedMessage(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_encrypted_file(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        silent: typing.Optional[bool] = None,
        peer: typing.Optional['InputEncryptedChat'] = None,
        random_id: typing.Optional[int] = None,
        data: typing.Optional[bytes] = None,
        file: typing.Optional['InputEncryptedFile'] = None,
        **other
    ) -> Result['SentEncryptedMessage', APIError]:
        result = await self.api.request("sendEncryptedFile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentEncryptedMessage(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_encrypted_service(
        self,
        peer: typing.Optional['InputEncryptedChat'] = None,
        random_id: typing.Optional[int] = None,
        data: typing.Optional[bytes] = None,
        **other
    ) -> Result['SentEncryptedMessage', APIError]:
        result = await self.api.request("sendEncryptedService", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentEncryptedMessage(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def received_queue(
        self,
        max_qts: typing.Optional[int] = None,
        **other
    ) -> Result[typing.List[int], APIError]:
        result = await self.api.request("receivedQueue", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def report_encrypted_spam(
        self,
        peer: typing.Optional['InputEncryptedChat'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("reportEncryptedSpam", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def save_big_file_part(
        self,
        file_id: typing.Optional[int] = None,
        file_part: typing.Optional[int] = None,
        file_total_parts: typing.Optional[int] = None,
        bytes: typing.Optional[bytes] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveBigFilePart", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def init_connection(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        api_id: typing.Optional[int] = None,
        device_model: typing.Optional[str] = None,
        system_version: typing.Optional[str] = None,
        app_version: typing.Optional[str] = None,
        system_lang_code: typing.Optional[str] = None,
        lang_pack: typing.Optional[str] = None,
        lang_code: typing.Optional[str] = None,
        proxy: typing.Optional['InputClientProxy'] = None,
        params: typing.Optional['JSONValue'] = None,
        query: typing.Optional[X] = None,
        **other
    ) -> Result['X', APIError]:
        result = await self.api.request("initConnection", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=X(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_support(
        self,
        **other
    ) -> Result['Support', APIError]:
        result = await self.api.request("getSupport", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Support(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def read_message_contents(
        self,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['AffectedMessages', APIError]:
        result = await self.api.request("readMessageContents", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedMessages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def check_username(
        self,
        username: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("checkUsername", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def update_username(
        self,
        username: typing.Optional[str] = None,
        **other
    ) -> Result['User', APIError]:
        result = await self.api.request("updateUsername", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=User(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def search(
        self,
        q: typing.Optional[str] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['Found', APIError]:
        result = await self.api.request("search", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Found(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_privacy(
        self,
        key: typing.Optional['InputPrivacyKey'] = None,
        **other
    ) -> Result['PrivacyRules', APIError]:
        result = await self.api.request("getPrivacy", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PrivacyRules(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_privacy(
        self,
        key: typing.Optional['InputPrivacyKey'] = None,
        rules: typing.Optional[typing.List['InputPrivacyRule']] = None,
        **other
    ) -> Result['PrivacyRules', APIError]:
        result = await self.api.request("setPrivacy", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PrivacyRules(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_account(
        self,
        reason: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteAccount", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_account_t_t_l(
        self,
        **other
    ) -> Result['AccountDaysTTL', APIError]:
        result = await self.api.request("getAccountTTL", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AccountDaysTTL(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_account_t_t_l(
        self,
        ttl: typing.Optional['AccountDaysTTL'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setAccountTTL", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def invoke_with_layer(
        self,
        layer: typing.Optional[int] = None,
        query: typing.Optional[X] = None,
        **other
    ) -> Result['X', APIError]:
        result = await self.api.request("invokeWithLayer", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=X(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def resolve_username(
        self,
        username: typing.Optional[str] = None,
        **other
    ) -> Result['ResolvedPeer', APIError]:
        result = await self.api.request("resolveUsername", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ResolvedPeer(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_change_phone_code(
        self,
        phone_number: typing.Optional[str] = None,
        settings: typing.Optional['CodeSettings'] = None,
        **other
    ) -> Result['SentCode', APIError]:
        result = await self.api.request("sendChangePhoneCode", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentCode(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def change_phone(
        self,
        phone_number: typing.Optional[str] = None,
        phone_code_hash: typing.Optional[str] = None,
        phone_code: typing.Optional[str] = None,
        **other
    ) -> Result['User', APIError]:
        result = await self.api.request("changePhone", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=User(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_stickers(
        self,
        emoticon: typing.Optional[str] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Stickers', APIError]:
        result = await self.api.request("getStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Stickers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_all_stickers(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['AllStickers', APIError]:
        result = await self.api.request("getAllStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AllStickers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def update_device_locked(
        self,
        period: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("updateDeviceLocked", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def import_bot_authorization(
        self,
        flags: typing.Optional[int] = None,
        api_id: typing.Optional[int] = None,
        api_hash: typing.Optional[str] = None,
        bot_auth_token: typing.Optional[str] = None,
        **other
    ) -> Result['Authorization', APIError]:
        result = await self.api.request("importBotAuthorization", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Authorization(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_web_page_preview(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        message: typing.Optional[str] = None,
        entities: typing.Optional[typing.List['MessageEntity']] = None,
        **other
    ) -> Result['MessageMedia', APIError]:
        result = await self.api.request("getWebPagePreview", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MessageMedia(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_authorizations(
        self,
        **other
    ) -> Result['Authorizations', APIError]:
        result = await self.api.request("getAuthorizations", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Authorizations(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def reset_authorization(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetAuthorization", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_password(
        self,
        **other
    ) -> Result['Password', APIError]:
        result = await self.api.request("getPassword", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Password(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_password_settings(
        self,
        password: typing.Optional['InputCheckPasswordSRP'] = None,
        **other
    ) -> Result['PasswordSettings', APIError]:
        result = await self.api.request("getPasswordSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PasswordSettings(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def update_password_settings(
        self,
        password: typing.Optional['InputCheckPasswordSRP'] = None,
        new_settings: typing.Optional['PasswordInputSettings'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("updatePasswordSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def check_password(
        self,
        password: typing.Optional['InputCheckPasswordSRP'] = None,
        **other
    ) -> Result['Authorization', APIError]:
        result = await self.api.request("checkPassword", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Authorization(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def request_password_recovery(
        self,
        **other
    ) -> Result['PasswordRecovery', APIError]:
        result = await self.api.request("requestPasswordRecovery", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PasswordRecovery(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def recover_password(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        code: typing.Optional[str] = None,
        new_settings: typing.Optional['PasswordInputSettings'] = None,
        **other
    ) -> Result['Authorization', APIError]:
        result = await self.api.request("recoverPassword", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Authorization(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def invoke_without_updates(
        self,
        query: typing.Optional[X] = None,
        **other
    ) -> Result['X', APIError]:
        result = await self.api.request("invokeWithoutUpdates", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=X(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def export_chat_invite(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        legacy_revoke_permanent: typing.Optional[bool] = None,
        request_needed: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        expire_date: typing.Optional[int] = None,
        usage_limit: typing.Optional[int] = None,
        title: typing.Optional[str] = None,
        **other
    ) -> Result['ExportedChatInvite', APIError]:
        result = await self.api.request("exportChatInvite", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ExportedChatInvite(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def check_chat_invite(
        self,
        hash: typing.Optional[str] = None,
        **other
    ) -> Result['ChatInvite', APIError]:
        result = await self.api.request("checkChatInvite", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChatInvite(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def import_chat_invite(
        self,
        hash: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("importChatInvite", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_sticker_set(
        self,
        stickerset: typing.Optional['InputStickerSet'] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['StickerSet', APIError]:
        result = await self.api.request("getStickerSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StickerSet(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def install_sticker_set(
        self,
        stickerset: typing.Optional['InputStickerSet'] = None,
        archived: typing.Optional[bool] = None,
        **other
    ) -> Result['StickerSetInstallResult', APIError]:
        result = await self.api.request("installStickerSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StickerSetInstallResult(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def uninstall_sticker_set(
        self,
        stickerset: typing.Optional['InputStickerSet'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("uninstallStickerSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def start_bot(
        self,
        bot: typing.Optional['InputUser'] = None,
        peer: typing.Optional['InputPeer'] = None,
        random_id: typing.Optional[int] = None,
        start_param: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("startBot", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_app_changelog(
        self,
        prev_app_version: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("getAppChangelog", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_messages_views(
        self,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[typing.List[int]] = None,
        increment: typing.Optional[bool] = None,
        **other
    ) -> Result['MessageViews', APIError]:
        result = await self.api.request("getMessagesViews", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MessageViews(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def read_history(
        self,
        channel: typing.Optional['InputChannel'] = None,
        max_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("readHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_messages(
        self,
        channel: typing.Optional['InputChannel'] = None,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['AffectedMessages', APIError]:
        result = await self.api.request("deleteMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedMessages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def report_spam(
        self,
        channel: typing.Optional['InputChannel'] = None,
        participant: typing.Optional['InputPeer'] = None,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("reportSpam", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_messages(
        self,
        channel: typing.Optional['InputChannel'] = None,
        id: typing.Optional[typing.List['InputMessage']] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_participants(
        self,
        channel: typing.Optional['InputChannel'] = None,
        filter: typing.Optional['ChannelParticipantsFilter'] = None,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['ChannelParticipants', APIError]:
        result = await self.api.request("getParticipants", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChannelParticipants(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_participant(
        self,
        channel: typing.Optional['InputChannel'] = None,
        participant: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['ChannelParticipant', APIError]:
        result = await self.api.request("getParticipant", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChannelParticipant(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_channels(
        self,
        id: typing.Optional[typing.List['InputChannel']] = None,
        **other
    ) -> Result['Chats', APIError]:
        result = await self.api.request("getChannels", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Chats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_full_channel(
        self,
        channel: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result['ChatFull', APIError]:
        result = await self.api.request("getFullChannel", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChatFull(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def create_channel(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        broadcast: typing.Optional[bool] = None,
        megagroup: typing.Optional[bool] = None,
        for_import: typing.Optional[bool] = None,
        title: typing.Optional[str] = None,
        about: typing.Optional[str] = None,
        geo_point: typing.Optional['InputGeoPoint'] = None,
        address: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("createChannel", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_admin(
        self,
        channel: typing.Optional['InputChannel'] = None,
        user_id: typing.Optional['InputUser'] = None,
        admin_rights: typing.Optional['ChatAdminRights'] = None,
        rank: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editAdmin", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_title(
        self,
        channel: typing.Optional['InputChannel'] = None,
        title: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editTitle", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_photo(
        self,
        channel: typing.Optional['InputChannel'] = None,
        photo: typing.Optional['InputChatPhoto'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editPhoto", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def check_username(
        self,
        channel: typing.Optional['InputChannel'] = None,
        username: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("checkUsername", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def update_username(
        self,
        channel: typing.Optional['InputChannel'] = None,
        username: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("updateUsername", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def join_channel(
        self,
        channel: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("joinChannel", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def leave_channel(
        self,
        channel: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("leaveChannel", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def invite_to_channel(
        self,
        channel: typing.Optional['InputChannel'] = None,
        users: typing.Optional[typing.List['InputUser']] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("inviteToChannel", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_channel(
        self,
        channel: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("deleteChannel", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_channel_difference(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        force: typing.Optional[bool] = None,
        channel: typing.Optional['InputChannel'] = None,
        filter: typing.Optional['ChannelMessagesFilter'] = None,
        pts: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['ChannelDifference', APIError]:
        result = await self.api.request("getChannelDifference", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChannelDifference(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_chat_admin(
        self,
        chat_id: typing.Optional[int] = None,
        user_id: typing.Optional['InputUser'] = None,
        is_admin: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("editChatAdmin", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def migrate_chat(
        self,
        chat_id: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("migrateChat", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def search_global(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        folder_id: typing.Optional[int] = None,
        q: typing.Optional[str] = None,
        filter: typing.Optional['MessagesFilter'] = None,
        min_date: typing.Optional[int] = None,
        max_date: typing.Optional[int] = None,
        offset_rate: typing.Optional[int] = None,
        offset_peer: typing.Optional['InputPeer'] = None,
        offset_id: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("searchGlobal", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def reorder_sticker_sets(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        masks: typing.Optional[bool] = None,
        order: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("reorderStickerSets", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_document_by_hash(
        self,
        sha256: typing.Optional[bytes] = None,
        size: typing.Optional[int] = None,
        mime_type: typing.Optional[str] = None,
        **other
    ) -> Result['Document', APIError]:
        result = await self.api.request("getDocumentByHash", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Document(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_saved_gifs(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['SavedGifs', APIError]:
        result = await self.api.request("getSavedGifs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SavedGifs(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_gif(
        self,
        id: typing.Optional['InputDocument'] = None,
        unsave: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveGif", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_inline_bot_results(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        bot: typing.Optional['InputUser'] = None,
        peer: typing.Optional['InputPeer'] = None,
        geo_point: typing.Optional['InputGeoPoint'] = None,
        query: typing.Optional[str] = None,
        offset: typing.Optional[str] = None,
        **other
    ) -> Result['BotResults', APIError]:
        result = await self.api.request("getInlineBotResults", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=BotResults(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_inline_bot_results(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        gallery: typing.Optional[bool] = None,
        private: typing.Optional[bool] = None,
        query_id: typing.Optional[int] = None,
        results: typing.Optional[typing.List['InputBotInlineResult']] = None,
        cache_time: typing.Optional[int] = None,
        next_offset: typing.Optional[str] = None,
        switch_pm: typing.Optional['InlineBotSwitchPM'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setInlineBotResults", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_inline_bot_result(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        silent: typing.Optional[bool] = None,
        background: typing.Optional[bool] = None,
        clear_draft: typing.Optional[bool] = None,
        hide_via: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        reply_to_msg_id: typing.Optional[int] = None,
        random_id: typing.Optional[int] = None,
        query_id: typing.Optional[int] = None,
        id: typing.Optional[str] = None,
        schedule_date: typing.Optional[int] = None,
        send_as: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("sendInlineBotResult", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def export_message_link(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        grouped: typing.Optional[bool] = None,
        thread: typing.Optional[bool] = None,
        channel: typing.Optional['InputChannel'] = None,
        id: typing.Optional[int] = None,
        **other
    ) -> Result['ExportedMessageLink', APIError]:
        result = await self.api.request("exportMessageLink", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ExportedMessageLink(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def toggle_signatures(
        self,
        channel: typing.Optional['InputChannel'] = None,
        enabled: typing.Optional[bool] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("toggleSignatures", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def resend_code(
        self,
        phone_number: typing.Optional[str] = None,
        phone_code_hash: typing.Optional[str] = None,
        **other
    ) -> Result['SentCode', APIError]:
        result = await self.api.request("resendCode", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentCode(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def cancel_code(
        self,
        phone_number: typing.Optional[str] = None,
        phone_code_hash: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("cancelCode", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_message_edit_data(
        self,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[int] = None,
        **other
    ) -> Result['MessageEditData', APIError]:
        result = await self.api.request("getMessageEditData", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MessageEditData(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_message(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        no_webpage: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[int] = None,
        message: typing.Optional[str] = None,
        media: typing.Optional['InputMedia'] = None,
        reply_markup: typing.Optional['ReplyMarkup'] = None,
        entities: typing.Optional[typing.List['MessageEntity']] = None,
        schedule_date: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_inline_bot_message(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        no_webpage: typing.Optional[bool] = None,
        id: typing.Optional['InputBotInlineMessageID'] = None,
        message: typing.Optional[str] = None,
        media: typing.Optional['InputMedia'] = None,
        reply_markup: typing.Optional['ReplyMarkup'] = None,
        entities: typing.Optional[typing.List['MessageEntity']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("editInlineBotMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_bot_callback_answer(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        game: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        data: typing.Optional[bytes] = None,
        password: typing.Optional['InputCheckPasswordSRP'] = None,
        **other
    ) -> Result['BotCallbackAnswer', APIError]:
        result = await self.api.request("getBotCallbackAnswer", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=BotCallbackAnswer(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_bot_callback_answer(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        alert: typing.Optional[bool] = None,
        query_id: typing.Optional[int] = None,
        message: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
        cache_time: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setBotCallbackAnswer", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_top_peers(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        correspondents: typing.Optional[bool] = None,
        bots_pm: typing.Optional[bool] = None,
        bots_inline: typing.Optional[bool] = None,
        phone_calls: typing.Optional[bool] = None,
        forward_users: typing.Optional[bool] = None,
        forward_chats: typing.Optional[bool] = None,
        groups: typing.Optional[bool] = None,
        channels: typing.Optional[bool] = None,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['TopPeers', APIError]:
        result = await self.api.request("getTopPeers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=TopPeers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def reset_top_peer_rating(
        self,
        category: typing.Optional['TopPeerCategory'] = None,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetTopPeerRating", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_peer_dialogs(
        self,
        peers: typing.Optional[typing.List['InputDialogPeer']] = None,
        **other
    ) -> Result['PeerDialogs', APIError]:
        result = await self.api.request("getPeerDialogs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PeerDialogs(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_draft(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        no_webpage: typing.Optional[bool] = None,
        reply_to_msg_id: typing.Optional[int] = None,
        peer: typing.Optional['InputPeer'] = None,
        message: typing.Optional[str] = None,
        entities: typing.Optional[typing.List['MessageEntity']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveDraft", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_all_drafts(
        self,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("getAllDrafts", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_featured_stickers(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['FeaturedStickers', APIError]:
        result = await self.api.request("getFeaturedStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=FeaturedStickers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def read_featured_stickers(
        self,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("readFeaturedStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_recent_stickers(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        attached: typing.Optional[bool] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['RecentStickers', APIError]:
        result = await self.api.request("getRecentStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=RecentStickers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_recent_sticker(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        attached: typing.Optional[bool] = None,
        id: typing.Optional['InputDocument'] = None,
        unsave: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveRecentSticker", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def clear_recent_stickers(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        attached: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("clearRecentStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_archived_stickers(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        masks: typing.Optional[bool] = None,
        offset_id: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['ArchivedStickers', APIError]:
        result = await self.api.request("getArchivedStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ArchivedStickers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_confirm_phone_code(
        self,
        hash: typing.Optional[str] = None,
        settings: typing.Optional['CodeSettings'] = None,
        **other
    ) -> Result['SentCode', APIError]:
        result = await self.api.request("sendConfirmPhoneCode", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentCode(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def confirm_phone(
        self,
        phone_code_hash: typing.Optional[str] = None,
        phone_code: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("confirmPhone", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_admined_public_channels(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        by_location: typing.Optional[bool] = None,
        check_limit: typing.Optional[bool] = None,
        **other
    ) -> Result['Chats', APIError]:
        result = await self.api.request("getAdminedPublicChannels", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Chats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_mask_stickers(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['AllStickers', APIError]:
        result = await self.api.request("getMaskStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AllStickers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_attached_stickers(
        self,
        media: typing.Optional['InputStickeredMedia'] = None,
        **other
    ) -> Result[typing.List['StickerSetCovered'], APIError]:
        result = await self.api.request("getAttachedStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def drop_temp_auth_keys(
        self,
        except_auth_keys: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("dropTempAuthKeys", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_game_score(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        edit_message: typing.Optional[bool] = None,
        force: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[int] = None,
        user_id: typing.Optional['InputUser'] = None,
        score: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("setGameScore", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_inline_game_score(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        edit_message: typing.Optional[bool] = None,
        force: typing.Optional[bool] = None,
        id: typing.Optional['InputBotInlineMessageID'] = None,
        user_id: typing.Optional['InputUser'] = None,
        score: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setInlineGameScore", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_game_high_scores(
        self,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[int] = None,
        user_id: typing.Optional['InputUser'] = None,
        **other
    ) -> Result['HighScores', APIError]:
        result = await self.api.request("getGameHighScores", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=HighScores(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_inline_game_high_scores(
        self,
        id: typing.Optional['InputBotInlineMessageID'] = None,
        user_id: typing.Optional['InputUser'] = None,
        **other
    ) -> Result['HighScores', APIError]:
        result = await self.api.request("getInlineGameHighScores", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=HighScores(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_common_chats(
        self,
        user_id: typing.Optional['InputUser'] = None,
        max_id: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['Chats', APIError]:
        result = await self.api.request("getCommonChats", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Chats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_all_chats(
        self,
        except_ids: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['Chats', APIError]:
        result = await self.api.request("getAllChats", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Chats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_bot_updates_status(
        self,
        pending_updates_count: typing.Optional[int] = None,
        message: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setBotUpdatesStatus", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_web_page(
        self,
        url: typing.Optional[str] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['WebPage', APIError]:
        result = await self.api.request("getWebPage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=WebPage(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def toggle_dialog_pin(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        pinned: typing.Optional[bool] = None,
        peer: typing.Optional['InputDialogPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("toggleDialogPin", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def reorder_pinned_dialogs(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        force: typing.Optional[bool] = None,
        folder_id: typing.Optional[int] = None,
        order: typing.Optional[typing.List['InputDialogPeer']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("reorderPinnedDialogs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_pinned_dialogs(
        self,
        folder_id: typing.Optional[int] = None,
        **other
    ) -> Result['PeerDialogs', APIError]:
        result = await self.api.request("getPinnedDialogs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PeerDialogs(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_custom_request(
        self,
        custom_method: typing.Optional[str] = None,
        params: typing.Optional['DataJSON'] = None,
        **other
    ) -> Result['DataJSON', APIError]:
        result = await self.api.request("sendCustomRequest", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=DataJSON(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def answer_webhook_j_s_o_n_query(
        self,
        query_id: typing.Optional[int] = None,
        data: typing.Optional['DataJSON'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("answerWebhookJSONQuery", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_web_file(
        self,
        location: typing.Optional['InputWebFileLocation'] = None,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['WebFile', APIError]:
        result = await self.api.request("getWebFile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=WebFile(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_payment_form(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        theme_params: typing.Optional['DataJSON'] = None,
        **other
    ) -> Result['PaymentForm', APIError]:
        result = await self.api.request("getPaymentForm", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PaymentForm(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_payment_receipt(
        self,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        **other
    ) -> Result['PaymentReceipt', APIError]:
        result = await self.api.request("getPaymentReceipt", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PaymentReceipt(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def validate_requested_info(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        save: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        info: typing.Optional['PaymentRequestedInfo'] = None,
        **other
    ) -> Result['ValidatedRequestedInfo', APIError]:
        result = await self.api.request("validateRequestedInfo", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ValidatedRequestedInfo(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_payment_form(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        form_id: typing.Optional[int] = None,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        requested_info_id: typing.Optional[str] = None,
        shipping_option_id: typing.Optional[str] = None,
        credentials: typing.Optional['InputPaymentCredentials'] = None,
        tip_amount: typing.Optional[int] = None,
        **other
    ) -> Result['PaymentResult', APIError]:
        result = await self.api.request("sendPaymentForm", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PaymentResult(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_tmp_password(
        self,
        password: typing.Optional['InputCheckPasswordSRP'] = None,
        period: typing.Optional[int] = None,
        **other
    ) -> Result['TmpPassword', APIError]:
        result = await self.api.request("getTmpPassword", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=TmpPassword(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_saved_info(
        self,
        **other
    ) -> Result['SavedInfo', APIError]:
        result = await self.api.request("getSavedInfo", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SavedInfo(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def clear_saved_info(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        credentials: typing.Optional[bool] = None,
        info: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("clearSavedInfo", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_bot_shipping_results(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        query_id: typing.Optional[int] = None,
        error: typing.Optional[str] = None,
        shipping_options: typing.Optional[typing.List['ShippingOption']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setBotShippingResults", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_bot_precheckout_results(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        success: typing.Optional[bool] = None,
        query_id: typing.Optional[int] = None,
        error: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setBotPrecheckoutResults", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def create_sticker_set(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        masks: typing.Optional[bool] = None,
        animated: typing.Optional[bool] = None,
        videos: typing.Optional[bool] = None,
        user_id: typing.Optional['InputUser'] = None,
        title: typing.Optional[str] = None,
        short_name: typing.Optional[str] = None,
        thumb: typing.Optional['InputDocument'] = None,
        stickers: typing.Optional[typing.List['InputStickerSetItem']] = None,
        software: typing.Optional[str] = None,
        **other
    ) -> Result['StickerSet', APIError]:
        result = await self.api.request("createStickerSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StickerSet(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def remove_sticker_from_set(
        self,
        sticker: typing.Optional['InputDocument'] = None,
        **other
    ) -> Result['StickerSet', APIError]:
        result = await self.api.request("removeStickerFromSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StickerSet(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def change_sticker_position(
        self,
        sticker: typing.Optional['InputDocument'] = None,
        position: typing.Optional[int] = None,
        **other
    ) -> Result['StickerSet', APIError]:
        result = await self.api.request("changeStickerPosition", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StickerSet(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def add_sticker_to_set(
        self,
        stickerset: typing.Optional['InputStickerSet'] = None,
        sticker: typing.Optional['InputStickerSetItem'] = None,
        **other
    ) -> Result['StickerSet', APIError]:
        result = await self.api.request("addStickerToSet", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StickerSet(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def upload_media(
        self,
        peer: typing.Optional['InputPeer'] = None,
        media: typing.Optional['InputMedia'] = None,
        **other
    ) -> Result['MessageMedia', APIError]:
        result = await self.api.request("uploadMedia", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MessageMedia(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_call_config(
        self,
        **other
    ) -> Result['DataJSON', APIError]:
        result = await self.api.request("getCallConfig", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=DataJSON(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def request_call(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        video: typing.Optional[bool] = None,
        user_id: typing.Optional['InputUser'] = None,
        random_id: typing.Optional[int] = None,
        g_a_hash: typing.Optional[bytes] = None,
        protocol: typing.Optional['PhoneCallProtocol'] = None,
        **other
    ) -> Result['PhoneCall', APIError]:
        result = await self.api.request("requestCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PhoneCall(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def accept_call(
        self,
        peer: typing.Optional['InputPhoneCall'] = None,
        g_b: typing.Optional[bytes] = None,
        protocol: typing.Optional['PhoneCallProtocol'] = None,
        **other
    ) -> Result['PhoneCall', APIError]:
        result = await self.api.request("acceptCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PhoneCall(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def confirm_call(
        self,
        peer: typing.Optional['InputPhoneCall'] = None,
        g_a: typing.Optional[bytes] = None,
        key_fingerprint: typing.Optional[int] = None,
        protocol: typing.Optional['PhoneCallProtocol'] = None,
        **other
    ) -> Result['PhoneCall', APIError]:
        result = await self.api.request("confirmCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PhoneCall(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def received_call(
        self,
        peer: typing.Optional['InputPhoneCall'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("receivedCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def discard_call(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        video: typing.Optional[bool] = None,
        peer: typing.Optional['InputPhoneCall'] = None,
        duration: typing.Optional[int] = None,
        reason: typing.Optional['PhoneCallDiscardReason'] = None,
        connection_id: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("discardCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_call_rating(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        user_initiative: typing.Optional[bool] = None,
        peer: typing.Optional['InputPhoneCall'] = None,
        rating: typing.Optional[int] = None,
        comment: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("setCallRating", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_call_debug(
        self,
        peer: typing.Optional['InputPhoneCall'] = None,
        debug: typing.Optional['DataJSON'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveCallDebug", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_cdn_file(
        self,
        file_token: typing.Optional[bytes] = None,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['CdnFile', APIError]:
        result = await self.api.request("getCdnFile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=CdnFile(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def reupload_cdn_file(
        self,
        file_token: typing.Optional[bytes] = None,
        request_token: typing.Optional[bytes] = None,
        **other
    ) -> Result[typing.List['FileHash'], APIError]:
        result = await self.api.request("reuploadCdnFile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_cdn_config(
        self,
        **other
    ) -> Result['CdnConfig', APIError]:
        result = await self.api.request("getCdnConfig", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=CdnConfig(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_lang_pack(
        self,
        lang_pack: typing.Optional[str] = None,
        lang_code: typing.Optional[str] = None,
        **other
    ) -> Result['LangPackDifference', APIError]:
        result = await self.api.request("getLangPack", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=LangPackDifference(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_strings(
        self,
        lang_pack: typing.Optional[str] = None,
        lang_code: typing.Optional[str] = None,
        keys: typing.Optional[typing.List[str]] = None,
        **other
    ) -> Result[typing.List['LangPackString'], APIError]:
        result = await self.api.request("getStrings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_difference(
        self,
        lang_pack: typing.Optional[str] = None,
        lang_code: typing.Optional[str] = None,
        from_version: typing.Optional[int] = None,
        **other
    ) -> Result['LangPackDifference', APIError]:
        result = await self.api.request("getDifference", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=LangPackDifference(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_languages(
        self,
        lang_pack: typing.Optional[str] = None,
        **other
    ) -> Result[typing.List['LangPackLanguage'], APIError]:
        result = await self.api.request("getLanguages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def edit_banned(
        self,
        channel: typing.Optional['InputChannel'] = None,
        participant: typing.Optional['InputPeer'] = None,
        banned_rights: typing.Optional['ChatBannedRights'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editBanned", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_admin_log(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        channel: typing.Optional['InputChannel'] = None,
        q: typing.Optional[str] = None,
        events_filter: typing.Optional['ChannelAdminLogEventsFilter'] = None,
        admins: typing.Optional[typing.List['InputUser']] = None,
        max_id: typing.Optional[int] = None,
        min_id: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['AdminLogResults', APIError]:
        result = await self.api.request("getAdminLog", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AdminLogResults(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_cdn_file_hashes(
        self,
        file_token: typing.Optional[bytes] = None,
        offset: typing.Optional[int] = None,
        **other
    ) -> Result[typing.List['FileHash'], APIError]:
        result = await self.api.request("getCdnFileHashes", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_screenshot_notification(
        self,
        peer: typing.Optional['InputPeer'] = None,
        reply_to_msg_id: typing.Optional[int] = None,
        random_id: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("sendScreenshotNotification", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_stickers(
        self,
        channel: typing.Optional['InputChannel'] = None,
        stickerset: typing.Optional['InputStickerSet'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_faved_stickers(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['FavedStickers', APIError]:
        result = await self.api.request("getFavedStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=FavedStickers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def fave_sticker(
        self,
        id: typing.Optional['InputDocument'] = None,
        unfave: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("faveSticker", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def read_message_contents(
        self,
        channel: typing.Optional['InputChannel'] = None,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("readMessageContents", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def reset_saved(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetSaved", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_unread_mentions(
        self,
        peer: typing.Optional['InputPeer'] = None,
        offset_id: typing.Optional[int] = None,
        add_offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        max_id: typing.Optional[int] = None,
        min_id: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getUnreadMentions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_history(
        self,
        channel: typing.Optional['InputChannel'] = None,
        max_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_recent_me_urls(
        self,
        referer: typing.Optional[str] = None,
        **other
    ) -> Result['RecentMeUrls', APIError]:
        result = await self.api.request("getRecentMeUrls", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=RecentMeUrls(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def toggle_pre_history_hidden(
        self,
        channel: typing.Optional['InputChannel'] = None,
        enabled: typing.Optional[bool] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("togglePreHistoryHidden", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def read_mentions(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['AffectedHistory', APIError]:
        result = await self.api.request("readMentions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedHistory(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_recent_locations(
        self,
        peer: typing.Optional['InputPeer'] = None,
        limit: typing.Optional[int] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getRecentLocations", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_multi_media(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        silent: typing.Optional[bool] = None,
        background: typing.Optional[bool] = None,
        clear_draft: typing.Optional[bool] = None,
        noforwards: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        reply_to_msg_id: typing.Optional[int] = None,
        multi_media: typing.Optional[typing.List['InputSingleMedia']] = None,
        schedule_date: typing.Optional[int] = None,
        send_as: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("sendMultiMedia", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def upload_encrypted_file(
        self,
        peer: typing.Optional['InputEncryptedChat'] = None,
        file: typing.Optional['InputEncryptedFile'] = None,
        **other
    ) -> Result['EncryptedFile', APIError]:
        result = await self.api.request("uploadEncryptedFile", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=EncryptedFile(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_web_authorizations(
        self,
        **other
    ) -> Result['WebAuthorizations', APIError]:
        result = await self.api.request("getWebAuthorizations", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=WebAuthorizations(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def reset_web_authorization(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetWebAuthorization", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def reset_web_authorizations(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetWebAuthorizations", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def search_sticker_sets(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        exclude_featured: typing.Optional[bool] = None,
        q: typing.Optional[str] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['FoundStickerSets', APIError]:
        result = await self.api.request("searchStickerSets", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=FoundStickerSets(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_file_hashes(
        self,
        location: typing.Optional['InputFileLocation'] = None,
        offset: typing.Optional[int] = None,
        **other
    ) -> Result[typing.List['FileHash'], APIError]:
        result = await self.api.request("getFileHashes", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_terms_of_service_update(
        self,
        **other
    ) -> Result['TermsOfServiceUpdate', APIError]:
        result = await self.api.request("getTermsOfServiceUpdate", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=TermsOfServiceUpdate(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def accept_terms_of_service(
        self,
        id: typing.Optional['DataJSON'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("acceptTermsOfService", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_all_secure_values(
        self,
        **other
    ) -> Result[typing.List['SecureValue'], APIError]:
        result = await self.api.request("getAllSecureValues", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_secure_value(
        self,
        types: typing.Optional[typing.List['SecureValueType']] = None,
        **other
    ) -> Result[typing.List['SecureValue'], APIError]:
        result = await self.api.request("getSecureValue", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def save_secure_value(
        self,
        value: typing.Optional['InputSecureValue'] = None,
        secure_secret_id: typing.Optional[int] = None,
        **other
    ) -> Result['SecureValue', APIError]:
        result = await self.api.request("saveSecureValue", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SecureValue(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_secure_value(
        self,
        types: typing.Optional[typing.List['SecureValueType']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteSecureValue", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_secure_value_errors(
        self,
        id: typing.Optional['InputUser'] = None,
        errors: typing.Optional[typing.List['SecureValueError']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setSecureValueErrors", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_authorization_form(
        self,
        bot_id: typing.Optional[int] = None,
        scope: typing.Optional[str] = None,
        public_key: typing.Optional[str] = None,
        **other
    ) -> Result['AuthorizationForm', APIError]:
        result = await self.api.request("getAuthorizationForm", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AuthorizationForm(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def accept_authorization(
        self,
        bot_id: typing.Optional[int] = None,
        scope: typing.Optional[str] = None,
        public_key: typing.Optional[str] = None,
        value_hashes: typing.Optional[typing.List['SecureValueHash']] = None,
        credentials: typing.Optional['SecureCredentialsEncrypted'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("acceptAuthorization", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_verify_phone_code(
        self,
        phone_number: typing.Optional[str] = None,
        settings: typing.Optional['CodeSettings'] = None,
        **other
    ) -> Result['SentCode', APIError]:
        result = await self.api.request("sendVerifyPhoneCode", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentCode(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def verify_phone(
        self,
        phone_number: typing.Optional[str] = None,
        phone_code_hash: typing.Optional[str] = None,
        phone_code: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("verifyPhone", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_verify_email_code(
        self,
        email: typing.Optional[str] = None,
        **other
    ) -> Result['SentEmailCode', APIError]:
        result = await self.api.request("sendVerifyEmailCode", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SentEmailCode(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def verify_email(
        self,
        email: typing.Optional[str] = None,
        code: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("verifyEmail", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_deep_link_info(
        self,
        path: typing.Optional[str] = None,
        **other
    ) -> Result['DeepLinkInfo', APIError]:
        result = await self.api.request("getDeepLinkInfo", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=DeepLinkInfo(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_saved(
        self,
        **other
    ) -> Result[typing.List['SavedContact'], APIError]:
        result = await self.api.request("getSaved", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_left_channels(
        self,
        offset: typing.Optional[int] = None,
        **other
    ) -> Result['Chats', APIError]:
        result = await self.api.request("getLeftChannels", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Chats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def init_takeout_session(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        contacts: typing.Optional[bool] = None,
        message_users: typing.Optional[bool] = None,
        message_chats: typing.Optional[bool] = None,
        message_megagroups: typing.Optional[bool] = None,
        message_channels: typing.Optional[bool] = None,
        files: typing.Optional[bool] = None,
        file_max_size: typing.Optional[int] = None,
        **other
    ) -> Result['Takeout', APIError]:
        result = await self.api.request("initTakeoutSession", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Takeout(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def finish_takeout_session(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        success: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("finishTakeoutSession", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_split_ranges(
        self,
        **other
    ) -> Result[typing.List['MessageRange'], APIError]:
        result = await self.api.request("getSplitRanges", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def invoke_with_messages_range(
        self,
        range: typing.Optional['MessageRange'] = None,
        query: typing.Optional[X] = None,
        **other
    ) -> Result['X', APIError]:
        result = await self.api.request("invokeWithMessagesRange", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=X(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def invoke_with_takeout(
        self,
        takeout_id: typing.Optional[int] = None,
        query: typing.Optional[X] = None,
        **other
    ) -> Result['X', APIError]:
        result = await self.api.request("invokeWithTakeout", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=X(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def mark_dialog_unread(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        unread: typing.Optional[bool] = None,
        peer: typing.Optional['InputDialogPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("markDialogUnread", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_dialog_unread_marks(
        self,
        **other
    ) -> Result[typing.List['DialogPeer'], APIError]:
        result = await self.api.request("getDialogUnreadMarks", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def toggle_top_peers(
        self,
        enabled: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("toggleTopPeers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def clear_all_drafts(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("clearAllDrafts", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_app_config(
        self,
        **other
    ) -> Result['JSONValue', APIError]:
        result = await self.api.request("getAppConfig", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=JSONValue(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_app_log(
        self,
        events: typing.Optional[typing.List['InputAppEvent']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveAppLog", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_passport_config(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['PassportConfig', APIError]:
        result = await self.api.request("getPassportConfig", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PassportConfig(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_language(
        self,
        lang_pack: typing.Optional[str] = None,
        lang_code: typing.Optional[str] = None,
        **other
    ) -> Result['LangPackLanguage', APIError]:
        result = await self.api.request("getLanguage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=LangPackLanguage(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def update_pinned_message(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        silent: typing.Optional[bool] = None,
        unpin: typing.Optional[bool] = None,
        pm_oneside: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("updatePinnedMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def confirm_password_email(
        self,
        code: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("confirmPasswordEmail", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def resend_password_email(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resendPasswordEmail", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def cancel_password_email(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("cancelPasswordEmail", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_support_name(
        self,
        **other
    ) -> Result['SupportName', APIError]:
        result = await self.api.request("getSupportName", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SupportName(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_user_info(
        self,
        user_id: typing.Optional['InputUser'] = None,
        **other
    ) -> Result['UserInfo', APIError]:
        result = await self.api.request("getUserInfo", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=UserInfo(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_user_info(
        self,
        user_id: typing.Optional['InputUser'] = None,
        message: typing.Optional[str] = None,
        entities: typing.Optional[typing.List['MessageEntity']] = None,
        **other
    ) -> Result['UserInfo', APIError]:
        result = await self.api.request("editUserInfo", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=UserInfo(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_contact_sign_up_notification(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("getContactSignUpNotification", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def set_contact_sign_up_notification(
        self,
        silent: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setContactSignUpNotification", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_notify_exceptions(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        compare_sound: typing.Optional[bool] = None,
        peer: typing.Optional['InputNotifyPeer'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("getNotifyExceptions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_vote(
        self,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        options: typing.Optional[typing.List[bytes]] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("sendVote", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_poll_results(
        self,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("getPollResults", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_onlines(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['ChatOnlines', APIError]:
        result = await self.api.request("getOnlines", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChatOnlines(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_chat_about(
        self,
        peer: typing.Optional['InputPeer'] = None,
        about: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("editChatAbout", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def edit_chat_default_banned_rights(
        self,
        peer: typing.Optional['InputPeer'] = None,
        banned_rights: typing.Optional['ChatBannedRights'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editChatDefaultBannedRights", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_wall_paper(
        self,
        wallpaper: typing.Optional['InputWallPaper'] = None,
        **other
    ) -> Result['WallPaper', APIError]:
        result = await self.api.request("getWallPaper", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=WallPaper(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def upload_wall_paper(
        self,
        file: typing.Optional['InputFile'] = None,
        mime_type: typing.Optional[str] = None,
        settings: typing.Optional['WallPaperSettings'] = None,
        **other
    ) -> Result['WallPaper', APIError]:
        result = await self.api.request("uploadWallPaper", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=WallPaper(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_wall_paper(
        self,
        wallpaper: typing.Optional['InputWallPaper'] = None,
        unsave: typing.Optional[bool] = None,
        settings: typing.Optional['WallPaperSettings'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveWallPaper", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def install_wall_paper(
        self,
        wallpaper: typing.Optional['InputWallPaper'] = None,
        settings: typing.Optional['WallPaperSettings'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("installWallPaper", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def reset_wall_papers(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetWallPapers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_auto_download_settings(
        self,
        **other
    ) -> Result['AutoDownloadSettings', APIError]:
        result = await self.api.request("getAutoDownloadSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AutoDownloadSettings(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_auto_download_settings(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        low: typing.Optional[bool] = None,
        high: typing.Optional[bool] = None,
        settings: typing.Optional['AutoDownloadSettings'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveAutoDownloadSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_emoji_keywords(
        self,
        lang_code: typing.Optional[str] = None,
        **other
    ) -> Result['EmojiKeywordsDifference', APIError]:
        result = await self.api.request("getEmojiKeywords", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=EmojiKeywordsDifference(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_emoji_keywords_difference(
        self,
        lang_code: typing.Optional[str] = None,
        from_version: typing.Optional[int] = None,
        **other
    ) -> Result['EmojiKeywordsDifference', APIError]:
        result = await self.api.request("getEmojiKeywordsDifference", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=EmojiKeywordsDifference(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_emoji_keywords_languages(
        self,
        lang_codes: typing.Optional[typing.List[str]] = None,
        **other
    ) -> Result[typing.List['EmojiLanguage'], APIError]:
        result = await self.api.request("getEmojiKeywordsLanguages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_emoji_u_r_l(
        self,
        lang_code: typing.Optional[str] = None,
        **other
    ) -> Result['EmojiURL', APIError]:
        result = await self.api.request("getEmojiURL", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=EmojiURL(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_peer_folders(
        self,
        folder_peers: typing.Optional[typing.List['InputFolderPeer']] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editPeerFolders", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_folder(
        self,
        folder_id: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("deleteFolder", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_search_counters(
        self,
        peer: typing.Optional['InputPeer'] = None,
        filters: typing.Optional[typing.List['MessagesFilter']] = None,
        **other
    ) -> Result[typing.List['SearchCounter'], APIError]:
        result = await self.api.request("getSearchCounters", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_groups_for_discussion(
        self,
        **other
    ) -> Result['Chats', APIError]:
        result = await self.api.request("getGroupsForDiscussion", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Chats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_discussion_group(
        self,
        broadcast: typing.Optional['InputChannel'] = None,
        group: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setDiscussionGroup", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def request_url_auth(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        button_id: typing.Optional[int] = None,
        url: typing.Optional[str] = None,
        **other
    ) -> Result['UrlAuthResult', APIError]:
        result = await self.api.request("requestUrlAuth", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=UrlAuthResult(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def accept_url_auth(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        write_allowed: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        button_id: typing.Optional[int] = None,
        url: typing.Optional[str] = None,
        **other
    ) -> Result['UrlAuthResult', APIError]:
        result = await self.api.request("acceptUrlAuth", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=UrlAuthResult(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def hide_peer_settings_bar(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("hidePeerSettingsBar", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def add_contact(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        add_phone_privacy_exception: typing.Optional[bool] = None,
        id: typing.Optional['InputUser'] = None,
        first_name: typing.Optional[str] = None,
        last_name: typing.Optional[str] = None,
        phone: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("addContact", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def accept_contact(
        self,
        id: typing.Optional['InputUser'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("acceptContact", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_creator(
        self,
        channel: typing.Optional['InputChannel'] = None,
        user_id: typing.Optional['InputUser'] = None,
        password: typing.Optional['InputCheckPasswordSRP'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editCreator", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_located(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        background: typing.Optional[bool] = None,
        geo_point: typing.Optional['InputGeoPoint'] = None,
        self_expires: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("getLocated", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_location(
        self,
        channel: typing.Optional['InputChannel'] = None,
        geo_point: typing.Optional['InputGeoPoint'] = None,
        address: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("editLocation", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def toggle_slow_mode(
        self,
        channel: typing.Optional['InputChannel'] = None,
        seconds: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("toggleSlowMode", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_scheduled_history(
        self,
        peer: typing.Optional['InputPeer'] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getScheduledHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_scheduled_messages(
        self,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getScheduledMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_scheduled_messages(
        self,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("sendScheduledMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_scheduled_messages(
        self,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("deleteScheduledMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def upload_theme(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        file: typing.Optional['InputFile'] = None,
        thumb: typing.Optional['InputFile'] = None,
        file_name: typing.Optional[str] = None,
        mime_type: typing.Optional[str] = None,
        **other
    ) -> Result['Document', APIError]:
        result = await self.api.request("uploadTheme", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Document(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def create_theme(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        slug: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
        document: typing.Optional['InputDocument'] = None,
        settings: typing.Optional[typing.List['InputThemeSettings']] = None,
        **other
    ) -> Result['Theme', APIError]:
        result = await self.api.request("createTheme", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Theme(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def update_theme(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        format: typing.Optional[str] = None,
        theme: typing.Optional['InputTheme'] = None,
        slug: typing.Optional[str] = None,
        title: typing.Optional[str] = None,
        document: typing.Optional['InputDocument'] = None,
        settings: typing.Optional[typing.List['InputThemeSettings']] = None,
        **other
    ) -> Result['Theme', APIError]:
        result = await self.api.request("updateTheme", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Theme(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_theme(
        self,
        theme: typing.Optional['InputTheme'] = None,
        unsave: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveTheme", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def install_theme(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        dark: typing.Optional[bool] = None,
        theme: typing.Optional['InputTheme'] = None,
        format: typing.Optional[str] = None,
        base_theme: typing.Optional['BaseTheme'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("installTheme", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_theme(
        self,
        format: typing.Optional[str] = None,
        theme: typing.Optional['InputTheme'] = None,
        document_id: typing.Optional[int] = None,
        **other
    ) -> Result['Theme', APIError]:
        result = await self.api.request("getTheme", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Theme(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_themes(
        self,
        format: typing.Optional[str] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Themes', APIError]:
        result = await self.api.request("getThemes", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Themes(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def export_login_token(
        self,
        api_id: typing.Optional[int] = None,
        api_hash: typing.Optional[str] = None,
        except_ids: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['LoginToken', APIError]:
        result = await self.api.request("exportLoginToken", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=LoginToken(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def import_login_token(
        self,
        token: typing.Optional[bytes] = None,
        **other
    ) -> Result['LoginToken', APIError]:
        result = await self.api.request("importLoginToken", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=LoginToken(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def accept_login_token(
        self,
        token: typing.Optional[bytes] = None,
        **other
    ) -> Result['Authorization', APIError]:
        result = await self.api.request("acceptLoginToken", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Authorization(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_content_settings(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        sensitive_enabled: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setContentSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_content_settings(
        self,
        **other
    ) -> Result['ContentSettings', APIError]:
        result = await self.api.request("getContentSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ContentSettings(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_inactive_channels(
        self,
        **other
    ) -> Result['InactiveChats', APIError]:
        result = await self.api.request("getInactiveChannels", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=InactiveChats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_multi_wall_papers(
        self,
        wallpapers: typing.Optional[typing.List['InputWallPaper']] = None,
        **other
    ) -> Result[typing.List['WallPaper'], APIError]:
        result = await self.api.request("getMultiWallPapers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_poll_votes(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[int] = None,
        option: typing.Optional[bytes] = None,
        offset: typing.Optional[str] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['VotesList', APIError]:
        result = await self.api.request("getPollVotes", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=VotesList(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def toggle_sticker_sets(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        uninstall: typing.Optional[bool] = None,
        archive: typing.Optional[bool] = None,
        unarchive: typing.Optional[bool] = None,
        stickersets: typing.Optional[typing.List['InputStickerSet']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("toggleStickerSets", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_bank_card_data(
        self,
        number: typing.Optional[str] = None,
        **other
    ) -> Result['BankCardData', APIError]:
        result = await self.api.request("getBankCardData", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=BankCardData(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_dialog_filters(
        self,
        **other
    ) -> Result[typing.List['DialogFilter'], APIError]:
        result = await self.api.request("getDialogFilters", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_suggested_dialog_filters(
        self,
        **other
    ) -> Result[typing.List['DialogFilterSuggested'], APIError]:
        result = await self.api.request("getSuggestedDialogFilters", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def update_dialog_filter(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        id: typing.Optional[int] = None,
        filter: typing.Optional['DialogFilter'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("updateDialogFilter", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def update_dialog_filters_order(
        self,
        order: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("updateDialogFiltersOrder", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_broadcast_stats(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        dark: typing.Optional[bool] = None,
        channel: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result['BroadcastStats', APIError]:
        result = await self.api.request("getBroadcastStats", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=BroadcastStats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def load_async_graph(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        token: typing.Optional[str] = None,
        x: typing.Optional[int] = None,
        **other
    ) -> Result['StatsGraph', APIError]:
        result = await self.api.request("loadAsyncGraph", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StatsGraph(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_sticker_set_thumb(
        self,
        stickerset: typing.Optional['InputStickerSet'] = None,
        thumb: typing.Optional['InputDocument'] = None,
        **other
    ) -> Result['StickerSet', APIError]:
        result = await self.api.request("setStickerSetThumb", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=StickerSet(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_bot_commands(
        self,
        scope: typing.Optional['BotCommandScope'] = None,
        lang_code: typing.Optional[str] = None,
        commands: typing.Optional[typing.List['BotCommand']] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setBotCommands", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_old_featured_stickers(
        self,
        offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['FeaturedStickers', APIError]:
        result = await self.api.request("getOldFeaturedStickers", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=FeaturedStickers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_promo_data(
        self,
        **other
    ) -> Result['PromoData', APIError]:
        result = await self.api.request("getPromoData", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=PromoData(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def hide_promo_data(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("hidePromoData", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def send_signaling_data(
        self,
        peer: typing.Optional['InputPhoneCall'] = None,
        data: typing.Optional[bytes] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("sendSignalingData", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_megagroup_stats(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        dark: typing.Optional[bool] = None,
        channel: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result['MegagroupStats', APIError]:
        result = await self.api.request("getMegagroupStats", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MegagroupStats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_global_privacy_settings(
        self,
        **other
    ) -> Result['GlobalPrivacySettings', APIError]:
        result = await self.api.request("getGlobalPrivacySettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=GlobalPrivacySettings(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_global_privacy_settings(
        self,
        settings: typing.Optional['GlobalPrivacySettings'] = None,
        **other
    ) -> Result['GlobalPrivacySettings', APIError]:
        result = await self.api.request("setGlobalPrivacySettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=GlobalPrivacySettings(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def dismiss_suggestion(
        self,
        peer: typing.Optional['InputPeer'] = None,
        suggestion: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("dismissSuggestion", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_countries_list(
        self,
        lang_code: typing.Optional[str] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['CountriesList', APIError]:
        result = await self.api.request("getCountriesList", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=CountriesList(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_replies(
        self,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        offset_id: typing.Optional[int] = None,
        offset_date: typing.Optional[int] = None,
        add_offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        max_id: typing.Optional[int] = None,
        min_id: typing.Optional[int] = None,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getReplies", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_discussion_message(
        self,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        **other
    ) -> Result['DiscussionMessage', APIError]:
        result = await self.api.request("getDiscussionMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=DiscussionMessage(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def read_discussion(
        self,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        read_max_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("readDiscussion", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def block_from_replies(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        delete_message: typing.Optional[bool] = None,
        delete_history: typing.Optional[bool] = None,
        report_spam: typing.Optional[bool] = None,
        msg_id: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("blockFromReplies", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_message_public_forwards(
        self,
        channel: typing.Optional['InputChannel'] = None,
        msg_id: typing.Optional[int] = None,
        offset_rate: typing.Optional[int] = None,
        offset_peer: typing.Optional['InputPeer'] = None,
        offset_id: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getMessagePublicForwards", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_message_stats(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        dark: typing.Optional[bool] = None,
        channel: typing.Optional['InputChannel'] = None,
        msg_id: typing.Optional[int] = None,
        **other
    ) -> Result['MessageStats', APIError]:
        result = await self.api.request("getMessageStats", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MessageStats(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def unpin_all_messages(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['AffectedHistory', APIError]:
        result = await self.api.request("unpinAllMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedHistory(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def create_group_call(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        rtmp_stream: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        random_id: typing.Optional[int] = None,
        title: typing.Optional[str] = None,
        schedule_date: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("createGroupCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def join_group_call(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        muted: typing.Optional[bool] = None,
        video_stopped: typing.Optional[bool] = None,
        call: typing.Optional['InputGroupCall'] = None,
        join_as: typing.Optional['InputPeer'] = None,
        invite_hash: typing.Optional[str] = None,
        params: typing.Optional['DataJSON'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("joinGroupCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def leave_group_call(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        source: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("leaveGroupCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def invite_to_group_call(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        users: typing.Optional[typing.List['InputUser']] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("inviteToGroupCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def discard_group_call(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("discardGroupCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def toggle_group_call_settings(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        reset_invite_hash: typing.Optional[bool] = None,
        call: typing.Optional['InputGroupCall'] = None,
        join_muted: typing.Optional[bool] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("toggleGroupCallSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_group_call(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['GroupCall', APIError]:
        result = await self.api.request("getGroupCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=GroupCall(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_group_participants(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        ids: typing.Optional[typing.List['InputPeer']] = None,
        sources: typing.Optional[typing.List[int]] = None,
        offset: typing.Optional[str] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['GroupParticipants', APIError]:
        result = await self.api.request("getGroupParticipants", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=GroupParticipants(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def check_group_call(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        sources: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result[typing.List[int], APIError]:
        result = await self.api.request("checkGroupCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_chat(
        self,
        chat_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteChat", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_phone_call_history(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        revoke: typing.Optional[bool] = None,
        **other
    ) -> Result['AffectedFoundMessages', APIError]:
        result = await self.api.request("deletePhoneCallHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedFoundMessages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def check_history_import(
        self,
        import_head: typing.Optional[str] = None,
        **other
    ) -> Result['HistoryImportParsed', APIError]:
        result = await self.api.request("checkHistoryImport", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=HistoryImportParsed(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def init_history_import(
        self,
        peer: typing.Optional['InputPeer'] = None,
        file: typing.Optional['InputFile'] = None,
        media_count: typing.Optional[int] = None,
        **other
    ) -> Result['HistoryImport', APIError]:
        result = await self.api.request("initHistoryImport", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=HistoryImport(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def upload_imported_media(
        self,
        peer: typing.Optional['InputPeer'] = None,
        import_id: typing.Optional[int] = None,
        file_name: typing.Optional[str] = None,
        media: typing.Optional['InputMedia'] = None,
        **other
    ) -> Result['MessageMedia', APIError]:
        result = await self.api.request("uploadImportedMedia", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MessageMedia(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def start_history_import(
        self,
        peer: typing.Optional['InputPeer'] = None,
        import_id: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("startHistoryImport", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_exported_chat_invites(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        revoked: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        admin_id: typing.Optional['InputUser'] = None,
        offset_date: typing.Optional[int] = None,
        offset_link: typing.Optional[str] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['ExportedChatInvites', APIError]:
        result = await self.api.request("getExportedChatInvites", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ExportedChatInvites(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_exported_chat_invite(
        self,
        peer: typing.Optional['InputPeer'] = None,
        link: typing.Optional[str] = None,
        **other
    ) -> Result['ExportedChatInvite', APIError]:
        result = await self.api.request("getExportedChatInvite", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ExportedChatInvite(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_exported_chat_invite(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        revoked: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        link: typing.Optional[str] = None,
        expire_date: typing.Optional[int] = None,
        usage_limit: typing.Optional[int] = None,
        request_needed: typing.Optional[bool] = None,
        title: typing.Optional[str] = None,
        **other
    ) -> Result['ExportedChatInvite', APIError]:
        result = await self.api.request("editExportedChatInvite", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ExportedChatInvite(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def delete_revoked_exported_chat_invites(
        self,
        peer: typing.Optional['InputPeer'] = None,
        admin_id: typing.Optional['InputUser'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteRevokedExportedChatInvites", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_exported_chat_invite(
        self,
        peer: typing.Optional['InputPeer'] = None,
        link: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("deleteExportedChatInvite", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_admins_with_invites(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['ChatAdminsWithInvites', APIError]:
        result = await self.api.request("getAdminsWithInvites", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChatAdminsWithInvites(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_chat_invite_importers(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        requested: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        link: typing.Optional[str] = None,
        q: typing.Optional[str] = None,
        offset_date: typing.Optional[int] = None,
        offset_user: typing.Optional['InputUser'] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['ChatInviteImporters', APIError]:
        result = await self.api.request("getChatInviteImporters", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ChatInviteImporters(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_history_t_t_l(
        self,
        peer: typing.Optional['InputPeer'] = None,
        period: typing.Optional[int] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("setHistoryTTL", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def report_profile_photo(
        self,
        peer: typing.Optional['InputPeer'] = None,
        photo_id: typing.Optional['InputPhoto'] = None,
        reason: typing.Optional['ReportReason'] = None,
        message: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("reportProfilePhoto", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def convert_to_gigagroup(
        self,
        channel: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("convertToGigagroup", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def check_history_import_peer(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['CheckedHistoryImportPeer', APIError]:
        result = await self.api.request("checkHistoryImportPeer", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=CheckedHistoryImportPeer(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def toggle_group_call_record(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        start: typing.Optional[bool] = None,
        video: typing.Optional[bool] = None,
        call: typing.Optional['InputGroupCall'] = None,
        title: typing.Optional[str] = None,
        video_portrait: typing.Optional[bool] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("toggleGroupCallRecord", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_group_call_participant(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        call: typing.Optional['InputGroupCall'] = None,
        participant: typing.Optional['InputPeer'] = None,
        muted: typing.Optional[bool] = None,
        volume: typing.Optional[int] = None,
        raise_hand: typing.Optional[bool] = None,
        video_stopped: typing.Optional[bool] = None,
        video_paused: typing.Optional[bool] = None,
        presentation_paused: typing.Optional[bool] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editGroupCallParticipant", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def edit_group_call_title(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        title: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("editGroupCallTitle", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_group_call_join_as(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['JoinAsPeers', APIError]:
        result = await self.api.request("getGroupCallJoinAs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=JoinAsPeers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def export_group_call_invite(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        can_self_unmute: typing.Optional[bool] = None,
        call: typing.Optional['InputGroupCall'] = None,
        **other
    ) -> Result['ExportedGroupCallInvite', APIError]:
        result = await self.api.request("exportGroupCallInvite", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ExportedGroupCallInvite(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def toggle_group_call_start_subscription(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        subscribed: typing.Optional[bool] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("toggleGroupCallStartSubscription", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def start_scheduled_group_call(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("startScheduledGroupCall", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_default_group_call_join_as(
        self,
        peer: typing.Optional['InputPeer'] = None,
        join_as: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveDefaultGroupCallJoinAs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def join_group_call_presentation(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        params: typing.Optional['DataJSON'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("joinGroupCallPresentation", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def leave_group_call_presentation(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("leaveGroupCallPresentation", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def check_short_name(
        self,
        short_name: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("checkShortName", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def suggest_short_name(
        self,
        title: typing.Optional[str] = None,
        **other
    ) -> Result['SuggestedShortName', APIError]:
        result = await self.api.request("suggestShortName", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SuggestedShortName(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def reset_bot_commands(
        self,
        scope: typing.Optional['BotCommandScope'] = None,
        lang_code: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("resetBotCommands", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_bot_commands(
        self,
        scope: typing.Optional['BotCommandScope'] = None,
        lang_code: typing.Optional[str] = None,
        **other
    ) -> Result[typing.List['BotCommand'], APIError]:
        result = await self.api.request("getBotCommands", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def reset_password(
        self,
        **other
    ) -> Result['ResetPasswordResult', APIError]:
        result = await self.api.request("resetPassword", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ResetPasswordResult(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def decline_password_reset(
        self,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("declinePasswordReset", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def check_recovery_password(
        self,
        code: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("checkRecoveryPassword", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_chat_themes(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['Themes', APIError]:
        result = await self.api.request("getChatThemes", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Themes(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_chat_theme(
        self,
        peer: typing.Optional['InputPeer'] = None,
        emoticon: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("setChatTheme", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def view_sponsored_message(
        self,
        channel: typing.Optional['InputChannel'] = None,
        random_id: typing.Optional[bytes] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("viewSponsoredMessage", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_sponsored_messages(
        self,
        channel: typing.Optional['InputChannel'] = None,
        **other
    ) -> Result['SponsoredMessages', APIError]:
        result = await self.api.request("getSponsoredMessages", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SponsoredMessages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_message_read_participants(
        self,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        **other
    ) -> Result[typing.List[int], APIError]:
        result = await self.api.request("getMessageReadParticipants", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_search_results_calendar(
        self,
        peer: typing.Optional['InputPeer'] = None,
        filter: typing.Optional['MessagesFilter'] = None,
        offset_id: typing.Optional[int] = None,
        offset_date: typing.Optional[int] = None,
        **other
    ) -> Result['SearchResultsCalendar', APIError]:
        result = await self.api.request("getSearchResultsCalendar", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SearchResultsCalendar(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_search_results_positions(
        self,
        peer: typing.Optional['InputPeer'] = None,
        filter: typing.Optional['MessagesFilter'] = None,
        offset_id: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['SearchResultsPositions', APIError]:
        result = await self.api.request("getSearchResultsPositions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SearchResultsPositions(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def hide_chat_join_request(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        approved: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        user_id: typing.Optional['InputUser'] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("hideChatJoinRequest", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def hide_all_chat_join_requests(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        approved: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        link: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("hideAllChatJoinRequests", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def toggle_no_forwards(
        self,
        peer: typing.Optional['InputPeer'] = None,
        enabled: typing.Optional[bool] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("toggleNoForwards", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def save_default_send_as(
        self,
        peer: typing.Optional['InputPeer'] = None,
        send_as: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("saveDefaultSendAs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def get_send_as(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['SendAsPeers', APIError]:
        result = await self.api.request("getSendAs", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=SendAsPeers(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_authorization_t_t_l(
        self,
        authorization_ttl_days: typing.Optional[int] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setAuthorizationTTL", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def change_authorization_settings(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        hash: typing.Optional[int] = None,
        encrypted_requests_disabled: typing.Optional[bool] = None,
        call_requests_disabled: typing.Optional[bool] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("changeAuthorizationSettings", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def delete_participant_history(
        self,
        channel: typing.Optional['InputChannel'] = None,
        participant: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['AffectedHistory', APIError]:
        result = await self.api.request("deleteParticipantHistory", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedHistory(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def send_reaction(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        big: typing.Optional[bool] = None,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        reaction: typing.Optional[str] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("sendReaction", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_messages_reactions(
        self,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[typing.List[int]] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("getMessagesReactions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_message_reactions_list(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        peer: typing.Optional['InputPeer'] = None,
        id: typing.Optional[int] = None,
        reaction: typing.Optional[str] = None,
        offset: typing.Optional[str] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['MessageReactionsList', APIError]:
        result = await self.api.request("getMessageReactionsList", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=MessageReactionsList(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_chat_available_reactions(
        self,
        peer: typing.Optional['InputPeer'] = None,
        available_reactions: typing.Optional[typing.List[str]] = None,
        **other
    ) -> Result['Updates', APIError]:
        result = await self.api.request("setChatAvailableReactions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Updates(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_available_reactions(
        self,
        hash: typing.Optional[int] = None,
        **other
    ) -> Result['AvailableReactions', APIError]:
        result = await self.api.request("getAvailableReactions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AvailableReactions(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def set_default_reaction(
        self,
        reaction: typing.Optional[str] = None,
        **other
    ) -> Result[bool, APIError]:
        result = await self.api.request("setDefaultReaction", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=result.unwrap())
        return Result(False, error=result.error)

    async def translate_text(
        self,
        flags: typing.Optional[typing.List[str]] = None,
        peer: typing.Optional['InputPeer'] = None,
        msg_id: typing.Optional[int] = None,
        text: typing.Optional[str] = None,
        from_lang: typing.Optional[str] = None,
        to_lang: typing.Optional[str] = None,
        **other
    ) -> Result['TranslatedText', APIError]:
        result = await self.api.request("translateText", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=TranslatedText(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_unread_reactions(
        self,
        peer: typing.Optional['InputPeer'] = None,
        offset_id: typing.Optional[int] = None,
        add_offset: typing.Optional[int] = None,
        limit: typing.Optional[int] = None,
        max_id: typing.Optional[int] = None,
        min_id: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("getUnreadReactions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def read_reactions(
        self,
        peer: typing.Optional['InputPeer'] = None,
        **other
    ) -> Result['AffectedHistory', APIError]:
        result = await self.api.request("readReactions", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=AffectedHistory(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def resolve_phone(
        self,
        phone: typing.Optional[str] = None,
        **other
    ) -> Result['ResolvedPeer', APIError]:
        result = await self.api.request("resolvePhone", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=ResolvedPeer(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_group_call_stream_channels(
        self,
        call: typing.Optional['InputGroupCall'] = None,
        **other
    ) -> Result['GroupCallStreamChannels', APIError]:
        result = await self.api.request("getGroupCallStreamChannels", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=GroupCallStreamChannels(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def get_group_call_stream_rtmp_url(
        self,
        peer: typing.Optional['InputPeer'] = None,
        revoke: typing.Optional[bool] = None,
        **other
    ) -> Result['GroupCallStreamRtmpUrl', APIError]:
        result = await self.api.request("getGroupCallStreamRtmpUrl", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=GroupCallStreamRtmpUrl(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)

    async def search_sent_media(
        self,
        q: typing.Optional[str] = None,
        filter: typing.Optional['MessagesFilter'] = None,
        limit: typing.Optional[int] = None,
        **other
    ) -> Result['Messages', APIError]:
        result = await self.api.request("searchSentMedia", self.get_params(locals()))
        if result.is_ok:
            return Result(True, value=Messages(**self.get_response(result.unwrap())))
        return Result(False, error=result.error)