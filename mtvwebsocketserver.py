import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import mtvutils as UT
import mpv

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        data, param = message.split(":")
        print(f"Client sent: {data}")
        response = ""
        # Respond based on the request
        if data == "HELLO":
            response = f"Hi there, {param}"
        elif data == "TIME":
            response = f"Current time: {UT.get_time()}"
        elif data == "PLAY":
            try:
                m = mpv.Context()
            except mpv.MPVError:
                print('failed creating context')
                return 1

            m.set_option('input-default-bindings')
            m.set_option('osc')
            m.set_option('input-vo-keyboard')
            m.set_option("fs", True)
            m.initialize()

            m.command('loadfile', param)

            while True:
                event = m.wait_event(.01)
                if event.id == mpv.Events.none:
                    continue
                print(event.name)
                if event.id in [mpv.Events.end_file, mpv.Events.shutdown]:
                    break
            response = f"Playing video at:\n\t {param}"
        elif data == "PAUSE":
            m.command('set_property', 'pause', 'yes')
            response = f"Pausing video playback"
        elif data == "RESUME":
            m.command('set_property', 'pause', 'no')
            response = f"Resuming video playback"
        elif data == "STOP":
            m.command('stop')
            response = f"Stopping video playback"
        elif data == "NEXT":
            m.command('seek', '20', 'relative+exact')
            response = f"Seeking forward 20 seconds"
        elif data == "PREVIOUS":
            m.command('seek', '-20', 'relative+exact')
            response = f"Playing previous video"
        else:
            response = "Unknown request."

        # Send the response back to the client
        self.write_message(response)

    def on_close(self):
        print("WebSocket closed")

def make_app():
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/mtvws", WebSocketHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    print("Server started on port 5000")
    tornado.ioloop.IOLoop.current().start()