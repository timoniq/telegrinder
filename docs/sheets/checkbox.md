# Checkbox

Via special scenarios you can easily create some common constructs. 
Scenarios are designed to be easy-to-use and as customizable as possible.

One of them is checkbox scenario, which is used to create an inline checkbox with particular options.

Callback data is generated and processed automatically. Checkbox performs event collection via `asyncio.Event`, so it is extremely easy to integrate such scenario in your funnel bot.

There is an obvious disadvantage of such way of collecting events: states are supposed to be short.

# First checkbox

Checkbox is created for each session. In some cases it will be easier for you to create a generator for them. Let's consider a simple case.

You want to create a checkbox to choose accessories user want to buy with their phone. User will be given a list of them.

You need to import required components. The special one for the needs of checkbox scenario will be `telegrinder.Checkbox`. Let's integrate it to your bot.

```python
from telegrinder import Telegrinder, API, Token, Message, Checkbox
from telegrinder.bot.rules import Text

api = API(token=Token("..."))
bot = Telegrinder(api=api)

@bot.on.message(Text("/start"))
async def start(m: Message):
    # now we need to create a checkbox
    
    # `msg` will be sent to the user with 
    # the checkbox reply markup. It usually 
    # contains an offering to choose needed options.
    
    # `ready_text` is the text on the button 
    # which will be used to submit the checkbox.
    
    # `max_in_row` sets the limit for options in a row
    checkbox = Checkbox(
        m.chat.id, 
        msg="Choose accessories you need:",
        multiple_choice=True,
        ready_text="That's all",
        max_in_row=2
    )
    
    # now you can add options 
    # into you checkbox. You can do it via .add_option method.
    # This also can be done in builder interface like this:
    # Checkbox(...).add_option(...).add_option(...)
    
    # checkbox option consists of four elements:
    # `name` of option is needed to later return the pick status
    # of option in dict
    # `default_text` is displayed on the button when option is not picked
    # `picked_text` is opposite
    # `is_picked` is needed to preset the button state
    
    checkbox.add_option(
        name="case",
        default_text="Case 5$",
        picked_text="[ Case 5$ ]",
        is_picked=False
    )
    
    checkbox.add_option(
        "charger", "Charger 9$", "[ Charger 9$ ]", 
        is_picked=True
    )
    
    # now your checkbox is ready to use.
    # picked is a dictionary option name to option state
    # message_id is the id of the one sent with `msg` text
    picked, message_id = checkbox.wait(m.ctx_api, bot.dispatch)
    
    # usually this message is edited 
    # with received information
    await m.ctx_api.edit_message_text(
        m.chat.id,
        message_id,
        text="You picked {}".format(
            ", ".join([a for a in picked if picked[a]])
            if picked
            else "nothing"
        )
    )

bot.run_forever()
```

# Advanced Usage

WIP