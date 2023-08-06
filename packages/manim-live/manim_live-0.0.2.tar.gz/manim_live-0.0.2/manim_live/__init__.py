import pyglet
import os

class ManimLive:
    def __init__(self, directory):
        self.directory = directory

    def run(self):
        window = pyglet.window.Window(fullscreen=True)
        player = pyglet.media.Player()

        for filename in os.listdir(self.directory):
            if filename.endswith(".mp4"):
                #vid_path.append(os.path.join(directory, filename))
                MediaLoad = pyglet.media.load(os.path.join(self.directory, filename))
                player.queue(MediaLoad)
            else:
                continue
            
        player.play()


        @window.event
        def on_draw():
            if player.source and player.source.video_format:
                player.get_texture().blit(0,0)   

        def on_eos():
            player.pause()

        @window.event
        def on_key_press(key, modifiers):
            if key == pyglet.window.key.N and not player.playing:
                player.play()

        player.push_handlers(on_eos) 

        pyglet.app.run()