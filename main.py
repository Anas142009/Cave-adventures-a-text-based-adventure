__version__ = "0.1.0"

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window


class AdventureApp(App):
    def build(self):
        self.ambience = SoundLoader.load("assets/ambience.mp3")
        if self.ambience:
            self.ambience.volume = 0.8
            self.ambience.loop = True
            
        self.collapse = SoundLoader.load("assets/collapse.mp3")
        if self.collapse:
            self.collapse.volume = 1
            self.collapse.loop = False

        self.crack = SoundLoader.load("assets/crack_sound.mp3")
        if self.crack:
            self.crack.volume = 1
            self.crack.loop = True

        self.death_sound = SoundLoader.load("assets/death")
        if self.death_sound:
            self.death_sound.volume = 1
            self.death_sound.loop = False

        self.death_sound = SoundLoader.load("assets/death")
        if self.death_sound:
            self.death_sound.volume = 1
            self.death_sound.loop = False

if __name__ == "__main__":
    JumpscareApp().run()
