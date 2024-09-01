import discord
import asyncio
from discord import Intents
from discord import app_commands
from discord.ext import commands
# Create an Intents object and specify what events your bot should listen for
intents = Intents.default()  # Start with default intents
intents.messages = True    # Enable listening for messages
intents.guilds = True
intents.members = True # Enable listening for guild-related events

bot = commands.Bot(command_prefix=".", intents=intents)

async def send_message_with_delay(channel, message):
    await asyncio.sleep(1)  # Wait for 1 second
    await channel.send(message)

# Create the Discord client object, passing the intents
client = discord.Client(intents=intents)

# ... rest of your code ...

# ayricaliklar (intents) değişkeni botun ayrıcalıklarını depolayacak
intents = discord.Intents.default()
# Mesajları okuma ayrıcalığını etkinleştirelim
intents.message_content = True
# client (istemci) değişkeniyle bir bot oluşturalım ve ayrıcalıkları ona aktaralım
client = discord.Client(intents=intents)

bakim_mode = False  # Declare bakim_mode as a global variable
status_messages = [".yardim", "Credits: @.acrostorm", ".komutlar", "Nerdeyse 30 Kişiyiz!", "MinecrafTR", "#30", "Yetkili Alımları Aktif!", "Sadece 1 Kişi Yetkili Olabilcek!"]

warnings = []

bakim_messages = ["⚠️ Bakım Modu ⚠️", "⚠️ Komutlar Düzgün Çalışmayabilir! ⚠️"]


@client.event
async def on_ready():
    print(f'{client.user} olarak giriş yaptık.')
    while True:
        if bakim_mode:
            for status in bakim_messages:
                await client.change_presence(activity=discord.Game(name=status))
                await asyncio.sleep(5)  # Wait for 5 seconds
        else:
            for status in status_messages:
                await client.change_presence(activity=discord.Game(name=status))
                await asyncio.sleep(5)  # Wait for 5 seconds


@client.event
async def on_member_join(member):
    role_id = 1271062721214808210  # Replace with your role ID
    role = discord.utils.get(member.guild.roles, id=role_id)
    if role:
        try:
            await member.add_roles(role)
            print(f"Assigned role {role.name} to {member.name}")
        except discord.Forbidden:
            print("Bot does not have permission to assign roles.")
        except discord.HTTPException as e:
            print(f"Failed to assign role: {e}")
    else:
        print("Role not found.")

@client.event
async def on_message(message):
    member = message.author  
    if message.content.startswith('merhaba'):
        await message.channel.send("Selam!")
    elif message.content.startswith("sa"):
        await message.channel.send("As!")
    elif message.content.startswith('baybay'):
        await message.channel.send("🤗 Baybay!")
    elif message.content.startswith('.ssu'):
        await message.delete()
        await message.channel.send("@everyone SUNUCU BAŞLANGICI! .ip YAZARAK IPYI ÖĞRENEBİLİRSİNİZ!")
    elif message.content.startswith('.sr'):
        await message.delete()
        await message.channel.send("@everyone Sunucuyu Bir Sebepten Dolayı Yeniden Başlatıyoruz! .ip Yazarak IP'yi Öğrenebilirsiniz!")
    elif message.content.startswith('.ssd'):
        await message.delete()
        await message.channel.send("@everyone Sunucuyu Kapattık! Herkese İyi Günler!")
    elif message.content.startswith('.aktifliktesti'):
        await message.delete()
        await message.channel.send("@everyone Aktiflik Testi!")
    elif message.content.startswith(".ip"):
        await message.channel.send("Sunucu IP: IEMMinecraft.aternos.me ")
    elif message.content.startswith('.deadchat'):
        await message.delete()
        await message.channel.send(" @everyone DEAD CHAT[!](https://tenor.com/view/googas-wet-wet-cat-dead-chat-dead-chat-xd-gif-20820186)")
    elif message.content.startswith('.komutlar'):
        await message.channel.send("Komutlar: .ip , .yardim Şuan Herkese Açık Başka Bir Komutum Yok. ")

    elif message.content.startswith('.hatirlatici'):
        await message.delete()
        await message.channel.send("@everyone SUNUCU HALA AKTİF! GİRİŞ SAĞLAYALIM! .ip YAZARAK IP'yi Öğrenebilirsiniz!")
    elif message.content.startswith('.yardim'):
        await message.delete()
        await message.channel.send("<@&1271057470458171474>, <@&1271572475397935217>, <@&1271736999266750465>, Yardım İstekleri Var!")
    elif message.content.startswith(".rpsbirkisi"):
        await message.delete()
        await message.channel.send("RP Start Olmasına Son 1 Kişi! Sunucuya Giriş Sağlayalım Lütfen.")


    elif message.content.startswith(".bakim"):
        role = discord.utils.get(message.guild.roles, name="Yönetici") 
        if role in message.author.roles:
            await message.delete()
            global bakim_mode # Declare that we're using the global bakim_mode
            bakim_mode = not bakim_mode
            if bakim_mode:
                await message.channel.send("⚠️ Bakım Modu ⚠️")
                await message.channel.send("⚠️ Komutlar Düzgün Çalışmayabilir! ⚠️")
            else:
                await message.channel.send("Bakım Modu Kapatıldı!")
        else:
            await message.channel.send(f" {member.mention} Bakım komutunu kullanmak için gerekli yetkiye sahip değilsin!")

    if message.content.startswith(".sil"):
        role = discord.utils.get(message.guild.roles, name="Yönetici")  # Get the "Yönetici" role
        if role in message.author.roles:
            try:
                # Get the number of messages to purge (default to 10 if not provided)
                amount = int(message.content.split()[-1])
                if amount > 100:
                    amount = 100  # Limit purging to 100 messages at a time
                # Delete messages
                deleted_messages = await message.channel.purge(limit=amount)
                await message.channel.send(f" {len(deleted_messages)} mesaj silindi.")
            except ValueError:
                await message.channel.send("Lütfen Geçerli Bir Limit Girin.")
        else:
            await message.channel.send(f" {member.mention} Bu komutu kullanmak için gerekli yetkiye sahip değilsin!")

    elif message.content.startswith('.uyar'):
        role = discord.utils.get(message.guild.roles, name="Yönetici") 
        if role in message.author.roles:
            # Get the user to DM
            try:
                # Check if the user is mentioned
                target_user = message.mentions[0] 
            except IndexError:
                # If no mention, try getting the user by ID
                try:
                    target_user_id = int(message.content.split()[1])  # Get ID from message
                    target_user = await client.fetch_user(target_user_id)
                except (ValueError, discord.NotFound):
                    await message.channel.send("Lütfen Geçerli Bir @ yada ID Girin!.")
                    return
            # Get the warning message
            warning_message = message.content.split('.uyar ')[1]
            # Send the DM
            try:
                embed = discord.Embed(
                    title="MinecrafTR Bildirimi",
                    description=f"Hey Dostum! Maalesefki Uyarıldın. Sebep: {warning_message}",
                    color=0xff0000
                )

                warnings_description = (
                    "Uyarı 1 = Sıkıntı Yok\n"
                    "Uyarı 2 = Discord Sunucusundan Kick\n"
                    "Uyarı 3 = Discord Sunucusundan 15 Dakikalık Ban\n"
                    "Uyarı 4 = Discord Sunucusundan 30 Dakikalık Ban\n"
                    "Uyarı 5 = Discord ve Minecraft Sunucusundan Ban"
                )

                embed.add_field(
                    name="Uyarılar",
                    value=warnings_description,
                    inline=False
                )

                await target_user.send(embed=embed)

            except discord.HTTPException:
                await message.channel.send(f"Uyarı mesajı {target_user.mention}'a gönderilemedi.")
   

                await message.channel.send(f"Uyarı mesajı {target_user.mention}'a gönderildi.")
            channel_id = 1277341814126543070

            channel = client.get_channel(channel_id)

            if channel:
                await channel.send(f"{target_user.mention} adlı kullanıcıya uyarı verildi. Mesaj: {warning_message}")
        else:
            await message.channel.send(f" {member.mention} Bu komutu kullanmak için gerekli yetkiye sahip değilsin")

    elif message.content.startswith('.ykomutlari'):
        role = discord.utils.get(message.guild.roles, name="Yönetici") 
        if role in message.author.roles:
            await message.delete()
            await message.author.send(f"Yetkili Komutları: .uyar, .aktifliktesti, .bakim, .ykomutlar, .ssu, .ssd, .sr, .deadchat, .rpsbirkisi, .hatirlatici .sil .ban .unban .kick")



        else:
            await message.channel.send(f" {member.mention} Yetkili Komutlarını Görmek İçin Gerekli Yetkiye Sahip Değilsin!")


    if message.content.startswith('.ban'):
        role = discord.utils.get(message.guild.roles, name="Yönetici")
        if role in message.author.roles:
            try:
                # Extract the user to ban
                user_to_ban = message.mentions[0]
                # Optionally, you can extract the reason from the command
                reason = ' '.join(message.content.split(' ')[2:]) if len(message.content.split()) > 2 else 'Sebep Belirtilmedi.'

       
                try:
                    embed = discord.Embed(
                        title="MinecrafTR Bildirimi",
                        description=f"Sunucudan Banlandınız. Sebep: {reason}",
                        color=0xff0000
                    )
                    embed.add_field(name="", value="Bu Ban Şuanlık Kaldırılamaz. Kaldırılırsa Yetkili Size Dönüş Yapıcaktır. Bu Yüzden Yetkilileri Engellemediğinizden Emin Olun.", inline=False)
                    await user_to_ban.send(embed=embed)
                except discord.HTTPException:
                    pass  # DM could not be sent, which is okay

                # Ban the user
                await user_to_ban.ban(reason=reason)

                # Send a DM if possibl

                await message.channel.send(f"{user_to_ban.mention} kullanıcısı yasaklandı. Sebep: {reason}")
            except IndexError:
                await message.channel.send("Lütfen yasaklamak istediğiniz kişiyi etiketleyin.")
            except discord.Forbidden:
                await message.channel.send("Bu kullanıcıyı yasaklayamıyorum, yeterli yetkiye sahip değilim.")
            except discord.HTTPException:
                await message.channel.send("Bir hata oluştu. Kullanıcıyı yasaklayamadım.")
        else:
            await message.channel.send(f"{message.author.mention} Bu komutu kullanmak için gerekli yetkiye sahip değilsin!")

    if message.content.startswith('.unban'):
        role = discord.utils.get(message.guild.roles, name="Yönetici")
        if role in message.author.roles:
            try:
                # Extract user ID and reason
                parts = message.content.split()
                if len(parts) < 2:
                    await message.channel.send("Lütfen geçerli bir kullanıcı ID'si girin.")
                    return

                user_id = int(parts[1])
                reason = ' '.join(parts[2:]) if len(parts) > 2 else 'No reason provided'

                # Attempt to unban the user
                user_to_unban = discord.Object(id=user_id)
                await message.guild.unban(user_to_unban, reason=reason)

                # Sending a confirmation message
                await message.channel.send(f"Kullanıcı <@{user_id}> yasaklamadan çıkarıldı. Sebep: {reason}")
            except ValueError:
                await message.channel.send("Lütfen geçerli bir kullanıcı ID'si girin.")
            except discord.NotFound:
                await message.channel.send("Bu kullanıcı sunucuda yasaklanmamış olabilir.")
            except discord.Forbidden:
                await message.channel.send("Bu kullanıcıyı yasaklamaktan çıkartamıyorum, yeterli yetkiye sahip değilim.")
            except discord.HTTPException as e:
                await message.channel.send(f"Bir hata oluştu: {e}")
        else:
            await message.channel.send(f"{message.author.mention} Bu komutu kullanmak için gerekli yetkiye sahip değilsin!")

    if message.content.startswith('.kick'):
        role = discord.utils.get(message.guild.roles, name="Yönetici")
        if role in message.author.roles:
            try:
                # Extract the user to kick
                user_to_kick = message.mentions[0]
                # Optionally, you can extract the reason from the command
                reason = ' '.join(message.content.split(' ')[2:]) if len(message.content.split()) > 2 else 'No reason provided'

                try:
                    await user_to_kick.send(f"Sunucudan Atıldınız. Sebep: {reason}")
                except discord.HTTPException:
                    pass  # DM could not be sent, which is okay


                # Kick the user
                await user_to_kick.kick(reason=reason)

                # Send a DM if possible


                await message.channel.send(f"{user_to_kick.mention} kullanıcısı sunucudan atıldı. Sebep: {reason}")
            except IndexError:
                await message.channel.send("Lütfen atmak istediğiniz kişiyi etiketleyin.")
            except discord.Forbidden:
                await message.channel.send("Bu kullanıcıyı atamıyorum, yeterli yetkiye sahip değilim.")
            except discord.HTTPException:
                await message.channel.send("Bir hata oluştu. Kullanıcıyı atamadım.")
        else:
            await message.channel.send(f"{message.author.mention} Bu komutu kullanmak için gerekli yetkiye sahip değilsin!")

    if message.content.startswith(".oylama"):
        # Command format: .oylama <question> | Option1 | Option2 | Option3
        parts = message.content.split('|')
        if len(parts) < 2:
            await message.channel.send("Anket oluşturmak için en az bir seçenek belirtmelisiniz.")
            return

        poll_question = parts[0].replace('.oylama', '').strip()
        options = [part.strip() for part in parts[1:]]

        if len(options) > 9:
            await message.channel.send("En fazla 9 seçenek ekleyebilirsiniz.")
            return

        # Create the poll message
        poll_message = await message.channel.send(f"**{poll_question}**\n" + '\n'.join([f"{chr(127462 + i)} {opt}" for i, opt in enumerate(options)]))


    elif message.content.startswith("@everyone"):
        role = discord.utils.get(message.guild.roles, name="Yönetici")
        if role in message.author.roles:
              pass

        else:
            await message.delete()
            await message.channel.send(f"{member.mention} Hey! Everyone atmak için gerekli yetkiye sahip değilsin! Otomatik Bir Şekilde Uayrıldın!")

    if message.content.startswith(".kilit"):
      role = discord.utils.get(message.guild.roles, name="Yönetici")
      if role in message.author.roles:
          channel = message.channel
          # Lock the channel by denying the SEND_MESSAGES permission to everyone
          await channel.set_permissions(message.guild.default_role, send_messages=False)
          await message.channel.send("Bu kanal kilitlendi. Yalnızca yetkili roller mesaj gönderebilir.")
      else:
          await message.channel.send(f"{member.mention} Bu komutu kullanmak için gerekli yetkiye sahip değilsin!")

    # Unlock the channel
    elif message.content.startswith(".akilitac"):
      role = discord.utils.get(message.guild.roles, name="Yönetici")
      if role in message.author.roles:
          channel = message.channel
          # Revert the permissions to allow @everyone to send messages
          await channel.set_permissions(message.guild.default_role, send_messages=True)
          await message.channel.send("Bu kanal kilidi açıldı. Herkes mesaj gönderebilir.")
      else:
          await message.channel.send(f"{member.mention} Bu komutu kullanmak için gerekli yetkiye sahip değilsin!")

    elif message.content.startswith(".embed"):
        role = discord.utils.get(message.guild.roles, name="Yönetici")
        if role in message.author.roles:
          channel = message.channel
          embed=discord.Embed(title="title", description="description", color=0xff0000)
          embed.add_field(name="field", value="value", inline=False)
          await message.channel.send(embed=embed)
        else:
            await message.channel.send("Bu Komutu Kullanmak İçin Yetkin YOK!")



# Bu Bot AcroStorm Trafından Yapılmıştır. Telif Hakları Saklıdır.



client.run("TOKEN")
