from mpv import MPVError, Context

class MTVPlayer:
    def __init__(self):
         
        try:
            self.mpv_context = Context()
            self.mpv_context.set_option('input-default-bindings')
            self.mpv_context.set_option('osc')
            self.mpv_context.set_option('input-vo-keyboard')
            self.mpv_context.set_option("fs", True)
            self.mpv_context.set_option("idle", "yes")
            self.mpv_context.initialize()
            # self.mpv_context.command('loadfile', video_path)
            print("Video Player Ready")
        except MPVError as e:
            print(f"Failed to create MPV context: {e}")
            self.close()
    
    def play(self, path):
        self.mpv_context.command('loadfile', path)

    def quit(self):
        self.mpv_context.command("stop")
    
