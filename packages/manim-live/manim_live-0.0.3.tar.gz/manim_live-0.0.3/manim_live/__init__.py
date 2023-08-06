import pyglet
import os

class ManimLive:
    def __init__(self, directory):
        self.directory = directory
        self.files = {}
        for i, filename in enumerate(os.listdir(self.directory)):
            if filename.endswith(".mp4"):
                self.files[filename[:-4]] = {}
                self.files[filename[:-4]]['name'] = filename
                self.files[filename[:-4]]['number'] = i
            else:
                continue

    def list_files(self):
        for i in self.files:
            print(f"file name: {self.files[i]['name']} order number: {self.files[i]['number']}")
            
    def change_order(self, file_numbers):
        for i, f in enumerate(self.files):
            self.files[f]['number'] = file_numbers[i]

    def run(self):
        window = pyglet.window.Window(fullscreen=True)
        player = pyglet.media.Player()

        for i in range(len(self.files)):
            for f in self.files: 
                if self.files[f]['number'] == i:
                    MediaLoad = pyglet.media.load(os.path.join(self.directory, self.files[f]['name']))
                    player.queue(MediaLoad)
            
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


el = ManimLive('./media/')
el.list_files()
el.change_order([2,0,1])
el.list_files()
el.run()