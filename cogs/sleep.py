import discord
import datetime
from discord.ext import commands


class SleepCog(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.hybrid_command(pass_context = True, aliases=['wa'], description='Format: hh.mm')
  async def wake(self,ctx,*,time:str='06.00'):
    embed = discord.Embed(colour = discord.Colour.magenta())
    bot_avt='https://cdn.discordapp.com/attachments/1037916100496719933/1043969655519318116/Sounds_Of_Silence_Deemo.png'
    embed.set_author(name='Sleep cycle calculator',icon_url=bot_avt)
    now=discord.utils.utcnow()
    if time or time==0: 
      time=float(time)
      hour=int((time*100)//100)
      minute=int(time*100-((time*100)//100)*100)
      time=f'at {hour:02d}:{minute:02d}'
      now=now.replace(hour=hour,minute=minute)
    cycle=[now + datetime.timedelta(minutes=-90*i) for i in range(1,7)]
    for i in range(6):
      embed.add_field(name=cycle[i].strftime(r"%H:%M"), value=f' {i+1} cycles of sleep', inline=True)  
    embed.title=f'If you want to wake up at {time}, you should be **falling sleep** around:'
    embed.set_footer(text="Remember average human takes around 15 minutes to fall asleep so plan accordingly!")
    await ctx.send(embed=embed) 

  @commands.hybrid_command(pass_context = True, aliases=['sl'], description='Format: Now / hh.mm')
  async def sleep(self,ctx,*,time:str=None):
    embed = discord.Embed(colour = discord.Colour.magenta())
    bot_avt='https://cdn.discordapp.com/attachments/1037916100496719933/1043969655519318116/Sounds_Of_Silence_Deemo.png'
    embed.set_author(name='Sleep cycle calculator',icon_url=bot_avt)
    now=discord.utils.utcnow()
    if not time or time =='now':
      time='now'
      cycle=[now + datetime.timedelta(hours=7,minutes=15+90*i) for i in range(1,7)]  
      for i in range(6):
        embed.add_field(name=cycle[i].strftime(r"%H:%M"), value=f' {i+1} cycles of sleep', inline=True)
    elif time or time==0: 
        time = float(time)
        hour=int((time*100)//100) #get hour from input
        minute=int(time*100-((time*100)//100)*100) #get minute from input
        time=f'at {hour:02d}:{minute:02d}'
        now=now.replace(hour=hour,minute=minute)+datetime.timedelta(hours=-7)
        cycle=[now + datetime.timedelta(hours=7,minutes=15+90*i) for i in range(1,7)]  
        for i in range(6):
          embed.add_field(name=cycle[i].strftime(r"%H:%M"), value=f' {i+1} cycles of sleep', inline=True)
    embed.title=f'If you sleep {time}, you should wake up around the following times:'    
    embed.set_footer(text="Remember average human takes around 15 minutes to fall asleep so plan accordingly!")
    await ctx.send(embed=embed) 
async def setup(client):
  await client.add_cog(SleepCog(client))
