import discord
#import asyncio
import requests
from discord.ext import commands



class OtherCog(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  #avatar command--------------------------------------------------
  @commands.hybrid_command(pass_context = True, aliases=['ava','avt','av'],with_app_command=True, description='Show avatar of member')
  async def avatar(self, ctx, *, member: discord.Member = None):
    if not member:
      member = ctx.message.author
    embed = discord.Embed(title=f'{member.display_name} avatar', url=member.avatar ,colour = discord.Colour.magenta())
    embed.set_image(url=member.avatar)
    await ctx.send(embed=embed) 

    #clear command--------------------------------------------------
  @commands.hybrid_command(pass_context = True, aliases=['delete','del','cl'], description='Delete message (max 20)')
  async def clear(self, ctx, amount:int=1):
    if amount >20: amount=20
    user_message=ctx.message
    await user_message.delete()
    await ctx.defer()
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title=f':x: {amount} Messages deleted', url=None, colour = discord.Colour.magenta())
    await ctx.send(embed=embed,delete_after=1)
     
    #command--------------------------------------------------

  @commands.hybrid_command()
  async def game(self,ctx):
    embed = discord.Embed(title='Link', url=' ' ,colour = discord.Colour.magenta())
    await ctx.send(embed=embed) 
  @commands.hybrid_command(description='Add bot')
  async def invite(self,ctx):
    bot_avt='https://cdn.discordapp.com/attachments/1037916100496719933/1043969655519318116/Sounds_Of_Silence_Deemo.png'
    embed = discord.Embed(title='Add Deemo to your server', url='https://discord.com/api/oauth2/authorize?client_id=901031889001922571&permissions=1099514817536&scope=bot' ,colour = discord.Colour.magenta())
    embed.set_author(name='Deemo Bot',icon_url=bot_avt)
    embed.set_thumbnail(url=bot_avt)
    await ctx.send(embed=embed) 
    
  @commands.hybrid_command()
  async def permission(self, ctx):
      member = ctx.guild.get_member(self.client.user.id)
      perms = '\n'.join([perm for perm, value in member.guild_permissions if value])
      embed = discord.Embed(title="Bot Permissions", description=perms)
      await ctx.send(embed=embed)

  @commands.command(aliases=['wea'], description='Weather')  
  async def weather(self, ctx):    
    api_key = " "    
    city = "Ho Chi Minh City"    
    country_code = "VN"    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}"
    response = requests.get(url)    
    data = response.json()    
    if data["cod"] != "404":        
      temperature = round((data["main"]["temp"])/10)
      humidity = data["main"]["humidity"]
      description = data["weather"][0]["description"]  
      embed = discord.Embed(title="Weather Report", color=discord.Color.magenta())
      embed.add_field(name="Nhiệt độ", value=f"{temperature}°C", inline=True)
      embed.add_field(name="Độ ẩm", value=f"{humidity}%", inline=True)
      embed.add_field(name="Ghi chú", value=description, inline=False)
      await ctx.send(embed=embed)

  @commands.command()
  async def pic(self, ctx, *, picture: str):
    response = requests.get(f'https://api.unsplash.com/photos/random?query={picture}&client_id= ')
    data = response.json()
    image_url = data['urls']['regular']
    description = data['description']
    embed = discord.Embed(title=f"{description}", color=discord.Color.blue())
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)      
    
async def setup(client):
  await client.add_cog(OtherCog(client))
