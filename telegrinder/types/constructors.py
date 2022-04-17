import typing
import inspect
from pydantic import BaseModel


class InputPeer(BaseModel):
    chat_id: typing.Optional[int] = None
    user_id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    channel_id: typing.Optional[int] = None
    peer: typing.Optional['InputPeer'] = None
    msg_id: typing.Optional[int] = None


class InputUser(BaseModel):
    user_id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    peer: typing.Optional['InputPeer'] = None
    msg_id: typing.Optional[int] = None


class InputContact(BaseModel):
    client_id: typing.Optional[int] = None
    phone: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None


class InputFile(BaseModel):
    id: typing.Optional[int] = None
    parts: typing.Optional[int] = None
    name: typing.Optional[str] = None
    md5_checksum: typing.Optional[str] = None


class InputMedia(BaseModel):
    file: typing.Optional['InputFile'] = None
    stickers: typing.Optional[typing.List['InputDocument']] = None
    ttl_seconds: typing.Optional[int] = None
    id: typing.Optional['InputPhoto'] = None
    geo_point: typing.Optional['InputGeoPoint'] = None
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    nosound_video: typing.Optional[bool] = None
    force_file: typing.Optional[bool] = None
    thumb: typing.Optional['InputFile'] = None
    mime_type: typing.Optional[str] = None
    attributes: typing.Optional[typing.List['DocumentAttribute']] = None
    query: typing.Optional[str] = None
    title: typing.Optional[str] = None
    address: typing.Optional[str] = None
    provider: typing.Optional[str] = None
    venue_id: typing.Optional[str] = None
    venue_type: typing.Optional[str] = None
    url: typing.Optional[str] = None
    description: typing.Optional[str] = None
    photo: typing.Optional['InputWebDocument'] = None
    invoice: typing.Optional['Invoice'] = None
    payload: typing.Optional[bytes] = None
    provider_data: typing.Optional['DataJSON'] = None
    start_param: typing.Optional[str] = None
    stopped: typing.Optional[bool] = None
    heading: typing.Optional[int] = None
    period: typing.Optional[int] = None
    proximity_notification_radius: typing.Optional[int] = None
    poll: typing.Optional['Poll'] = None
    correct_answers: typing.Optional[typing.List[bytes]] = None
    solution: typing.Optional[str] = None
    solution_entities: typing.Optional[typing.List['MessageEntity']] = None
    emoticon: typing.Optional[str] = None


class InputChatPhoto(BaseModel):
    file: typing.Optional['InputFile'] = None
    video: typing.Optional['InputFile'] = None
    video_start_ts: typing.Optional[float] = None
    id: typing.Optional['InputPhoto'] = None


class InputGeoPoint(BaseModel):
    lat: typing.Optional[float] = None
    long: typing.Optional[float] = None
    accuracy_radius: typing.Optional[int] = None


class InputPhoto(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    file_reference: typing.Optional[bytes] = None


class InputFileLocation(BaseModel):
    volume_id: typing.Optional[int] = None
    local_id: typing.Optional[int] = None
    secret: typing.Optional[int] = None
    file_reference: typing.Optional[bytes] = None
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    thumb_size: typing.Optional[str] = None
    big: typing.Optional[bool] = None
    peer: typing.Optional['InputPeer'] = None
    photo_id: typing.Optional[int] = None
    stickerset: typing.Optional['InputStickerSet'] = None
    thumb_version: typing.Optional[int] = None
    call: typing.Optional['InputGroupCall'] = None
    time_ms: typing.Optional[int] = None
    scale: typing.Optional[int] = None
    video_channel: typing.Optional[int] = None
    video_quality: typing.Optional[int] = None


class Peer(BaseModel):
    user_id: typing.Optional[int] = None
    chat_id: typing.Optional[int] = None
    channel_id: typing.Optional[int] = None


class FileType(BaseModel):
    pass


class User(BaseModel):
    id: typing.Optional[int] = None
    self: typing.Optional[bool] = None
    contact: typing.Optional[bool] = None
    mutual_contact: typing.Optional[bool] = None
    deleted: typing.Optional[bool] = None
    bot: typing.Optional[bool] = None
    bot_chat_history: typing.Optional[bool] = None
    bot_nochats: typing.Optional[bool] = None
    verified: typing.Optional[bool] = None
    restricted: typing.Optional[bool] = None
    min: typing.Optional[bool] = None
    bot_inline_geo: typing.Optional[bool] = None
    support: typing.Optional[bool] = None
    scam: typing.Optional[bool] = None
    apply_min_photo: typing.Optional[bool] = None
    fake: typing.Optional[bool] = None
    access_hash: typing.Optional[int] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    username: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    photo: typing.Optional['UserProfilePhoto'] = None
    status: typing.Optional['UserStatus'] = None
    bot_info_version: typing.Optional[int] = None
    restriction_reason: typing.Optional[typing.List['RestrictionReason']] = None
    bot_inline_placeholder: typing.Optional[str] = None
    lang_code: typing.Optional[str] = None


class UserProfilePhoto(BaseModel):
    has_video: typing.Optional[bool] = None
    photo_id: typing.Optional[int] = None
    stripped_thumb: typing.Optional[bytes] = None
    dc_id: typing.Optional[int] = None


class UserStatus(BaseModel):
    expires: typing.Optional[int] = None
    was_online: typing.Optional[int] = None


class Chat(BaseModel):
    id: typing.Optional[int] = None
    creator: typing.Optional[bool] = None
    left: typing.Optional[bool] = None
    deactivated: typing.Optional[bool] = None
    call_active: typing.Optional[bool] = None
    call_not_empty: typing.Optional[bool] = None
    noforwards: typing.Optional[bool] = None
    title: typing.Optional[str] = None
    photo: typing.Optional['ChatPhoto'] = None
    participants_count: typing.Optional[int] = None
    date: typing.Optional[int] = None
    version: typing.Optional[int] = None
    migrated_to: typing.Optional['InputChannel'] = None
    admin_rights: typing.Optional['ChatAdminRights'] = None
    default_banned_rights: typing.Optional['ChatBannedRights'] = None
    broadcast: typing.Optional[bool] = None
    verified: typing.Optional[bool] = None
    megagroup: typing.Optional[bool] = None
    restricted: typing.Optional[bool] = None
    signatures: typing.Optional[bool] = None
    min: typing.Optional[bool] = None
    scam: typing.Optional[bool] = None
    has_link: typing.Optional[bool] = None
    has_geo: typing.Optional[bool] = None
    slowmode_enabled: typing.Optional[bool] = None
    fake: typing.Optional[bool] = None
    gigagroup: typing.Optional[bool] = None
    join_to_send: typing.Optional[bool] = None
    join_request: typing.Optional[bool] = None
    access_hash: typing.Optional[int] = None
    username: typing.Optional[str] = None
    restriction_reason: typing.Optional[typing.List['RestrictionReason']] = None
    banned_rights: typing.Optional['ChatBannedRights'] = None
    until_date: typing.Optional[int] = None


class ChatFull(BaseModel):
    can_set_username: typing.Optional[bool] = None
    has_scheduled: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    about: typing.Optional[str] = None
    participants: typing.Optional['ChatParticipants'] = None
    chat_photo: typing.Optional['Photo'] = None
    notify_settings: typing.Optional['PeerNotifySettings'] = None
    exported_invite: typing.Optional['ExportedChatInvite'] = None
    bot_info: typing.Optional[typing.List['BotInfo']] = None
    pinned_msg_id: typing.Optional[int] = None
    folder_id: typing.Optional[int] = None
    call: typing.Optional['InputGroupCall'] = None
    ttl_period: typing.Optional[int] = None
    groupcall_default_join_as: typing.Optional['Peer'] = None
    theme_emoticon: typing.Optional[str] = None
    requests_pending: typing.Optional[int] = None
    recent_requesters: typing.Optional[typing.List[int]] = None
    available_reactions: typing.Optional[typing.List[str]] = None
    full_chat: typing.Optional['ChatFull'] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    can_view_participants: typing.Optional[bool] = None
    can_set_stickers: typing.Optional[bool] = None
    hidden_prehistory: typing.Optional[bool] = None
    can_set_location: typing.Optional[bool] = None
    can_view_stats: typing.Optional[bool] = None
    blocked: typing.Optional[bool] = None
    participants_count: typing.Optional[int] = None
    admins_count: typing.Optional[int] = None
    kicked_count: typing.Optional[int] = None
    banned_count: typing.Optional[int] = None
    online_count: typing.Optional[int] = None
    read_inbox_max_id: typing.Optional[int] = None
    read_outbox_max_id: typing.Optional[int] = None
    unread_count: typing.Optional[int] = None
    migrated_from_chat_id: typing.Optional[int] = None
    migrated_from_max_id: typing.Optional[int] = None
    stickerset: typing.Optional['StickerSet'] = None
    available_min_id: typing.Optional[int] = None
    linked_chat_id: typing.Optional[int] = None
    location: typing.Optional['ChannelLocation'] = None
    slowmode_seconds: typing.Optional[int] = None
    slowmode_next_send_date: typing.Optional[int] = None
    stats_dc: typing.Optional[int] = None
    pts: typing.Optional[int] = None
    pending_suggestions: typing.Optional[typing.List[str]] = None
    default_send_as: typing.Optional['Peer'] = None


class ChatParticipant(BaseModel):
    user_id: typing.Optional[int] = None
    inviter_id: typing.Optional[int] = None
    date: typing.Optional[int] = None


class ChatParticipants(BaseModel):
    chat_id: typing.Optional[int] = None
    self_participant: typing.Optional['ChatParticipant'] = None
    participants: typing.Optional[typing.List['ChatParticipant']] = None
    version: typing.Optional[int] = None


class ChatPhoto(BaseModel):
    has_video: typing.Optional[bool] = None
    photo_id: typing.Optional[int] = None
    stripped_thumb: typing.Optional[bytes] = None
    dc_id: typing.Optional[int] = None


class Message(BaseModel):
    id: typing.Optional[int] = None
    peer_id: typing.Optional['Peer'] = None
    out: typing.Optional[bool] = None
    mentioned: typing.Optional[bool] = None
    media_unread: typing.Optional[bool] = None
    silent: typing.Optional[bool] = None
    post: typing.Optional[bool] = None
    from_scheduled: typing.Optional[bool] = None
    legacy: typing.Optional[bool] = None
    edit_hide: typing.Optional[bool] = None
    pinned: typing.Optional[bool] = None
    noforwards: typing.Optional[bool] = None
    from_id: typing.Optional['Peer'] = None
    fwd_from: typing.Optional['MessageFwdHeader'] = None
    via_bot_id: typing.Optional[int] = None
    reply_to: typing.Optional['MessageReplyHeader'] = None
    date: typing.Optional[int] = None
    message: typing.Optional[str] = None
    media: typing.Optional['MessageMedia'] = None
    reply_markup: typing.Optional['ReplyMarkup'] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None
    views: typing.Optional[int] = None
    forwards: typing.Optional[int] = None
    replies: typing.Optional['MessageReplies'] = None
    edit_date: typing.Optional[int] = None
    post_author: typing.Optional[str] = None
    grouped_id: typing.Optional[int] = None
    reactions: typing.Optional['MessageReactions'] = None
    restriction_reason: typing.Optional[typing.List['RestrictionReason']] = None
    ttl_period: typing.Optional[int] = None
    action: typing.Optional['MessageAction'] = None


class MessageMedia(BaseModel):
    photo: typing.Optional['Photo'] = None
    ttl_seconds: typing.Optional[int] = None
    geo: typing.Optional['GeoPoint'] = None
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    user_id: typing.Optional[int] = None
    document: typing.Optional['Document'] = None
    webpage: typing.Optional['WebPage'] = None
    title: typing.Optional[str] = None
    address: typing.Optional[str] = None
    provider: typing.Optional[str] = None
    venue_id: typing.Optional[str] = None
    venue_type: typing.Optional[str] = None
    game: typing.Optional['Game'] = None
    shipping_address_requested: typing.Optional[bool] = None
    test: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    receipt_msg_id: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    total_amount: typing.Optional[int] = None
    start_param: typing.Optional[str] = None
    heading: typing.Optional[int] = None
    period: typing.Optional[int] = None
    proximity_notification_radius: typing.Optional[int] = None
    poll: typing.Optional['Poll'] = None
    results: typing.Optional['PollResults'] = None
    value: typing.Optional[int] = None
    emoticon: typing.Optional[str] = None


class MessageAction(BaseModel):
    title: typing.Optional[str] = None
    users: typing.Optional[typing.List[int]] = None
    photo: typing.Optional['Photo'] = None
    user_id: typing.Optional[int] = None
    inviter_id: typing.Optional[int] = None
    channel_id: typing.Optional[int] = None
    chat_id: typing.Optional[int] = None
    game_id: typing.Optional[int] = None
    score: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    total_amount: typing.Optional[int] = None
    payload: typing.Optional[bytes] = None
    info: typing.Optional['PaymentRequestedInfo'] = None
    shipping_option_id: typing.Optional[str] = None
    charge: typing.Optional['PaymentCharge'] = None
    video: typing.Optional[bool] = None
    call_id: typing.Optional[int] = None
    reason: typing.Optional['PhoneCallDiscardReason'] = None
    duration: typing.Optional[int] = None
    message: typing.Optional[str] = None
    domain: typing.Optional[str] = None
    values: typing.Optional[typing.List['SecureValue']] = None
    credentials: typing.Optional['SecureCredentialsEncrypted'] = None
    types: typing.Optional[typing.List['SecureValueType']] = None
    from_id: typing.Optional['Peer'] = None
    to_id: typing.Optional['Peer'] = None
    distance: typing.Optional[int] = None
    call: typing.Optional['InputGroupCall'] = None
    period: typing.Optional[int] = None
    schedule_date: typing.Optional[int] = None
    emoticon: typing.Optional[str] = None


class Dialog(BaseModel):
    pinned: typing.Optional[bool] = None
    unread_mark: typing.Optional[bool] = None
    peer: typing.Optional['Peer'] = None
    top_message: typing.Optional[int] = None
    read_inbox_max_id: typing.Optional[int] = None
    read_outbox_max_id: typing.Optional[int] = None
    unread_count: typing.Optional[int] = None
    unread_mentions_count: typing.Optional[int] = None
    unread_reactions_count: typing.Optional[int] = None
    notify_settings: typing.Optional['PeerNotifySettings'] = None
    pts: typing.Optional[int] = None
    draft: typing.Optional['DraftMessage'] = None
    folder_id: typing.Optional[int] = None
    folder: typing.Optional['Folder'] = None
    unread_muted_peers_count: typing.Optional[int] = None
    unread_unmuted_peers_count: typing.Optional[int] = None
    unread_muted_messages_count: typing.Optional[int] = None
    unread_unmuted_messages_count: typing.Optional[int] = None


class Photo(BaseModel):
    id: typing.Optional[int] = None
    has_stickers: typing.Optional[bool] = None
    access_hash: typing.Optional[int] = None
    file_reference: typing.Optional[bytes] = None
    date: typing.Optional[int] = None
    sizes: typing.Optional[typing.List['PhotoSize']] = None
    video_sizes: typing.Optional[typing.List['VideoSize']] = None
    dc_id: typing.Optional[int] = None
    photo: typing.Optional['Photo'] = None
    users: typing.Optional[typing.List['User']] = None


class PhotoSize(BaseModel):
    type: typing.Optional[str] = None
    w: typing.Optional[int] = None
    h: typing.Optional[int] = None
    size: typing.Optional[int] = None
    bytes: typing.Optional[bytes] = None
    sizes: typing.Optional[typing.List[int]] = None


class GeoPoint(BaseModel):
    long: typing.Optional[float] = None
    lat: typing.Optional[float] = None
    access_hash: typing.Optional[int] = None
    accuracy_radius: typing.Optional[int] = None


class SentCode(BaseModel):
    type: typing.Optional['SentCodeType'] = None
    phone_code_hash: typing.Optional[str] = None
    next_type: typing.Optional['CodeType'] = None
    timeout: typing.Optional[int] = None


class Authorization(BaseModel):
    setup_password_required: typing.Optional[bool] = None
    otherwise_relogin_days: typing.Optional[int] = None
    tmp_sessions: typing.Optional[int] = None
    user: typing.Optional['User'] = None
    current: typing.Optional[bool] = None
    official_app: typing.Optional[bool] = None
    password_pending: typing.Optional[bool] = None
    encrypted_requests_disabled: typing.Optional[bool] = None
    call_requests_disabled: typing.Optional[bool] = None
    hash: typing.Optional[int] = None
    device_model: typing.Optional[str] = None
    platform: typing.Optional[str] = None
    system_version: typing.Optional[str] = None
    api_id: typing.Optional[int] = None
    app_name: typing.Optional[str] = None
    app_version: typing.Optional[str] = None
    date_created: typing.Optional[int] = None
    date_active: typing.Optional[int] = None
    ip: typing.Optional[str] = None
    country: typing.Optional[str] = None
    region: typing.Optional[str] = None
    terms_of_service: typing.Optional['TermsOfService'] = None


class ExportedAuthorization(BaseModel):
    id: typing.Optional[int] = None
    bytes: typing.Optional[bytes] = None


class InputNotifyPeer(BaseModel):
    peer: typing.Optional['InputPeer'] = None


class InputPeerNotifySettings(BaseModel):
    show_previews: typing.Optional[bool] = None
    silent: typing.Optional[bool] = None
    mute_until: typing.Optional[int] = None
    sound: typing.Optional[str] = None


class PeerNotifySettings(BaseModel):
    show_previews: typing.Optional[bool] = None
    silent: typing.Optional[bool] = None
    mute_until: typing.Optional[int] = None
    sound: typing.Optional[str] = None


class PeerSettings(BaseModel):
    report_spam: typing.Optional[bool] = None
    add_contact: typing.Optional[bool] = None
    block_contact: typing.Optional[bool] = None
    share_contact: typing.Optional[bool] = None
    need_contacts_exception: typing.Optional[bool] = None
    report_geo: typing.Optional[bool] = None
    autoarchived: typing.Optional[bool] = None
    invite_members: typing.Optional[bool] = None
    request_chat_broadcast: typing.Optional[bool] = None
    geo_distance: typing.Optional[int] = None
    request_chat_title: typing.Optional[str] = None
    request_chat_date: typing.Optional[int] = None
    settings: typing.Optional['PeerSettings'] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class WallPaper(BaseModel):
    id: typing.Optional[int] = None
    creator: typing.Optional[bool] = None
    default: typing.Optional[bool] = None
    pattern: typing.Optional[bool] = None
    dark: typing.Optional[bool] = None
    access_hash: typing.Optional[int] = None
    slug: typing.Optional[str] = None
    document: typing.Optional['Document'] = None
    settings: typing.Optional['WallPaperSettings'] = None


class ReportReason(BaseModel):
    pass


class UserFull(BaseModel):
    blocked: typing.Optional[bool] = None
    phone_calls_available: typing.Optional[bool] = None
    phone_calls_private: typing.Optional[bool] = None
    can_pin_message: typing.Optional[bool] = None
    has_scheduled: typing.Optional[bool] = None
    video_calls_available: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    about: typing.Optional[str] = None
    settings: typing.Optional['PeerSettings'] = None
    profile_photo: typing.Optional['Photo'] = None
    notify_settings: typing.Optional['PeerNotifySettings'] = None
    bot_info: typing.Optional['BotInfo'] = None
    pinned_msg_id: typing.Optional[int] = None
    common_chats_count: typing.Optional[int] = None
    folder_id: typing.Optional[int] = None
    ttl_period: typing.Optional[int] = None
    theme_emoticon: typing.Optional[str] = None
    private_forward_name: typing.Optional[str] = None
    full_user: typing.Optional['UserFull'] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class Contact(BaseModel):
    user_id: typing.Optional[int] = None
    mutual: typing.Optional[bool] = None


class ImportedContact(BaseModel):
    user_id: typing.Optional[int] = None
    client_id: typing.Optional[int] = None


class ContactStatus(BaseModel):
    user_id: typing.Optional[int] = None
    status: typing.Optional['UserStatus'] = None


class Contacts(BaseModel):
    contacts: typing.Optional[typing.List['Contact']] = None
    saved_count: typing.Optional[int] = None
    users: typing.Optional[typing.List['User']] = None


class ImportedContacts(BaseModel):
    imported: typing.Optional[typing.List['ImportedContact']] = None
    popular_invites: typing.Optional[typing.List['PopularContact']] = None
    retry_contacts: typing.Optional[typing.List[int]] = None
    users: typing.Optional[typing.List['User']] = None


class Blocked(BaseModel):
    blocked: typing.Optional[typing.List['PeerBlocked']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    count: typing.Optional[int] = None


class Dialogs(BaseModel):
    dialogs: typing.Optional[typing.List['Dialog']] = None
    messages: typing.Optional[typing.List['Message']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    count: typing.Optional[int] = None


class Messages(BaseModel):
    messages: typing.Optional[typing.List['Message']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    inexact: typing.Optional[bool] = None
    count: typing.Optional[int] = None
    next_rate: typing.Optional[int] = None
    offset_id_offset: typing.Optional[int] = None
    pts: typing.Optional[int] = None


class Chats(BaseModel):
    chats: typing.Optional[typing.List['Chat']] = None
    count: typing.Optional[int] = None


class AffectedHistory(BaseModel):
    pts: typing.Optional[int] = None
    pts_count: typing.Optional[int] = None
    offset: typing.Optional[int] = None


class MessagesFilter(BaseModel):
    missed: typing.Optional[bool] = None


class Update(BaseModel):
    message: typing.Optional['Message'] = None
    pts: typing.Optional[int] = None
    pts_count: typing.Optional[int] = None
    id: typing.Optional[int] = None
    random_id: typing.Optional[int] = None
    messages: typing.Optional[typing.List[int]] = None
    user_id: typing.Optional[int] = None
    action: typing.Optional['SendMessageAction'] = None
    chat_id: typing.Optional[int] = None
    from_id: typing.Optional['Peer'] = None
    participants: typing.Optional['ChatParticipants'] = None
    status: typing.Optional['UserStatus'] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    username: typing.Optional[str] = None
    date: typing.Optional[int] = None
    photo: typing.Optional['UserProfilePhoto'] = None
    previous: typing.Optional[bool] = None
    qts: typing.Optional[int] = None
    chat: typing.Optional['EncryptedChat'] = None
    max_date: typing.Optional[int] = None
    inviter_id: typing.Optional[int] = None
    version: typing.Optional[int] = None
    dc_options: typing.Optional[typing.List['DcOption']] = None
    peer: typing.Optional['NotifyPeer'] = None
    notify_settings: typing.Optional['PeerNotifySettings'] = None
    popup: typing.Optional[bool] = None
    inbox_date: typing.Optional[int] = None
    type: typing.Optional[str] = None
    media: typing.Optional['MessageMedia'] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None
    key: typing.Optional['PrivacyKey'] = None
    rules: typing.Optional[typing.List['PrivacyRule']] = None
    phone: typing.Optional[str] = None
    folder_id: typing.Optional[int] = None
    max_id: typing.Optional[int] = None
    still_unread_count: typing.Optional[int] = None
    webpage: typing.Optional['WebPage'] = None
    channel_id: typing.Optional[int] = None
    views: typing.Optional[int] = None
    is_admin: typing.Optional[bool] = None
    stickerset: typing.Optional['StickerSet'] = None
    masks: typing.Optional[bool] = None
    order: typing.Optional[typing.List[int]] = None
    query_id: typing.Optional[int] = None
    query: typing.Optional[str] = None
    geo: typing.Optional['GeoPoint'] = None
    peer_type: typing.Optional['InlineQueryPeerType'] = None
    offset: typing.Optional[str] = None
    msg_id: typing.Optional['InputBotInlineMessageID'] = None
    chat_instance: typing.Optional[int] = None
    data: typing.Optional[bytes] = None
    game_short_name: typing.Optional[str] = None
    draft: typing.Optional['DraftMessage'] = None
    pinned: typing.Optional[bool] = None
    timeout: typing.Optional[int] = None
    payload: typing.Optional[bytes] = None
    shipping_address: typing.Optional['PostAddress'] = None
    info: typing.Optional['PaymentRequestedInfo'] = None
    shipping_option_id: typing.Optional[str] = None
    currency: typing.Optional[str] = None
    total_amount: typing.Optional[int] = None
    phone_call: typing.Optional['PhoneCall'] = None
    lang_code: typing.Optional[str] = None
    difference: typing.Optional['LangPackDifference'] = None
    available_min_id: typing.Optional[int] = None
    unread: typing.Optional[bool] = None
    poll_id: typing.Optional[int] = None
    poll: typing.Optional['Poll'] = None
    results: typing.Optional['PollResults'] = None
    default_banned_rights: typing.Optional['ChatBannedRights'] = None
    folder_peers: typing.Optional[typing.List['FolderPeer']] = None
    settings: typing.Optional['PeerSettings'] = None
    peers: typing.Optional[typing.List['PeerLocated']] = None
    theme: typing.Optional['Theme'] = None
    options: typing.Optional[typing.List[bytes]] = None
    filter: typing.Optional['DialogFilter'] = None
    phone_call_id: typing.Optional[int] = None
    forwards: typing.Optional[int] = None
    top_msg_id: typing.Optional[int] = None
    read_max_id: typing.Optional[int] = None
    broadcast_id: typing.Optional[int] = None
    broadcast_post: typing.Optional[int] = None
    peer_id: typing.Optional['Peer'] = None
    blocked: typing.Optional[bool] = None
    call: typing.Optional['InputGroupCall'] = None
    ttl_period: typing.Optional[int] = None
    actor_id: typing.Optional[int] = None
    prev_participant: typing.Optional['ChatParticipant'] = None
    new_participant: typing.Optional['ChatParticipant'] = None
    invite: typing.Optional['ExportedChatInvite'] = None
    stopped: typing.Optional[bool] = None
    presentation: typing.Optional[bool] = None
    params: typing.Optional['DataJSON'] = None
    bot_id: typing.Optional[int] = None
    commands: typing.Optional[typing.List['BotCommand']] = None
    requests_pending: typing.Optional[int] = None
    recent_requesters: typing.Optional[typing.List[int]] = None
    about: typing.Optional[str] = None
    reactions: typing.Optional['MessageReactions'] = None


class State(BaseModel):
    pts: typing.Optional[int] = None
    qts: typing.Optional[int] = None
    date: typing.Optional[int] = None
    seq: typing.Optional[int] = None
    unread_count: typing.Optional[int] = None


class Difference(BaseModel):
    date: typing.Optional[int] = None
    seq: typing.Optional[int] = None
    new_messages: typing.Optional[typing.List['Message']] = None
    new_encrypted_messages: typing.Optional[typing.List['EncryptedMessage']] = None
    other_updates: typing.Optional[typing.List['Update']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    state: typing.Optional['State'] = None
    intermediate_state: typing.Optional['State'] = None
    pts: typing.Optional[int] = None


class Updates(BaseModel):
    out: typing.Optional[bool] = None
    mentioned: typing.Optional[bool] = None
    media_unread: typing.Optional[bool] = None
    silent: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    user_id: typing.Optional[int] = None
    message: typing.Optional[str] = None
    pts: typing.Optional[int] = None
    pts_count: typing.Optional[int] = None
    date: typing.Optional[int] = None
    fwd_from: typing.Optional['MessageFwdHeader'] = None
    via_bot_id: typing.Optional[int] = None
    reply_to: typing.Optional['MessageReplyHeader'] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None
    ttl_period: typing.Optional[int] = None
    from_id: typing.Optional[int] = None
    chat_id: typing.Optional[int] = None
    update: typing.Optional['Update'] = None
    updates: typing.Optional[typing.List['Update']] = None
    users: typing.Optional[typing.List['User']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    seq_start: typing.Optional[int] = None
    seq: typing.Optional[int] = None
    media: typing.Optional['MessageMedia'] = None


class Photos(BaseModel):
    photos: typing.Optional[typing.List['Photo']] = None
    users: typing.Optional[typing.List['User']] = None
    count: typing.Optional[int] = None


class File(BaseModel):
    type: typing.Optional['FileType'] = None
    mtime: typing.Optional[int] = None
    bytes: typing.Optional[bytes] = None
    dc_id: typing.Optional[int] = None
    file_token: typing.Optional[bytes] = None
    encryption_key: typing.Optional[bytes] = None
    encryption_iv: typing.Optional[bytes] = None
    file_hashes: typing.Optional[typing.List['FileHash']] = None


class DcOption(BaseModel):
    ipv6: typing.Optional[bool] = None
    media_only: typing.Optional[bool] = None
    tcpo_only: typing.Optional[bool] = None
    cdn: typing.Optional[bool] = None
    static: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    ip_address: typing.Optional[str] = None
    port: typing.Optional[int] = None
    secret: typing.Optional[bytes] = None


class Config(BaseModel):
    phonecalls_enabled: typing.Optional[bool] = None
    default_p2p_contacts: typing.Optional[bool] = None
    preload_featured_stickers: typing.Optional[bool] = None
    ignore_phone_entities: typing.Optional[bool] = None
    revoke_pm_inbox: typing.Optional[bool] = None
    blocked_mode: typing.Optional[bool] = None
    pfs_enabled: typing.Optional[bool] = None
    date: typing.Optional[int] = None
    expires: typing.Optional[int] = None
    test_mode: typing.Optional[bool] = None
    this_dc: typing.Optional[int] = None
    dc_options: typing.Optional[typing.List['DcOption']] = None
    dc_txt_domain_name: typing.Optional[str] = None
    chat_size_max: typing.Optional[int] = None
    megagroup_size_max: typing.Optional[int] = None
    forwarded_count_max: typing.Optional[int] = None
    online_update_period_ms: typing.Optional[int] = None
    offline_blur_timeout_ms: typing.Optional[int] = None
    offline_idle_timeout_ms: typing.Optional[int] = None
    online_cloud_timeout_ms: typing.Optional[int] = None
    notify_cloud_delay_ms: typing.Optional[int] = None
    notify_default_delay_ms: typing.Optional[int] = None
    push_chat_period_ms: typing.Optional[int] = None
    push_chat_limit: typing.Optional[int] = None
    saved_gifs_limit: typing.Optional[int] = None
    edit_time_limit: typing.Optional[int] = None
    revoke_time_limit: typing.Optional[int] = None
    revoke_pm_time_limit: typing.Optional[int] = None
    rating_e_decay: typing.Optional[int] = None
    stickers_recent_limit: typing.Optional[int] = None
    stickers_faved_limit: typing.Optional[int] = None
    channels_read_media_period: typing.Optional[int] = None
    tmp_sessions: typing.Optional[int] = None
    pinned_dialogs_count_max: typing.Optional[int] = None
    pinned_infolder_count_max: typing.Optional[int] = None
    call_receive_timeout_ms: typing.Optional[int] = None
    call_ring_timeout_ms: typing.Optional[int] = None
    call_connect_timeout_ms: typing.Optional[int] = None
    call_packet_timeout_ms: typing.Optional[int] = None
    me_url_prefix: typing.Optional[str] = None
    autoupdate_url_prefix: typing.Optional[str] = None
    gif_search_username: typing.Optional[str] = None
    venue_search_username: typing.Optional[str] = None
    img_search_username: typing.Optional[str] = None
    static_maps_provider: typing.Optional[str] = None
    caption_length_max: typing.Optional[int] = None
    message_length_max: typing.Optional[int] = None
    webfile_dc_id: typing.Optional[int] = None
    suggested_lang_code: typing.Optional[str] = None
    lang_pack_version: typing.Optional[int] = None
    base_lang_pack_version: typing.Optional[int] = None


class NearestDc(BaseModel):
    country: typing.Optional[str] = None
    this_dc: typing.Optional[int] = None
    nearest_dc: typing.Optional[int] = None


class AppUpdate(BaseModel):
    can_not_skip: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    version: typing.Optional[str] = None
    text: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None
    document: typing.Optional['Document'] = None
    url: typing.Optional[str] = None
    sticker: typing.Optional['Document'] = None


class InviteText(BaseModel):
    message: typing.Optional[str] = None


class EncryptedChat(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    date: typing.Optional[int] = None
    admin_id: typing.Optional[int] = None
    participant_id: typing.Optional[int] = None
    folder_id: typing.Optional[int] = None
    g_a: typing.Optional[bytes] = None
    g_a_or_b: typing.Optional[bytes] = None
    key_fingerprint: typing.Optional[int] = None
    history_deleted: typing.Optional[bool] = None


class InputEncryptedChat(BaseModel):
    chat_id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None


class EncryptedFile(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    size: typing.Optional[int] = None
    dc_id: typing.Optional[int] = None
    key_fingerprint: typing.Optional[int] = None


class InputEncryptedFile(BaseModel):
    id: typing.Optional[int] = None
    parts: typing.Optional[int] = None
    md5_checksum: typing.Optional[str] = None
    key_fingerprint: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None


class EncryptedMessage(BaseModel):
    random_id: typing.Optional[int] = None
    chat_id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    bytes: typing.Optional[bytes] = None
    file: typing.Optional['EncryptedFile'] = None


class DhConfig(BaseModel):
    random: typing.Optional[bytes] = None
    g: typing.Optional[int] = None
    p: typing.Optional[bytes] = None
    version: typing.Optional[int] = None


class SentEncryptedMessage(BaseModel):
    date: typing.Optional[int] = None
    file: typing.Optional['EncryptedFile'] = None


class InputDocument(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    file_reference: typing.Optional[bytes] = None


class Document(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    file_reference: typing.Optional[bytes] = None
    date: typing.Optional[int] = None
    mime_type: typing.Optional[str] = None
    size: typing.Optional[int] = None
    thumbs: typing.Optional[typing.List['PhotoSize']] = None
    video_thumbs: typing.Optional[typing.List['VideoSize']] = None
    dc_id: typing.Optional[int] = None
    attributes: typing.Optional[typing.List['DocumentAttribute']] = None


class Support(BaseModel):
    phone_number: typing.Optional[str] = None
    user: typing.Optional['User'] = None


class NotifyPeer(BaseModel):
    peer: typing.Optional['Peer'] = None


class SendMessageAction(BaseModel):
    progress: typing.Optional[int] = None
    emoticon: typing.Optional[str] = None
    msg_id: typing.Optional[int] = None
    interaction: typing.Optional['DataJSON'] = None


class Found(BaseModel):
    my_results: typing.Optional[typing.List['Peer']] = None
    results: typing.Optional[typing.List['Peer']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class InputPrivacyKey(BaseModel):
    pass


class PrivacyKey(BaseModel):
    pass


class InputPrivacyRule(BaseModel):
    users: typing.Optional[typing.List['InputUser']] = None
    chats: typing.Optional[typing.List[int]] = None


class PrivacyRule(BaseModel):
    users: typing.Optional[typing.List[int]] = None
    chats: typing.Optional[typing.List[int]] = None


class PrivacyRules(BaseModel):
    rules: typing.Optional[typing.List['PrivacyRule']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class AccountDaysTTL(BaseModel):
    days: typing.Optional[int] = None


class DocumentAttribute(BaseModel):
    w: typing.Optional[int] = None
    h: typing.Optional[int] = None
    mask: typing.Optional[bool] = None
    alt: typing.Optional[str] = None
    stickerset: typing.Optional['InputStickerSet'] = None
    mask_coords: typing.Optional['MaskCoords'] = None
    round_message: typing.Optional[bool] = None
    supports_streaming: typing.Optional[bool] = None
    duration: typing.Optional[int] = None
    voice: typing.Optional[bool] = None
    title: typing.Optional[str] = None
    performer: typing.Optional[str] = None
    waveform: typing.Optional[bytes] = None
    file_name: typing.Optional[str] = None


class Stickers(BaseModel):
    hash: typing.Optional[int] = None
    stickers: typing.Optional[typing.List['Document']] = None


class StickerPack(BaseModel):
    emoticon: typing.Optional[str] = None
    documents: typing.Optional[typing.List[int]] = None


class AllStickers(BaseModel):
    hash: typing.Optional[int] = None
    sets: typing.Optional[typing.List['StickerSet']] = None


class AffectedMessages(BaseModel):
    pts: typing.Optional[int] = None
    pts_count: typing.Optional[int] = None


class WebPage(BaseModel):
    id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    url: typing.Optional[str] = None
    display_url: typing.Optional[str] = None
    hash: typing.Optional[int] = None
    type: typing.Optional[str] = None
    site_name: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    photo: typing.Optional['Photo'] = None
    embed_url: typing.Optional[str] = None
    embed_type: typing.Optional[str] = None
    embed_width: typing.Optional[int] = None
    embed_height: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    author: typing.Optional[str] = None
    document: typing.Optional['Document'] = None
    cached_page: typing.Optional['Page'] = None
    attributes: typing.Optional[typing.List['WebPageAttribute']] = None
    cached_page_views: typing.Optional[int] = None


class Authorizations(BaseModel):
    authorization_ttl_days: typing.Optional[int] = None
    authorizations: typing.Optional[typing.List['Authorization']] = None


class Password(BaseModel):
    has_recovery: typing.Optional[bool] = None
    has_secure_values: typing.Optional[bool] = None
    has_password: typing.Optional[bool] = None
    current_algo: typing.Optional['PasswordKdfAlgo'] = None
    srp_B: typing.Optional[bytes] = None
    srp_id: typing.Optional[int] = None
    hint: typing.Optional[str] = None
    email_unconfirmed_pattern: typing.Optional[str] = None
    new_algo: typing.Optional['PasswordKdfAlgo'] = None
    new_secure_algo: typing.Optional['SecurePasswordKdfAlgo'] = None
    secure_random: typing.Optional[bytes] = None
    pending_reset_date: typing.Optional[int] = None


class PasswordSettings(BaseModel):
    email: typing.Optional[str] = None
    secure_settings: typing.Optional['SecureSecretSettings'] = None


class PasswordInputSettings(BaseModel):
    new_algo: typing.Optional['PasswordKdfAlgo'] = None
    new_password_hash: typing.Optional[bytes] = None
    hint: typing.Optional[str] = None
    email: typing.Optional[str] = None
    new_secure_settings: typing.Optional['SecureSecretSettings'] = None


class PasswordRecovery(BaseModel):
    email_pattern: typing.Optional[str] = None


class ReceivedNotifyMessage(BaseModel):
    id: typing.Optional[int] = None


class ExportedChatInvite(BaseModel):
    revoked: typing.Optional[bool] = None
    permanent: typing.Optional[bool] = None
    request_needed: typing.Optional[bool] = None
    link: typing.Optional[str] = None
    admin_id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    start_date: typing.Optional[int] = None
    expire_date: typing.Optional[int] = None
    usage_limit: typing.Optional[int] = None
    usage: typing.Optional[int] = None
    requested: typing.Optional[int] = None
    title: typing.Optional[str] = None
    invite: typing.Optional['ExportedChatInvite'] = None
    users: typing.Optional[typing.List['User']] = None
    new_invite: typing.Optional['ExportedChatInvite'] = None


class ChatInvite(BaseModel):
    chat: typing.Optional['Chat'] = None
    channel: typing.Optional[bool] = None
    broadcast: typing.Optional[bool] = None
    public: typing.Optional[bool] = None
    megagroup: typing.Optional[bool] = None
    request_needed: typing.Optional[bool] = None
    title: typing.Optional[str] = None
    about: typing.Optional[str] = None
    photo: typing.Optional['Photo'] = None
    participants_count: typing.Optional[int] = None
    participants: typing.Optional[typing.List['User']] = None
    expires: typing.Optional[int] = None


class InputStickerSet(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    short_name: typing.Optional[str] = None
    emoticon: typing.Optional[str] = None


class StickerSet(BaseModel):
    archived: typing.Optional[bool] = None
    official: typing.Optional[bool] = None
    masks: typing.Optional[bool] = None
    animated: typing.Optional[bool] = None
    videos: typing.Optional[bool] = None
    installed_date: typing.Optional[int] = None
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    title: typing.Optional[str] = None
    short_name: typing.Optional[str] = None
    thumbs: typing.Optional[typing.List['PhotoSize']] = None
    thumb_dc_id: typing.Optional[int] = None
    thumb_version: typing.Optional[int] = None
    count: typing.Optional[int] = None
    hash: typing.Optional[int] = None
    set: typing.Optional['StickerSet'] = None
    packs: typing.Optional[typing.List['StickerPack']] = None
    documents: typing.Optional[typing.List['Document']] = None


class BotCommand(BaseModel):
    command: typing.Optional[str] = None
    description: typing.Optional[str] = None


class BotInfo(BaseModel):
    user_id: typing.Optional[int] = None
    description: typing.Optional[str] = None
    commands: typing.Optional[typing.List['BotCommand']] = None


class KeyboardButton(BaseModel):
    text: typing.Optional[str] = None
    url: typing.Optional[str] = None
    requires_password: typing.Optional[bool] = None
    data: typing.Optional[bytes] = None
    same_peer: typing.Optional[bool] = None
    query: typing.Optional[str] = None
    fwd_text: typing.Optional[str] = None
    button_id: typing.Optional[int] = None
    request_write_access: typing.Optional[bool] = None
    bot: typing.Optional['InputUser'] = None
    quiz: typing.Optional[bool] = None
    user_id: typing.Optional['InputUser'] = None


class KeyboardButtonRow(BaseModel):
    buttons: typing.Optional[typing.List['KeyboardButton']] = None


class ReplyMarkup(BaseModel):
    selective: typing.Optional[bool] = None
    single_use: typing.Optional[bool] = None
    placeholder: typing.Optional[str] = None
    resize: typing.Optional[bool] = None
    rows: typing.Optional[typing.List['KeyboardButtonRow']] = None


class MessageEntity(BaseModel):
    offset: typing.Optional[int] = None
    length: typing.Optional[int] = None
    language: typing.Optional[str] = None
    url: typing.Optional[str] = None
    user_id: typing.Optional[int] = None


class InputChannel(BaseModel):
    channel_id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    peer: typing.Optional['InputPeer'] = None
    msg_id: typing.Optional[int] = None


class ResolvedPeer(BaseModel):
    peer: typing.Optional['Peer'] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class MessageRange(BaseModel):
    min_id: typing.Optional[int] = None
    max_id: typing.Optional[int] = None


class ChannelDifference(BaseModel):
    final: typing.Optional[bool] = None
    pts: typing.Optional[int] = None
    timeout: typing.Optional[int] = None
    dialog: typing.Optional['Dialog'] = None
    messages: typing.Optional[typing.List['Message']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    new_messages: typing.Optional[typing.List['Message']] = None
    other_updates: typing.Optional[typing.List['Update']] = None


class ChannelMessagesFilter(BaseModel):
    exclude_new_messages: typing.Optional[bool] = None
    ranges: typing.Optional[typing.List['MessageRange']] = None


class ChannelParticipant(BaseModel):
    user_id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    via_request: typing.Optional[bool] = None
    inviter_id: typing.Optional[int] = None
    admin_rights: typing.Optional['ChatAdminRights'] = None
    rank: typing.Optional[str] = None
    participant: typing.Optional['ChannelParticipant'] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    can_edit: typing.Optional[bool] = None
    self: typing.Optional[bool] = None
    promoted_by: typing.Optional[int] = None
    left: typing.Optional[bool] = None
    peer: typing.Optional['Peer'] = None
    kicked_by: typing.Optional[int] = None
    banned_rights: typing.Optional['ChatBannedRights'] = None


class ChannelParticipantsFilter(BaseModel):
    q: typing.Optional[str] = None
    top_msg_id: typing.Optional[int] = None


class ChannelParticipants(BaseModel):
    count: typing.Optional[int] = None
    participants: typing.Optional[typing.List['ChannelParticipant']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class TermsOfService(BaseModel):
    popup: typing.Optional[bool] = None
    id: typing.Optional['DataJSON'] = None
    text: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None
    min_age_confirm: typing.Optional[int] = None


class SavedGifs(BaseModel):
    hash: typing.Optional[int] = None
    gifs: typing.Optional[typing.List['Document']] = None


class InputBotInlineMessage(BaseModel):
    message: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None
    reply_markup: typing.Optional['ReplyMarkup'] = None
    no_webpage: typing.Optional[bool] = None
    geo_point: typing.Optional['InputGeoPoint'] = None
    heading: typing.Optional[int] = None
    period: typing.Optional[int] = None
    proximity_notification_radius: typing.Optional[int] = None
    title: typing.Optional[str] = None
    address: typing.Optional[str] = None
    provider: typing.Optional[str] = None
    venue_id: typing.Optional[str] = None
    venue_type: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    description: typing.Optional[str] = None
    photo: typing.Optional['InputWebDocument'] = None
    invoice: typing.Optional['Invoice'] = None
    payload: typing.Optional[bytes] = None
    provider_data: typing.Optional['DataJSON'] = None


class InputBotInlineResult(BaseModel):
    id: typing.Optional[str] = None
    type: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    url: typing.Optional[str] = None
    thumb: typing.Optional['InputWebDocument'] = None
    content: typing.Optional['InputWebDocument'] = None
    send_message: typing.Optional['InputBotInlineMessage'] = None
    photo: typing.Optional['InputPhoto'] = None
    document: typing.Optional['InputDocument'] = None
    short_name: typing.Optional[str] = None


class BotInlineMessage(BaseModel):
    message: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None
    reply_markup: typing.Optional['ReplyMarkup'] = None
    no_webpage: typing.Optional[bool] = None
    geo: typing.Optional['GeoPoint'] = None
    heading: typing.Optional[int] = None
    period: typing.Optional[int] = None
    proximity_notification_radius: typing.Optional[int] = None
    title: typing.Optional[str] = None
    address: typing.Optional[str] = None
    provider: typing.Optional[str] = None
    venue_id: typing.Optional[str] = None
    venue_type: typing.Optional[str] = None
    phone_number: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    vcard: typing.Optional[str] = None
    shipping_address_requested: typing.Optional[bool] = None
    test: typing.Optional[bool] = None
    description: typing.Optional[str] = None
    photo: typing.Optional['WebDocument'] = None
    currency: typing.Optional[str] = None
    total_amount: typing.Optional[int] = None


class BotInlineResult(BaseModel):
    id: typing.Optional[str] = None
    type: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    url: typing.Optional[str] = None
    thumb: typing.Optional['WebDocument'] = None
    content: typing.Optional['WebDocument'] = None
    send_message: typing.Optional['BotInlineMessage'] = None
    photo: typing.Optional['Photo'] = None
    document: typing.Optional['Document'] = None


class BotResults(BaseModel):
    gallery: typing.Optional[bool] = None
    query_id: typing.Optional[int] = None
    next_offset: typing.Optional[str] = None
    switch_pm: typing.Optional['InlineBotSwitchPM'] = None
    results: typing.Optional[typing.List['BotInlineResult']] = None
    cache_time: typing.Optional[int] = None
    users: typing.Optional[typing.List['User']] = None


class ExportedMessageLink(BaseModel):
    link: typing.Optional[str] = None
    html: typing.Optional[str] = None


class MessageFwdHeader(BaseModel):
    imported: typing.Optional[bool] = None
    from_id: typing.Optional['Peer'] = None
    from_name: typing.Optional[str] = None
    date: typing.Optional[int] = None
    channel_post: typing.Optional[int] = None
    post_author: typing.Optional[str] = None
    saved_from_peer: typing.Optional['Peer'] = None
    saved_from_msg_id: typing.Optional[int] = None
    psa_type: typing.Optional[str] = None


class CodeType(BaseModel):
    pass


class SentCodeType(BaseModel):
    length: typing.Optional[int] = None
    pattern: typing.Optional[str] = None
    prefix: typing.Optional[str] = None


class BotCallbackAnswer(BaseModel):
    alert: typing.Optional[bool] = None
    has_url: typing.Optional[bool] = None
    native_ui: typing.Optional[bool] = None
    message: typing.Optional[str] = None
    url: typing.Optional[str] = None
    cache_time: typing.Optional[int] = None


class MessageEditData(BaseModel):
    caption: typing.Optional[bool] = None


class InputBotInlineMessageID(BaseModel):
    dc_id: typing.Optional[int] = None
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    owner_id: typing.Optional[int] = None


class InlineBotSwitchPM(BaseModel):
    text: typing.Optional[str] = None
    start_param: typing.Optional[str] = None


class PeerDialogs(BaseModel):
    dialogs: typing.Optional[typing.List['Dialog']] = None
    messages: typing.Optional[typing.List['Message']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    state: typing.Optional['State'] = None


class TopPeer(BaseModel):
    peer: typing.Optional['Peer'] = None
    rating: typing.Optional[float] = None


class TopPeerCategory(BaseModel):
    pass


class TopPeerCategoryPeers(BaseModel):
    category: typing.Optional['TopPeerCategory'] = None
    count: typing.Optional[int] = None
    peers: typing.Optional[typing.List['TopPeer']] = None


class TopPeers(BaseModel):
    categories: typing.Optional[typing.List['TopPeerCategoryPeers']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class DraftMessage(BaseModel):
    date: typing.Optional[int] = None
    no_webpage: typing.Optional[bool] = None
    reply_to_msg_id: typing.Optional[int] = None
    message: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None


class FeaturedStickers(BaseModel):
    count: typing.Optional[int] = None
    hash: typing.Optional[int] = None
    sets: typing.Optional[typing.List['StickerSetCovered']] = None
    unread: typing.Optional[typing.List[int]] = None


class RecentStickers(BaseModel):
    hash: typing.Optional[int] = None
    packs: typing.Optional[typing.List['StickerPack']] = None
    stickers: typing.Optional[typing.List['Document']] = None
    dates: typing.Optional[typing.List[int]] = None


class ArchivedStickers(BaseModel):
    count: typing.Optional[int] = None
    sets: typing.Optional[typing.List['StickerSetCovered']] = None


class StickerSetInstallResult(BaseModel):
    sets: typing.Optional[typing.List['StickerSetCovered']] = None


class StickerSetCovered(BaseModel):
    set: typing.Optional['StickerSet'] = None
    cover: typing.Optional['Document'] = None
    covers: typing.Optional[typing.List['Document']] = None


class MaskCoords(BaseModel):
    n: typing.Optional[int] = None
    x: typing.Optional[float] = None
    y: typing.Optional[float] = None
    zoom: typing.Optional[float] = None


class InputStickeredMedia(BaseModel):
    id: typing.Optional['InputPhoto'] = None


class Game(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    short_name: typing.Optional[str] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    photo: typing.Optional['Photo'] = None
    document: typing.Optional['Document'] = None


class InputGame(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    bot_id: typing.Optional['InputUser'] = None
    short_name: typing.Optional[str] = None


class HighScore(BaseModel):
    pos: typing.Optional[int] = None
    user_id: typing.Optional[int] = None
    score: typing.Optional[int] = None


class HighScores(BaseModel):
    scores: typing.Optional[typing.List['HighScore']] = None
    users: typing.Optional[typing.List['User']] = None


class RichText(BaseModel):
    text: typing.Optional[str] = None
    url: typing.Optional[str] = None
    webpage_id: typing.Optional[int] = None
    email: typing.Optional[str] = None
    texts: typing.Optional[typing.List['RichText']] = None
    phone: typing.Optional[str] = None
    document_id: typing.Optional[int] = None
    w: typing.Optional[int] = None
    h: typing.Optional[int] = None
    name: typing.Optional[str] = None


class PageBlock(BaseModel):
    text: typing.Optional['RichText'] = None
    author: typing.Optional['RichText'] = None
    published_date: typing.Optional[int] = None
    language: typing.Optional[str] = None
    name: typing.Optional[str] = None
    items: typing.Optional[typing.List['PageListItem']] = None
    caption: typing.Optional['RichText'] = None
    photo_id: typing.Optional[int] = None
    url: typing.Optional[str] = None
    webpage_id: typing.Optional[int] = None
    autoplay: typing.Optional[bool] = None
    loop: typing.Optional[bool] = None
    video_id: typing.Optional[int] = None
    cover: typing.Optional['PageBlock'] = None
    full_width: typing.Optional[bool] = None
    allow_scrolling: typing.Optional[bool] = None
    html: typing.Optional[str] = None
    poster_photo_id: typing.Optional[int] = None
    w: typing.Optional[int] = None
    h: typing.Optional[int] = None
    author_photo_id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    blocks: typing.Optional[typing.List['PageBlock']] = None
    channel: typing.Optional['Chat'] = None
    audio_id: typing.Optional[int] = None
    bordered: typing.Optional[bool] = None
    striped: typing.Optional[bool] = None
    title: typing.Optional['RichText'] = None
    rows: typing.Optional[typing.List['PageTableRow']] = None
    open: typing.Optional[bool] = None
    articles: typing.Optional[typing.List['PageRelatedArticle']] = None
    geo: typing.Optional['GeoPoint'] = None
    zoom: typing.Optional[int] = None


class PhoneCallDiscardReason(BaseModel):
    pass


class DataJSON(BaseModel):
    data: typing.Optional[str] = None


class LabeledPrice(BaseModel):
    label: typing.Optional[str] = None
    amount: typing.Optional[int] = None


class Invoice(BaseModel):
    test: typing.Optional[bool] = None
    name_requested: typing.Optional[bool] = None
    phone_requested: typing.Optional[bool] = None
    email_requested: typing.Optional[bool] = None
    shipping_address_requested: typing.Optional[bool] = None
    flexible: typing.Optional[bool] = None
    phone_to_provider: typing.Optional[bool] = None
    email_to_provider: typing.Optional[bool] = None
    currency: typing.Optional[str] = None
    prices: typing.Optional[typing.List['LabeledPrice']] = None
    max_tip_amount: typing.Optional[int] = None
    suggested_tip_amounts: typing.Optional[typing.List[int]] = None


class PaymentCharge(BaseModel):
    id: typing.Optional[str] = None
    provider_charge_id: typing.Optional[str] = None


class PostAddress(BaseModel):
    street_line1: typing.Optional[str] = None
    street_line2: typing.Optional[str] = None
    city: typing.Optional[str] = None
    state: typing.Optional[str] = None
    country_iso2: typing.Optional[str] = None
    post_code: typing.Optional[str] = None


class PaymentRequestedInfo(BaseModel):
    name: typing.Optional[str] = None
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None
    shipping_address: typing.Optional['PostAddress'] = None


class PaymentSavedCredentials(BaseModel):
    id: typing.Optional[str] = None
    title: typing.Optional[str] = None


class WebDocument(BaseModel):
    url: typing.Optional[str] = None
    access_hash: typing.Optional[int] = None
    size: typing.Optional[int] = None
    mime_type: typing.Optional[str] = None
    attributes: typing.Optional[typing.List['DocumentAttribute']] = None


class InputWebDocument(BaseModel):
    url: typing.Optional[str] = None
    size: typing.Optional[int] = None
    mime_type: typing.Optional[str] = None
    attributes: typing.Optional[typing.List['DocumentAttribute']] = None


class InputWebFileLocation(BaseModel):
    url: typing.Optional[str] = None
    access_hash: typing.Optional[int] = None
    geo_point: typing.Optional['InputGeoPoint'] = None
    w: typing.Optional[int] = None
    h: typing.Optional[int] = None
    zoom: typing.Optional[int] = None
    scale: typing.Optional[int] = None


class WebFile(BaseModel):
    size: typing.Optional[int] = None
    mime_type: typing.Optional[str] = None
    file_type: typing.Optional['FileType'] = None
    mtime: typing.Optional[int] = None
    bytes: typing.Optional[bytes] = None


class PaymentForm(BaseModel):
    can_save_credentials: typing.Optional[bool] = None
    password_missing: typing.Optional[bool] = None
    form_id: typing.Optional[int] = None
    bot_id: typing.Optional[int] = None
    invoice: typing.Optional['Invoice'] = None
    provider_id: typing.Optional[int] = None
    url: typing.Optional[str] = None
    native_provider: typing.Optional[str] = None
    native_params: typing.Optional['DataJSON'] = None
    saved_info: typing.Optional['PaymentRequestedInfo'] = None
    saved_credentials: typing.Optional['PaymentSavedCredentials'] = None
    users: typing.Optional[typing.List['User']] = None


class ValidatedRequestedInfo(BaseModel):
    id: typing.Optional[str] = None
    shipping_options: typing.Optional[typing.List['ShippingOption']] = None


class PaymentResult(BaseModel):
    updates: typing.Optional['Updates'] = None
    url: typing.Optional[str] = None


class PaymentReceipt(BaseModel):
    date: typing.Optional[int] = None
    bot_id: typing.Optional[int] = None
    provider_id: typing.Optional[int] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    photo: typing.Optional['WebDocument'] = None
    invoice: typing.Optional['Invoice'] = None
    info: typing.Optional['PaymentRequestedInfo'] = None
    shipping: typing.Optional['ShippingOption'] = None
    tip_amount: typing.Optional[int] = None
    currency: typing.Optional[str] = None
    total_amount: typing.Optional[int] = None
    credentials_title: typing.Optional[str] = None
    users: typing.Optional[typing.List['User']] = None


class SavedInfo(BaseModel):
    has_saved_credentials: typing.Optional[bool] = None
    saved_info: typing.Optional['PaymentRequestedInfo'] = None


class InputPaymentCredentials(BaseModel):
    id: typing.Optional[str] = None
    tmp_password: typing.Optional[bytes] = None
    save: typing.Optional[bool] = None
    data: typing.Optional['DataJSON'] = None
    payment_data: typing.Optional['DataJSON'] = None
    payment_token: typing.Optional['DataJSON'] = None


class TmpPassword(BaseModel):
    tmp_password: typing.Optional[bytes] = None
    valid_until: typing.Optional[int] = None


class ShippingOption(BaseModel):
    id: typing.Optional[str] = None
    title: typing.Optional[str] = None
    prices: typing.Optional[typing.List['LabeledPrice']] = None


class InputStickerSetItem(BaseModel):
    document: typing.Optional['InputDocument'] = None
    emoji: typing.Optional[str] = None
    mask_coords: typing.Optional['MaskCoords'] = None


class InputPhoneCall(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None


class PhoneCall(BaseModel):
    id: typing.Optional[int] = None
    video: typing.Optional[bool] = None
    access_hash: typing.Optional[int] = None
    date: typing.Optional[int] = None
    admin_id: typing.Optional[int] = None
    participant_id: typing.Optional[int] = None
    protocol: typing.Optional['PhoneCallProtocol'] = None
    receive_date: typing.Optional[int] = None
    g_a_hash: typing.Optional[bytes] = None
    g_b: typing.Optional[bytes] = None
    p2p_allowed: typing.Optional[bool] = None
    g_a_or_b: typing.Optional[bytes] = None
    key_fingerprint: typing.Optional[int] = None
    connections: typing.Optional[typing.List['PhoneConnection']] = None
    start_date: typing.Optional[int] = None
    need_rating: typing.Optional[bool] = None
    need_debug: typing.Optional[bool] = None
    reason: typing.Optional['PhoneCallDiscardReason'] = None
    duration: typing.Optional[int] = None
    phone_call: typing.Optional['PhoneCall'] = None
    users: typing.Optional[typing.List['User']] = None


class PhoneConnection(BaseModel):
    id: typing.Optional[int] = None
    ip: typing.Optional[str] = None
    ipv6: typing.Optional[str] = None
    port: typing.Optional[int] = None
    peer_tag: typing.Optional[bytes] = None
    turn: typing.Optional[bool] = None
    stun: typing.Optional[bool] = None
    username: typing.Optional[str] = None
    password: typing.Optional[str] = None


class PhoneCallProtocol(BaseModel):
    udp_p2p: typing.Optional[bool] = None
    udp_reflector: typing.Optional[bool] = None
    min_layer: typing.Optional[int] = None
    max_layer: typing.Optional[int] = None
    library_versions: typing.Optional[typing.List[str]] = None


class CdnFile(BaseModel):
    request_token: typing.Optional[bytes] = None
    bytes: typing.Optional[bytes] = None


class CdnPublicKey(BaseModel):
    dc_id: typing.Optional[int] = None
    public_key: typing.Optional[str] = None


class CdnConfig(BaseModel):
    public_keys: typing.Optional[typing.List['CdnPublicKey']] = None


class LangPackString(BaseModel):
    key: typing.Optional[str] = None
    value: typing.Optional[str] = None
    zero_value: typing.Optional[str] = None
    one_value: typing.Optional[str] = None
    two_value: typing.Optional[str] = None
    few_value: typing.Optional[str] = None
    many_value: typing.Optional[str] = None
    other_value: typing.Optional[str] = None


class LangPackDifference(BaseModel):
    lang_code: typing.Optional[str] = None
    from_version: typing.Optional[int] = None
    version: typing.Optional[int] = None
    strings: typing.Optional[typing.List['LangPackString']] = None


class LangPackLanguage(BaseModel):
    official: typing.Optional[bool] = None
    rtl: typing.Optional[bool] = None
    beta: typing.Optional[bool] = None
    name: typing.Optional[str] = None
    native_name: typing.Optional[str] = None
    lang_code: typing.Optional[str] = None
    base_lang_code: typing.Optional[str] = None
    plural_code: typing.Optional[str] = None
    strings_count: typing.Optional[int] = None
    translated_count: typing.Optional[int] = None
    translations_url: typing.Optional[str] = None


class ChannelAdminLogEventAction(BaseModel):
    prev_value: typing.Optional[str] = None
    new_value: typing.Optional[str] = None
    prev_photo: typing.Optional['Photo'] = None
    new_photo: typing.Optional['Photo'] = None
    message: typing.Optional['Message'] = None
    prev_message: typing.Optional['Message'] = None
    new_message: typing.Optional['Message'] = None
    participant: typing.Optional['ChannelParticipant'] = None
    prev_participant: typing.Optional['ChannelParticipant'] = None
    new_participant: typing.Optional['ChannelParticipant'] = None
    prev_stickerset: typing.Optional['InputStickerSet'] = None
    new_stickerset: typing.Optional['InputStickerSet'] = None
    prev_banned_rights: typing.Optional['ChatBannedRights'] = None
    new_banned_rights: typing.Optional['ChatBannedRights'] = None
    call: typing.Optional['InputGroupCall'] = None
    join_muted: typing.Optional[bool] = None
    invite: typing.Optional['ExportedChatInvite'] = None
    prev_invite: typing.Optional['ExportedChatInvite'] = None
    new_invite: typing.Optional['ExportedChatInvite'] = None
    approved_by: typing.Optional[int] = None


class ChannelAdminLogEvent(BaseModel):
    id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    user_id: typing.Optional[int] = None
    action: typing.Optional['ChannelAdminLogEventAction'] = None


class AdminLogResults(BaseModel):
    events: typing.Optional[typing.List['ChannelAdminLogEvent']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class ChannelAdminLogEventsFilter(BaseModel):
    join: typing.Optional[bool] = None
    leave: typing.Optional[bool] = None
    invite: typing.Optional[bool] = None
    ban: typing.Optional[bool] = None
    unban: typing.Optional[bool] = None
    kick: typing.Optional[bool] = None
    unkick: typing.Optional[bool] = None
    promote: typing.Optional[bool] = None
    demote: typing.Optional[bool] = None
    info: typing.Optional[bool] = None
    settings: typing.Optional[bool] = None
    pinned: typing.Optional[bool] = None
    edit: typing.Optional[bool] = None
    delete: typing.Optional[bool] = None
    group_call: typing.Optional[bool] = None
    invites: typing.Optional[bool] = None
    send: typing.Optional[bool] = None


class PopularContact(BaseModel):
    client_id: typing.Optional[int] = None
    importers: typing.Optional[int] = None


class FavedStickers(BaseModel):
    hash: typing.Optional[int] = None
    packs: typing.Optional[typing.List['StickerPack']] = None
    stickers: typing.Optional[typing.List['Document']] = None


class RecentMeUrl(BaseModel):
    url: typing.Optional[str] = None
    user_id: typing.Optional[int] = None
    chat_id: typing.Optional[int] = None
    chat_invite: typing.Optional['ChatInvite'] = None
    set: typing.Optional['StickerSetCovered'] = None


class RecentMeUrls(BaseModel):
    urls: typing.Optional[typing.List['RecentMeUrl']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class InputSingleMedia(BaseModel):
    media: typing.Optional['InputMedia'] = None
    random_id: typing.Optional[int] = None
    message: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None


class WebAuthorization(BaseModel):
    hash: typing.Optional[int] = None
    bot_id: typing.Optional[int] = None
    domain: typing.Optional[str] = None
    browser: typing.Optional[str] = None
    platform: typing.Optional[str] = None
    date_created: typing.Optional[int] = None
    date_active: typing.Optional[int] = None
    ip: typing.Optional[str] = None
    region: typing.Optional[str] = None


class WebAuthorizations(BaseModel):
    authorizations: typing.Optional[typing.List['WebAuthorization']] = None
    users: typing.Optional[typing.List['User']] = None


class InputMessage(BaseModel):
    id: typing.Optional[int] = None
    query_id: typing.Optional[int] = None


class InputDialogPeer(BaseModel):
    peer: typing.Optional['InputPeer'] = None
    folder_id: typing.Optional[int] = None


class DialogPeer(BaseModel):
    peer: typing.Optional['Peer'] = None
    folder_id: typing.Optional[int] = None


class FoundStickerSets(BaseModel):
    hash: typing.Optional[int] = None
    sets: typing.Optional[typing.List['StickerSetCovered']] = None


class FileHash(BaseModel):
    offset: typing.Optional[int] = None
    limit: typing.Optional[int] = None
    hash: typing.Optional[bytes] = None


class InputClientProxy(BaseModel):
    address: typing.Optional[str] = None
    port: typing.Optional[int] = None


class TermsOfServiceUpdate(BaseModel):
    expires: typing.Optional[int] = None
    terms_of_service: typing.Optional['TermsOfService'] = None


class InputSecureFile(BaseModel):
    id: typing.Optional[int] = None
    parts: typing.Optional[int] = None
    md5_checksum: typing.Optional[str] = None
    file_hash: typing.Optional[bytes] = None
    secret: typing.Optional[bytes] = None
    access_hash: typing.Optional[int] = None


class SecureFile(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    size: typing.Optional[int] = None
    dc_id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    file_hash: typing.Optional[bytes] = None
    secret: typing.Optional[bytes] = None


class SecureData(BaseModel):
    data: typing.Optional[bytes] = None
    data_hash: typing.Optional[bytes] = None
    secret: typing.Optional[bytes] = None


class SecurePlainData(BaseModel):
    phone: typing.Optional[str] = None
    email: typing.Optional[str] = None


class SecureValueType(BaseModel):
    pass


class SecureValue(BaseModel):
    type: typing.Optional['SecureValueType'] = None
    data: typing.Optional['SecureData'] = None
    front_side: typing.Optional['SecureFile'] = None
    reverse_side: typing.Optional['SecureFile'] = None
    selfie: typing.Optional['SecureFile'] = None
    translation: typing.Optional[typing.List['SecureFile']] = None
    files: typing.Optional[typing.List['SecureFile']] = None
    plain_data: typing.Optional['SecurePlainData'] = None
    hash: typing.Optional[bytes] = None


class InputSecureValue(BaseModel):
    type: typing.Optional['SecureValueType'] = None
    data: typing.Optional['SecureData'] = None
    front_side: typing.Optional['InputSecureFile'] = None
    reverse_side: typing.Optional['InputSecureFile'] = None
    selfie: typing.Optional['InputSecureFile'] = None
    translation: typing.Optional[typing.List['InputSecureFile']] = None
    files: typing.Optional[typing.List['InputSecureFile']] = None
    plain_data: typing.Optional['SecurePlainData'] = None


class SecureValueHash(BaseModel):
    type: typing.Optional['SecureValueType'] = None
    hash: typing.Optional[bytes] = None


class SecureValueError(BaseModel):
    type: typing.Optional['SecureValueType'] = None
    data_hash: typing.Optional[bytes] = None
    field: typing.Optional[str] = None
    text: typing.Optional[str] = None
    file_hash: typing.Optional[bytes] = None
    hash: typing.Optional[bytes] = None


class SecureCredentialsEncrypted(BaseModel):
    data: typing.Optional[bytes] = None
    hash: typing.Optional[bytes] = None
    secret: typing.Optional[bytes] = None


class AuthorizationForm(BaseModel):
    required_types: typing.Optional[typing.List['SecureRequiredType']] = None
    values: typing.Optional[typing.List['SecureValue']] = None
    errors: typing.Optional[typing.List['SecureValueError']] = None
    users: typing.Optional[typing.List['User']] = None
    privacy_policy_url: typing.Optional[str] = None


class SentEmailCode(BaseModel):
    email_pattern: typing.Optional[str] = None
    length: typing.Optional[int] = None


class DeepLinkInfo(BaseModel):
    update_app: typing.Optional[bool] = None
    message: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None


class SavedContact(BaseModel):
    phone: typing.Optional[str] = None
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    date: typing.Optional[int] = None


class Takeout(BaseModel):
    id: typing.Optional[int] = None


class PasswordKdfAlgo(BaseModel):
    salt1: typing.Optional[bytes] = None
    salt2: typing.Optional[bytes] = None
    g: typing.Optional[int] = None
    p: typing.Optional[bytes] = None


class SecurePasswordKdfAlgo(BaseModel):
    salt: typing.Optional[bytes] = None


class SecureSecretSettings(BaseModel):
    secure_algo: typing.Optional['SecurePasswordKdfAlgo'] = None
    secure_secret: typing.Optional[bytes] = None
    secure_secret_id: typing.Optional[int] = None


class InputCheckPasswordSRP(BaseModel):
    srp_id: typing.Optional[int] = None
    A: typing.Optional[bytes] = None
    M1: typing.Optional[bytes] = None


class SecureRequiredType(BaseModel):
    native_names: typing.Optional[bool] = None
    selfie_required: typing.Optional[bool] = None
    translation_required: typing.Optional[bool] = None
    type: typing.Optional['SecureValueType'] = None
    types: typing.Optional[typing.List['SecureRequiredType']] = None


class PassportConfig(BaseModel):
    hash: typing.Optional[int] = None
    countries_langs: typing.Optional['DataJSON'] = None


class InputAppEvent(BaseModel):
    time: typing.Optional[float] = None
    type: typing.Optional[str] = None
    peer: typing.Optional[int] = None
    data: typing.Optional['JSONValue'] = None


class JSONObjectValue(BaseModel):
    key: typing.Optional[str] = None
    value: typing.Optional['JSONValue'] = None


class JSONValue(BaseModel):
    value: typing.Optional[bool] = None


class PageTableCell(BaseModel):
    header: typing.Optional[bool] = None
    align_center: typing.Optional[bool] = None
    align_right: typing.Optional[bool] = None
    valign_middle: typing.Optional[bool] = None
    valign_bottom: typing.Optional[bool] = None
    text: typing.Optional['RichText'] = None
    colspan: typing.Optional[int] = None
    rowspan: typing.Optional[int] = None


class PageTableRow(BaseModel):
    cells: typing.Optional[typing.List['PageTableCell']] = None


class PageCaption(BaseModel):
    text: typing.Optional['RichText'] = None
    credit: typing.Optional['RichText'] = None


class PageListItem(BaseModel):
    text: typing.Optional['RichText'] = None
    blocks: typing.Optional[typing.List['PageBlock']] = None


class PageListOrderedItem(BaseModel):
    num: typing.Optional[str] = None
    text: typing.Optional['RichText'] = None
    blocks: typing.Optional[typing.List['PageBlock']] = None


class PageRelatedArticle(BaseModel):
    url: typing.Optional[str] = None
    webpage_id: typing.Optional[int] = None
    title: typing.Optional[str] = None
    description: typing.Optional[str] = None
    photo_id: typing.Optional[int] = None
    author: typing.Optional[str] = None
    published_date: typing.Optional[int] = None


class Page(BaseModel):
    part: typing.Optional[bool] = None
    rtl: typing.Optional[bool] = None
    v2: typing.Optional[bool] = None
    url: typing.Optional[str] = None
    blocks: typing.Optional[typing.List['PageBlock']] = None
    photos: typing.Optional[typing.List['Photo']] = None
    documents: typing.Optional[typing.List['Document']] = None
    views: typing.Optional[int] = None


class SupportName(BaseModel):
    name: typing.Optional[str] = None


class UserInfo(BaseModel):
    message: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None
    author: typing.Optional[str] = None
    date: typing.Optional[int] = None


class PollAnswer(BaseModel):
    text: typing.Optional[str] = None
    option: typing.Optional[bytes] = None


class Poll(BaseModel):
    id: typing.Optional[int] = None
    closed: typing.Optional[bool] = None
    public_voters: typing.Optional[bool] = None
    multiple_choice: typing.Optional[bool] = None
    quiz: typing.Optional[bool] = None
    question: typing.Optional[str] = None
    answers: typing.Optional[typing.List['PollAnswer']] = None
    close_period: typing.Optional[int] = None
    close_date: typing.Optional[int] = None


class PollAnswerVoters(BaseModel):
    chosen: typing.Optional[bool] = None
    correct: typing.Optional[bool] = None
    option: typing.Optional[bytes] = None
    voters: typing.Optional[int] = None


class PollResults(BaseModel):
    min: typing.Optional[bool] = None
    results: typing.Optional[typing.List['PollAnswerVoters']] = None
    total_voters: typing.Optional[int] = None
    recent_voters: typing.Optional[typing.List[int]] = None
    solution: typing.Optional[str] = None
    solution_entities: typing.Optional[typing.List['MessageEntity']] = None


class ChatOnlines(BaseModel):
    onlines: typing.Optional[int] = None


class StatsURL(BaseModel):
    url: typing.Optional[str] = None


class ChatAdminRights(BaseModel):
    change_info: typing.Optional[bool] = None
    post_messages: typing.Optional[bool] = None
    edit_messages: typing.Optional[bool] = None
    delete_messages: typing.Optional[bool] = None
    ban_users: typing.Optional[bool] = None
    invite_users: typing.Optional[bool] = None
    pin_messages: typing.Optional[bool] = None
    add_admins: typing.Optional[bool] = None
    anonymous: typing.Optional[bool] = None
    manage_call: typing.Optional[bool] = None
    other: typing.Optional[bool] = None


class ChatBannedRights(BaseModel):
    view_messages: typing.Optional[bool] = None
    send_messages: typing.Optional[bool] = None
    send_media: typing.Optional[bool] = None
    send_stickers: typing.Optional[bool] = None
    send_gifs: typing.Optional[bool] = None
    send_games: typing.Optional[bool] = None
    send_inline: typing.Optional[bool] = None
    embed_links: typing.Optional[bool] = None
    send_polls: typing.Optional[bool] = None
    change_info: typing.Optional[bool] = None
    invite_users: typing.Optional[bool] = None
    pin_messages: typing.Optional[bool] = None
    until_date: typing.Optional[int] = None


class InputWallPaper(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    slug: typing.Optional[str] = None


class WallPapers(BaseModel):
    hash: typing.Optional[int] = None
    wallpapers: typing.Optional[typing.List['WallPaper']] = None


class CodeSettings(BaseModel):
    allow_flashcall: typing.Optional[bool] = None
    current_number: typing.Optional[bool] = None
    allow_app_hash: typing.Optional[bool] = None
    allow_missed_call: typing.Optional[bool] = None
    logout_tokens: typing.Optional[typing.List[bytes]] = None


class WallPaperSettings(BaseModel):
    blur: typing.Optional[bool] = None
    motion: typing.Optional[bool] = None
    background_color: typing.Optional[int] = None
    second_background_color: typing.Optional[int] = None
    third_background_color: typing.Optional[int] = None
    fourth_background_color: typing.Optional[int] = None
    intensity: typing.Optional[int] = None
    rotation: typing.Optional[int] = None


class AutoDownloadSettings(BaseModel):
    disabled: typing.Optional[bool] = None
    video_preload_large: typing.Optional[bool] = None
    audio_preload_next: typing.Optional[bool] = None
    phonecalls_less_data: typing.Optional[bool] = None
    photo_size_max: typing.Optional[int] = None
    video_size_max: typing.Optional[int] = None
    file_size_max: typing.Optional[int] = None
    video_upload_maxbitrate: typing.Optional[int] = None
    low: typing.Optional['AutoDownloadSettings'] = None
    medium: typing.Optional['AutoDownloadSettings'] = None
    high: typing.Optional['AutoDownloadSettings'] = None


class EmojiKeyword(BaseModel):
    keyword: typing.Optional[str] = None
    emoticons: typing.Optional[typing.List[str]] = None


class EmojiKeywordsDifference(BaseModel):
    lang_code: typing.Optional[str] = None
    from_version: typing.Optional[int] = None
    version: typing.Optional[int] = None
    keywords: typing.Optional[typing.List['EmojiKeyword']] = None


class EmojiURL(BaseModel):
    url: typing.Optional[str] = None


class EmojiLanguage(BaseModel):
    lang_code: typing.Optional[str] = None


class Folder(BaseModel):
    autofill_new_broadcasts: typing.Optional[bool] = None
    autofill_public_groups: typing.Optional[bool] = None
    autofill_new_correspondents: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    title: typing.Optional[str] = None
    photo: typing.Optional['ChatPhoto'] = None


class InputFolderPeer(BaseModel):
    peer: typing.Optional['InputPeer'] = None
    folder_id: typing.Optional[int] = None


class FolderPeer(BaseModel):
    peer: typing.Optional['Peer'] = None
    folder_id: typing.Optional[int] = None


class SearchCounter(BaseModel):
    inexact: typing.Optional[bool] = None
    filter: typing.Optional['MessagesFilter'] = None
    count: typing.Optional[int] = None


class UrlAuthResult(BaseModel):
    request_write_access: typing.Optional[bool] = None
    bot: typing.Optional['User'] = None
    domain: typing.Optional[str] = None
    url: typing.Optional[str] = None


class ChannelLocation(BaseModel):
    geo_point: typing.Optional['GeoPoint'] = None
    address: typing.Optional[str] = None


class PeerLocated(BaseModel):
    peer: typing.Optional['Peer'] = None
    expires: typing.Optional[int] = None
    distance: typing.Optional[int] = None


class RestrictionReason(BaseModel):
    platform: typing.Optional[str] = None
    reason: typing.Optional[str] = None
    text: typing.Optional[str] = None


class InputTheme(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    slug: typing.Optional[str] = None


class Theme(BaseModel):
    creator: typing.Optional[bool] = None
    default: typing.Optional[bool] = None
    for_chat: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    slug: typing.Optional[str] = None
    title: typing.Optional[str] = None
    document: typing.Optional['Document'] = None
    settings: typing.Optional[typing.List['ThemeSettings']] = None
    emoticon: typing.Optional[str] = None
    installs_count: typing.Optional[int] = None


class Themes(BaseModel):
    hash: typing.Optional[int] = None
    themes: typing.Optional[typing.List['Theme']] = None


class LoginToken(BaseModel):
    expires: typing.Optional[int] = None
    token: typing.Optional[bytes] = None
    dc_id: typing.Optional[int] = None
    authorization: typing.Optional['Authorization'] = None


class ContentSettings(BaseModel):
    sensitive_enabled: typing.Optional[bool] = None
    sensitive_can_change: typing.Optional[bool] = None


class InactiveChats(BaseModel):
    dates: typing.Optional[typing.List[int]] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class BaseTheme(BaseModel):
    pass


class InputThemeSettings(BaseModel):
    message_colors_animated: typing.Optional[bool] = None
    base_theme: typing.Optional['BaseTheme'] = None
    accent_color: typing.Optional[int] = None
    outbox_accent_color: typing.Optional[int] = None
    message_colors: typing.Optional[typing.List[int]] = None
    wallpaper: typing.Optional['InputWallPaper'] = None
    wallpaper_settings: typing.Optional['WallPaperSettings'] = None


class ThemeSettings(BaseModel):
    message_colors_animated: typing.Optional[bool] = None
    base_theme: typing.Optional['BaseTheme'] = None
    accent_color: typing.Optional[int] = None
    outbox_accent_color: typing.Optional[int] = None
    message_colors: typing.Optional[typing.List[int]] = None
    wallpaper: typing.Optional['WallPaper'] = None


class WebPageAttribute(BaseModel):
    documents: typing.Optional[typing.List['Document']] = None
    settings: typing.Optional['ThemeSettings'] = None


class MessageUserVote(BaseModel):
    user_id: typing.Optional[int] = None
    option: typing.Optional[bytes] = None
    date: typing.Optional[int] = None
    options: typing.Optional[typing.List[bytes]] = None


class VotesList(BaseModel):
    count: typing.Optional[int] = None
    votes: typing.Optional[typing.List['MessageUserVote']] = None
    users: typing.Optional[typing.List['User']] = None
    next_offset: typing.Optional[str] = None


class BankCardOpenUrl(BaseModel):
    url: typing.Optional[str] = None
    name: typing.Optional[str] = None


class BankCardData(BaseModel):
    title: typing.Optional[str] = None
    open_urls: typing.Optional[typing.List['BankCardOpenUrl']] = None


class DialogFilter(BaseModel):
    contacts: typing.Optional[bool] = None
    non_contacts: typing.Optional[bool] = None
    groups: typing.Optional[bool] = None
    broadcasts: typing.Optional[bool] = None
    bots: typing.Optional[bool] = None
    exclude_muted: typing.Optional[bool] = None
    exclude_read: typing.Optional[bool] = None
    exclude_archived: typing.Optional[bool] = None
    id: typing.Optional[int] = None
    title: typing.Optional[str] = None
    emoticon: typing.Optional[str] = None
    pinned_peers: typing.Optional[typing.List['InputPeer']] = None
    include_peers: typing.Optional[typing.List['InputPeer']] = None
    exclude_peers: typing.Optional[typing.List['InputPeer']] = None


class DialogFilterSuggested(BaseModel):
    filter: typing.Optional['DialogFilter'] = None
    description: typing.Optional[str] = None


class StatsDateRangeDays(BaseModel):
    min_date: typing.Optional[int] = None
    max_date: typing.Optional[int] = None


class StatsAbsValueAndPrev(BaseModel):
    current: typing.Optional[float] = None
    previous: typing.Optional[float] = None


class StatsPercentValue(BaseModel):
    part: typing.Optional[float] = None
    total: typing.Optional[float] = None


class StatsGraph(BaseModel):
    token: typing.Optional[str] = None
    error: typing.Optional[str] = None
    json_: typing.Optional['DataJSON'] = None
    zoom_token: typing.Optional[str] = None


class MessageInteractionCounters(BaseModel):
    msg_id: typing.Optional[int] = None
    views: typing.Optional[int] = None
    forwards: typing.Optional[int] = None


class BroadcastStats(BaseModel):
    period: typing.Optional['StatsDateRangeDays'] = None
    followers: typing.Optional['StatsAbsValueAndPrev'] = None
    views_per_post: typing.Optional['StatsAbsValueAndPrev'] = None
    shares_per_post: typing.Optional['StatsAbsValueAndPrev'] = None
    enabled_notifications: typing.Optional['StatsPercentValue'] = None
    growth_graph: typing.Optional['StatsGraph'] = None
    followers_graph: typing.Optional['StatsGraph'] = None
    mute_graph: typing.Optional['StatsGraph'] = None
    top_hours_graph: typing.Optional['StatsGraph'] = None
    interactions_graph: typing.Optional['StatsGraph'] = None
    iv_interactions_graph: typing.Optional['StatsGraph'] = None
    views_by_source_graph: typing.Optional['StatsGraph'] = None
    new_followers_by_source_graph: typing.Optional['StatsGraph'] = None
    languages_graph: typing.Optional['StatsGraph'] = None
    recent_message_interactions: typing.Optional[typing.List['MessageInteractionCounters']] = None


class PromoData(BaseModel):
    expires: typing.Optional[int] = None
    proxy: typing.Optional[bool] = None
    peer: typing.Optional['Peer'] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    psa_type: typing.Optional[str] = None
    psa_message: typing.Optional[str] = None


class VideoSize(BaseModel):
    type: typing.Optional[str] = None
    w: typing.Optional[int] = None
    h: typing.Optional[int] = None
    size: typing.Optional[int] = None
    video_start_ts: typing.Optional[float] = None


class StatsGroupTopPoster(BaseModel):
    user_id: typing.Optional[int] = None
    messages: typing.Optional[int] = None
    avg_chars: typing.Optional[int] = None


class StatsGroupTopAdmin(BaseModel):
    user_id: typing.Optional[int] = None
    deleted: typing.Optional[int] = None
    kicked: typing.Optional[int] = None
    banned: typing.Optional[int] = None


class StatsGroupTopInviter(BaseModel):
    user_id: typing.Optional[int] = None
    invitations: typing.Optional[int] = None


class MegagroupStats(BaseModel):
    period: typing.Optional['StatsDateRangeDays'] = None
    members: typing.Optional['StatsAbsValueAndPrev'] = None
    messages: typing.Optional['StatsAbsValueAndPrev'] = None
    viewers: typing.Optional['StatsAbsValueAndPrev'] = None
    posters: typing.Optional['StatsAbsValueAndPrev'] = None
    growth_graph: typing.Optional['StatsGraph'] = None
    members_graph: typing.Optional['StatsGraph'] = None
    new_members_by_source_graph: typing.Optional['StatsGraph'] = None
    languages_graph: typing.Optional['StatsGraph'] = None
    messages_graph: typing.Optional['StatsGraph'] = None
    actions_graph: typing.Optional['StatsGraph'] = None
    top_hours_graph: typing.Optional['StatsGraph'] = None
    weekdays_graph: typing.Optional['StatsGraph'] = None
    top_posters: typing.Optional[typing.List['StatsGroupTopPoster']] = None
    top_admins: typing.Optional[typing.List['StatsGroupTopAdmin']] = None
    top_inviters: typing.Optional[typing.List['StatsGroupTopInviter']] = None
    users: typing.Optional[typing.List['User']] = None


class GlobalPrivacySettings(BaseModel):
    archive_and_mute_new_noncontact_peers: typing.Optional[bool] = None


class CountryCode(BaseModel):
    country_code: typing.Optional[str] = None
    prefixes: typing.Optional[typing.List[str]] = None
    patterns: typing.Optional[typing.List[str]] = None


class Country(BaseModel):
    hidden: typing.Optional[bool] = None
    iso2: typing.Optional[str] = None
    default_name: typing.Optional[str] = None
    name: typing.Optional[str] = None
    country_codes: typing.Optional[typing.List['CountryCode']] = None


class CountriesList(BaseModel):
    countries: typing.Optional[typing.List['Country']] = None
    hash: typing.Optional[int] = None


class MessageViews(BaseModel):
    views: typing.Optional[int] = None
    forwards: typing.Optional[int] = None
    replies: typing.Optional['MessageReplies'] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class DiscussionMessage(BaseModel):
    messages: typing.Optional[typing.List['Message']] = None
    max_id: typing.Optional[int] = None
    read_inbox_max_id: typing.Optional[int] = None
    read_outbox_max_id: typing.Optional[int] = None
    unread_count: typing.Optional[int] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class MessageReplyHeader(BaseModel):
    reply_to_scheduled: typing.Optional[bool] = None
    reply_to_msg_id: typing.Optional[int] = None
    reply_to_peer_id: typing.Optional['Peer'] = None
    reply_to_top_id: typing.Optional[int] = None


class MessageReplies(BaseModel):
    comments: typing.Optional[bool] = None
    replies: typing.Optional[int] = None
    replies_pts: typing.Optional[int] = None
    recent_repliers: typing.Optional[typing.List['Peer']] = None
    channel_id: typing.Optional[int] = None
    max_id: typing.Optional[int] = None
    read_max_id: typing.Optional[int] = None


class PeerBlocked(BaseModel):
    peer_id: typing.Optional['Peer'] = None
    date: typing.Optional[int] = None


class MessageStats(BaseModel):
    views_graph: typing.Optional['StatsGraph'] = None


class GroupCall(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None
    duration: typing.Optional[int] = None
    join_muted: typing.Optional[bool] = None
    can_change_join_muted: typing.Optional[bool] = None
    join_date_asc: typing.Optional[bool] = None
    schedule_start_subscribed: typing.Optional[bool] = None
    can_start_video: typing.Optional[bool] = None
    record_video_active: typing.Optional[bool] = None
    rtmp_stream: typing.Optional[bool] = None
    listeners_hidden: typing.Optional[bool] = None
    participants_count: typing.Optional[int] = None
    title: typing.Optional[str] = None
    stream_dc_id: typing.Optional[int] = None
    record_start_date: typing.Optional[int] = None
    schedule_date: typing.Optional[int] = None
    unmuted_video_count: typing.Optional[int] = None
    unmuted_video_limit: typing.Optional[int] = None
    version: typing.Optional[int] = None
    call: typing.Optional['GroupCall'] = None
    participants: typing.Optional[typing.List['GroupCallParticipant']] = None
    participants_next_offset: typing.Optional[str] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class InputGroupCall(BaseModel):
    id: typing.Optional[int] = None
    access_hash: typing.Optional[int] = None


class GroupCallParticipant(BaseModel):
    muted: typing.Optional[bool] = None
    left: typing.Optional[bool] = None
    can_self_unmute: typing.Optional[bool] = None
    just_joined: typing.Optional[bool] = None
    versioned: typing.Optional[bool] = None
    min: typing.Optional[bool] = None
    muted_by_you: typing.Optional[bool] = None
    volume_by_admin: typing.Optional[bool] = None
    self: typing.Optional[bool] = None
    video_joined: typing.Optional[bool] = None
    peer: typing.Optional['Peer'] = None
    date: typing.Optional[int] = None
    active_date: typing.Optional[int] = None
    source: typing.Optional[int] = None
    volume: typing.Optional[int] = None
    about: typing.Optional[str] = None
    raise_hand_rating: typing.Optional[int] = None
    video: typing.Optional['GroupCallParticipantVideo'] = None
    presentation: typing.Optional['GroupCallParticipantVideo'] = None


class GroupParticipants(BaseModel):
    count: typing.Optional[int] = None
    participants: typing.Optional[typing.List['GroupCallParticipant']] = None
    next_offset: typing.Optional[str] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    version: typing.Optional[int] = None


class InlineQueryPeerType(BaseModel):
    pass


class HistoryImport(BaseModel):
    id: typing.Optional[int] = None


class HistoryImportParsed(BaseModel):
    pm: typing.Optional[bool] = None
    group: typing.Optional[bool] = None
    title: typing.Optional[str] = None


class AffectedFoundMessages(BaseModel):
    pts: typing.Optional[int] = None
    pts_count: typing.Optional[int] = None
    offset: typing.Optional[int] = None
    messages: typing.Optional[typing.List[int]] = None


class ChatInviteImporter(BaseModel):
    requested: typing.Optional[bool] = None
    user_id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    about: typing.Optional[str] = None
    approved_by: typing.Optional[int] = None


class ExportedChatInvites(BaseModel):
    count: typing.Optional[int] = None
    invites: typing.Optional[typing.List['ExportedChatInvite']] = None
    users: typing.Optional[typing.List['User']] = None


class ChatInviteImporters(BaseModel):
    count: typing.Optional[int] = None
    importers: typing.Optional[typing.List['ChatInviteImporter']] = None
    users: typing.Optional[typing.List['User']] = None


class ChatAdminWithInvites(BaseModel):
    admin_id: typing.Optional[int] = None
    invites_count: typing.Optional[int] = None
    revoked_invites_count: typing.Optional[int] = None


class ChatAdminsWithInvites(BaseModel):
    admins: typing.Optional[typing.List['ChatAdminWithInvites']] = None
    users: typing.Optional[typing.List['User']] = None


class CheckedHistoryImportPeer(BaseModel):
    confirm_text: typing.Optional[str] = None


class JoinAsPeers(BaseModel):
    peers: typing.Optional[typing.List['Peer']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class ExportedGroupCallInvite(BaseModel):
    link: typing.Optional[str] = None


class GroupCallParticipantVideoSourceGroup(BaseModel):
    semantics: typing.Optional[str] = None
    sources: typing.Optional[typing.List[int]] = None


class GroupCallParticipantVideo(BaseModel):
    paused: typing.Optional[bool] = None
    endpoint: typing.Optional[str] = None
    source_groups: typing.Optional[typing.List['GroupCallParticipantVideoSourceGroup']] = None
    audio_source: typing.Optional[int] = None


class SuggestedShortName(BaseModel):
    short_name: typing.Optional[str] = None


class BotCommandScope(BaseModel):
    peer: typing.Optional['InputPeer'] = None
    user_id: typing.Optional['InputUser'] = None


class ResetPasswordResult(BaseModel):
    retry_date: typing.Optional[int] = None
    until_date: typing.Optional[int] = None


class SponsoredMessage(BaseModel):
    random_id: typing.Optional[bytes] = None
    from_id: typing.Optional['Peer'] = None
    chat_invite: typing.Optional['ChatInvite'] = None
    chat_invite_hash: typing.Optional[str] = None
    channel_post: typing.Optional[int] = None
    start_param: typing.Optional[str] = None
    message: typing.Optional[str] = None
    entities: typing.Optional[typing.List['MessageEntity']] = None


class SponsoredMessages(BaseModel):
    messages: typing.Optional[typing.List['SponsoredMessage']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class SearchResultsCalendarPeriod(BaseModel):
    date: typing.Optional[int] = None
    min_msg_id: typing.Optional[int] = None
    max_msg_id: typing.Optional[int] = None
    count: typing.Optional[int] = None


class SearchResultsCalendar(BaseModel):
    inexact: typing.Optional[bool] = None
    count: typing.Optional[int] = None
    min_date: typing.Optional[int] = None
    min_msg_id: typing.Optional[int] = None
    offset_id_offset: typing.Optional[int] = None
    periods: typing.Optional[typing.List['SearchResultsCalendarPeriod']] = None
    messages: typing.Optional[typing.List['Message']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class SearchResultsPosition(BaseModel):
    msg_id: typing.Optional[int] = None
    date: typing.Optional[int] = None
    offset: typing.Optional[int] = None


class SearchResultsPositions(BaseModel):
    count: typing.Optional[int] = None
    positions: typing.Optional[typing.List['SearchResultsPosition']] = None


class SendAsPeers(BaseModel):
    peers: typing.Optional[typing.List['Peer']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None


class LoggedOut(BaseModel):
    future_auth_token: typing.Optional[bytes] = None


class ReactionCount(BaseModel):
    chosen: typing.Optional[bool] = None
    reaction: typing.Optional[str] = None
    count: typing.Optional[int] = None


class MessageReactions(BaseModel):
    min: typing.Optional[bool] = None
    can_see_list: typing.Optional[bool] = None
    results: typing.Optional[typing.List['ReactionCount']] = None
    recent_reactions: typing.Optional[typing.List['MessagePeerReaction']] = None


class MessageReactionsList(BaseModel):
    count: typing.Optional[int] = None
    reactions: typing.Optional[typing.List['MessagePeerReaction']] = None
    chats: typing.Optional[typing.List['Chat']] = None
    users: typing.Optional[typing.List['User']] = None
    next_offset: typing.Optional[str] = None


class AvailableReaction(BaseModel):
    inactive: typing.Optional[bool] = None
    reaction: typing.Optional[str] = None
    title: typing.Optional[str] = None
    static_icon: typing.Optional['Document'] = None
    appear_animation: typing.Optional['Document'] = None
    select_animation: typing.Optional['Document'] = None
    activate_animation: typing.Optional['Document'] = None
    effect_animation: typing.Optional['Document'] = None
    around_animation: typing.Optional['Document'] = None
    center_icon: typing.Optional['Document'] = None


class AvailableReactions(BaseModel):
    hash: typing.Optional[int] = None
    reactions: typing.Optional[typing.List['AvailableReaction']] = None


class TranslatedText(BaseModel):
    text: typing.Optional[str] = None


class MessagePeerReaction(BaseModel):
    big: typing.Optional[bool] = None
    unread: typing.Optional[bool] = None
    peer_id: typing.Optional['Peer'] = None
    reaction: typing.Optional[str] = None


class GroupCallStreamChannel(BaseModel):
    channel: typing.Optional[int] = None
    scale: typing.Optional[int] = None
    last_timestamp_ms: typing.Optional[int] = None


class GroupCallStreamChannels(BaseModel):
    channels: typing.Optional[typing.List['GroupCallStreamChannel']] = None


class GroupCallStreamRtmpUrl(BaseModel):
    url: typing.Optional[str] = None
    key: typing.Optional[str] = None


for v in locals().copy().values():
    if inspect.isclass(v) and issubclass(v, BaseModel):
        v.update_forward_refs()

__all__ = (
    'InputPeer',
    'InputUser',
    'InputContact',
    'InputFile',
    'InputMedia',
    'InputChatPhoto',
    'InputGeoPoint',
    'InputPhoto',
    'InputFileLocation',
    'Peer',
    'FileType',
    'User',
    'UserProfilePhoto',
    'UserStatus',
    'Chat',
    'ChatFull',
    'ChatParticipant',
    'ChatParticipants',
    'ChatPhoto',
    'Message',
    'MessageMedia',
    'MessageAction',
    'Dialog',
    'Photo',
    'PhotoSize',
    'GeoPoint',
    'SentCode',
    'Authorization',
    'ExportedAuthorization',
    'InputNotifyPeer',
    'InputPeerNotifySettings',
    'PeerNotifySettings',
    'PeerSettings',
    'WallPaper',
    'ReportReason',
    'UserFull',
    'Contact',
    'ImportedContact',
    'ContactStatus',
    'Contacts',
    'ImportedContacts',
    'Blocked',
    'Dialogs',
    'Messages',
    'Chats',
    'AffectedHistory',
    'MessagesFilter',
    'Update',
    'State',
    'Difference',
    'Updates',
    'Photos',
    'File',
    'DcOption',
    'Config',
    'NearestDc',
    'AppUpdate',
    'InviteText',
    'EncryptedChat',
    'InputEncryptedChat',
    'EncryptedFile',
    'InputEncryptedFile',
    'EncryptedMessage',
    'DhConfig',
    'SentEncryptedMessage',
    'InputDocument',
    'Document',
    'Support',
    'NotifyPeer',
    'SendMessageAction',
    'Found',
    'InputPrivacyKey',
    'PrivacyKey',
    'InputPrivacyRule',
    'PrivacyRule',
    'PrivacyRules',
    'AccountDaysTTL',
    'DocumentAttribute',
    'Stickers',
    'StickerPack',
    'AllStickers',
    'AffectedMessages',
    'WebPage',
    'Authorizations',
    'Password',
    'PasswordSettings',
    'PasswordInputSettings',
    'PasswordRecovery',
    'ReceivedNotifyMessage',
    'ExportedChatInvite',
    'ChatInvite',
    'InputStickerSet',
    'StickerSet',
    'BotCommand',
    'BotInfo',
    'KeyboardButton',
    'KeyboardButtonRow',
    'ReplyMarkup',
    'MessageEntity',
    'InputChannel',
    'ResolvedPeer',
    'MessageRange',
    'ChannelDifference',
    'ChannelMessagesFilter',
    'ChannelParticipant',
    'ChannelParticipantsFilter',
    'ChannelParticipants',
    'TermsOfService',
    'SavedGifs',
    'InputBotInlineMessage',
    'InputBotInlineResult',
    'BotInlineMessage',
    'BotInlineResult',
    'BotResults',
    'ExportedMessageLink',
    'MessageFwdHeader',
    'CodeType',
    'SentCodeType',
    'BotCallbackAnswer',
    'MessageEditData',
    'InputBotInlineMessageID',
    'InlineBotSwitchPM',
    'PeerDialogs',
    'TopPeer',
    'TopPeerCategory',
    'TopPeerCategoryPeers',
    'TopPeers',
    'DraftMessage',
    'FeaturedStickers',
    'RecentStickers',
    'ArchivedStickers',
    'StickerSetInstallResult',
    'StickerSetCovered',
    'MaskCoords',
    'InputStickeredMedia',
    'Game',
    'InputGame',
    'HighScore',
    'HighScores',
    'RichText',
    'PageBlock',
    'PhoneCallDiscardReason',
    'DataJSON',
    'LabeledPrice',
    'Invoice',
    'PaymentCharge',
    'PostAddress',
    'PaymentRequestedInfo',
    'PaymentSavedCredentials',
    'WebDocument',
    'InputWebDocument',
    'InputWebFileLocation',
    'WebFile',
    'PaymentForm',
    'ValidatedRequestedInfo',
    'PaymentResult',
    'PaymentReceipt',
    'SavedInfo',
    'InputPaymentCredentials',
    'TmpPassword',
    'ShippingOption',
    'InputStickerSetItem',
    'InputPhoneCall',
    'PhoneCall',
    'PhoneConnection',
    'PhoneCallProtocol',
    'CdnFile',
    'CdnPublicKey',
    'CdnConfig',
    'LangPackString',
    'LangPackDifference',
    'LangPackLanguage',
    'ChannelAdminLogEventAction',
    'ChannelAdminLogEvent',
    'AdminLogResults',
    'ChannelAdminLogEventsFilter',
    'PopularContact',
    'FavedStickers',
    'RecentMeUrl',
    'RecentMeUrls',
    'InputSingleMedia',
    'WebAuthorization',
    'WebAuthorizations',
    'InputMessage',
    'InputDialogPeer',
    'DialogPeer',
    'FoundStickerSets',
    'FileHash',
    'InputClientProxy',
    'TermsOfServiceUpdate',
    'InputSecureFile',
    'SecureFile',
    'SecureData',
    'SecurePlainData',
    'SecureValueType',
    'SecureValue',
    'InputSecureValue',
    'SecureValueHash',
    'SecureValueError',
    'SecureCredentialsEncrypted',
    'AuthorizationForm',
    'SentEmailCode',
    'DeepLinkInfo',
    'SavedContact',
    'Takeout',
    'PasswordKdfAlgo',
    'SecurePasswordKdfAlgo',
    'SecureSecretSettings',
    'InputCheckPasswordSRP',
    'SecureRequiredType',
    'PassportConfig',
    'InputAppEvent',
    'JSONObjectValue',
    'JSONValue',
    'PageTableCell',
    'PageTableRow',
    'PageCaption',
    'PageListItem',
    'PageListOrderedItem',
    'PageRelatedArticle',
    'Page',
    'SupportName',
    'UserInfo',
    'PollAnswer',
    'Poll',
    'PollAnswerVoters',
    'PollResults',
    'ChatOnlines',
    'StatsURL',
    'ChatAdminRights',
    'ChatBannedRights',
    'InputWallPaper',
    'WallPapers',
    'CodeSettings',
    'WallPaperSettings',
    'AutoDownloadSettings',
    'EmojiKeyword',
    'EmojiKeywordsDifference',
    'EmojiURL',
    'EmojiLanguage',
    'Folder',
    'InputFolderPeer',
    'FolderPeer',
    'SearchCounter',
    'UrlAuthResult',
    'ChannelLocation',
    'PeerLocated',
    'RestrictionReason',
    'InputTheme',
    'Theme',
    'Themes',
    'LoginToken',
    'ContentSettings',
    'InactiveChats',
    'BaseTheme',
    'InputThemeSettings',
    'ThemeSettings',
    'WebPageAttribute',
    'MessageUserVote',
    'VotesList',
    'BankCardOpenUrl',
    'BankCardData',
    'DialogFilter',
    'DialogFilterSuggested',
    'StatsDateRangeDays',
    'StatsAbsValueAndPrev',
    'StatsPercentValue',
    'StatsGraph',
    'MessageInteractionCounters',
    'BroadcastStats',
    'PromoData',
    'VideoSize',
    'StatsGroupTopPoster',
    'StatsGroupTopAdmin',
    'StatsGroupTopInviter',
    'MegagroupStats',
    'GlobalPrivacySettings',
    'CountryCode',
    'Country',
    'CountriesList',
    'MessageViews',
    'DiscussionMessage',
    'MessageReplyHeader',
    'MessageReplies',
    'PeerBlocked',
    'MessageStats',
    'GroupCall',
    'InputGroupCall',
    'GroupCallParticipant',
    'GroupParticipants',
    'InlineQueryPeerType',
    'HistoryImport',
    'HistoryImportParsed',
    'AffectedFoundMessages',
    'ChatInviteImporter',
    'ExportedChatInvites',
    'ChatInviteImporters',
    'ChatAdminWithInvites',
    'ChatAdminsWithInvites',
    'CheckedHistoryImportPeer',
    'JoinAsPeers',
    'ExportedGroupCallInvite',
    'GroupCallParticipantVideoSourceGroup',
    'GroupCallParticipantVideo',
    'SuggestedShortName',
    'BotCommandScope',
    'ResetPasswordResult',
    'SponsoredMessage',
    'SponsoredMessages',
    'SearchResultsCalendarPeriod',
    'SearchResultsCalendar',
    'SearchResultsPosition',
    'SearchResultsPositions',
    'SendAsPeers',
    'LoggedOut',
    'ReactionCount',
    'MessageReactions',
    'MessageReactionsList',
    'AvailableReaction',
    'AvailableReactions',
    'TranslatedText',
    'MessagePeerReaction',
    'GroupCallStreamChannel',
    'GroupCallStreamChannels',
    'GroupCallStreamRtmpUrl',
)
