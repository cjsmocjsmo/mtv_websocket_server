from mpv import MPVError, Context

class MTVPlayer:
    def __init__(self, path):
         
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
            
        self.LOADFILE = self.mpv_context.command('loadfile', path)
        self.PLAY = self.mpv_context.command('playlist-play-index=current')
        self.STOP = self.mpv_context.command('stop')

    def loadfile(self):
        print("Video playing")
        return self.LOADFILE
    
    def stop(self):
        print("Video stopped")
        return self.STOP
    
    def play(self):
        print("Video resumed")
        return self.PLAY
    
    def quit(self):
        self.mpv_context.command("quit")
        return "Video stopped"
    
    def clear(self):
        self.mpv_context.command("playlist-clear")
        print("Playlist cleared")
        return "Connection closed"
    
