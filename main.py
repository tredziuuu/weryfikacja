import random
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = "TWÓJ_TOKEN"
ROLE_ID = 1483018446055669852  # ID roli do nadania

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ------------------------------
#  KOMENDA /verify – panel
# ------------------------------
@bot.tree.command(name="verify", description="Wyświetla panel weryfikacyjny")
async def verify(interaction: discord.Interaction):

    button = discord.ui.Button(
        label="Zweryfikuj się",
        style=discord.ButtonStyle.success,
        custom_id="start_verify"
    )

    view = discord.ui.View()
    view.add_item(button)

    await interaction.response.send_message(
        "🔐 **Kliknij aby zweryfikować**",
        view=view
    )


# ------------------------------
#  OBSŁUGA PRZYCISKU
# ------------------------------
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    if interaction.data.get("custom_id") == "start_verify":

        # Generowanie działania
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        correct = a + b

        await interaction.response.send_message(
            f"Aby się zweryfikować, odpowiedz ile to: **{a} + {b}**",
            ephemeral=True
        )

        def check(msg):
            return msg.author.id == interaction.user.id

        try:
            msg = await bot.wait_for("message", timeout=15, check=check)

            if msg.content.isdigit() and int(msg.content) == correct:
                role = interaction.guild.get_role(ROLE_ID)
                member = interaction.guild.get_member(interaction.user.id)

                await member.add_roles(role)
                await interaction.followup.send(
                    "✔ Zweryfikowano! Rola została nadana.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ Zła odpowiedź. Kliknij przycisk ponownie.",
                    ephemeral=True
                )

        except:
            await interaction.followup.send(
                "⏳ Minął czas. Kliknij przycisk ponownie.",
                ephemeral=True
            )


# ------------------------------
#  SYNC KOMEND
# ------------------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Zalogowano jako {bot.user}")


bot.run(TOKEN)
