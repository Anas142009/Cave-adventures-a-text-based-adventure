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
        self.images_on = True # default value
        self.ambience_on = True
        self.effects_on = True
        Clock.schedule_once(self.loadlogo, 3)
        return self.layout
        
    def loadlogo(self, dt):
        self.logo = Image( #all of them have = to designate and a comma to  follow up
            source="assets/Logo.png",
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
    
        self.layout.add_widget(self.logo)
        Clock.schedule_once(self.disclaimer, 4)
        
    def disclaimer(self, dt):
        self.layout.clear_widgets()
        self.disc_text = "Disclaimer\n\n The graphics and audio in this game are added for extra immersion.\n They are not meant to accurately represent the descriptive text that forms this game." 
        self.disclaimer_label = Label(
            text="",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            text_size=(Window.width * 0.9, None), # Prevents text from stretching off screen
            halign='center'
        )
        self.layout.add_widget(self.disclaimer_label)
        self.char_index = 0
        Clock.schedule_interval(lambda dt: self.typewrite(dt, self.disc_text, self.disclaimer_label), 0.05)
        schedule_time = len(self.disc_text) * 0.05 + 0.5
        Clock.schedule_once(self.add_understand, schedule_time)

    def add_understand(self, dt):
        self.understand_button = Button(
            text="I understand",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'y': 0.05},
            size_hint=(1, 0.1),
        )
        self.understand_button.bind(on_press=self.main_menu)
        self.layout.add_widget(self.understand_button)
        
    def main_menu(self, instance):
        self.layout.clear_widgets()
        
        self.gamename = Label(
            text="CAVE\nADVENTURES",
            font_size="30sp",
            pos_hint={'center_x': 0.5, 'top': 0.05},
        )
        
        self.start_button = Button(
            text="Start",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.65, 0.2)
        )
        self.UI_image = Image(
            source="assets/Cave.jpg",
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )
        
        self.option_button = Button(
            text="Options",
            font_size="22sp",
            pos_hint={'center_x': 0.5, 'bottom': 0.3},
            size_hint=(0.5, 0.1)
        )
        
        self.quit_button = Button(
            text="Quit",
            font_size="22sp",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'bottom':0.1}
        )
        
        self.UI_image.opacity=0.95
        self.quit_button.bind(on_press=self.quit)
        self.option_button.bind(on_press=self.option_menu)
        self.start_button.bind(on_press=self.start_game)
        
        if self.images_on == True:
            self.layout.add_widget(self.UI_image)
            
        self.layout.add_widget(self.option_button)
        self.layout.add_widget(self.quit_button)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.gamename)
        
        if self.ambience_on == True:
            self.ambience.play()

    def start_game(self, instance):
        self.stop()
            
    def option_menu(self, instance):
        self.layout.clear_widgets()
        self.back_button = Button(
            text="back",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'y': 0.1},
            size_hint=(0.5, 0.09)
        )
        self.back_button.bind(on_press=self.main_menu)
        
        self.images_label = Label(
            text="Images:",
            font_size="24sp",
            pos_hint={'left': 0.05, 'y': 0.97}
        )
        self.yes_image = Button(
            text="On",
            font_size="24sp",
            size_hint=(0.33, 0.09),
            pos_hint={'center_x': 0.5, 'y': 0.97}
        )
        self.no_image = Button(
            text="Off",
            font_size="24sp",
            size_hint=(0.33, 0.09),
            pos_hint={'right': 0.05, 'y': 0.97}
        )
        self.yes_image.bind(on_press=self.turn_on_image)
        self.no_image.bind(on_press=self.turn_off_image)
        if self.images_on == True:
            self.yes_image.disabled = True
        else:
            self.no_image.disabled = True
        
        self.ambience_label = Label(
            text="Ambience:",
            font_size="24sp",
            pos_hint={'left': 0.05, 'y': 0.55}
        )
        self.yes_ambience = Button(
            text="On",
            font_size="24sp",
            size_hint=(0.33, 0.09),
            pos_hint={'center_x': 0.5, 'y': 0.55}
        )
        self.no_ambience = Button(
            text="Off",
            font_size="24sp",
            size_hint=(0.33, 0.09),
            pos_hint={'right': 0.05, 'y': 0.55}
        )
        self.yes_ambience.bind(on_press=self.turn_on_ambience)
        self.no_ambience.bind(on_press=self.turn_off_ambience)
        if self.ambience_on == True:
            self.yes_ambience.disabled = True
        else:
            self.no_ambience.disabled = True
        
        self.effects_label = Label(
            text="Effects:",
            font_size="24sp",
            pos_hint={'left': 0.05, 'y': 0.25}
        )
        self.yes_effect = Button(
            text="On",
            font_size="24sp",
            size_hint=(0.33, 0.09),
            pos_hint={'center_x': 0.5, 'y': 0.25}
        )
        self.no_effect = Button(
            text="Off",
            font_size="24sp",
            size_hint=(0.33, 0.09),
            pos_hint={'right': 0.05, 'y': 0.25}
        )
        self.yes_effect.bind(on_press=self.turn_on_effect)
        self.no_effect.bind(on_press=self.turn_off_effect)
        if self.effects_on == True:
            self.yes_effect.disabled = True
        else:
            self.no_effect.disabled = True
        
        
        self.layout.add_widget(self.images_label)
        self.layout.add_widget(self.effects_label)
        self.layout.add_widget(self.ambience_label)
        self.layout.add_widget(self.back_button)
        self.layout.add_widget(self.yes_image)
        self.layout.add_widget(self.no_image)
        self.layout.add_widget(self.yes_ambience)
        self.layout.add_widget(self.no_ambience)
        self.layout.add_widget(self.yes_effect)
        self.layout.add_widget(self.no_effect)
        
    def typewrite(self, dt, target_text, label):
        if self.char_index < len(target_text):
            label.text += target_text[self.char_index] #The [] act as an index to determine which character to write.
            self.char_index += 1 #The addition makes it move from one character to the next.
        else:
            return False # Returning False automatically stops the interval loop

    def turn_on_image(self, instance):
        self.images_on = True
        self.yes_image.disabled = True
        self.no_image.disabled = False

    def turn_off_image(self, instance):
        self.images_on = False
        self.yes_image.disabled = False
        self.no_image.disabled = True

    def turn_on_ambience(self, instance):
        self.ambience_on = True
        self.yes_ambience.disabled = True
        self.no_ambience.disabled = False

    def turn_off_ambience(self, instance):
        self.ambience_on = False
        self.yes_ambience.disabled = False
        self.no_ambience.disabled = True

    def turn_on_effect(self, instance):
        self.effects_on = True
        self.yes_effect.disabled = True
        self.no_effect.disabled = False

    def turn_off_effect(self, instance):
        self.effects_on = False
        self.yes_effect.disabled = False
        self.no_effect.disabled = True
        
    def quit(self, instance):
        self.stop()
        
            
if __name__ == "__main__":
    AdventureApp().run()
