from discord.ext import commands

class CaecarCog(commands.Cog):
  def __init__(self, client):
    self.client = client
  #Caecer Cipher--------------------------------------------------
  @commands.command(pass_context=True,aliases=['ec'])
  async def encrypt(self, ctx, amount:int, *,input:str):
    if not 1<=amount<=25:
      await ctx.send('Amount of shifted char must between 1 and 25')
    else:
      result=''
      for i in range(len(input)):
        char = input[i]
        if char.isalpha()==False:
          result +=char
        else:
          n=ord(char)+amount
          if char.isupper():
            if n>90:
              n=ord(char)+amount-90+64
              result += chr(n)
            else:
              result += chr(n)
          elif char.islower():
            if n>122:
              n=ord(char)+amount-122+96
              result += chr(n)
            else:
              result += chr(n)
      await ctx.channel.purge(limit=1)        
      await ctx.send(result)
  
  @commands.command(pass_context=True,aliases=['dc'])
  async def decrypt(self, ctx, amount:int, *,input:str):
    if not 1<=amount<=25:
      await ctx.send('Amount of shifted char must between 1 and 25')
    else:
      result=''
      for i in range(len(input)):
        char = input[i]
        if char.isalpha()==False:
          result +=char
        else:
          n=ord(char)-amount
          if char.isupper():
            if n<65:
              n=ord(char)-64+90-amount
              result += chr(n)
            else:
              result += chr(n)
          elif char.islower():
            if n<97:
              n=ord(char)-96+122-amount
              result += chr(n)
            else:
              result += chr(n)
      await ctx.channel.purge(limit=1)        
      await ctx.send(result)
  @commands.command(pass_context=True,aliases=['re:',':'])
  async def replica(self, ctx, *,input:str):
    await ctx.channel.purge(limit=1)
    await ctx.send(input)

async def setup(client):
  await client.add_cog(CaecarCog(client))  
