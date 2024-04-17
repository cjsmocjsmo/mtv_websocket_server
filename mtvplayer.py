from mpv import MPVError, Context

class MTVPlayer:
    def __init__(self):
         
        try:
            self.mpv_context = Context()
            self.mpv_context.set_option('input-default-bindings')
            self.mpv_context.set_option('osc')
            self.mpv_context.set_option('input-vo-keyboard')
            self.mpv_context.set_option("fs", True)
            self.mpv_context.initialize()
            #   self.mpv_context.command('loadfile', video_path)
            print("Video Player Ready")
        except MPVError as e:
            print(f"Failed to create MPV context: {e}")
            self.close()

    def loadfile(self, path):
        self.mpv_context.command('loadfile', path)
        return "Video playing"
    
    def stop(self):
        self.mpv_context.command('stop')
        return "Video stopped"
    
    def play(self):
        self.mpv_context.command('playlist-play-index=current')
        return "Video resumed"
    
    def quit(self):
        self.mpv_context.command("quit")
        return "Video stopped"
    
    def clear(self):
        self.mpv_context.command("playlist-clear")
        print("Playlist cleared")
        return "Connection closed"
    
