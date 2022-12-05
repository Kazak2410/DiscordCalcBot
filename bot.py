import disnake
from disnake.ext import commands
from disnake.ui import Button, View


PREFIX = "/"

bot = commands.Bot(command_prefix=PREFIX, intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print("bot connected")


class CalcButton(Button):
    def __init__(self, style, label, row):
        super().__init__(style=style, label=label, row=row)

    async def callback(self, interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message(content="")


buttons = [
        CalcButton(style=disnake.ButtonStyle.gray, label="7", row=0),
        CalcButton(style=disnake.ButtonStyle.gray, label="8", row=0),
        CalcButton(style=disnake.ButtonStyle.gray, label="9", row=0),
        CalcButton(style=disnake.ButtonStyle.blurple, label="/", row=0),
        CalcButton(style=disnake.ButtonStyle.red, label="<-", row=0),

        CalcButton(style=disnake.ButtonStyle.gray, label="4", row=1),
        CalcButton(style=disnake.ButtonStyle.gray, label="5", row=1),
        CalcButton(style=disnake.ButtonStyle.gray, label="6", row=1),
        CalcButton(style=disnake.ButtonStyle.blurple, label="*", row=1),
        CalcButton(style=disnake.ButtonStyle.red, label="Clear", row=1),

        CalcButton(style=disnake.ButtonStyle.gray, label="1", row=2),
        CalcButton(style=disnake.ButtonStyle.gray, label="2", row=2),
        CalcButton(style=disnake.ButtonStyle.gray, label="3", row=2),
        CalcButton(style=disnake.ButtonStyle.blurple, label="-", row=2),
        CalcButton(style=disnake.ButtonStyle.red, label="Exit", row=2),

        CalcButton(style=disnake.ButtonStyle.gray, label="00", row=3),
        CalcButton(style=disnake.ButtonStyle.gray, label="0", row=3),
        CalcButton(style=disnake.ButtonStyle.gray, label=".", row=3),
        CalcButton(style=disnake.ButtonStyle.blurple, label="+", row=3),
        CalcButton(style=disnake.ButtonStyle.green, label="=", row=3)
]


@bot.command()
async def calc(ctx):
    main = await ctx.send(content="Loading...")
    emb = disnake.Embed(title="`Calculator`")
    expression = ''
    symbols = ("*", "+", "/", "-")
    view = View()

    for button in buttons:
        view.add_item(button)

    await main.edit(content='', view=view, embed=emb)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    while True:
        event = await bot.wait_for("button_click", check=check)

        if ctx.author == event.author:
            if event.component.label == "=":
                expression = str(eval(expression))
                emb.description = expression
                await main.edit(embed=emb)

            elif event.component.label == "<-":
                expression = expression[:-1]
                emb.description = expression
                await main.edit(embed=emb)

            elif event.component.label == "Clear":
                expression = ''
                emb.description = expression
                await main.edit(embed=emb)

            elif event.component.label == "Exit":
                await main.edit(content="Calculator is closed", embed=None, view=None)
                break
            else:
                if event.component.label in ("*", "/", "+") and len(expression) == 0 or \
                        event.component.label in symbols and len(expression) != 0 and expression[-1] in symbols:
                    await main.reply(content="Некоректная запись!")
                else:
                    expression += event.component.label

                emb.description = expression
                await main.edit(embed=emb)


def run_bot():
    bot.run("MTA0NzAxODQyODgyNjkxMDc1MA.G-JFaX.cLvZ8WGCr11Abo-O-QOZKufJv4O4pqccs-QYwg")