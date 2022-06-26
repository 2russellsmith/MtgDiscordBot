# bot.py
import os
import discord
import pathlib
import requests as requests
from urllib.parse import urlparse

from dotenv import load_dotenv
from discord.ext import commands

from comboFinder import combo_finder
print("loading headless browsing")
from headless_browsing import download_link_from_moxfield, download_link_from_manabox
print("done loading headless browsing")


# ENV_LOCATION = str(pathlib.Path(__file__).parent.resolve()) + ".env"
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print("TOKEN: " + TOKEN)
GUILD = os.getenv('DISCORD_GUILD')
print("GUILD: " + GUILD)
client = discord.Client()

bot = commands.Bot(command_prefix='!')
playerWins = {}
playerGamesPlayed = {}
games = []


@bot.command(name='log_game', help='Log a commander game! Params: Winner, list of other players')
async def log_game(ctx, winner: str, loser1: str, loser2: str, loser3: str):
    winner = winner.lower()
    loser1 = loser1.lower()
    loser2 = loser2.lower()
    loser3 = loser3.lower()
    winner_deck = ""
    deck1 = ""
    deck2 = ""
    deck3 = ""

    if "-" in winner:
        winner_deck = winner.split("-")[1]
        winner = winner.split("-")[0]

    if "-" in loser1:
        deck1 = loser1.split("-")[1]
        loser1 = loser1.split("-")[0]

    if "-" in loser2:
        deck2 = loser2.split("-")[1]
        loser2 = loser2.split("-")[0]

    if "-" in loser3:
        deck3 = loser3.split("-")[1]
        loser3 = loser3.split("-")[0]

    games.append({"winner": winner, "winningDeck": winner_deck,
                  "loser1": loser1, "deck1": deck1,
                  "loser2": loser2, "deck2": deck2,
                  "loser3": loser3, "deck3": deck3})
    await ctx.send("Game has been logged! Congrats to " + winner + "! Shuffle up and play again!")


@bot.command(name='winrate', help='Check winrate by putting in players name')
async def winrate(ctx, player: str):
    player = player.lower().split("-")[0]
    if player in playerWins:
        await ctx.send(player + " - Wins:" + str(playerWins[player]) + " Total:" + str(playerGamesPlayed[player]))
    elif player in playerGamesPlayed:
        await ctx.send(player + " - Wins:0 Total:" + str(playerGamesPlayed[player]))
    else:
        await ctx.send(player + " has no logged games")


@bot.command(name='vs_players', help='Check winrate between two people putting in players names')
async def vs_players(ctx, player1: str, player2: str):
    player1 = player1.lower()
    player2 = player2.lower()
    player1wins = 0
    player2wins = 0
    total_games_together = 0
    for game in games:
        if player1 in game.values() and player2 in game.values():
            if game["winner"] == player1:
                player1wins += 1
            if game["winner"] == player2:
                player2wins += 1
            total_games_together += 1

    await ctx.send(player1 + " and " + player2 + " have played " + str(total_games_together) + " game(s) together.\n"
                   + player1 + " has won " + str(player1wins) + ".\n"
                   + player2 + " has won " + str(player2wins) + ".\n")


@bot.command(name='vs_decks', help='Check winrate between two people and their decks putting in players names ('
                                   'russell-rielle jake-lavinia)')
async def vs_decks(ctx, player1input: str, player2input: str):
    player1, player1_deck = player1input.lower().split("-")
    player2, player2_deck = player2input.lower().split("-")
    player1wins = 0
    player2wins = 0
    total_games_together = 0
    for game in games:
        if player1 in game.values() \
                and player2 in game.values()\
                and player1_deck in game.values() \
                and player2_deck in game.values():
            if game["winner"] == player1 and game["winningDeck"] == player1_deck:
                player1wins += 1
            if game["winner"] == player2 and game["winningDeck"] == player2_deck:
                player2wins += 1
            total_games_together += 1

    await ctx.send(player1input + " and " + player2input + " have played " + str(total_games_together) + " game(s) together.\n"
                   + player1input + " has won " + str(player1wins) + ".\n"
                   + player2input + " has won " + str(player2wins) + ".\n")


@bot.command(name='rankings', help='See who is the best')
async def rankings(ctx):
    await ctx.send("Rankings:\n 1) Russell's Rielle Deck \n2) Russell's Gitrog Deck \n3)Russell's Scion of the Ur Dragon"
                   " Deck \n4)Russell's Other Decks \n5) Everyone else's Decks")


@bot.command(name='combofinder', help='Finds combos and other stuff in your deck')
async def combofinder(ctx, link=None, result_type: str = ""):
    print(ctx.author.name + " started a deck analysis.")
    if len(ctx.message.attachments) == 0 and link == None:
        await ctx.send("Please attach the decklist to your message, or provide a link to your decklist.")
        return
    decklist = ""
    if link is not None:
        deck_hosted = urlparse(link).hostname
        if deck_hosted == "www.moxfield.com":
            file_url = download_link_from_moxfield(link)
            decklist = str(requests.get(file_url).text)
        elif deck_hosted == "manabox.app":
            file_location = download_link_from_manabox(link)
            decklist = open(file_location, "r").read()
            os.remove(file_location)
        else:
            await ctx.send("We are sorry, but we do not support automatic decklist export from " + deck_hosted + " yet.")
            return
    else:
        # Get decklist from attachment
        decklist = str(requests.get(ctx.message.attachments[0].url).text)
    analysis = combo_finder(decklist)
    if result_type == "File":
        await ctx.send(file=discord.File(r'analyzeResults.txt'))
    else:
        await ctx.send(analysis)


def print_analysis(analysis):
    return "".join(list(map(str, analysis))) + "Combo count: " + str(len(analysis))


bot.run(TOKEN)
print("Bot is running...")
