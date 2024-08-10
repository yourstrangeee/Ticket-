import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio

class DeleteView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Delete Ticket", style=discord.ButtonStyle.red, emoji="", custom_id="trash")
    async def deletee(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        await interaction.channel.send("Deleting the ticket soon",delete_after=2)
        await asyncio.sleep(2)
        await interaction.channel.delete()

class CloseView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="closeticket", emoji="")
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send("Closing this ticket soon", delete_after=2)
        await asyncio.sleep(2)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=False, send_messages=False)
        }
        await interaction.channel.set_permissions(interaction.user, overwrite=None)
        await interaction.channel.edit(overwrites=overwrites)
        await interaction.channel.send(
            embed=discord.Embed(
                description="Ticket Closed!",
                color=discord.Color.red()
            ),
            view=DeleteView()
        )

class CreateView(Button):
    def __init__(self):
        super().__init__(label='Create ticket', style=discord.ButtonStyle.grey, custom_id='create', emoji='📩')
        self.callback = self.button_callback
    
    async def button_callback(self, interaction: discord.Interaction):
        categ = discord.utils.get(interaction.guild.categories, name='Ticket-category')
        
        if not categ:
            categ = await interaction.guild.create_category_channel(name='Ticket-category')
        
        for ch in categ.channels:
            if ch.topic == str(interaction.user.id):
                await interaction.response.send_message("You already have a ticket open.", ephemeral=True)
                return
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
        }
        channel = await categ.create_text_channel(
            f"ticket-{interaction.user.name}", 
            overwrites=overwrites, topic=f"{str(interaction.user.name)} Ticket ")
        await interaction.response.send_message(f"Created your ticket in {channel.mention}.", ephemeral=True)
        embed = discord.Embed(
            title='Ticket Created!',
            description=f"Hey {interaction.user.mention} Thanks for reaching!",
            color=0x00FFCA
        )
        await channel.send(f"{interaction.user.mention}, Successfully created Your Ticket Channel", embed=embed, view=CloseView())

class CreateTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CreateView())

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="panelsend",helps='Helps you create tickets for support in your server')
    @commands.has_permissions(manage_guild=True)
    async def sendpanel(self, ctx: commands.Context):
        embed = discord.Embed(title='Ticket Panel', description='To create a ticket Click on the button below', color=discord.Color.red)
        embed.set_footer(text=f"Ticketing by {ctx.me.display_name}", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        await ctx.send(
            embed=embed,
            view=CreateTicketView()
        )

async def setup(bot):
    await bot.add_cog(TicketCog(bot))
    bot.add_view(DeleteView())
    bot.add_view(CloseView())
    bot.add_view(CreateTicketView())
