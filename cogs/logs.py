import time
import nextcord
import asyncio
from nextcord.ext import commands, tasks
class Logs(commands.Cog):
    def __init__(self, bot):
        # self.creators = [555638466365489172, 772444493487407105]
        self.bot = bot
        self.logchannel = bot.get_channel(955864566758264842)

    async def perms_to_normal(self, owerwrites):
        owerwrites_new = {}
        for target in owerwrites.keys():
            owerwrites_new[target.name] = [ow.all() for ow in owerwrites[target].pair()]
        return owerwrites_new

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    # 	await ctx.send(str(error))
    # 	raise error

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot: return
        if before.content == after.content: return
        attach = ''
        if len(before.attachments) == 0:
            attach = 'нет'
        else:
            for attachment in before.attachments:
                attach += attachment.url+'\n'
        attach2 = ''
        if len(after.attachments) == 0:
            attach2 = 'нет'
        else:
            for attachment in after.attachments:
                attach2 += attachment.url+'\n'
        emb = nextcord.Embed(
                title = "Сообщение отредактировано",
                description = f"[Ссылка]({before.jump_url})",
                color = 0x00aaf2
            )
        emb.add_field(name = f'Содержимое до:', value = f"`{self.bot.minify_text(before.content)}`", inline = False)#Вложения: `{attach}`", inline = False)
        emb.add_field(name = f'Содержимое после:', value = f" `{self.bot.minify_text(after.content)}`", inline=False)#f"Вложения: `{attach}`", inline = False)
        emb.add_field(name = "Автор сообщения:", value = f"{before.author.mention}", inline = False)
        emb.set_author(name = f'{before.author.display_name} || {before.author}', icon_url = before.author.avatar.url if before.author.avatar else before.author.default_avatar)
        emb.set_footer(text = f'ID: {before.id}')

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot: return
        attach = ''
        if len(message.attachments) == 0:
            attach = 'нет'
        else:
            for attachment in message.attachments:
                attach += attachment.url+'\n'
        del_by_who = None
        async for action in message.guild.audit_logs(action = nextcord.AuditLogAction.message_delete):
            if action.target.id == message.author.id:
                del_by_who = action.user
            break
        emb = nextcord.Embed(
                title = "Сообщение удалено",
                color = 0xff0303
            )
        cont = self.bot.minify_text(message.content)
        emb.add_field(name = f'Содержимое удалённого сообщения:', value = f'`{cont}`', inline = False)
        emb.add_field(name = "Вложения:", value = f'`{self.bot.minify_text(attach)}`', inline = False)
        emb.add_field(name = "Автор сообщения:", value = f"{message.author.mention}", inline = False)
        if del_by_who is not None:
            emb.add_field(name = 'Удалено:', value = f'{del_by_who.mention}')
        emb.set_author(name = f'{message.author.display_name} || {message.author}', icon_url = message.author.avatar.url if message.author.avatar else message.author.default_avatar)
        emb.set_footer(text = f'ID: {message.id}')

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        emb = nextcord.Embed(
                title = "Сообщения удалены",
                color = 0xff0303
            )
        emb.add_field(name = f'Количество: `{len(payload.message_ids)}`', value = f"Канал: {self.bot.get_guild(payload.guild_id).get_channel(payload.channel_id).mention}", inline = False)

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        perms = await self.perms_to_normal(channel.overwrites)
        emb = nextcord.Embed(
                title = "Создан канал",
                color = 0x00e508
            )
        emb.add_field(name = f'Название: ', value = f'#{channel.name}', inline = False)
        emb.add_field(name = f"Категория: ", value = f"#{channel.category.name if channel.category else 'нет'}", inline = False)
        emb.add_field(name = f"Тип: {channel.type}", value = f"** **", inline = False)
        emb.add_field(name = f'Права: ', value = f'{perms}')
        if str(channel.type) == "text":
            emb.add_field(name = f"NSFW: {'да' if channel.is_nsfw() else 'нет'}", value = f"** **", inline = False)
            emb.add_field(name = f"Тема: ", value = f"{channel.topic if channel.topic else 'нет'}", inline = False)
            emb.add_field(name = f"Слоумод: {str(channel.slowmode_delay)+' секунд' if channel.slowmode_delay != 0 else 'нет'}", value = f"** **", inline = False)
        elif str(channel.type) == "voice":
            emb.add_field(name = f"Битрейт: {channel.bitrate}", value = f"** **", inline = False)
            emb.add_field(name = f"Регион RTC: {str(channel.rtc_region).capitalize()}", value = f"** **", inline = False)
            emb.add_field(name = f"Лимит пользователей: {channel.user_limit}", value = f"** **", inline = False)
        elif str(channel.type) == "stage_voice":
            emb.add_field(name = f"Битрейт: {channel.bitrate}", value = f"** **", inline = False)
            emb.add_field(name = f"Регион RTC: {str(channel.rtc_region).capitalize() if channel.rtc_region else 'Автоматически'}", value = f"** **", inline = False)
            emb.add_field(name = f"Лимит пользователей: {channel.user_limit}", value = f"** **", inline = False)
            emb.add_field(name = f"Тема: ", value = f"{channel.topic if channel.topic else 'нет'}", inline = False)

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        perms = await self.perms_to_normal(channel.overwrites)
        emb = nextcord.Embed(
                title = "Удалён канал",
                color = 0xff0303
            )
        emb.add_field(name = f'Название: ', value = f'#{channel.name}', inline = False)
        emb.add_field(name = f"Категория: ", value = f"#{channel.category.name if channel.category else 'нет'}", inline = False)
        emb.add_field(name = f"Тип: {channel.type}", value = f"** **", inline = False)
        emb.add_field(name = f'Права: ', value = f'{perms}')
        if str(channel.type) == "text":
            emb.add_field(name = f"Был ли NSFW: {'да' if channel.is_nsfw() else 'нет'}", value = f"** **", inline = False)
            emb.add_field(name = f"Тема: ", value = f"{channel.topic if channel.topic else 'нет'}", inline = False)
            emb.add_field(name = f"Слоумод: {str(channel.slowmode_delay)+' секунд' if channel.slowmode_delay != 0 else 'нет'}", value = f"** **", inline = False)
        elif str(channel.type) == "voice":
            emb.add_field(name = f"Битрейт: {channel.bitrate}", value = f"** **", inline = False)
            emb.add_field(name = f"Регион RTC: {str(channel.rtc_region).capitalize()}", value = f"** **", inline = False)
            emb.add_field(name = f"Лимит пользователей: {channel.user_limit}", value = f"** **", inline = False)
        elif str(channel.type) == "stage_voice":
            emb.add_field(name = f"Битрейт: {channel.bitrate}", value = f"** **", inline = False)
            emb.add_field(name = f"Регион RTC: {str(channel.rtc_region).capitalize() if channel.rtc_region else 'Автоматически'}", value = f"** **", inline = False)
            emb.add_field(name = f"Лимит пользователей: {channel.user_limit}", value = f"** **", inline = False)
            emb.add_field(name = f"Тема: ", value = f"{channel.topic if channel.topic else 'нет'}", inline = False)

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: nextcord.TextChannel, after: nextcord.TextChannel):
        perms_before = await self.perms_to_normal(before.overwrites)
        perms_after = await self.perms_to_normal(after.overwrites)
        emb = nextcord.Embed(
                title = "Изменён канал",
                color = 0xffff00
            )
        emb.add_field(name = f'Название до: #{before.name}', value = f'Название после: #{after.name}', inline = False)
        if before.category != after.category:
            emb.add_field(name = f"Категория до: #{before.category.name if before.category else 'нет'}", value = f"Категория после: {after.category.mention if after.category else 'нет'}", inline = False)
        if before.type != after.type:
            emb.add_field(name = f"Тип до: {before.type}", value = f"Тип после: {after.type}", inline = False)
        if perms_before != perms_after:
            emb.add_field(name = f'Права до:', value = f"{perms_before}")
            emb.add_field(name = f'Права после:', value=f" {perms_after}")
        if str(before.type) == "text" and str(after.type) == "text":
            if before.is_nsfw() != after.is_nsfw():
                emb.add_field(name = f"Был ли NSFW: {'да' if before.is_nsfw() else 'нет'}", value = f"Стал ли NSFW: {'да' if after.is_nsfw() else 'нет'}", inline = False)
            if before.topic != after.topic:
                emb.add_field(name = f"Тема до: ", value = f"{before.topic if before.topic else 'нет'}", inline = False)
                emb.add_field(name="Тема после:", value = f"{after.topic if after.topic else 'нет'}", inline = False)
            if before.slowmode_delay != after.slowmode_delay:
                emb.add_field(name = f"Слоумод до: {str(before.slowmode_delay)+' секунд' if before.slowmode_delay != 0 else 'нет'}", value = f"Слоумод после: {str(before.slowmode_delay)+' секунд' if before.slowmode_delay != 0 else 'нет'}", inline = False)
        elif str(before.type) == "voice" and str(after.type) == "voice":
            if before.bitrate != after.bitrate:
                emb.add_field(name = f"Битрейт до: {before.bitrate}", value = f"Битрейт после: {after.bitrate}", inline = False)
            if before.rtc_region != after.rtc_region:
                emb.add_field(name = f"Регион RTC до: {str(before.rtc_region).capitalize()}", value = f"Регион RTC после: {str(after.rtc_region).capitalize()}", inline = False)
            if before.user_limit != after.user_limit:
                emb.add_field(name = f"Лимит пользователей до: {before.user_limit}", value = f"Лимит пользователей после: {after.user_limit}", inline = False)
            if before.members != after.members: return
        elif str(before.type) == "stage_voice" and str(after.type) == "stage_voice":
            if before.bitrate != after.bitrate:
                emb.add_field(name = f"Битрейт до: {before.bitrate}", value = f"Битрейт после: {after.bitrate}", inline = False)
            if before.rtc_region != after.rtc_region:
                emb.add_field(name = f"Регион RTC до: {str(before.rtc_region).capitalize() if before.rtc_region else 'Автоматически'}", value = f"Регион RTC после: {str(after.rtc_region).capitalize() if after.rtc_region else 'Автоматически'}", inline = False)
            if before.user_limit != after.user_limit:
                emb.add_field(name = f"Лимит пользователей до: {before.user_limit}", value = f"Лимит пользователей после: {after.user_limit}", inline = False)
            if before.topic != after.topic:
                emb.add_field(name = f"Тема до: ", value = f"{before.topic if before.topic else 'нет'}", inline = False)
                emb.add_field(name="Тема после:", value = f"{after.topic if after.topic else 'нет'}", inline = False)
            if before.members != after.members: return

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        emb = nextcord.Embed(
                title = "К серверу присоединился участник",
                color = 0x33ff33
            )
        act = "** **"
        alert = "** **"
        emb.add_field(name = f"Имя: {member}", value = f"Отображаемое имя: {member.display_name}", inline = False)
        emb.add_field(name = f'Бот: {"да" if member.bot else "нет"}', value = "** **", inline = False)
        time_after_create = time.time() - member.created_at.timestamp()
        if round(time_after_create) < 60*60*12:
            alert = f':warning: ВНИМАНИЕ: аккаунт создан менее 12ч назад! ({str(time_after_create)[:-7]} назад)'
        emb.add_field(name = f'Дата создания аккаунта: {member.created_at}', value = f'{alert}', inline = False)
        if member.activity:
            activ = member.activity[0]
            if isinstance(activ.type, nextcord.ActivityType.streaming):
                act = f'Стримит на {activ.platform}: `{activ.name}`'
            elif isinstance(activ.type, nextcord.ActivityType.game):
                act = f'Играет в `{activ.name}`'
            elif isinstance(activ.type, nextcord.ActivityType.competing):
                act = f'Соревнуется в `{activ.name}`'
            elif isinstance(activ.type, nextcord.ActivityType.listening):
                act = f'Слушает `{activ.name}`'
            elif isinstance(activ.type, nextcord.ActivityType.custom):
                act = f'Статус: {str(activ.emoji) if activ.emoji else ""}{activ.name}'
            emb.add_field(name = f'{act}', value = "** **", inline = False)
        emb.set_thumbnail(url = member.avatar.url if member.avatar else member.default_avatar)

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        emb = nextcord.Embed(
                title = "Участник вышел с сервера",
                color = 0xff3333
            )
        emb.add_field(name = f"Имя: {member}", value = f"Отображаемое имя: {member.display_name}", inline = False)
        emb.add_field(name = f'Бот: {"да" if member.bot else "нет"}', value = "** **", inline = False)
        emb.add_field(name = f'Дата создания аккаунта: {member.created_at}', value = f'** **', inline = False)
        emb.add_field(name = 'Роли:', value = '** **'.join([r.mention for r in member.roles]), inline = False)
        emb.set_thumbnail(url = member.avatar.url if member.avatar else member.default_avatar)

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        emb = nextcord.Embed(
                title = "Пользователь забанен",
                description = f"Забаненый: {user}",
                color = 0xff0000
            ).set_thumbnail(url = user.avatar.url if user.avatar else user.default_avatar)

        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        emb = nextcord.Embed(
                title = "Пользователь рзбанен",
                description = f"Разбаненый: {user}",
                color = 0x00ff00
            ).set_thumbnail(url = user.avatar.url if user.avatar else user.default_avatar)
        
        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        emb = nextcord.Embed(title = "** **", description = f"Изменения коснулись: {after.mention}", color = 0xbbbb00)
        if before.status != after.status: return
        if before.activity != after.activity: return

        if before.pending and not after.pending:
            emb.title = "Пользователь верифицирован на сервере"
            emb.description = f"Пользователь {after.mention} прошёл верификацию"
            emb.color = 0x00ff00
        if before.roles != after.roles:
            emb.title = "Участник изменён"
            emb.add_field(name = 'Роли до:', value = ", ".join([r.mention for r in before.roles]))
            emb.add_field(name = 'Роли после:', value = ", ".join([r.mention for r in after.roles]))
            
        elif before.display_name != after.display_name:
            emb.title = "Участник изменён"
            emb.add_field(name = f'Никнейм участника изменён на: {after.display_name}', value = f"Старый никнейм: {before.display_name}")
        if emb.title == "** **": return
        emb.set_thumbnail(url = after.avatar.url if after.avatar else after.default_avatar)
        emb.add_field(name = 'Debug: активность (баг с мобильным Rich Presence)', value = f'`{before.activity}`\n`{after.activity}`\n`{before.status}`\n`{after.status}`')
        
        self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if after.mutual_guilds:
            emb = nextcord.Embed(title = 'Пользователь изменён', description = f"Изменения коснулись: {after.mention}", color = 0xbbbb00)
            emb.set_thumbnail(url = after.avatar.url)
            if before.name != after.name:
                emb.add_field(name = 'Изменено имя пользователя', value = f'До: {before.name}\nПосле: {after.name}', inline = False)
            if before.discriminator != after.discriminator:
                emb.add_field(name = 'Изменён тег пользователя', value = f'До: {before.discriminator}\nПосле: {after.discriminator}', inline = False)
            if before.avatar != after.avatar:
                emb.add_field(name = 'Изменён аватар пользователя', value = f'До: {before.avatar.url}\nПосле: {after.avatar.url}', inline = False)
            emb.set_thumbnail(url = after.avatar.url if after.avatar else after.default_avatar)
            # emb.add_field(name = 'Debug: активность (баг с мобильным Rich Presence)', value = f'`{before.activity}`\n`{after.activity}`\n`{before.status}`\n`{after.status}`')
            self.logchannel = self.bot.get_channel(955864566758264842)
        await self.logchannel.send(embed = emb)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        # ch_pre = await self.guildinfo.find_one({'guild_id': invite.guild.id})
        # if ch_pre is None:
        # 	return
        # elif ch_pre['logchannel'] == 0:
        # 	return
        # ch = invite.guild.get_channel(ch_pre['logchannel'])
        # await ch.send(embed = emb)
        pass

def setup(bot):
    bot.add_cog(Logs(bot))
    print('Ког "Logs" загружен')
def teardown(bot):
    print('Ког "Logs" отгружен')