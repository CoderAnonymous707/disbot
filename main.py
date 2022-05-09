# Importing a few libraries
import discord
import wikipedia as wiki
import requests
import os
import random
import json
import random
# from keep_alive import keep_alive

# Creating a new client - this is the connection to discord!
client = discord.Client()

def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    jsonData = json.loads(response.text)
    quote = jsonData[0]["q"] + " -" + jsonData[0]["a"]
    return quote

def getTruth():
    response = requests.get("https://api.truthordarebot.xyz/v1/truth")
    jsonData = response.json()

    question = str(jsonData["question"])
    rating = str(jsonData["rating"])

    return [question, rating]

def getDare():
    response = requests.get("https://api.truthordarebot.xyz/api/dare")
    jsonData = response.json()

    question = str(jsonData["question"])
    rating = str(jsonData["rating"])

    return [question, rating]

# Stuff which can be said on &hello
helloMsgs = ["Hi!", "Hello, world!", "Nice to meet you!", "Hello", "Hiii"]

# Stuff with can be said on &thanks
thanksMsgs = ["You're welcome!", "Anytime", "Thank YOU!", "Welcome pal!"]

truth = {"pg": ["If you had a chance to switch souls with a random person, with who would you swap",
               "What is your favorite flavour of icecream?",
               "What is one video that you regret watching?",
               "What is one picture that you regret seeing?",
               "Send your most favorite emote",
               "Who do you not want in your life?",
               "What is your favorite subject in school?",
               "What is your ambition?",
               "Who is the most unique person you have met in this world?",
               "Who do you feel pity for?"],
         "pg13": ["One morning, you wake up as your opposite gender. What would you do?",
                 "If a random person proposes to you, what would be your reaction?",
                 "Who in this server do you want to propose to you?",
                 "Decribe your crush, but don't give it away",
                 "Are you sure about marrying your crush/BF/GF in the future?",
                 "Who was your first celebrity crush?",
                 "What's the strangest dream you've had?",
                 "Type out the first word that comes to your mind",
                 "Who do you really this is a playboy?",
                 "Who is most likely to be in a secret relationship/have a secret crush here?",
                 "Who was your first crush? Did it go out well?"],
         "r": ["If you had to fuck a person here, who would you?",
              "Have you ever been alone in a room with your partner?",],
        }

dare = {
    "pg": ["Tell a lie", 
          "Annoy one of your friends", 
          "Act as if you have had a memory loss for the next 5 rounds",
          "Listen to the song recommended by the person who answers with a song first in the VC",
          "Reveal your deepest secret to the group",
          "Imitate the teacher you hate the most",
          "Imitate the teacher you like the most",
          "Imitate someone everyone knows until everyone finds the person you are imitating"],
    "pg13": ["Call your ex and ask them can we start again",
            "Tell your crush you like them over text. Screenshot the conversation",
            "Write a short love poem",
            "Change the status in discord praising the person who used the command",
            "Flirt with your crush, and send the screenshot here",
            "Chat as if you are chatting with your crush/gf/bf for the next minute"],
}

# This line is called everytime some event occurs
@client.event
# If the bot is ready to respond
async def on_ready():
    print("Logged in as {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='&help'))


# If there is any message
@client.event
async def on_message(message):
    # Turning the message to lower case
    # message = message.lower()

    # The message is not by us, instead a user
    if message.author == client.user:
        return
        
    def randomRating(type):
        if type == 0:
            num = round(random.randint(0, 1))
        elif type == 1:
            num = round(random.randint(0, 2))
                
        if num == 0:
            return 'pg'
        elif num == 1:
            return 'pg13'
        elif num == 2:
            return 'r'
        
    # If the user entered &hello
        
    if message.content.startswith("&hello"):
        await message.reply(helloMsgs[round(random.randint(0, len(helloMsgs) - 1))], mention_author=True)
        
    # If the user entered help
    elif message.content.startswith("&help"):

        helpMenu = discord.Embed(title="Help Menu", description="Here to help you with the commands!", color=0xfffb00)

        commands = ["&help", "&hello", "&whats", "&quote", "&meme", "&random", "&tod", "&truth", "&dare"]
        descriptions = ["Returns a list of available commands for Disbot",
                        "Returns a kind greeting!",
                        "Returns information about something. Use like this: \n`&whats *subject*, *number of lines`",
                        "Returns an inspiring quote!",
                        "Returns a meme",
                        "Returns a random number from the range specified. Use like this: \n`&random *minimum number in range*, *maximum number in range*`",
                       "Returns a Truth or a Dare Question",
                       "Returns a Truth Question (add `custom` at the end to return a custom added truth question)",
                       "Returns a Dare (add `custom` at the end to return a custom added dare)"]
        
        i = 0
        while i < len(commands) and i < len(descriptions):
            helpMenu.add_field(name=commands[i], value=descriptions[i])
            i += 1

        await message.reply(embed=helpMenu, mention_author=True)

    # If the user entered &find
    
    elif message.content.startswith("&whats"):
        pageError = False
        removeCmd = message.content.replace("&whats", "")
        subject = removeCmd.split(",")

        if len(subject) == 1:
            sents = 1
        else:
            sents = int(subject[1])

        try:
            s = subject[0]
            p = str(wiki.summary(s, sentences=sents))
        except wiki.DisambiguationError as e:
            s = random.choice(e.options)
            p = str(wiki.summary(s, sentences=sents))
        except wiki.exceptions.PageError:
            p = "No results found!"
            pageError = True

        if pageError == False:
            link = wiki.page(s).url
            title = wiki.page(s).title
            # subjectImg = wiki.page(s).images[0]

            wikiEmbed = discord.Embed(title=title, url=link, description=p, color=0x00ffdd)
            # wikiEmbed.set_image(url=subjectImg)
        elif pageError == True:
            wikiEmbed = discord.Embed(description="No results found!\n*Not the answer you excepted? Try being **more specific** next time!*", color=0xff0000)

        await message.reply(embed=wikiEmbed, mention_author=True)

    # If the user entered &quote
    
    elif message.content.startswith("&quote"):
        answer = getQuote()
        await message.reply(answer, mention_author=True)

    # If the user entered &thanks
    
    elif message.content.startswith("&thanks"):
        await message.reply(thanksMsgs[round(random.randint(0, len(thanksMsgs) - 1))], mention_author=True)

    
    elif message.content.startswith("&meme"):
        response_2 = requests.get("https://meme-api.herokuapp.com/gimme")
        json_data_2 = response_2.json()
        meme_url = str(json_data_2['url'])
        meme_title = str(json_data_2['title'])
        meme_author = str(json_data_2['author'])
        meme_nsfw = json_data_2['nsfw']

        # Creating an embed
        if meme_nsfw == False:
            embedding = discord.Embed(title=meme_title, url=json_data_2['postLink'],
                                      description="Post By: {0}".format(meme_author))
            embedding.set_image(url=meme_url)
            await message.reply(embed=embedding, mention_author=True)

        elif meme_nsfw == True:
            await message.reply(
                "This meme is potentially NSFW. If you'd like to view it, use this link: ||" + meme_url + "||\n\n**You have been warned!**", mention_author=False)

    
    elif message.content.startswith("&random"):
        removeCmd = message.content.replace("&random", "")
        rnge = removeCmd.split(",")
        
        try: 
            if len(rnge) == 1:
                minNum = 0
                maxNum = int(rnge[0])
            elif len(rnge) == 2:
                minNum = int(rnge[0])
                maxNum = int(rnge[1])

            randNumEmbed = discord.Embed(title="The number is " + str(round(random.randint(minNum, maxNum))), color=0x00a8db)
        
        except ValueError:
            randNumEmbed = discord.Embed(title="Invalid Input", description="Please check if you have entered a valid number for the range and try again!", color=0xdb3300)

        await message.reply(embed=randNumEmbed, mention_author=True)

    
    elif message.content.startswith("&tod"):
        tod = random.randint(0, 1)

        question = ''
        rating = ''
        type = ''
        
        choice = round(random.randint(0, 1))
        print(choice)

        if choice == 0:
            
            rating = randomRating(tod)
            
            if tod == 0:
                qnNum = round(random.randint(0, len(truth[str(rating)]) - 1))
                type = "Truth"
                question = truth[str(rating)][qnNum]
            
            if tod == 1:
                qnNum = random.randint(0, len(dare[rating]) - 1)
                type = "Dare"
                question = dare[str(rating)][qnNum]

        elif choice == 1:
            # truth
            if tod == 0:
                truthVar = getTruth()

                question = truthVar[0]
                rating = truthVar[1]
                type = "Truth"
            # dare
            elif tod == 1:
                dareVar = getDare()

                question = dareVar[0]
                rating = dareVar[1]
                type = "Dare"
        
        todEmbed = discord.Embed(title=question, description=str(type) + " | " + str(rating).upper(),color=0xfcf400)
        
        await message.reply(embed=todEmbed, mention_author=True)
        

# So that the bot can run!

    elif message.content.startswith("&truth"):
        removeCmd = message.content.replace("&truth", "")

        if "custom" in removeCmd:
            rating = randomRating(1)

            questionNum = round(random.randint(0, len(truth[rating]) - 1))
            question = truth[str(rating)][questionNum]
        else:
            choice = random.randint(0, 1)

            if choice == 0:
                truthQn = getTruth()
    
                question = truthQn[0]
                rating = truthQn[1]
            else:
                rating = randomRating(1)

                questionNum = round(random.randint(0, len(truth[rating]) - 1))
                question = truth[str(rating)][questionNum]

        todEmbed = discord.Embed(title=question, description="Truth | " + str(rating).upper(),color=0xfcf400)
        
        await message.reply(embed=todEmbed, mention_author=True)

    elif message.content.startswith("&dare"):
        removeCmd = message.content.replace("&dare", "")

        if "custom" in removeCmd:
            rating = randomRating(0)

            questionNum = random.randint(0, len(dare[rating]) - 1)
            print(questionNum)
            print(rating)
            question = dare[str(rating)][questionNum]
        else:
            choice = random.randint(0, 1)

            if choice == 0:
                truthQn = getDare()
    
                question = truthQn[0]
                rating = truthQn[1]
            else:
                rating = randomRating(0)

                questionNum = random.randint(0, len(dare[rating]) - 1)
                print(questionNum)
                print(rating)
                question = dare[str(rating)][questionNum]

        todEmbed = discord.Embed(title=question, description="Dare | " + str(rating).upper(),color=0xfcf400)
        
        await message.reply(embed=todEmbed, mention_author=True)

client.run(os.getenv("token"))