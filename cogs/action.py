import discord
import requests
import datetime
import re
from discord.ext import commands
from discord import app_commands
class ActionCog(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.hybrid_command(pass_context = True, description='Slap someone')
  async def slap(self, ctx,*,member: discord.Member):
    r=requests.get("https://api.waifu.pics/sfw/slap")#"http://api.nekos.fun:8080/api/slap")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} vã mặt {member.display_name}")
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
  @commands.hybrid_command(pass_context = True, description='Bonk someone')
  async def bonk(self, ctx,*,member: discord.Member):
    r=requests.get("https://api.waifu.pics/sfw/bonk")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} gõ đầu {member.display_name}")
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
  @commands.hybrid_command(pass_context = True, description='Kick someone')
  async def kick(self, ctx,*,member: discord.Member):
    r=requests.get("https://api.waifu.pics/sfw/kick")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} đá {member.display_name}")
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
  @commands.hybrid_command(pass_context = True, description='Kill someone')
  async def kill(self, ctx,*,member: discord.Member):
    r=requests.get("https://api.waifu.pics/sfw/kill")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} cho {member.display_name} một vé lên thiên đàng")
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
  @commands.hybrid_command(pass_context = True, description='Yeet someone')
  async def yeet(self, ctx,*,member: discord.Member):
    r=requests.get("https://api.waifu.pics/sfw/yeet")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} yeet {member.display_name}")
    em.set_image(url=res['url'])
    await ctx.send(embed=em)

  @commands.hybrid_command(pass_context = True, description='Punch someone')
  async def punch(self, ctx,*,member: discord.Member):
    em = discord.Embed(colour = discord.Colour.magenta())
    r=requests.get("https://nekos.best/api/v2/punch")
    res=r.json()
    em.set_author(name=f"{ctx.author.display_name} đấm {member.display_name}")
    em.set_image(url=res["results"][0]["url"])
    await ctx.send(embed=em)

  @commands.hybrid_command(pass_context = True, description='Kiss someone')
  async def kiss(self, ctx,*,member: discord.Member):
    em = discord.Embed(colour = discord.Colour.magenta())
    r=requests.get("https://nekos.best/api/v2/kiss")
    res=r.json()
    em.set_author(name=f"{ctx.author.display_name} hun {member.display_name} ")
    em.set_image(url=res["results"][0]["url"])
    await ctx.send(embed=em) 
####################################################################################################
  @commands.hybrid_command(pass_context = True, description='Random dog image')
  async def dog(self, ctx):
    r=requests.get("https://random.dog/woof.json")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} request random dog image")
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
  @commands.hybrid_command(pass_context = True, description='Random cat image')
  async def cat(self, ctx):
    r=requests.get("http://shibe.online/api/cats")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} request random cat image")
    em.set_image(url=res[0])
    await ctx.send(embed=em) 
  @commands.hybrid_command(pass_context = True, description='Random shiba image')
  async def shiba(self, ctx):
    r=requests.get("http://shibe.online/api/shibes")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} request random shiba image")
    em.set_image(url=res[0])
    await ctx.send(embed=em)
  @commands.hybrid_command(pass_context = True, description='Random bird image')
  async def bird(self, ctx):
    r=requests.get("http://shibe.online/api/birds")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=f"{ctx.author.display_name} request random bird image")
    em.set_image(url=res[0])
    await ctx.send(embed=em)  
#################################################################################################### 

  @commands.command(pass_context = True, description='Meme')
  async def meme(self, ctx):
    r=requests.get("https://meme-api.com/gimme")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=res['title'])
    em.set_image(url=res['url'])
    await ctx.send(embed=em)
  @commands.hybrid_command(pass_context = True, description='Meme')
  async def food(self, ctx):
    r=requests.get("https://www.themealdb.com/api/json/v1/1/random.php?")
    res=r.json()
    em = discord.Embed(colour = discord.Colour.magenta())
    em.set_author(name=res['meals'][0]['strMeal'])
    em.set_image(url=res['meals'][0]['strMealThumb'])
    await ctx.send(embed=em)  

  @commands.hybrid_command(pass_context = True, aliases=['pod', 'apo'], description='Astronomy picture of the day (format DD.MM.YYYY)')
  @app_commands.describe(date='<DD.MM.YYYY>')
  async def apod(self,ctx,*,date:str=None):
    if not date==None:
      if not re.match(r'[0-9]{2}.[0-9]{2}.[0-9]{4}$', date):
        em = discord.Embed(title=f'**Wrong input format, please try again!**', colour = discord.Colour.magenta())
        await ctx.send(embed=em)
      else:
        d_m_y=date.split('.')
        date=f'{d_m_y[2]}-{d_m_y[1]}-{d_m_y[0]}'
    else: 
      date=discord.utils.utcnow()+ datetime.timedelta(hours=7)
      date=date.strftime('%Y-%m-%d')
    try:
      api_key ='mIIWAWS2fHjcfS7EcLXeQrBhdYx9rHwLuu7UTBKQ'
      url=f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}"
      r=requests.get(url)
      res=r.json()
      title=res['title']
      explanation=res['explanation']
      em = discord.Embed(title=f'**{title}**', description=f'{explanation}', colour = discord.Colour.magenta())
      em.set_image(url=res['url'])
      em.set_footer(text=f'{date}')
      await ctx.send(embed=em)
    except Exception as e:
      print(e)


  
      
async def setup(client):
  await client.add_cog(ActionCog(client))  
