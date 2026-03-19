import os
import discord
from discord.ext import commands
from discord.ui import View, Button

TOKEN = os.getenv("MTQ4NDE5NDU1OTMxNDYyODYwOA.GTow4h.Ep-wh1esv913oTzZ9NgwfNrywhn-QlBgJAUNAE")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

VERIFY_CHANNEL_ID = 1484204843588653079   # ID kanału weryfikacji
ROLE_ID = 1483018446055669852           # ID roli do nadania


class VerifyButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Zweryfikuj się", style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: Button):
        role = interaction.guild.get_role(ROLE_ID)

        if role is None:
            return await interaction.response.send_message(
                "Nie mogę znaleźć roli do nadania.", ephemeral=True
            )

        try:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f"Zweryfikowano pomyślnie, {interaction.user.mention}!", ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                "Wystąpił błąd przy nadawaniu roli.", ephemeral=True
            )
            print(e)


@bot.event
async def on_ready():
    print(f"Bot zalogowany jako {bot.user}")


@bot.command()
async def sendverify(ctx):
    """Wysyła embed z przyciskiem weryfikacji"""
    if ctx.channel.id != VERIFY_CHANNEL_ID:
        return await ctx.send("Użyj tej komendy na kanale weryfikacji.")

    embed = discord.Embed(
        title="Weryfikacja",
        description="Kliknij przycisk poniżej, aby się zweryfikować.",
        color=discord.Color.green()
    )

    await ctx.send(embed=embed, view=VerifyButton())


bot.run("MTQ4NDE5NDU1OTMxNDYyODYwOA.GTow4h.Ep-wh1esv913oTzZ9NgwfNrywhn-QlBgJAUNAE")

