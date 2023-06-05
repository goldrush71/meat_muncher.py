import discord, random, csv, pandas as pd, time

n_images = ['big_biden.jpg', '2.jpg','3.webp','4.webp','5.jpg']
biden_images = []

for image in n_images:
    image = 'biden_images/' + image
    biden_images.append(image)
#jackpot is a gamemode where multiple players put money into a pot, then one is randomly decided to receive all of the money.
#players who put in more money have increased odds of winning, but they can't tip the table completely in their favor. 
#this promotes players to keep raising their bets against each other to achieve their desired odds before the winner is decided.
def check_balance_available(balance, request):
    if request > balance or request < 1:
        return False
    return True

pot = {}
pot_players = [] 
def pot_setup():
    global pot, pot_players
    pot = 0
    pot_players = [] 




class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        #if message.content == 'thank you meat muncher.': await message.channel.send('four days')
        if message.author == self.user:
            return
        if random.randint(0,1023) == 1:
            await message.reply('No.')
            return
        prefix = '!meat '

        if message.content.startswith(prefix):
            command = message.content[len(prefix):]

            if command == 'show me the meat':
                await message.channel.send(f':meat_on_bone: here it is')

            elif command == 'help':
                with open('documentation.txt','rb') as f:
                    await message.channel.send(file=discord.File(f))
    
            elif command.startswith('rd'):
                await message.channel.send(f'{random.randint(1,int(command[2:]))}')

            elif command == 'biden':
                with open(random.choice(biden_images), 'rb') as f:
                    picture = discord.File(f)
                    await message.channel.send(file=picture)

            elif command == 'qb.add' and message.reference is not None:
                mes = await message.channel.fetch_message(message.reference.message_id)
                with open('quotes.csv',mode='a',newline='') as qb:
                    writer = csv.writer(qb)
                    writer.writerow([str(mes.author),mes.content,mes.created_at])
                    await message.channel.send(str([mes.author,mes.content,mes.created_at]))
                
            elif command == 'qb.quotebook':
                with open(file='quotes.csv',mode='rb') as f:
                    await message.channel.send(file=discord.File(f))
                
            elif command == 'qb.random':
                book = pd.read_csv('quotes.csv')
                rows = 0
                for row in book:
                    rows+=1
                row = random.randint(1,rows)
                name = book['userid'][row]
                stuff = book['content'][row]
                dt = book['time'][row]
                await message.channel.send(f'{name} said "{stuff}" on {dt[:19]}')

            elif command.startswith('mc.'):
                mcc = message.content[len(prefix)+len('mc.'):]
                print(mcc)
                wallet_exists = False #all the code here makes sure that there is a wallet before commands are executed
                rowpos = 0 #this is very important
                with open('meatcoin.csv',mode='r+',newline='') as f:
                    reader = csv.reader(f, delimiter=',') # good point by @paco 
                    try: #it has to try here because there's a possibility that the user doesn't have a wallet yet.
                        for row in reader:
                            if row[0] == str(message.author):
                                meatuser = row[0]
                                balance = row[1]
                                wallet_exists = True
                                break
                            rowpos+=1
                        rowpos-=1
                    except: #I don't think this actually solves anything, but the try statement does need to exist. 
                        #Also if the except statement is separate from the following if statement then the code breaks. 
                        print('i never claimed to be different. i only said i was bored')
                    if wallet_exists == False: #so a simple wallet is created, and the balance is set.
                        meatwriter = csv.writer(f)
                        meatwriter.writerow([message.author,10])
                        meatuser = message.author
                        balance = 10

                balance = float(balance)
                if mcc == 'balance':
                    await message.channel.send(f'{meatuser}, your balance is: {str(balance)}:meat_on_bone:')
                    #I think that meatuser and balance will always be defined, but I'm sure I'll eat those words someday.
                
                elif mcc.startswith('bet '):

                    betamnt = int(mcc[len('bet '):])
                    if betamnt <= balance and betamnt >=0:
                        oldbal = balance
                        differ = int(betamnt * (random.randint(-100000,100000)/100000))
                        balance += differ
                        winmes = f'You won {str(differ)} coins!'
                        losemes = f'You lost {str(differ*-1)} coins!'
                        if oldbal < balance:
                            sendmes = winmes
                        else: 
                            sendmes = losemes
                        await message.reply(sendmes + f'\nYour balance is now {balance}:meat_on_bone:')
                    elif betamnt > balance:
                        await message.reply(f"You don't have enough coins to bet that much. Your balance is {balance}:meat_on_bone:")
                    elif betamnt <= 0:
                        await message.reply('No.')

                elif mcc.startswith('pot '):
                    mcpc = mcc[len('pot '):]
                    if mcpc == 'join':
                        pot_players.append(message.author)
                    elif mcpc.startswith('bet '):
                        if check_balance_available(balance, int(mcpc[4:])):
                            betamnt = mcpc[4:]
                            pot
                elif mcc.startswith('transfer '):
                    transfer_receiver = mcc[len('transfer '):mcc.index('#')+4]
                    

                #writing to save meatcoin balance
                df = pd.read_csv("meatcoin.csv")
                df.loc[rowpos, "balance"]=balance
                df.to_csv("meatcoin.csv", index=False)  
                

            else:
                await message.channel.send("Command not recognized.\nUse !meat help for a list of all commands.")
    
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTExNDA0MjEwOTg2MzkyMzcyMg.G5L98E.FVpoioeWRdpF-J9qEI9EwHkg7Lg6ULUyKTQG4k')