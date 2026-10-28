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
            self.vic_ambience.volume = 1
            self.vic_ambience.loop = True

        self.vic_ambience2 = SoundLoader.load("assets/victory_ambience_2.mp3")
        if self.vic_ambience2:
            self.vic_ambience2.volume = 0.75
            self.vic_ambience2.loop = True

        self.layout = FloatLayout()
        
        self.logo = Image( #all of them have = to designate and a comma to  follow up
            source="assets/logo.png",
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )

        self.layout.add_widget(self.logo)
        Clock.schedule_once(self.disclaimer, 6)
        return self.layout

    def disclaimer(self, dt):
        self.layout.clear_widgets()
        self.disc_text = "Disclaimer\n\n The graphics and audio in this game are added for extra immersion.\n They are not meant to accurately represent the descriptive text forming this game." 
        self.disclaimer_label = Label(
            text="",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            text_size=(Window.width * 0.9, None), # Prevents text from stretching off screen
            halign='center'
        )
        self.layout.add_widget(self.disclaimer_label)
        self.char_index = 0
        Clock.schedule_interval(lambda dt: self.typewrite(dt, self.disc_text, self.disclaimer_label), 0.1)
        Clock.schedule_once(self.main_menu, 5)

    def main_menu(self, dt):
        self.layout.clear_widgets()
        self.title = Label(
            text="CAVE\nADVENTURES",
            font_size="30sp",
            pos_hint={'center_x': 0.5, 'top': 0.05},
            halign='center'
        )
        self.start_button = Button(
            text="Start",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'bottom': 0.05),
            halign='center'
        )
        self.UI_image = Image(
            source="assets/
            

    def typewrite(self, dt, target_text, label):
        if self.char_index < len(target_text):
           label.text += target_text[self.char_index] #The [] act as an index to determine which character to write.
           self.char_index += 1 #The addition makes it move from one character to the next.
        else:
           return False # Returning False automatically stops the interval loop
        
        
            
if __name__ == "__main__":
    AdventureApp().run()
