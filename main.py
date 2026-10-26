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

        self.death_sound = SoundLoader.load("assets/Death.mp3")
        if self.death_sound:
            self.death_sound.volume = 1
            self.death_sound.loop = False

        self.ambience_2 = SoundLoader.load("assets/eyes.mp3")
        if self.ambience_2:
            self.ambience_2.volume = 0.6
            self.ambience_2.loop = True

        self.grapple = SoundLoader.load("assets/grapple.mp3")
        if self.grapple:
            self.grapple.volume = 1
            self.grapple.loop = False

        self.impact = SoundLoader.load("assets/hit_ground.mp3")
        if self.impact:
            self.impact.volume = 1
            self.impact.loop = False

        self.vic_ambience = SoundLoader.load("assets/victory_ambience.mp3")
        if self.vic_ambience:
            self.vic_ammbience.volume = 1
            self.vic_ambience.loop = True

        self.vic_ambience2 = SoundLoader.load("assets/victory_ambience_2.mp3")
        if self.vic_ambience2:
            self.vic_ammbience2.volume = 0.75
            self.vic_ambience2.loop = True


if __name__ == "__main__":
    JumpscareApp().run()
