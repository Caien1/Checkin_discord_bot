import discord
from dotenv import load_dotenv
from db import *
from forest_gerator import *
import os

 

load_dotenv()
token = os.getenv("TOKEN");
intents = discord.Intents.default()
intents.message_content = True


client =discord.Client(intents=intents)


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
        print(disply_users(cursor))
        close_connection(connection)

        if success and did_exist:
            await message.channel.send(f"Thanks for the Checkin {message.author}")
        elif success:
            await message.channel.send(f"Welcome to the family perform daily checking to win points {message.author.name}")
        else:
            await message.channel.send(f"Please try again later you alredy have done your checkin {message.author.display_name}")


             


    if message.content.startswith('!forest'):
        
        img = message.author.avatar
        print(type(img))
    
        image = await send_imag(img)

        embed= discord.Embed(
             title="Your level",
             description="None"

        )
        embed.set_image(url="attachment://image.png")

        await message.channel.send(embed=embed,file=discord.File(image,filename="image.png",))
    
    if message.content.startswith('!leaderboard'):
                connection, cursor= create_db_connection();
                value=get_leaderboard(cursor,message.author.id)
                close_connection(connection)
                string =""
                for idx,row in enumerate(value,start=1):
                    user=""
                    try:
                        user = await client.fetch_user(row[0])
                    finally:
                        string += f"Rank {idx}: User ID {user}, Points: {row[1]}\n"
                    
                    

                   # string += " ".join(str(val) for val in row)
                user = await client.fetch_user(830016053739388938)
                     

                await message.channel.send(f"This will load an image in the future\n{string},{user.bot}")

client.run(token)