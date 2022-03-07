#
#  Bulonebot
#  Bulone discord bot.
#  Copyright  Patrick Huang  2022
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import asyncio
import random
import discord
from context import Context


async def readwrite(ctx: Context):
    await ctx.send("Read and", 3)
    if random.randint(0, 3) == 3:
        await ctx.send("Let's try that again. Remember, it needs to be like the breaks on a car. "
            "If they don't work, the car will crash, just like your Java program.", 2)
        await ctx.send("Read and", 3)
    await ctx.send("Write", 4)


async def greetings(ctx: Context):
    await ctx.send("Hi everyone. Please form three straight lines in front of the door.", 8)
    for mem in ctx.chn.members:
        if mem.status != discord.Status.offline and mem.name != "BuloneBot":
            greet = random.choice(ctx.json("greetings"))
            await ctx.send(f"{greet} {mem.name}", random.uniform(1, 3))

    for i in range(3):
        await ctx.send(f"Line {i+1}, come on in.", random.uniform(1, 3))


async def schedule(ctx: Context):
    activities = ctx.json("activities")
    homework = ctx.json("homework")

    agenda = "Here's what we're going to be doing today:\n"
    agenda += "* We will be having some time for writing prompts and the turn and talk time like usual.\n"
    for act in random.sample(activities, random.randint(1, len(activities))):
        agenda += "* We will " + act + "\n"
    await ctx.send(agenda, 12)

    hw = "Homework for today is:\n"
    hw += "* Finish the writing prompt from today.\n"
    for h in random.sample(homework, random.randint(1, len(homework))):
        hw += "* " + h + "\n"
    await ctx.send(hw, 12)

    if random.randint(0, 1) == 0:
        await ctx.send("Nod your head if you understand.", 2)
    else:
        await ctx.send("Summarize in your own words to the people next to you what I just said.", 2)
    await asyncio.sleep(4)


async def wprompt(ctx: Context):
    quote = random.choice(ctx.json("quotes"))
    exclam = ctx.json("exclam")

    if ctx.voice:
        path, author, title = ctx.rand_piece()
        await ctx.send("Our prompt for today will be a section of a piano piece.", 1)
        await ctx.send(f"The piece we will be listening to is {title} by {author}.", 3)
        await ctx.play_audio(path)
        await ctx.send("Think about it. If it gives you any ideas, write about it. Otherwise, "
            "write about any school appropriate topic.", 1)
        await ctx.send("I will come around to check your writing prompts from last time.", 2)
        await asyncio.sleep(45)
    else:
        await ctx.send("Please copy down the quote you see. If it gives you any ideas, "
            "start writing. Otherwise, write about any school appropriate topic.", 1)
        await ctx.send("I will come around to check your writing prompts from last time.", 2)
        await ctx.send(f"Quote: **{quote}**", 45)
    await readwrite(ctx)

    await ctx.send("You have 30 seconds to share what you wrote about with your "
        "neighbors. After that, I will call on 3 randoms, and we'll open it up to "
        "volunteers.", 3)
    await asyncio.sleep(30)
    await readwrite(ctx)

    members = [m.name for m in ctx.chn.members if m.status != discord.Status.offline and m.name != "BuloneBot"]
    n_members = min(len(members), 3)
    peeps = random.sample(members, n_members)
    for i, peep in enumerate(peeps):
        await ctx.send(f"Person {i+1} is **{peep}**. You have 20 seconds to share.", 2)
        await asyncio.sleep(20)
        if random.randint(0, 4) == 0:
            await ctx.send(f"Interesting. Everybody say {random.choice(exclam)}", 6)
        elif random.randint(0, 4) == 0:
            await ctx.send(f"Raise your hand if you can relate to this.", 6)

    if random.randint(0, 3) == 0:
        await ctx.send("Keep in mind that the grading report is coming up, so you may need some participation points.", 5)
    await ctx.send("Now, are there any volunteers? You have 60 seconds to share. ", 2)
    await asyncio.sleep(45)


async def start(ctx: Context):
    await ctx.send("BuloneBot: The Bulone experience on Discord.", 4)

    await greetings(ctx)
    await readwrite(ctx)
    await schedule(ctx)
    await readwrite(ctx)
    await wprompt(ctx)
    await readwrite(ctx)

    await ctx.send("Done", 1)
