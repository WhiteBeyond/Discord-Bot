from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return('Hello, I am Deemo Bot ~~ Invite me ~~ [ https://discord.com/api/oauth2/authorize?client_id=901031889001922571&permissions=1099514817536&scope=bot ]')
  

def run():
  app.run(host='0.0.0.0',port=8080)
def keep_alive():
  t = Thread(target=run)
  t.start()
