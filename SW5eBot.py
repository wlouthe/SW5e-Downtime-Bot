import discord
import asyncio
import math
import random
import re

f = open("botkey","r")

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    random.seed()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('$sw'):
        txt = message.content.split()
        txt.pop(0)
        skillbonus = []
        minScore = 0
        maxAttempts = 3
        rollMod = 0
        rollMod100 = 0
        job = ""
        output = ""
        comp = False
        altcomp = False
        complicationRoll = random.randrange(1,6)
        complicationDie = "1d6"
        complicationChance = 1
        complicationModifier = -1
        rollCt = 1
        myTotal = 0
        dcmod = 0
        adv = False
        disadv = False
        argCt = 0
        isCheater = False

        if len(txt)<1:
            await message.channel.send("Please include some arguments. Type '$sw help' for detailed usage information. Type '$sw examples' for some common usage demonstration.")
            return

        if txt[0] == "help":
            await message.author.send('''
Start a sentence with **$sw** to make sure the bot is listening, then the following commands can be used separated  by spaces

**"$sw examples"** will send you some examples of some common commands you might run.

**"roll:[skill bonus]"** (i.e. roll:8) to roll a basic skill. if you want to try multiple attempts but need a different skill each time (i.e. racing), try roll:[skill1]:[skill2]:[skill3]. Note: **min** is required for multiple rolls

**"min:[mod]"** modifier can be used to specify number the minimum modifier you want to accept. Difficulty does increase by 5 with each roll. Normal modifiers are as follows:
    DC:Mod
    10:+5
    15:+10
    20:+15
    25:+20
    30:+25

For example:"$sw roll:6 min:5" would roll until at least a 5 modifier is attained (attempting to get at least a 10, 15, then 20 on each of its attempts, stopping on success or continuing until 3 attempts are made).

**"max:[number]"** modifier specifies the maximum number of rolls you would like to make at most (requires use of min).

**"job:[name]"** modifier will help fill in the specifics of what you're rolling for and their results. The list of jobs you can enter as of now are:
bh (bounty hunter)
carousing
crafting
crime
espionage
gambling
merc
pitfight
race
research
training
work if you are making a second or third roll without the use of the min function
''')
            await message.author.send('''
"mod:[num]" can be used to add or subtract an additional modifier to the roll (such as bounty hunters extra credit bonus) or any other modifiers you may have/ been granted by your DM

"mod100:[num]" adds a modifier directly into the final d100 roll. Most likely used with crafting items using the table found below.

Crafting
Rarity     d100 Roll Modifier
Standard                +10
Premium                 +0
Prototype                -10
Advanced               -20
Legendary              -30
Artifact                   -40

"dcmod:[num]" should be used if you want to roll individually or there is some other increase the the difficulty. dcmod:5 or dcmod:10 should be used if you are making a second or third roll without the use of the min function

"comp" will print out a complication roll. if a job is specified, the complications for a class will be printed out

"comp:[num]" will call comp and set the % chance of getting a complication you can either put in the d10 number or the percent (i.e. comp:3 and comp:30 both give a 3/10 chance for a complication) and will override any other percent (for example if youre working with a shady dealer when buying/selling enhanced items have a 50% complication chance)

"altcomp" is a method for ignoring normal complications instead getting disadvantage on your next downtime roll if you get a complication.

"adv" or "disadv" for (dis)advantage on all your d20 rolls


Finally, an example of a standard complete command might be "$sw roll:8:6 min:5 job:race comp". This command would be for someone with perhaps an 8 in mechanics tools, and a 6 in piloting and tech (thus the roll:8:6), who wants to reroll to try and get at least a +5 to his roll modifier (hence min:5) but doesnt want to risk failing 3 times, which is only why they rolled twice (roll:8:6) instead of 3 times (roll:8:6:6). job:race specifies that this is to be done in racing, and comp then specifies that you want to see any of the resulting complications.
''')
            return
        if txt[0] == "examples":
            await message.author.send('''
Some example commands you could try are as follows:

Racing, with a skill in mechanic's kit being 8, piloting 4, and technology 6, also assuming that you want to try to get at least a +5 if you can, but dont want to risk a full 30% chance to get a complication you could try

**$sw roll:8:6:4 min:5 job:race comp**

If youre crafting, making a standard enhanced item with tools that you have a +10 in, you could try

**$sw roll:10 job:crafting mod100:10 comp**

You have advantage on investigation (with a skill of +12) checks and are doing some mercenary detective work, you could try

**$sw roll:12 job:merc comp adv**

You're bounty hunting(+11 skill) and want better odds at finding your mark so you pay an extra 1000cr for an increase to your mod.

**$sw roll:11 job:bh comp  mod:2**

You want to roll one at a time (given the racing scenario before) and decide if you want to try again manually (you should announce this before hand, ignoring the d100 roll and rolling your own after).

**$sw roll:8 job:race"**
then
**$sw roll:6 job:race dcmod:5**
then
**$sw roll:4 job:race dcmod:10**
and then roll a d100 and add your final kept result

Assuming that you rolled 3 times in the last scenario and only want to see the results, try
**$sw job:race comp:3**
''')
            return
        output=str(message.author.mention) + "(" + str(message.author) + "): '**" + str(message.content) + "**'\n"
        await message.delete()
        txt.sort()
        for x in txt:
            if x.startswith("adv"):
                    adv = True
                    continue

            if x.startswith("disadv"):
                    disadv = True
                    continue

            if x.startswith("comp"):
                comp = True
                temp = x.split(":")
                if len(temp)>1:
                    try:
                        temp = temp.pop()
                        if int(temp) > 100:
                            complicationModifier = 10
                        else:
                            complicationModifier = int(temp) if int(temp)<10 else math.floor(int(temp)/10)
                        argCt+=1
                    except:
                        await message.channel.send("the bonus roll mod must be a number")

            if x.startswith("altcomp"):
                comp = True
                altcomp = True
                temp = x.split(":")
                if len(temp)>1:
                    try:
                        temp = temp.pop()
                        if int(temp) > 100:
                            complicationModifier = 10
                        else:
                            complicationModifier = int(temp) if int(temp)<10 else math.floor(int(temp)/10)
                        argCt+=1
                    except:
                        await message.channel.send("the bonus roll mod must be a number")

            if x.startswith("dcmod"):
                temp = x.split(":")
                if len(temp)>1:
                    try:
                        temp = temp.pop()
                        dcmod += (-1 if temp.startswith("-") else 1)*(int(temp.replace("-","").replace("+","")))
                    except:
                        await message.channel.send("the bonus DC mod must be a number")

            if x.startswith("job"):
                temp = x.split(":")
                if len(temp)>1:
                    job = temp.pop()#.decode("utf8","ignore")
                    if job == "bh":
                        output+="Upfront cost: 500cr, +500cr for an additional +1 to roll modifier\n"
                    elif job == "carousing":
                        output+="Upfront cost: 100 (low class), 500 (middle class), or 2500 (upper class)cr\n"
                    elif job == "crafting":
                        output+="Upfront cost: varies\n"
                    elif job == "crime":
                        output+="Upfront cost: 250cr\n"
                    elif job == "espionage":
                        output+="Upfront cost: 100 (low class), 500 (middle class), or 2500 (upper class)cr\n"
                    elif job == "gambling":
                        output+="Upfront cost: 100-10000cr\n"
                    elif job == "merc":
                        output+="Upfront cost: 100cr\n"
                    elif job == "race":
                        output+="Upfront cost: 250cr fee, speeder rental 1000cr\n"
                    elif job == "research":
                        output+="Upfront cost: 500cr\n"
                    elif job == "training":
                        output+="Upfront cost: varies\n"
                    else:
                        continue
                    continue

            #if x.startswith("max"):
            #    temp = x.split(":")
            #    if len(temp) > 1:
            #        try:
            #            maxAttempts = int(temp.pop())
            #            continue
            #        except ValueError:
            #            await message.channel.send("If max is used, it must be a number")

            if x.startswith("min"):
                temp = x.split(":")
                if len(temp) > 1:
                    try:
                        minScore = int(temp.pop().replace("+",""))
                        minScore-=minScore%5
                        continue
                    except ValueError:
                        await message.channel.send("If min is used, it must be a positive number")

            if x.startswith("mod"):
                if x.startswith("mod100"):
                    temp = x.split(":")
                    if len(temp)>1:
                        try:
                            temp = temp.pop()
                            rollMod100 += (-1 if temp.startswith("-") else 1)*(int(temp.replace("-","").replace("+","")))
                        except:
                            await message.channel.send("the bonus roll mod must be a number")
                else:
                    temp = x.split(":")
                    if len(temp)>1:
                        try:
                            temp = temp.pop()
                            rollMod += (-1 if temp.startswith("-") else 1)*(int(temp.replace("-","").replace("+","")))
                        except:
                            await message.channel.send("the bonus roll mod must be a number")

            if x.startswith('roll'):
                temp = x.split(":")
                if len(temp)>1:
                    temp.pop(0)
                    try:
                        for y in temp:
                            skillbonus.append(int(y))
                            argCt+=1

                    except ValueError:
                        await message.channel.send("Skill bonuses must be numbers")
                        return

            if x.startswith("single"):
                continue

        if argCt==0:
            await message.channel.send("The arguments used either are incorrect or dont work on their own. Type '$sw help' for detailed usage information. Type '$sw examples' for some common usage demonstration.")
            return

        if len(skillbonus)!=0:

            myd20=[random.randrange(1,20),random.randrange(1,20),random.randrange(1,20)]

            for x in skillbonus:
                tRoll = myd20.pop()
                if (adv):
                    tRollArray = [tRoll,random.randrange(1,20)]
                    tRollArray.sort()
                    tRollArray.reverse()
                    myTotal = tRollArray[0]+x+rollMod
                    output+="Rolling 2d20KH1(**"+str(tRollArray[0])+"**/"+str(tRollArray[1])+")+skill(**"+str(x)+"**)"
                elif (disadv):
                    tRollArray = [tRoll,random.randrange(1,20)]
                    tRollArray.sort()
                    myTotal = tRollArray[0]+x+rollMod
                    output+="Rolling 2d20KL1(**"+str(tRollArray[0])+"**/"+str(tRollArray[1])+")+skill(**"+str(x)+"**)"
                else:

                    myTotal = tRoll+x+rollMod
                    output+="Rolling 1d20(**"+str(tRoll)+"**)+skill(**"+str(x)+"**)"

                if rollMod != 0:
                    output+=("-" if rollMod<0 else "+")+"mods(**"+str(rollMod)+"**)"
                output+="=**"+str(myTotal)+"**... modifier=**+"
                myTotal = myTotal-(5*(rollCt))-dcmod-(myTotal%5)
                if myTotal < 0:
                    myTotal = 0
                if myTotal > 25:
                    myTotal = 25

                output+=""+str(myTotal)+"**"

                if minScore != 0:
                    output+=" : DC:"+str(minScore+dcmod+rollCt*5)+" for +" +str(minScore)
                elif dcmod !=0:
                    output+=" : DC:+"+str(dcmod)

                output+="\n"

                if myTotal >= minScore:
                    break

                if rollCt == maxAttempts:
                    break

                rollCt+=1

            complicationChance = rollCt


            myd100 = random.randrange(1,100)
            if (disadv):
                myd100RollArray = [myd100, random.randrange(1,100)]
                myd100RollArray.sort()
                output+="Rolling 2d100KL1(**"+str(myd100RollArray[0])+"**/"+str(myd100RollArray[1])+")"
                if rollMod100 != 0:
                    output+="+mod(**"+str(rollMod100)+"**)"
                output+="+result(**"+str(myTotal)+"**)=**"
                myResult = myd100RollArray[0]+myTotal+rollMod100
                output+=str(myResult)+"**\n"
            else:
                output+="Rolling d100(**"+str(myd100)+"**)"
                if rollMod100 != 0:
                    output+="+mod(**"+str(rollMod100)+"**)"
                output+="+result(**"+str(myTotal)+"**)=**"
                myResult = myd100+myTotal+rollMod100
                output+=str(myResult)+"**\n"

        if job != "":

            if job == "buyenhanced":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You fail to catch your target.\n"
                    elif myResult <=70:
                        output+="You fail to catch your target, but stumble across a lesser bounty, earning 500 cr.\n"
                    elif myResult <=100:
                        output+="You catch your target, resulting in a 1,000 cr bounty.\n"
                    elif myResult <=110:
                        output+="You catch a high-value target, resulting in a 2,500 cr bounty.\n"
                    else:
                        output+="You catch a kingpin, resulting in a 10,000 cr bounty and a nickname.\n"

                complicationChance = 1

                if complicationRoll == 1:
                    complicationTxt = "Your quarry swears up-and-down that you’ve got the wrong person."
                elif complicationRoll == 2:
                    complicationTxt = "Your target manages to escape after you’ve collected your bounty, and they are coming for you."
                elif complicationRoll == 3:
                    complicationTxt = "Your target was very valuable to a crime boss, and they’ve sworn to take revenge on you."
                elif complicationRoll == 4:
                    complicationTxt = "Your target had connections with an esteemed noble family, and they’re publicly besmirching you."
                elif complicationRoll == 5:
                    complicationTxt = "Your target was a high-ranking member of a guild. You’ve earned their ire."
                else:
                    complicationTxt = "Another bounty hunter was also on the hunt. You just barely beat them, and they’re not happy."

            if job == "sellenhanced":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="A buyer offering one-quarter of the item’s value, or a shady buyer offering half the item’s value.\n"
                    elif myResult <=70:
                        output+="A buyer offering half the item’s value, or a shady buyer offering the full item’s value.\n"
                    elif myResult <=100:
                        output+="A buyer offering the full item’s value.\n"
                    elif myResult <=110:
                        output+="A shady buyer offering one and a half times the item’s value, no questions asked.\n"
                    else:
                        output+="A buyer offering one and a half times the item’s value, but they also want a favor.\n"

                complicationChance = 1

                if complicationRoll == 1:
                    complicationTxt = "The item is perceived as a fake."
                elif complicationRoll == 2:
                    complicationTxt = "The item is stolen before the sale."
                elif complicationRoll == 3:
                    complicationTxt = "The item is a relic cursed by a dark entity."
                elif complicationRoll == 4:
                    complicationTxt = "The item’s original owner will kill to reclaim it; the party’s enemies spread news of the transaction."
                elif complicationRoll == 5:
                    complicationTxt = "The other party is murdered before the transaction is completed."
                else:
                    complicationTxt = "A third party enters the transaction, offering an alternative item."

            if job == "bh":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You fail to catch your target.\n"
                    elif myResult <=70:
                        output+="You fail to catch your target, but stumble across a lesser bounty, earning 500 cr.\n"
                    elif myResult <=100:
                        output+="You catch your target, resulting in a 1,000 cr bounty.\n"
                    elif myResult <=110:
                        output+="You catch a high-value target, resulting in a 2,500 cr bounty.\n"
                    else:
                        output+="You catch a kingpin, resulting in a 10,000 cr bounty and a nickname.\n"

                complicationChance = 1

                if complicationRoll == 1:
                    complicationTxt = "Your quarry swears up-and-down that you’ve got the wrong person."
                elif complicationRoll == 2:
                    complicationTxt = "Your target manages to escape after you’ve collected your bounty, and they are coming for you."
                elif complicationRoll == 3:
                    complicationTxt = "Your target was very valuable to a crime boss, and they’ve sworn to take revenge on you."
                elif complicationRoll == 4:
                    complicationTxt = "Your target had connections with an esteemed noble family, and they’re publicly besmirching you."
                elif complicationRoll == 5:
                    complicationTxt = "Your target was a high-ranking member of a guild. You’ve earned their ire."
                else:
                    complicationTxt = "Another bounty hunter was also on the hunt. You just barely beat them, and they’re not happy."

            if job == "carousing":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You make a hostile contact.\n"
                    elif myResult <=70:
                        output+="You make no new contacts.\n"
                    elif myResult <=100:
                        output+="You make an allied contact.\n"
                    elif myResult <=110:
                        output+="You make two allied contacts.\n"
                    else:
                        output+="You make three allied contacts.\n"

                complicationChance = 1
                complicationDie = "1d8"
                complicationRoll = random.randrange(1,8)

                if complicationRoll == 1:
                    complicationTxt = "Low:A pickpocket lifts 1d10 (***"+str(random.randrange(1,10))+"***) x 50 cr from you. | Medium: You accidentally insulted a guild master, and only a public apology will let you do business with the guild again. | High: A pushy noble family wants to marry off one of their scions to you."
                elif complicationRoll == 2:
                    complicationTxt = "Low: A bar brawl leaves you with a scar. | Medium: You swore to complete some quest on behalf of a guild. | High: You tripped and fell during a dance, and people can't stop talking about it."
                elif complicationRoll == 3:
                    complicationTxt = "Low: You have fuzzy memories of doing something very, very illegal, but you can't remember exactly what. | Medium: A particularly obnoxious person has taken an intense romantic interest in you. | High: You have agreed to take on a noble's debts."
                elif complicationRoll == 4:
                    complicationTxt = "Low: You are banned from a cantina for some obnoxious behavior. | Medium: A social gaffe has made you the talk of the town. | High: You have been challenged to a duel by an embarrassed nobleman."
                elif complicationRoll == 5:
                    complicationTxt = "Low: After a few drinks, you swore in a public place to pursue a dangerous quest. | Medium: You have made a foe out of a local bounty hunter. | High: You have made a foe out of a local noble."
                elif complicationRoll == 6:
                    complicationTxt = "Low: Surprise! You're married. | Medium: You have been recruited to help run a local festival, play, or similar event. | High: A boring noble insists you visit each day and listen to long, tedious expositions on lineage."
                elif complicationRoll == 7:
                    complicationTxt = "Low: Streaking naked through the streets seemed like a great idea at the time. | Medium: You made a drunken toast that scandalized the locals. | High: You have become the target of a variety of embarrassing rumors."
                else:
                    complicationTxt = "Low: Everyone is calling you by some weird, embarrassing nickname, like Puddle Drinker or Bench Slayer, and no one will say why. | Medium: You spent an additional 1,000 cr trying to impress people. | High: You spent an additional 5,000 cr trying to impress people."

            if job == "crafting":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You inefficiently craft the item, expending twice the requisite raw materials.\n"
                    elif myResult <=70:
                        output+="You inefficiently craft the item, expending one and a half times the requisite raw materials.\n"
                    elif myResult <=100:
                        output+="You craft the item with no significant issue.\n"
                    elif myResult <=110:
                        output+="You efficiently craft the item, using only half the requisite materials. If the item required a rare material, you also used a reduced amount of that material.\n"
                    else:
                        output+="You expertly craft the item, using only one-quarter the requisite materials. If the item required a rare material, you also used a reduced amount of that material.\n"

                complicationChance = 1

                if complicationRoll == 1:
                    complicationTxt = "Rumors swirl that what you’re working on is unstable and a threat to the community."
                elif complicationRoll == 2:
                    complicationTxt = "Your tools are stolen, forcing you to buy new ones."
                elif complicationRoll == 3:
                    complicationTxt = "An affluent craftsman shows keen interest in your work and insists on observing you."
                elif complicationRoll == 4:
                    complicationTxt = "A powerful wealthy individual offers a heft price for your work and is not interested in hearing no for an answer."
                elif complicationRoll == 5:
                    complicationTxt = "	A noteworthy craftsman accuses you of stealing its secret knowledge to fuel your work."
                else:
                    complicationTxt = "A competitor spreads rumors that your work is shoddy and prone to failure."

            if job == "crime":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="The robbery fails, but you escape.\n"
                    elif myResult <=70:
                        output+="You earn 500 cr by robbing a struggling merchant.\n"
                    elif myResult <=100:
                        output+="You earn 1,000 cr by robbing a prosperous figure.\n"
                    elif myResult <=110:
                        output+="You earn 2,500 cr by robbing a noble.\n"
                    else:
                        output+="You earn 10,000 cr by robbing one of the richest figures in town.\n"

                complicationDie = "1d8"
                complicationRoll = random.randrange(1,8)
                complicationChance = rollCt

                if complicationRoll == 1:
                    complicationTxt = "A bounty equal to your earnings is offered for information about your crime."
                elif complicationRoll == 2:
                    complicationTxt = "An unknown person contacts you, threatening to reveal your crime if you don’t render a service."
                elif complicationRoll == 3:
                    complicationTxt = "Your victim is financially ruined by your crime."
                elif complicationRoll == 4:
                    complicationTxt = "Someone who knows of your crime has been arrested on an unrelated matter."
                elif complicationRoll == 5:
                    complicationTxt = "Your loot is a single, easily identifiable item that you can’t fence in this region."
                elif complicationRoll == 6:
                    complicationTxt = "You robbed someone under the protection of a local crime lord, who now wants revenge."
                elif complicationRoll == 7:
                    complicationTxt = "Your victim calls in a favor from a guard, doubling the efforts to solve the case."
                else:
                    complicationTxt = "Your victim asks one of your adventuring companions to solve the crime."

            if job == "espionage":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You fail to find any useful information with which to blackmail, and your face is clearly identified.\n"
                    elif myResult <=70:
                        output+="You find no useful information.\n"
                    elif myResult <=100:
                        output+="You find information with which to blackmail one person.\n"
                    elif myResult <=110:
                        output+="You find information with which to blackmail two people.\n"
                    else:
                        output+="You find information with which to blackmail three people.\n"

                complicationChance = rollCt

                if complicationRoll == 1:
                    complicationTxt = "A bounty equal to the credits spent is offered for information about your crime."
                elif complicationRoll == 2:
                    complicationTxt = "An unknown person contacts you, threatening to reveal your activities if you don’t render a service."
                elif complicationRoll == 3:
                    complicationTxt = "Your victim asks one of your adventuring companions to solve the crime."
                elif complicationRoll == 4:
                    complicationTxt = "Someone who knows of your activities has been arrested on an unrelated matter."
                elif complicationRoll == 5:
                    complicationTxt = "Your victim calls in a favor from a guard, doubling the efforts to solve the case."
                else:
                    complicationTxt = "You blackmailed someone under the protection of a local crime lord, who now wants revenge."

            if job == "gambling":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You lose your entire stake.\n"
                    elif myResult <=70:
                        output+="You lose half your stake.\n"
                    elif myResult <=100:
                        output+="You break even. Not bad.\n"
                    elif myResult <=110:
                        output+="You win an amount equal to your stake.\n"
                    else:
                        output+="You win an amount equal to three times your stake.\n"

                complicationChance = rollCt

                if complicationRoll == 1:
                    complicationTxt = "You are accused of cheating. You decide whether you did cheat or were framed."
                elif complicationRoll == 2:
                    complicationTxt = "The town guards raid the gambling hall and throw you in jail."
                elif complicationRoll == 3:
                    complicationTxt = "A noble in town loses badly to you and loudly vows to get revenge."
                elif complicationRoll == 4:
                    complicationTxt = "You won a sum from a low-ranking member of a nefarious guild, and the guild wants it money back."
                elif complicationRoll == 5:
                    complicationTxt = "A local crime boss insists you start frequenting their gambling parlor, and no others."
                else:
                    complicationTxt = "A high-stakes gambler comes to town and insists that you take part in a game."

            if job == "merc":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="The character finds a job, but fails to complete it successfully and goes unpaid.\n"
                    elif myResult <=70:
                        output+="You complete a relatively simple job, earning 250 cr.\n"
                    elif myResult <=100:
                        output+="You complete a moderately difficult job, earning 500 cr.\n"
                    elif myResult <=110:
                        output+="You complete an exceptionally difficult task, earning 1,250 cr.\n"
                    else:
                        output+="You complete an insanely difficult task, earning 5,000 cr and a favor from your employer.\n"

                complicationChance = rollCt

                if complicationRoll == 1:
                    complicationTxt = "You manage to offend a bystander with an innocuous comment, and it turns out they’re important."
                elif complicationRoll == 2:
                    complicationTxt = "You have a run-in with the law."
                elif complicationRoll == 3:
                    complicationTxt = "You beat out another individual who wanted your job, earning their ire."
                elif complicationRoll == 4:
                    complicationTxt = "Your boss works for a local criminal organization, and insists you perform further work for them."
                elif complicationRoll == 5:
                    complicationTxt = "Another person offers to pay you to fail in your task."
                else:
                    complicationTxt = "You are forced into a physical altercation, resulting in a scar."

            if job == "pitfight":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You lose all of your bouts.\n"
                    elif myResult <=70:
                        output+="You win some of your bouts, earning 250 cr.\n"
                    elif myResult <=100:
                        output+="You win half of your bouts, earning 500 cr.\n"
                    elif myResult <=110:
                        output+="You win most of your bouts, earning 1,500 cr.\n"
                    else:
                        output+="You go undefeated, earning 5,000 cr and a title recognized by the people of this town.\n"

                complicationChance = rollCt

                if complicationRoll == 1:
                    complicationTxt = "An opponent swears to take revenge on you."
                elif complicationRoll == 2:
                    complicationTxt = "A crime boss approaches you and offers to pay you to intentionally lose a few matches."
                elif complicationRoll == 3:
                    complicationTxt = "You defeat a popular local champion, drawing the crowd’s ire."
                elif complicationRoll == 4:
                    complicationTxt = "You defeat a noble’s servant, drawing the wrath of the noble’s house."
                elif complicationRoll == 5:
                    complicationTxt = "You are accused of cheating. Whether the allegation is true or not, your reputation is tarnished."
                else:
                    complicationTxt = "You accidentally deliver a near fatal wound to an opponent."

            if job == "race":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You lose all of your races.\n"
                    elif myResult <=70:
                        output+="You win some of your races, earning 500 cr.\n"
                    elif myResult <=100:
                        output+="You win half of your races, earning 1,000 cr.\n"
                    elif myResult <=110:
                        output+="You win most of your races, earning 2,500 cr.\n"
                    else:
                        output+="You go undefeated, earning 10,000 cr and a title recognized by the people of this town.\n"

                complicationChance = rollCt

                if complicationRoll == 1:
                    complicationTxt = "You side-swipe another racer, earning their ire."
                elif complicationRoll == 2:
                    complicationTxt = "A crime boss approaches you and offers to pay you to intentionally lose a few races."
                elif complicationRoll == 3:
                    complicationTxt = "You are accused of cheating. Whether the allegation is true or not, your reputation is tarnished."
                elif complicationRoll == 4:
                    complicationTxt = "You beat a low-ranking member of a nefarious guild, and the guild isn’t happy."
                elif complicationRoll == 5:
                    complicationTxt = "A local crime boss insists you start racing for them, and no others."
                else:
                    complicationTxt = "A renowned racer comes to town and insists on a race."

            if job == "research":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You learn nothing.\n"
                    elif myResult <=70:
                        output+="You learn one piece of lore.\n"
                    elif myResult <=100:
                        output+="You learn two pieces of lore.\n"
                    elif myResult <=110:
                        output+="You learn three pieces of lore.\n"
                    else:
                        output+="You learn five pieces of lore, as well as the relative location of an item worth at least 5,000 cr.\n"

                complicationChance = 1

                if complicationRoll == 1:
                    complicationTxt = "You accidentally damage a rare, fragile source of information."
                elif complicationRoll == 2:
                    complicationTxt = "You offend a scholar, who demands an extravagant gift."
                elif complicationRoll == 3:
                    complicationTxt = "If you had known the source of information was cursed, you never would have opened it."
                elif complicationRoll == 4:
                    complicationTxt = "A scholar becomes obsessed with convincing you of a number of strange theories."
                elif complicationRoll == 5:
                    complicationTxt = "Your actions cause you to be banned from a library or some other academic institution."
                else:
                    complicationTxt = "You uncovered useful lore, but only by promising to complete a dangerous task in return."

            if job == "training":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="Your training falters, advancing only half a workweek towards completion.\n"
                    elif myResult <=70:
                        output+="Your training is adequate, advancing one workweek towards completion.\n"
                    elif myResult <=100:
                        output+="Your training has a breakthrough, advancing two workweeks towards completion.\n"
                    elif myResult <=110:
                        output+="Your training is excellent, advancing three workweeks towards completion.\n"
                    else:
                        output+="Your training is masterful, advancing four workweeks towards completion.\n"

                complicationChance = 1

                if complicationRoll == 1:
                    complicationTxt = "Your earn the ire of another of the teacher’s students."
                elif complicationRoll == 2:
                    complicationTxt = "Your teacher instructs you in rare, archaic methods, which draw comments from others."
                elif complicationRoll == 3:
                    complicationTxt = "Your teacher is a spy sent to learn your plans."
                elif complicationRoll == 4:
                    complicationTxt = "Your teacher is a wanted criminal."
                elif complicationRoll == 5:
                    complicationTxt = "Your teacher is a cruel taskmaster."
                else:
                    complicationTxt = "Your teacher asks for help dealing with a threat."

            if job == "work":
                if len(skillbonus)>0:
                    if myResult <= 40:
                        output+="You earn enough to support a poor lifestyle for the week, with 10 cr left over.\n"
                    elif myResult <=70:
                        output+="You earn enough to support a modest lifestyle for the week, with 50 cr left over.\n"
                    elif myResult <=100:
                        output+="You earn enough to support a comfortable lifestyle for the week, with 100 cr left over.\n"
                    elif myResult <=110:
                        output+="You earn enough to support a wealthy lifestyle for the week, with 200 cr left over.\n"
                    else:
                        output+="You somehow earn enough to support an aristocratic lifestyle for the week, with 500 cr left over.\n"

                complicationChance = 1
                complicationDie = "1d8"
                complicationRoll = random.randrange(1,8)

                if complicationRoll == 1:
                    complicationTxt = "You manage to outperform someone who hpitfightas been working longer than you, and they’re not impressed."
                elif complicationRoll == 2:
                    complicationTxt = "You bump a coworker in a clearly accidental fashion, but they blow it out of proportion, causing everyone to dislike you."
                elif complicationRoll == 3:
                    complicationTxt = "A patron asks for a service not provided by your workplace, and asks for the manager when you try to explain this."
                elif complicationRoll == 4:
                    complicationTxt = "Your manager takes credit for the work you are doing, asserting it is their own."
                elif complicationRoll == 5:
                    complicationTxt = "One of your coworkers slows down their workload so you have to pick up their slack."
                elif complicationRoll == 6:
                    complicationTxt = "You sustain a small injury, resulting in a scar."
                elif complicationRoll == 7:
                    complicationTxt = "Your coworkers, as a group, tell your boss a series of baseless lies. Your boss believes them over you."
                else:
                    complicationTxt = "Your coworkers bestow a nickname on you based on an obscure, mundane thing you did or said. They no longer call you by your name."


        complication = random.randrange(1,10)
        if comp:
            if complicationModifier > 0:
                complicationChance = complicationModifier
            output+="Complication? Chance: "+str(complicationChance)+"0% Rolling 1d10(**"+str(complication)+"**): "+str("yes. " if complication <= complicationChance else "no. ")

            if complication <= complicationChance:
                output+="Result = "+complicationDie+"(**" +str(complicationRoll)+ "**). "
                if job != "" and altcomp == False:
                    output+="\n"+complicationTxt
                if job != "" and altcomp == True:
                    output+="\n***DISADVANTAGE ON NEXT DOWNTIME ROLL!!!***"

        await message.channel.send(output)


client.run(f.read())
