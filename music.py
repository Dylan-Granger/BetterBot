import discord
from discord.ext import commands
from  youtube_dl import YoutubeDL

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.is_playing = False
        self.is_paused = False
        
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)
            print(self.music_queue)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_vid(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            self.music_queue.pop(0)
            
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False


    @commands.command(name='play', aliases=['p', 'playing', 'hit_it'], help='Play the selected song from youtube')
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send('Connect to a voice channel sped kid')
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == bool:
                await ctx.send("Couldn't find that shit homes my bad g")
            else:
                await ctx.send("Its in the queu now B")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    self.is_playing = True
                    await self.play_vid(ctx)

    @commands.command(name="pause", aliases=['stop_tha_shit'], help='Pauses the current song playing (use when someone is playing some wack shit)')
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command()
    async def resume(self, ctx, *args):
        if self.paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(name='skip', aliases=['s'], help = "Skips the song being played cause its trash af")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_next(ctx)

    @commands.command(name="queue", aliases=['q'], help="Shows queue pretty self explanatory")
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("this queue empty af")
    
    @commands.command(name='clear', aliases=['c', 'obliterate', 'purge'], help="empty's the queue")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("queue cleared")


    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from the voice channel")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await ctx.voice_client.disconnect()