import type { PageScenes } from "../render/chat";

// Keys are page keys; inner keys are the index of the fenced block in that page.
// Replies must match what the code in the chapter actually returns.
export const scenes: Record<string, PageScenes> = {
  home: {
    0: [{ u: "/start" }, { b: "Hello, George! I'm Telegrinder Demo." }],
  },
  "tutorial/1_setting_up": {
    0: [{ sys: "The bot exists but is not listening yet" }],
    1: [{ u: "privetik" }, { b: "privetik" }, { sticker: true }, { sys: "A sticker has no text, so no reply" }],
    2: [{ sys: "bot.run_forever() started polling" }, { u: "privetik" }, { b: "privetik" }],
    3: [{ u: "privetik" }, { b: "privetik" }, { sticker: true }, { b: "No text" }],
  },
  "tutorial/2_rules": {
    0: [{ u: "anything" }, { sys: "A message event reached the message view" }],
    3: [{ u: "ping" }, { b: "Pong" }, { u: "pong" }, { sys: 'Text("ping") did not match' }],
    5: [{ u: "/hey" }, { b: "Hey hey!" }, { sys: "Now a user with another ID writes" }, { u: "/hey" }, { sys: "IsMessageFromUserId(123) returned False" }],
    6: [{ u: "2 + 3" }, { b: "5" }, { u: "12 + 30" }, { b: "42" }],
    7: [{ u: "42" }, { b: "42 / 3 = 14.0", reply: "42" }, { u: "forty two" }, { sys: "IsIntegerText returned False" }],
  },
  "tutorial/4_api": {
    0: [{ u: "hello" }, { b: "Hi!" }],
    2: [{ u: "hello" }, { sys: "message.api.send_message(chat_id=…)" }, { b: "Hi!" }],
    3: [{ u: "hello" }, { b: "Hi!" }, { sys: "case Ok(message): message_id is saved" }],
    5: [{ b: "Happy birthday" }, { edit: "Oops wrong chat" }, { del: true }],
  },
  "tutorial/5_nodes": {
    1: [{ u: "HELLO, BOT" }, { b: "hello, bot" }, { sticker: true }, { sys: "NodeError: Message has no text." }],
    4: [{ u: "39" }, { b: "39 + 3 = 42" }, { u: "abc" }, { sys: "NodeError: Text is not a digit." }],
  },
  "tutorial/6_dispatch": {
    1: [{ u: "/repeat hi 3" }, { b: "hi, hi, hi" }, { u: "/repeat ok" }, { b: "ok, ok, ok, ok, ok" }],
    2: [{ sys: "bot.on.load(chat_utilities.dp)" }, { u: "/repeat hi 2" }, { b: "hi, hi" }],
    5: [{ u: "/ban" }, { sys: "admin_router is not loaded into the bot yet" }],
    6: [{ sys: "bot.on.load(admin)" }, { u: "/ban" }, { b: "Admin action" }],
  },
  "tutorial/7_keyboard": {
    1: [{ u: "/keyboard" }, { b: "Here is your keyboard" }, { kb: [["1", "2"], ["3"]] }],
    2: [{ kb: [["1", "2"], ["3"]] }, { press: "1" }, { u: "1" }, { b: "You pressed button 1" }],
    4: [{ u: "/eat" }, { b: "What do you want to eat?" }, { kb: [["Apple", "Banana"], ["Kiwi"]] }],
    5: [
      { u: "/eat" }, { b: "What do you want to eat?" }, { kb: [["Apple", "Banana"], ["Kiwi"]] },
      { press: "Apple" }, { u: "Apple" }, { kb: null }, { b: "Good choice" },
    ],
    6: [
      { sys: "MenuKeyboard.get_markup()" },
      { kb: [[{ t: "Profile", s: "success" }, { t: "Balance", s: "primary" }], [{ t: "Exit", s: "danger" }]] },
    ],
    8: [{ u: "/inline_keyboard" }, { b: "Here is your inline keyboard", inline: [["1", "2"], ["3"]] }],
    9: [{ u: "/inline_keyboard" }, { b: "Here is your inline keyboard", inline: [["1", "2"], ["3"]] }, { press: "1" }, { toast: "Button 1 pressed" }],
    11: [
      { b: "Here is your inline keyboard", inline: [["1", "2"], ["3"]] },
      { press: "3" }, { toast: "Button 3 pressed" }, { press: "2" }, { toast: "Button 2 pressed" },
    ],
    13: [{ b: "🍩", inline: [["Buy doughnut"]] }, { press: "Buy doughnut" }, { edit: "You bought doughnut for 100" }],
  },
  "tutorial/8_text": {
    0: [
      { u: "/formatting" },
      { b: "<b><i>Bold and italic text</i></b>", html: true },
      { b: 'Hello, <a class="mention">George</a>!', html: true },
      { b: '<span class="datetime">Tomorrow</span>', html: true },
    ],
    2: [
      { sys: "This is how text renders in Telegram" },
      {
        b: 'Documentation: <a>Python docs</a><br>Token: <span class="spoiler"><code>123:secret-token</code></span><br><b>Do not share this with anyone.</b>',
        html: true,
      },
    ],
    4: [{ sys: "first_name is <i>George</i>" }, { u: "hi" }, { b: "Your nickname: <b>&lt;i&gt;George&lt;/i&gt;</b>", html: true }],
    6: [{ sys: "User locale: en" }, { u: "hi" }, { b: "hi" }, { u: "hello" }, { b: "Hello, George!" }],
  },
  "tutorial/9_states": {
    0: [
      { u: "hello" }, { b: "You are currently normal." },
      { u: "/bless" }, { b: "You are now blessed." },
      { u: "/curse" }, { b: "You are now cursed." },
      { u: "/bless" }, { b: "You are currently cursed." },
    ],
    3: [
      { u: "/choice" },
      { b: "Choose something", inline: [["Apple 🔴"], ["Banana 🟢"], ["Pear 🔴"], ["Ready"]] },
      { press: "Apple 🔴" }, { relabel: { "Apple 🔴": "Apple 🟢", "Banana 🟢": "Banana 🔴" } },
      { press: "Ready" }, { edit: "You chose: apple" },
    ],
    4: [
      { u: "/checkbox" },
      { b: "Check your checkbox", inline: [["Apple", "Banana 🍌"], ["Pear"], ["Ready", "Cancel"]] },
      { press: "Apple" }, { relabel: { Apple: "Apple 🍏" } },
      { press: "Ready" }, { edit: "You picked: apple, banana" },
    ],
    6: [
      { u: "/die" }, { b: "You are now dead because of sadness" },
      { u: "how are you?" }, { b: "You are currently dead because of sadness" },
      { u: "/resurrect" }, { b: "You resurrected" },
      { u: "how are you?" }, { b: "You are currently alive" },
    ],
    8: [{ u: "/be_born" }, { b: "You were born" }, { u: "Gh0$T_рa$$w0rd" }, { b: "You are now a ghost" }],
  },
  "tutorial/10_media": {
    0: [{ u: "/photo" }, { photo: "satie", caption: "Erik" }],
    1: [{ photo: "cat", out: true }, { b: "Photo downloaded!" }],
    2: [{ photo: "kitten", out: true }, { b: "File path: photos/file_0.jpg" }],
    3: [{ album: ["satie", "cat", "kitten"], caption: "assets" }, { b: "Received media group with 3 items<br>Caption: assets", html: true }],
  },
  "tutorial/11_handling_errors": {
    0: [
      { u: "oops" }, { b: "Oh no" }, { b: "Something went wrong: Wow" },
      { u: "woops" }, { b: "Something went wrong: Wow oopsii!" },
    ],
  },
};
