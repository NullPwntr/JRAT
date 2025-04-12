import discord
from discord.ext import commands
import os
import difflib
import JRAT

def get_exact_words(input_str, words):
    exact_words = difflib.get_close_matches(input_str, words, n=1, cutoff=0.7)
    if len(exact_words) > 0:
        if exact_words[0] == input_str:
            return ""
        return exact_words[0]
    else:
        return ""

def get_correct_word(input : str, words : list[str]):
    corrected_string = ' '.join(get_exact_words(word, words) for word in input.split())
    return corrected_string

ADMIN = JRAT.ADMIN

class MyHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        """
        This is triggered when !help is invoked.

        This example demonstrates how to list the commands that the member invoking the help command can run.
        """
        if os.getlogin() == ADMIN:
            filtered = await self.filter_commands(self.context.bot.commands, sort=True)
            names = [command.name for command in filtered]
            available_commands = ""
            available_commands2 = ""
            available_commands = self.context.bot.description+"\n\n"

            for command in filtered:
                if len(available_commands) < 2000:
                    available_commands += f"\n`{command.name}` - {command.help}"
                else:
                    available_commands2 += f"\n`{command.name}` - {command.help}"
            embed  = discord.Embed(title="🐚 JRAT 🔑",description=available_commands)
            embed2  = discord.Embed(title="",description=available_commands2)
            
            await self.context.send(embed=embed)
            await self.context.send(embed=embed2)

    async def send_command_help(self, command):
        """This is triggered when !help <command> is invoked."""
        if os.getlogin() == ADMIN:
            await self.context.send(embed=discord.Embed(title="",description=f"`{command.name}` - {command.help}"))

    async def send_group_help(self, group):
        """This is triggered when !help <group> is invoked."""
        if os.getlogin() == ADMIN:
            await self.context.send("This is the help page for a group command")

    async def send_cog_help(self, cog):
        """This is triggered when !help <cog> is invoked."""
        if os.getlogin() == ADMIN:
            await self.context.send("This is the help page for a cog")

    async def send_error_message(self, error):
        """If there is an error, send a embed containing the error."""
        channel = self.get_destination() # this defaults to the command context channel
        if os.getlogin() == ADMIN:
            if "No command called" in error:
                cmds = []
                for cmd in self.context.bot.commands:
                    cmds.append(cmd.name)
                command = error.split("\"")[1].split("\"")[0]
                
                corrected = get_correct_word(command, cmds)
                fix_message = ''
                if len(corrected) > 0:
                    fix_message = f'Did you mean "{corrected}"?'
                await channel.send(f'No command called "{command}" found. {fix_message}')

                return
            await channel.send(error)