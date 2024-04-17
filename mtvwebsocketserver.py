# import tornado.ioloop
# import tornado.web
# import tornado.websocket
# import os
# import mtvutils as UT
# import mpv
# import subprocess


# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("index.html")

# class WebSocketHandler(tornado.websocket.WebSocketHandler):
#     # m = None
#     # try:
#     #     m = mpv.Context()
#     # except mpv.MPVError:
#     #     print('failed creating context')
#     #     # return 1

#     def open(self):
#         print("WebSocket opened")

#     def on_message(self, message):
#         data, param = message.split(":")
#         print(f"Client sent: {data}")
#         response = ""
#         # Respond based on the request
#         if data == "HELLO":
#             response = f"Hi there, {param}"
#         elif data == "TIME":
#             response = f"Current time: {UT.get_time()}"
#         elif data == "PLAY":
#             subprocess.run(["mpv", param, "--fs"])
#             try:
#                 m = mpv.Context()
#             except mpv.MPVError:
#                 print('failed creating context')
#                 return 1

#             m.set_option('input-default-bindings')
#             m.set_option('osc')
#             m.set_option('input-vo-keyboard')
#             m.set_option("fs", True)
#             m.initialize()
#             print("LOADING FILE")
#             m.command('loadfile', param)

#             while True:
#                 event = m.wait_event(.01)
#                 if event.id == mpv.Events.none:
#                     continue
#                 print(event.name)
#                 if event.id in [mpv.Events.end_file, mpv.Events.shutdown]:
#                     break
#             response = f"Playing video at:\n\t {param}"
#         elif data == "PAUSE":
            
#             # m.command('set_property', 'pause', 'yes')
#             response = f"Pausing video playback"
#         elif data == "RESUME":
#             m.command('set_property', 'pause', 'no')
#             response = f"Resuming video playback"
#         elif data == "STOP":
#             m.command('stop')
#             response = f"Stopping video playback"
#         elif data == "NEXT":
#             m.command('seek', '20', 'relative+exact')
#             response = f"Seeking forward 20 seconds"
#         elif data == "PREVIOUS":
#             m.command('seek', '-20', 'relative+exact')
#             response = f"Playing previous video"
#         else:
#             response = "Unknown request."

#         # Send the response back to the client
#         self.write_message(response)

#     def on_close(self):
#         print("WebSocket closed")

# def make_app():
#     settings = {
#         "template_path": os.path.join(os.path.dirname(__file__), "templates"),
#         "static_path": os.path.join(os.path.dirname(__file__), "static")
#     }
#     return tornado.web.Application([
#         (r"/", MainHandler),
#         (r"/mtvws", WebSocketHandler),
#     ], **settings)

# if __name__ == "__main__":
#     app = make_app()
#     app.listen(5000)
#     print("Server started on port 5000")
#     tornado.ioloop.IOLoop.current().start()

import os
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
import mtvutils as MTVUT

from mpv import MPVError, Context

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class VideoHandler(tornado.websocket.WebSocketHandler):
  def open(self):
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
      return

  def on_message(self, message):
    mtvcommand, path = message.split(":")
    if mtvcommand == "TIME":
        txt = f"Current time: {MTVUT.get_time()}"
        self.write_message(txt)
    elif mtvcommand == "LOADFILE":
        #vid should autostart
        self.mpv_context.command('loadfile', path)
        self.write_message("Video playing")
    elif mtvcommand == "STOP":
        #Stops vidio playback but does not clean player
        self.mpv_context.command('stop')
        self.write_message("Video paused")
    elif mtvcommand == "PLAY":
        # Resumes video playback after pause
        self.mpv_context.command('set_property', 'pause', 'no')
        self.write_message("Video resumed")
    elif mtvcommand == "QUIT":
        self.mpv_context.command("quit")
        #quits the player
        self.write_message("Video stopped")
    elif mtvcommand == "DESTROY":
        self.mpv_context.terminate_destroy()
        self.write_message("Video destroyed")
    else:
        self.write_message("Invalid command")

  def on_close(self):
    self.mpv_context.terminate_destroy()
    print("Video stopped and connection closed")

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