import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_GUILD_IDS = os.environ.get("DISCORD_GUILD_IDS")
DISCORD_NFD_ROLE_NAME = os.environ.get("DISCORD_NFD_ROLE_NAME")
NFD_ROOT = os.environ.get("NFD_ROOT")
NFD_DISCORD_CHECK_URL = os.environ.get("NFD_DISCORD_CHECK_URL")


def check_for_nfd(discord_id):
    ''' Check if a user has an NFD and return the name of the NFD if they do '''
    response = requests.get(NFD_DISCORD_CHECK_URL + discord_id, timeout=5)
    if response.status_code == 200:
        # extract data in json format
        nfds = response.json()

        for nfd in nfds:
            user_nfd_name = str(nfd['name'])
            # print out some specific fields
            if user_nfd_name.endswith(NFD_ROOT):
                #print(f"Found NFD: {nfd_name}")
                return True, user_nfd_name
    else:
        return False, None

class NFDRole(commands.Cog):
    ''' Check if a user has an NFD and give them the NFD role if they do '''
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='nfd_role', guild_ids=[DISCORD_GUILD_IDS])
    async def nfd_role(self, ctx: discord.ApplicationContext):
        ''' Check if a user has an NFD and give them the NFD role if they do '''
        guild = ctx.guild
        if guild is None:
            # Make sure we're still in the guild, and it's cached.
            return

        try:
            role_id = discord.utils.get(ctx.guild.roles, name=DISCORD_NFD_ROLE_NAME)
        except KeyError:
                # If the nfd_holder role doesn't exist, we can't continue.
            return

        role = guild.get_role(role_id.id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            user_has_nfd, user_nfd_name = check_for_nfd(str(ctx.user.id))
            if user_has_nfd is False:
                # If the user doesn't have an NFD, we can't continue.
                await ctx.respond("You do not have a *.algo NFD verified", ephemeral=True)
                return
        except TypeError:
            await ctx.respond("You do not have a *.algo NFD verified", ephemeral=True)
            return

        try:
            # Finally, add the role.
            await ctx.user.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

        await ctx.respond(f"I found that you have verified the following NFD: {user_nfd_name}. You have been given the {role.name} role!", ephemeral=True)


def setup(bot):
    ''' Add the cog to the bot '''
    bot.add_cog(NFDRole(bot))
