import discord
from discord.ext import commands
import os
import asyncio
from datetime import datetime
from pymongo import MongoClient

from cogs.season1df import get_season1df_score

client = MongoClient("mongodb://localhost:27017/")
db = client["discord_bot"]
reviews_collection = db["reviews"]

class Raiderio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Comanda pentru a verifica review-urile unui jucător pe baza link-ului de Raider.io
    @commands.command(name="check")
    async def check_reviews(self, ctx, *links):
        for link in links:
            if "https://raider.io/characters" not in link:
                await ctx.send("Te rog oferă un links valid de Raider.io")
                continue
            try:
                player_key = link.lower().strip()
                dm_channel = await ctx.author.create_dm()
                await dm_channel.send(f"{link}")

                reviews = self.get_reviews(player_key)

                if reviews:
                    # Calculăm media notelor
                    ratings = [rev['rating'] for rev in reviews]
                    avg_rating = sum(ratings) / len(ratings)
                    await dm_channel.send(f"Rating: **{avg_rating:.2f} / 10.00**")

                    # Afișăm comentariile
                    await dm_channel.send(" Comentarii:")
                    for rev in reviews:
                        await dm_channel.send(f"„{rev['comment']}” – de la <@{rev['user_id']}>")
                else:
                    await dm_channel.send("❌ Nu există încă review-uri pentru acest jucător.")
            except discord.Forbidden:
                await ctx.send("❌ Nu îți pot trimite mesaj în privat. Asigură-te că ai DM-urile activate.")
            except Exception as e:
                print(e)
                
# Comanda pentru a lăsa un review pentru un jucător pe baza link-ului de Raider.io
    @commands.command(name="review")
    async def leave_review(self, ctx, links: str):
        if "raider.io" not in links:
            await ctx.send("Te rog oferă un links valid de Raider.io.")
            return

        player_key = links.lower().strip()

        try:
            dm_channel = await ctx.author.create_dm()
            await dm_channel.send(f"📝 Vrei să lași un review pentru: {links}")

            await dm_channel.send("📌 Scrie o nota de la 1 la 10:")

            def check_rating(user_message):
                # filtrăm doar mesajele de la userul corect în DM
                return user_message.author == ctx.author and user_message.channel == dm_channel

            while True:
                try:
                    rating_msg = await self.bot.wait_for('message', check=check_rating, timeout=60)
                    try:
                        rating = float(rating_msg.content)
                        if 1.0 <= rating <= 10.0:
                            break  
                        else:
                            await dm_channel.send("❌ Salut boss, numărul nu e bun! Te rog pune unul între 1 și 10.")
                    except ValueError:
                        await dm_channel.send("❌ Salut boss, te rog pune unul între 1 și 10.")
                except asyncio.TimeoutError:
                    await dm_channel.send("⏱️ Timpul a expirat, încearcă din nou mai târziu.")
                    return

            await dm_channel.send("💬 Scrie un comentariu scurt despre acest jucător:")

            def check_comment(user_message):
                return user_message.author == ctx.author and user_message.channel == dm_channel

            comment_msg = await self.bot.wait_for('message', check=check_comment, timeout=300)
            comment = comment_msg.content

            self.save_review(player_key, ctx.author.id, rating, comment)
            await dm_channel.send("✅ Mulțumim! Review-ul tău a fost salvat.")

        except discord.Forbidden:
            await ctx.send("❌ Nu îți pot trimite mesaj în privat. Asigură-te că ai DM-urile activate.")
        except asyncio.TimeoutError:
            await dm_channel.send("Timpul a expirat. Te rog încearcă din nou mai târziu.")

    def get_reviews(self, player_key):
        reviews = list(reviews_collection.find({"url": player_key}))
        return reviews

    def save_review(self, player_key, user_id, rating, comment):
        review_doc = {
            "url": player_key,
            "user_id": str(user_id),
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.utcnow().isoformat()
        }
        reviews_collection.insert_one(review_doc)
        
    # Comanda pentru a verifica scorul de Mythic+ al unui jucător în sezonul 1 din Dragonflight
    @commands.command(name="checkdf1")
    async def check_df1(self, ctx, *links):
        for link in links:
            if "https://raider.io/characters" not in link:
                await ctx.send("Te rog oferă un links valid de Raider.io")
                continue
            try:
                player_key = link.lower().strip()
                season1df_score = get_season1df_score(player_key)
                dm_channel = await ctx.author.create_dm()
                await dm_channel.send(f"Season 1 DF Score: {season1df_score}")
            except discord.Forbidden:
                await ctx.send("❌ Nu îți pot trimite mesaj în privat. Asigură-te că ai DM-urile activate.")
            except Exception as e:
                print(e)
        pass

# setup() pentru a înregistra cog-ul
async def setup(bot):
    await bot.add_cog(Raiderio(bot))
