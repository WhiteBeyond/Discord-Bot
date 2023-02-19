import discord
from discord.ext import commands

class HelpCog(commands.Cog):
  def __init__(self, client):
    self.client = client
#help--------------------------------------------------
  @commands.hybrid_command(pass_context = True, description='All available commands')
  async def help(self, ctx):
    bot_avt='https://cdn.discordapp.com/attachments/1037916100496719933/1043969655519318116/Sounds_Of_Silence_Deemo.png'
    embed = discord.Embed(title="Command prefix: >", description="Use the command prefix to start a bot command: >[command]", colour = discord.Colour.magenta())
    embed.set_author(name='Deemo Bot',icon_url=bot_avt)
    embed.add_field(name='Basic infomation', value='`help`', inline=False)
    embed.add_field(name='Voice commands', value='`join` | `leave`', inline=False)
    embed.add_field(name='Music commands', value='`play` | `queue` | `nowplaying` | `pause` | `resume` | `skip` | `stop` | `loop`', inline=False)    
    embed.add_field(name='Funny', value='`slap` | `punch` | `bonk` | `kick` | `kill` | `yeet` | `kiss`', inline=False)
    embed.add_field(name='Caesar Cipher', value='`encrypt` | `decrypt`', inline=True)
    embed.add_field(name='Sleep cycle', value='`sleep` | `wake`', inline=True)
    embed.add_field(name='Pet', value='`cat` | `dog` | `shiba` | `bird`', inline=False)
    embed.add_field(name='Others', value='`meme` | `invite` | `clear` | `avatar` | `image`', inline=True)
    embed.set_thumbnail(url=bot_avt)
    embed.set_footer(text="More commands will be added in the future")
    await ctx.send(embed=embed)
  

    
async def setup(client):
  await client.add_cog(HelpCog(client))
