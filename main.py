#import library
import discord
import os
import random
import datetime
import asyncio

#from discord import app_commands
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from keep_alive import keep_alive 

 
#command prefix--------------------------------------------------
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = '>', intents=intents, help_command=None)

#cogs---------------------------------------------------------------------------
cogs =['cogs.help','cogs.action','cogs.caecar','cogs.other','cogs.hidden','cogs.sleep']  
    
#bot status
#--------------------------------------------------------------------------------
@client.event
async def on_ready():
  activity = discord.Activity(type=discord.ActivityType.playing, name='>help')  
  await client.change_presence(status=discord.Status.online, activity=activity)
  print('Log in as {0.user}'.format(client))
  print('-----------------------------------')

  for cog in cogs:  
    try:
      await client.load_extension(cog)
      print(cog+' loaded')
    except Exception as e:
      print(e)  
  try:
    sync= await client.tree.sync()
  except Exception as e:
    print(e)  
#MUSIC--------------------------------------------------
#check queue
queues = {}
def check_queue(ctx, id):
  if str(id) in queues.keys():
    voice = ctx.guild.voice_client
    source = queues[id].pop(0)
    np_qq[id][0]=qq[id].pop(0)
    voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
 #join command--------------------------------------------------   
@client.hybrid_command(pass_context = True, aliases=['j','jon','jion'], description='Join a voice channel')
async def join(ctx):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
    else:
      voice = await channel.connect()      
    await ctx.send(':microphone: *Join voice*', delete_after=5)
  else:
    await ctx.send('*You are not in a voice channel*', delete_after=5)
#leave command--------------------------------------------------
@client.hybrid_command(pass_context = True, aliases=['l','le','disconnect','dis'], description='Disconnect from voice channel')
async def leave(ctx):
  if not (ctx.author.voice):
    await ctx.send('*You are not in a voice channel*', delete_after=5)
  elif (ctx.voice_client) and (ctx.author.voice):
    await ctx.guild.voice_client.disconnect()
    await ctx.send(':wave: *Leave voice*', delete_after=5)
  else:
    await ctx.send('*Deemo is not in a voice channel*', delete_after=5)
#loop command--------------------------------------------------
@client.hybrid_command(pass_context = True, aliases=['repeat','lo'], description='Toggle loop mode ON/OFF')
async def loop(ctx):
  global loop
  if loop:
    await ctx.send('*Loop mode: off*', delete_after=5)
    loop = False
  else:
    await ctx.send(':repeat_one: *Loop mode: ON - Stop and play new song to loop*', delete_after=5)
    loop = True
#Loop
loop = False

#play/p queue/q command--------------------------------------------------
@client.hybrid_command(pass_context = True, aliases=['p','pl','ply','plya'], description = 'URl or song name')
async def play(ctx, *, song):
  url = song
  await ctx.typing()
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      await voice.move_to(channel)
    else:
      voice = await channel.connect()
  else:
    await ctx.send('`You are not in a voice channel`')
  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'default_search':"ytsearch", 'source_address': '0.0.0.0', 'force-ipv4': True,'cachedir': False}
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      if 'entries' in info:
        url = info["entries"][0]["formats"][0]['url']
      elif 'formats' in info:
        url = info["formats"][0]['url']
      #get title      
      title = info.get('title')
      if title == None:
        title = info['entries'][0]['title']
      #get duration  
      duration = info.get('duration')
      if duration == None:
        duration = info['entries'][0]['duration']
      A = int(duration)//60
      B = int(duration)%60
      C = str(str(A)+':'+str(B))
      A1=0
      if A >=60:
        A1=int(duration)//60//60
        A =(int(duration)//60)%60
        C = str(str(A1)+':'+str(A)+':'+str(B)) 
  source = (FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
  guild_id = ctx.message.guild.id
  if voice.is_playing() or voice.is_paused():    
    if guild_id in queues:
      queues[guild_id].append(source)
      qq[guild_id].append(title)
    else:
      queues[guild_id] = [source]
      qq[guild_id] = [title]
    embed_q = discord.Embed(colour = discord.Colour.magenta())
    embed_q.add_field(name=f'『  {str(title)}  』({C})\n:headphones: added to queue', value=f'『{ctx.author.mention}』' , inline=False)
    await ctx.send(embed=embed_q)        
  elif not voice.is_playing() and not voice.is_paused():
    if loop:
      def repeat(guild, voice, audio):
        if loop:
          voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS), after=lambda x=0: repeat(guild, voice, FFmpegPCMAudio(url, **FFMPEG_OPTIONS)))
          voice.is_playing()
        else:
          check_queue(ctx, ctx.message.guild.id)
      voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS),after=lambda x=0: repeat(ctx.guild, voice, FFmpegPCMAudio(url, **FFMPEG_OPTIONS)))
      embed_l = discord.Embed(colour = discord.Colour.magenta())
      embed_l.add_field(name=f':headphones: Looping:『 {str(title)} 』({C})', value=f'『{ctx.author.mention}』' , inline=False)
      await ctx.send(embed=embed_l)
      if guild_id in queues:
        np_qq[guild_id].append(title)
      else:
        np_qq[guild_id] = [title]
    else:
      voice.play(FFmpegPCMAudio(url, **FFMPEG_OPTIONS),after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
      voice.is_playing()
      embed_p = discord.Embed(colour = discord.Colour.magenta())
      embed_p.add_field(name=f':headphones: Playing:『  {str(title)} 』({C})', value='『'+ctx.author.mention+'』' , inline=False)
      await ctx.send(embed=embed_p)
      if guild_id in queues:
        np_qq[guild_id].clear()
        qq[guild_id].clear()
        np_qq[guild_id].append(title)
      else:
        np_qq[guild_id] = [title]
#now playing and queue--------------------------------------------------
qq = {}
np_qq = {}
@client.hybrid_command(pass_context = True, aliases=['sq','nowplay','nowplaying','np','queue'], description='Display curent queue')
async def showqueue(ctx):
  guild_id = ctx.message.guild.id
  voice = get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    guild_id = ctx.message.guild.id
    title =''
    np_title=np_qq[guild_id][0]
    if guild_id in qq:
      for n in range(0,len(qq[guild_id])):
        title = title+'\n'+str(n+1)+': '+qq[guild_id][n]
        n = n+1
    if title == '':
      title = 'empty'
    embed = discord.Embed(colour = discord.Colour.magenta())
    embed.add_field(name=':headphones: Now playing:', value=f'**{np_title}**' , inline=False)
    embed.add_field(name=':headphones: Current queue:', value=title , inline=False)
    await ctx.send(embed=embed, delete_after=10)  
  else:
    await ctx.send('*Queue empty*')
#pause command--------------------------------------------------
@client.hybrid_command(pass_context = True,aliases=['pa'], description='Pause')
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if not (ctx.author.voice):
    await ctx.send('(You are not in a voice channel*', delete_after=5)
  else:  
    if voice.is_playing():
      voice.pause()
      await ctx.send(':pause_button: *Paused*', delete_after=5)
    else:
      await ctx.send('*Currently playing no audio*', delete_after=5)
#resume command--------------------------------------------------
@client.hybrid_command(pass_context = True, aliases=['re','resum'], description='Resume')
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if not (ctx.author.voice):
    await ctx.send('*You are not in voice*', delete_after=5)
  else:  
    if voice.is_paused():
      voice.resume()
      await ctx.send(':play_pause: *Resume*', delete_after=5)
    else:
      await ctx.send("*The audio is not paused*", delete_after=5)
#skip command--------------------------------------------------
@client.hybrid_command(pass_context = True, aliases=['sk','skpi'], description='Skip')
async def skip(ctx):
  try:
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    guild_id = ctx.message.guild.id
    if not (ctx.author.voice):
      await ctx.send('*You are not in a voice channel*', delete_after=5)
    else:
      if voice.is_playing():
        await ctx.send(':track_next: *Skip*', delete_after=5)
        voice.stop()
        if len(queues[guild_id])>0:
          source = queues[guild_id].pop(0)
          np_qq[guild_id][0]=qq[guild_id].pop(0)
          voice.play(source, after=lambda x=0: check_queue(ctx, guild_id))

      else:
        await ctx.send('*Currently playing no audio*', delete_after=5)
  except KeyError as e:
    print(e)
#stop command--------------------------------------------------
@client.hybrid_command(pass_context = True, aliases=['st','stpo'], description='Stop')
async def stop(ctx):
  global loop
  if loop:  loop=False
  if (ctx.author.voice):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
      if voice.is_playing() or voice.is_paused():
        voice.stop()
        await ctx.send(':stop_button: *Stop playing*', delete_after=5)
      else: await ctx.send('*Not playing any song*', delete_after=5)
    else: await ctx.send('*Deemo is not connected to voice channel*', delete_after=5)
  else: await ctx.send('*You are not in a voice channel*', delete_after=5)
    

#auto disconnect--------------------------------------------------
@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    global loop
    if voice_state is None:
      return 
    if len(voice_state.channel.members) == 1:
      await voice_state.disconnect()
      if loop == True:
        loop = False

#skip to--------------------------------------------------
@client.command(pass_context = True)
async def skipto(ctx, amount=1):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  guild_id = ctx.message.guild.id
  embed = discord.Embed(colour = discord.Colour.magenta())
  if not (ctx.author.voice):
    await ctx.send('*You are not in a voice channel*', delete_after=5)
  else:
    if voice.is_playing():
      embed.add_field(name=f':track_next: Skip to {str(amount)}:', value = qq[guild_id][amount-1], inline=True)
      await ctx.send(embed=embed)
      for i in range(0,amount):
        source = queues[guild_id].pop(0)
        np_qq[guild_id][0]=qq[guild_id].pop(0)
      voice.pause()
      voice.play(source, after=lambda x=0: check_queue(ctx, ctx.message.guild.id))
    else:
      await ctx.send('*Currently playing no audio*', delete_after=5)
#random image--------------------------------------------------
@client.command(pass_context = True,aliases=['i','im'])
async def image(ctx, *,input:str='random'):
  channel1 = client.get_channel( ) #nsfnw channel
  if input=='random':
    channel = client.get_channel( )  
    messages = [message async for message in channel.history(limit=900)]
    message_attachments = [message.attachments for message in messages if message.attachments]
    image_attachments = [attachment.url 
        for attachments in message_attachments 
        for attachment in attachments 
        if attachment.url.endswith(".png") or attachment.url.endswith(".jpg") or attachment.url.endswith(".gif")]
    random_number = random.randint(0, len(image_attachments))
    await ctx.send(image_attachments[random_number])
  elif input=='r18':
    random_channel = random.randint(0,4)
    if random_channel<=2:
      channel = client.get_channel( )
    else:
      channel = client.get_channel( )
    messages = [message async for message in channel.history(limit=900)]
    message_attachments = [message.attachments for message in messages if message.attachments]
    image_attachments = [attachment.url 
        for attachments in message_attachments 
        for attachment in attachments 
        if attachment.url.endswith(".png") or attachment.url.endswith(".jpg") or attachment.url.endswith(".gif")]
    random_number = random.randint(0, len(image_attachments))
    await channel1.send(image_attachments[random_number])

#auto send message--------------------------------------------------
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  else:
    if not message.channel.id == ( ):#bot_nsfw
      if message.guild.id ==( ):# or message.guild.id ==( ):#server
        rand_num = random.randint(0,400)
        if rand_num == 0:
          await message.channel.send('https://cdn.discordapp.com/attachments/901788626239762503/1060656600190308483/Untitled-1.png')
          #'https://media.discordapp.net/attachments/1036558805506473994/1036559895220195398/l.png')
        elif rand_num == 1:
          await message.channel.send('https://cdn.discordapp.com/attachments/901788626239762503/1060656625993654333/new.png')
    elif message.channel.id == ( ):
        if len(message.attachments) <= 0:
          await asyncio.sleep(2)
          await message.channel.purge(limit=1)

  await client.process_commands(message)
#hidden
@client.command(pass_context = True,aliases=['hd'])
async def hidden(ctx, amount:int=1):
  if ' ' in str(ctx.author):
    c=client.get_channel( )
  else:
    if ctx.channel.is_nsfw():
      c = ctx.author
    else:
      await ctx.send('`ERROR`')
  for i in range(amount):
    random_channel = random.randint(0,1) 
    if random_channel==0:
      channel = client.get_channel( )
    else:
      channel = client.get_channel( )
    messages = [message async for message in channel.history(limit=900)]
    message_attachments = [message.attachments for message in messages if message.attachments]
    image_attachments = [attachment.url 
        for attachments in message_attachments 
        for attachment in attachments 
        if attachment.url.endswith(".png") or attachment.url.endswith(".jpg") or attachment.url.endswith(".gif")]
    random_number = random.randint(0, len(image_attachments))
    await c.send(image_attachments[random_number])
@client.command(pass_context = True, aliases=['dmc'])
async def dmdelte(ctx,*,amount:int=1):
  dmchannel = await ctx.author.create_dm()
  async for message in dmchannel.history(limit=amount):
    if message.author == client.user:
        await message.delete()
''''''
#timeout command--------------------------------------------------
@client.command(pass_context = True, aliases=['bannnnnn'])
async def ban(ctx,member: discord.Member,* , minutes: int=1):
  per=0
  name =['Aina','MrPenguin','F','e','n','A']
  for i in range (len(name)):
    if name[i] in str(ctx.author): 
      per=per+1
    else: per=per
  if per>=1:
    per =0
    if minutes >5: minutes=5
    if not random.randint(0,1)==1: 
      await ctx.channel.purge(limit=1)
      #member=ctx.author
      minutes=100
    await member.edit(timed_out_until=discord.utils.utcnow() + datetime.timedelta(minutes=minutes),reason=None)
    if minutes==0:
      await ctx.send(f"{member.display_name} được unban")
    else: 
      await ctx.send(f"{member.display_name} bị khóa mõm trong {minutes} phút")
      if member == ctx.author: 
        await ctx.channel.purge(limit=1)
  elif per==0:
    await ctx.send('Bạn tủi zì mà đòi xài lệnh >ban')
    per=0
@client.command(pass_context = True, aliases=['unb'])
async def unban(ctx,*,member: discord.Member):
  await member.edit(timed_out_until=discord.utils.utcnow() + datetime.timedelta(minutes=0),reason=None)
  await ctx.send(f"{member.display_name} được unban",  delete_after=10)
@client.hybrid_command()
async def ping(ctx):
  embed = discord.Embed(title=('Pong! {0} ms'.format(round(client.latency*1000))), colour = discord.Colour.magenta())
  await ctx.send(embed=embed) 
      
#Test--------------------------------------------------
@client.hybrid_command(pass_context = True, description='hi')
async def hi(ctx):
  await ctx.defer(ephemeral=True)
  embed = discord.Embed(colour = discord.Colour.magenta())
  embed.add_field(name='`Hi Im Deemo Bot`', value=f'『{ctx.author.mention}』' , inline=True)
  await ctx.send(embed=embed)

@client.hybrid_command(pass_context = True)
async def test(ctx,*,member_name: discord.Member):
  await ctx.defer(ephemeral=True)
  #if random.randint(0,1)==1:  member = ctx.author
  #await ctx.send(member_name.display_name)
  #if 'Aina' in str(ctx.author):
  #  await ctx.author.send('This is a secret message')
  guild_id = ctx.message.guild.id
  await ctx.send(f'n_p:  {np_qq[guild_id]}')       
  await ctx.send(f'qq:  {qq[guild_id]}')     
  await ctx.send(f'queues:  {np_qq[guild_id]}')     

@client.command()
async def xend(ctx):
    message = "Click the button below: [Click Here](https://replit.com/@Eien-nini/DiscordBot#main.py)"
    await ctx.send(message)

board=[]
game_state = False

@client.command(pass_context = True)
async def caro(ctx, *, input:str=None):
  global game_state
  #guild_id=ctx.message.guild.id
  if not game_state and input=='start':
    await ctx.send('game start')
    game_state=True
    blank = '...'
    for i in range (0,10):
        board.append(f'{blank}')
  if game_state and input!='start':
    if 'O' in input:
      X_O='O'
    elif 'X' in input:
      X_O='X'
    i=[int(s) for s in input if s.isdigit()]
    board[i[0]]=X_O
  em = discord.Embed(colour = discord.Colour.magenta())
  em.add_field(name=f'| {board[7]} |', value='===', inline=True)
  em.add_field(name=f'| {board[8]} |', value='===', inline=True)
  em.add_field(name=f'| {board[9]} |', value='===', inline=True)
  em.add_field(name=f'| {board[4]} |', value='===', inline=True)
  em.add_field(name=f'| {board[5]} |', value='===', inline=True)
  em.add_field(name=f'| {board[6]} |', value='===', inline=True)
  em.add_field(name=f'| {board[1]} |', value='\u200b', inline=True)
  em.add_field(name=f'| {board[2]} |', value='\u200b', inline=True)
  em.add_field(name=f'| {board[3]} |', value='\u200b', inline=True)  
  await ctx.send(embed=em)
    
#--------------------------------------------------
@client.event 
async def on_command_error(ctx, error): 
  if isinstance(error, commands.CommandNotFound):
    error=ctx.message.content  
    if '@' in ctx.message.content:
      error=error[ : error.index('@')-2 : ]
    await ctx.send(f':no_entry_sign: `làm gì có cái command {error} `')
  elif isinstance(error, commands.CommandInvokeError):  
    await ctx.send(f':no_entry_sign: `{ctx.message.content} error`')
while __name__ == '__main__':
  try:
    keep_alive()
    client.run(os.environ['TOKEN'])
  except discord.errors.HTTPException as e:
    print(e)
    os.system('kill 1')
  
