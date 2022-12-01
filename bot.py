import disnake
from disnake.ext import commands
from disnake.ui import Button, View


PREFIX = "/"

bot = commands.Bot(command_prefix=PREFIX, intents=disnake.Intents.all())


elements = ['1', '2', '3', '*', '4', '5', '6', '//', '7', '8', '9', '+', ',', '0', '=', '-']


@bot.event
async def on_ready():
    print("bot connected")


class ButtonNumber(Button):
    def __init__(self, label, row, style):
        super().__init__(label=label, row=row, style=style)
        self.emb = disnake.Embed(title=self.label)

    async def callback(self, interaction: disnake.ApplicationCommandInteraction):
        if self.label != '=':
            lst_values.append(self.label)
            calc_emb.title = ''.join(i for i in lst_values)
        else:
            calc_emb.title = eval(''.join(i for i in lst_values))

        await interaction.response.edit_message(embed=calc_emb)


calc_emb = disnake.Embed(title='Введите значения...')
lst_values = []


@bot.command()
async def calc(ctx):
    view = View()

    row = 4
    start = 0
    finish = 3

    for i in range(row):
        for j in range(start, finish + 1):
            view.add_item(ButtonNumber(label=elements[j], row=i, style=disnake.ButtonStyle.grey))
        start = finish + 1
        finish += 4

    await ctx.send(embed=calc_emb, view=view)


def run_bot():
    bot.run("MTA0NzAxODQyODgyNjkxMDc1MA.GJlhJ7.DGoYaiwx-zXrXbSk_T-cUK6IrS88dj4ztvf14Q")