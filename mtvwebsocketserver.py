import os
import time
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
import mtvplayer as MTVP

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class VideoHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    self.write_message("Connection established")

  def on_message(self, message):
    mtvplayer = MTVP.MTVPlayer()
    mtvcommand, path = message.split(":")
    if mtvcommand == "TIME":
        txt = f"Current time: {time.ctime()}"
        self.write_message(txt)
    elif mtvcommand == "PLAY":
        mtvplayer.play(path)
        self.write_message("Video playing")
    elif mtvcommand == "STOP":
        mtvplayer.stop()
        self.write_message("Video paused")
    else:
        self.write_message("Invalid command")

  def on_close(self):
    print("Connection closed")

def make_app():
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/mtvws", VideoHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    print("Server started on port 5000")
    tornado.ioloop.IOLoop.current().start()