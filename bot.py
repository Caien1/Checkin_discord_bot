import discord
from dotenv import load_dotenv
from db import *
from forest_gerator import *
import os
import datetime
from http.server import *
 

load_dotenv()
token = os.getenv("TOKEN");
intents = discord.Intents.default()
intents.message_content = True


client =discord.Client(intents=intents)

  
# creating a class for handling  
# basic Get and Post Requests 
class GFG(BaseHTTPRequestHandler): 
    
    # creating a function for Get Request 
    def do_GET(self): 
        
        # Success Response --> 200 
        self.send_response(200) 
          
        # Type of file that we are using for creating our 
        # web server. 
        self.send_header('content-type', 'text/html') 
        self.end_headers() 
          
        # what we write in this function it gets visible on our 
        # web-server 
        self.wfile.write('<h1>GFG - (GeeksForGeeks)</h1>'.encode()) 
  
  
# this is the object which take port  
# number and the server-name 
# for running the server 
port = HTTPServer(('', 5555), GFG) 
  
# this is used for running our  
# server as long as we wish 
# i.e. forever 
port.serve_forever() 


@client.event
async def on_ready():

    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!checkin'):

        success,did_exist=main(message.author.id)
        connection, cursor = create_db_connection();
       # print(disply_users(cursor))
        close_connection(connection)

        if success and did_exist:
            await message.channel.send(f"✅ Thanks for the check-in, **{message.author.display_name}**! 🎉")
        elif success:
            await message.channel.send(f"🎉 Welcome to the family! 🏆 Perform daily check-ins to win points, **{message.author.display_name}**! 😊")
        else:
            await message.channel.send(f"⏰ Come back tomorrow! You’ve already done your check-in for today, **{message.author.display_name}**. 👍")

             
    if message.content.startswith('!laas'):
        msg = """

**meditation on malice**

wilful ignorance is the deceit of the self 
fake imagery crafted into existence 
a feeble attempt to stay hidden 
from the scanning eyes of death
cosmological charade 
cyclically cynical"""
        embed = discord.Embed(
             title="Who is Laas? Well here is a poem by him",
             description=msg,
             color=discord.Color.from_rgb(00,255,193)
             
        )
        await message.channel.send(embed=embed)
            
    if message.content.startswith('yes'):
        name = message.author.display_name +" has vowed allegiance to Dick Cheney"


        embed = discord.Embed(
             title="Member Added",
             description=name,
             color=discord.Color.red()
             
        )
        embed.set_image(url="https://media.discordapp.net/attachments/1144622555471282338/1326132538116145164/image.png")
        await message.channel.send(embed=embed)



    if message.content.startswith('!thefourth'):
        msg = """
The Fourth Reich Of Fun (TFROF) was a long-standing internet-dynasty created from smoke and mirrors amidst the ashes of broken memes and depressing dreams —
later known as the Rift Of Depression caused by a severe draught of FUN gamma and  deltarays in the great doomsdaydecay during approximately Fuckuabry 2021 and Nofunmember of that horrid year humanity as whole experienced, 
 instigated by the late great visionary and misunderstood artist, memer and do-it-yourself-dictator Laas (real name: ミームの王,) who was shunned by most except his trusty German right hand Simon "Panzerwunderhund" and left hand "Dobrodestroymachine" Niko S. who started as smalltime henchman but took over and ruled the dynasty for over 130 years after "Laas" was poisoned and killed by a Slovenian assassin and begrudged early follower known by her codename double D in late 2022

"""
        embed = discord.Embed(
             title="The Fourth Reich Of Fun",
             description=msg,
             color=discord.Color.from_rgb(00,255,193)
             
        )
        await message.channel.send(embed=embed)


    if message.content.startswith('!forest'):
        
        img = message.author.avatar
        points = ""
        #print(type(img))
        connection,cursor = create_db_connection()
        if(check_if_user_exists(cursor,message.author.id)):
            points = await get_user_points(cursor,message.author.id)
        else:
             message.channel.send("❗ Please use `!checkin` first! 🙏")

        #print(points[0][0])
    
        image= await send_imag(img,points[0][0])

        embed= discord.Embed(
             title="Your level",
             description="Novice"

        )
        embed.set_image(url="attachment://image.png")

        await message.channel.send(embed=embed,file=discord.File(image,filename="image.png",))
    
    
    if message.content.startswith('!leaderboard'):
             #   begin_process= time.time()
                connection, cursor= create_db_connection();
                value=await get_leaderboard(cursor,message.author.id)
                close_connection(connection)
                ##Time consuming part begins-
              #  begin_api_call = time.time()
                string =""
                for idx,row in enumerate(value,start=1):
                    user=""
                    try:
                        user = await client.fetch_user(row[0])
                    finally:
                        string += f"🏅 Rank {idx}: **{user.display_name}**, 🏆 Points: {row[1]}\n"

               # end_api_call = time.time()
              #  print(f"time taken : {end_api_call-begin_api_call}")   


                     
                embed= discord.Embed(
                     title="🏆 Leaderboard 🏆",
                    description=string,
                    color= discord.Color.gold(),
                )
                
                embed.set_footer(text="🔥 Keep climbing to the top! 🔥")
                embed.timestamp = datetime.datetime.now()
              #  end_process=time.time()
              #  print(f"Total time {end_process-begin_process}")
                await message.channel.send(embed=embed)

client.run(token)