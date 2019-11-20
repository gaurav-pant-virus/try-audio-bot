from .audio_player import AudioPlayer


# we will register all gogs here.
def register_cog(bot):
    bot.add_cog(AudioPlayer(bot))
