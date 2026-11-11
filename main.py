__version__ = "0.1.0"
import os
import platform

os.environ['KIVY_CLOCK'] = 'interrupt'
# Force Windows environments to use ANGLE/DirectX to prevent OpenGL 1.1 crashes
if platform.system() == 'Windows':
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
    
    
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class AdventureApp(App):
    def build(self):
        self.ambience = SoundLoader.load("assets/ambience.mp3")
        if self.ambience:
            self.ambience.volume = 0.75
            self.ambience.loop = True
            
        self.collapse = SoundLoader.load("assets/collapse.mp3")
        if self.collapse:
            self.collapse.volume = 1
            self.collapse.loop = False

        self.crack = SoundLoader.load("assets/crack_sound.mp3")
        if self.crack:
            self.crack.volume = 0.8
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

        self.grapple_back = SoundLoader.load("assets/grapple_back.mp3")        
        if self.grapple_back:
            self.grapple_back.volume = 1
            self.grapple_back.loop = False
            
        self.impact = SoundLoader.load("assets/hit_ground.wav")
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

        self.bat_sound = SoundLoader.load("assets/Bat_sounds.mp3")
        if self.bat_sound:
            self.bat_sound.volume = 1
            self.bat_sound.loop = True
            
        self.bat_sound2 = SoundLoader.load("assets/bat_sounds2.mp3")
        if self.bat_sound2:
            self.bat_sound2.volume = 1
            self.bat_sound2.loop = True
            
        self.bat_sound3 = SoundLoader.load("assets/bat_sounds3.mp3")
        if self.bat_sound3:
            self.bat_sound3.volume = 1
            self.bat_sound3.loop = True
            
        self.boulder_sound = SoundLoader.load("assets/boulder_rolling.mp3")
        if self.boulder_sound:
            self.boulder_sound.volume = 1
            self.boulder_sound.loop = True
        
        self.bat_death = SoundLoader.load("assets/bat_eat.mp3")
        if self.bat_death:
            self.bat_death.volume = 1
            self.bat_death.loop = False
            
        self.crush = SoundLoader.load("assets/bone_break.mp3")
        if self.crush:
            self.crush.volume = 1
            self.crush.loop = False
            
        self.shot = SoundLoader.load("assets/guntrap.mp3")
        if self.shot:
            self.shot.volume = 1
            self.shot.loop = False
            
        self.slamdoor = SoundLoader.load("assets/slamdoor.mp3")
        if self.slamdoor:
            self.slamdoor.volume = 1
            self.slamdoor.loop = False
            
        self.layout = FloatLayout()
        
        #(set all default values here:-
        self.images_on = True 
        self.ambience_on = True
        self.effects_on = True
        self.brown = get_color_from_hex("B3865B")
        self.bat_eaten = "eaten by bats"
        self.fall_death = "fell to doom"
        self.crush_death = "crushed to death"
        self.death_count = 0
        #)
        
        self.continue_button = Button(
            text="Continue",
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            font_size="27sp",
            color=self.brown
        )
        
        self.text_background = Image(
            source="assets/Text_background.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        
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
        self.skip_button = Button(
            text="skip",
            size_hint=(0.1, 0.05),
            pos_hint={'right': 1, 'center_y': 0.25},
            background_normal="",
            background_color=self.brown
        )
        self.skip_button.opacity = 0.5
        self.skip_button.bind(on_press=self.skip_disc)
        self.current_skip_func = self.skip_disc
        
        self.understand_button = Button(
            text="I understand",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'y': 0.05},
            size_hint=(1, 0.1),
        )
        self.understand_button.bind(on_press=self.main_menu)
        
        self.layout.add_widget(self.skip_button)
        self.layout.add_widget(self.disclaimer_label)
        self.char_index = 0
        self.type_write = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.disc_text, self.disclaimer_label), 0.05)
        schedule_time = len(self.disc_text) * 0.05
        self.understood = Clock.schedule_once(self.add_understand, schedule_time)
         

    def skip_disc(self, instance):
        if self.char_index < len(self.disc_text):
            self.layout.add_widget(self.understand_button)
            self.disclaimer_label.text = self.disc_text
            self.type_write.cancel()
            self.understood.cancel()
            self.skip_button.unbind(on_press=self.skip_disc)
            self.layout.remove_widget(self.skip_button)
            self.char_index = 0
        else:
            self.skip_button.unbind(on_press=self.skip_disc)
            self.layout.remove_widget(self.skip_button)
            self.char_index = 0
            
    def add_understand(self, dt):
        self.layout.add_widget(self.understand_button)
        
    def main_menu(self, instance):
        self.layout.clear_widgets()
        
        self.havegrapple = False
        self.started = False
        self.right_grnd_brkn = False
        self.batted = False
        self.quick_timer = 5
        self.skip_button.pos_hint = {'right': 1, 'center_y': 0.425}
        
        self.gamename = Label(
            text="CAVE\nADVENTURES",
            font_size="40sp",
            text_size=(Window.width * 0.9, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            halign='center',
            bold=True,
            italic=True,
            color=self.brown
        )
        
        self.start_button = Button(
            text="Start",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            size_hint=(0.65, 0.2),
            bold=True
        )
        
        self.title_background = Image(
            source="assets/Text_background.png",
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
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
            pos_hint={'center_x': 0.5, 'y': 0.2},
            size_hint=(0.5, 0.1),
            bold=True
        )
        
        self.quit_button = Button(
            text="Quit",
            font_size="22sp",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'y':0.1},
            bold=True
        )
        
        self.secret_btn = Button(
            text="secret code",
            font_size="10sp",
            size_hint=(0.2, 0.1),
            pos_hint={'right': 1, 'y': 0},
            background_color=[0, 0, 0, 0],
            color=[1, 1, 1, 1]
        )
        
        self.secret_stroke = Button(
            text="secret code",
            font_size="11sp",
            size_hint=(0.2, 0.105),
            pos_hint={'right': 1, 'y': 0},
            background_color=[0, 0, 0, 0],
            color=[0, 0, 0, 1]
        )
        self.secret_stroke.disabled = True
        
        self.title_background.opacity = 0.5
        self.UI_image.opacity = 1
        self.quit_button.bind(on_press=self.quit)
        self.option_button.bind(on_press=self.option_menu)
        self.start_button.bind(on_press=self.start_game)
        
        if self.images_on == True:
            self.layout.add_widget(self.UI_image)
        if self.death_count >= 10:
            self.layout.add_widget(self.secret_stroke)
            self.layout.add_widget(self.secret_btn) 
        self.layout.add_widget(self.title_background)
        self.layout.add_widget(self.option_button)
        self.layout.add_widget(self.quit_button)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.gamename)
        
        
        if self.ambience_on == True:
            self.ambience.play()

    def start_game(self, instance):
        self.layout.clear_widgets()
        
        self.skip_button.pos_hint = {'right': 1, 'center_y': 0.425}
        self.skip_button.opacity = 0.5
        
        if self.started == False:
            self.fork_text = "You wake up in an unfamiliar place. You don't remember how you got here. you can vaguely recognise this place as a cave. You look around, you see the path ahead of you splitting into three openings, you don't know where they may lead. The only other openings are two conveniently placed holes, that are lighting the cave. The holes are too high up and too small for you to get out of. Your only path is through one of the three openings ahead of you. Which one do you choose?"
            self.started = True
        else:
            self.fork_text = "You're back at the three openings. How do you proceed?"
        self.fork_label = Label(
            text="",
            font_size="21sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=get_color_from_hex("B3865B"),
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            bold=True,
            valign='top'       
        )
        self.fork_image = Image(
            source="assets/fork.jpeg",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        
        self.skip_button.disabled = False
        self.current_skip_func = self.skip_fork
        self.skip_button.bind(on_press=self.skip_fork)
        
        if self.images_on == True:
            self.fork_image.opacity = 1
            self.layout.add_widget(self.fork_image)
        self.text_background.opacity = 1
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.fork_label)
        self.layout.add_widget(self.skip_button)
        
        self.char_index = 0
        self.type_write_fork = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.fork_text, self.fork_label), 0.045)
        schedule_time = len(self.fork_text) * 0.045 - 0.18
        self.option_fork = Clock.schedule_once(self.add_fork_options, schedule_time)
       
    def skip_fork(self, instance):
         if self.char_index < len(self.fork_text):
            self.fork_label.text = self.fork_text
            self.type_write_fork.cancel()
            self.option_fork.cancel()
            self.layout.remove_widget(self.skip_button)
            self.skip_button.unbind(on_press=self.skip_fork)
            self.option_fork = Clock.schedule_once(self.add_fork_options, 0)
            self.char_index = 0
         else:
            self.layout.remove_widget(self.skip_button)
            self.skip_button.unbind(on_press=self.skip_fork)
            self.char_index = 0
            
    def add_fork_options(self, dt):
        self.r_opening = Button(
            text="Go right -->",
            size_hint=(0.33, 0.4),
            font_size="22sp",
            pos_hint={'right': 1, 'center_y': 0.2},
            text_size=(Window.width * 0.33, Window.height * 0.4),
            halign='right',
            valign='middle',
            background_color=self.brown
        )
        self.r_opening.bind(on_press=self.grapple_path)

        self.l_opening = Button(
            text="<-- Go left",
            size_hint=(0.33, 0.4),
            font_size="22sp",
            pos_hint={'x': 0, 'center_y': 0.2},
            text_size=(Window.width * 0.33, Window.height * 0.4),
            halign='left',
            valign='middle',
            background_color=self.brown
        )
        self.l_opening.bind(on_press=self.long_path)

        self.m_opening = Button(
            text="Go middle",
            font_size="22sp",
            size_hint=(0.33, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            text_size=(Window.width * 0.33, Window.height * 0.4),
            halign='center',
            valign='middle',
            background_color=self.brown
        )
        self.m_opening.bind(on_press=self.big_hole)

        self.layout.add_widget(self.l_opening)
        self.layout.add_widget(self.r_opening)
        self.layout.add_widget(self.m_opening)

    def big_hole(self, instance):
        self.layout.clear_widgets()
        #REMOVE    THIS    AFTER    TESTING:(
        #self.havegrapple = True
        #)
        if self.havegrapple == True:
            self.hole_text = "You walk straight forward.\nA giant pit stops you in your path.\nYour grapple gun might get you over it, do you want to use it?"
        else:
            self.hole_text = "You walk straight forward.\nA giant pit stops you in your path.\nYou can't find a way to get across."

        self.pit_label = Label(
            text="",
            font_size="27sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=get_color_from_hex("B3865B"),
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            bold=True,
            valign='top'       
        )
        self.pit_image = Image(
            source="assets/pit.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        ) 
        
        self.text_background.opacity = 0.8
        self.char_index = 0
        self.current_skip_func = self.skip_pit
        self.skip_button.bind(on_press=self.skip_pit)
        self.skip_button.opacity = 0.5
        self.skip_button.disabled = False
          
        if self.images_on == True:
            self.layout.add_widget(self.pit_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.pit_label)
        self.layout.add_widget(self.skip_button)
        
        self.type_write_pit = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.hole_text, self.pit_label), 0.05)
        schedule_time = len(self.hole_text) * 0.05 + 1.8
        self.add_pit_options = Clock.schedule_once(self.pit_options, schedule_time)
        pause_timing = len("You walk straight forward.") * 0.05 - 0.05
        self.threshold = "You walk straight forward."
        self.pause_type_write = Clock.schedule_once(lambda dt:  self.pause_typewrite(dt, self.type_write_pit, 1, self.threshold), pause_timing)
        self.threshold2 = "You walk straight forward.\nA giant pit stops you in your path."
        pause_timing2 = len("You walk straight forward.\nA giant pit stops you in your path.") * 0.05 + 0.85
        self.pause_type_write2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_pit, 0.5, self.threshold2), pause_timing2)
        
    def skip_pit(self, instance):
         if self.char_index < len(self.hole_text):
            self.pit_label.text = self.hole_text
            self.type_write_pit.cancel()
            self.add_pit_options.cancel()
            self.pause_type_write.cancel()
            self.pause_type_write2.cancel()
            try:
                self.resumption.cancel()
            except:
                pass
            self.layout.remove_widget(self.skip_button)
            self.skip_button.unbind(on_press=self.skip_pit)
            self.char_index = 0
            self.option_fork = Clock.schedule_once(self.pit_options, 0)
         else:
            self.layout.remove_widget(self.skip_button)
            self.skip_button.unbind(on_press=self.skip_pit)
            self.char_index = 0
    
    def pit_options(self, dt):
        self.return_button = Button(
            text="Go back",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y':0.1},
            font_size="24sp",
            background_color=self.brown
        )
        self.return_button.bind(on_press=self.start_game)
        self.grapple_across = Button(
            text="Use the grapple gun",
            size_hint=(1,  0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            font_size="24sp",
            background_color=self.brown
        )
        if not self.batted:
            self.grapple_across.bind(on_press=self.grappled)
        else:
            self.grapple_across.bind(on_press=self.grappled2)
        
        if self.havegrapple == True:
            self.layout.add_widget(self.return_button)
            self.layout.add_widget(self.grapple_across)
        else:
            self.layout.add_widget(self.return_button)
                   
    def grappled2(self, instance):
        self.layout.clear_widgets()
        self.grappled2_text = "You grapple back to the area where the bats attacked you. You take one last moment to consider your options."
        self.threshold2="You grapple back to the area where the bats attacked you."
        self.grappled2_label = Label(
            text="",
            font_size="30sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0,  'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True,
            color=self.brown
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.grappled2_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_grappled2
        self.skip_button.bind(on_press=self.skip_grappled2)
        
        self.type_write_grappled2 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.grappled2_text, self.grappled2_label), 0.05)
        pause_time2 = len(self.threshold2) * 0.05 - 0.2
        if self.effects_on:
            self.play_grap = Clock.schedule_once(lambda dt: self.grapple.play(), pause_time2 + 0.2)
            self.play_grapB = Clock.schedule_once(lambda dt: self.grapple_back.play(), pause_time2 + 3.7)
            self.pause_grappled2_2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_grappled2, 6, self.threshold2), pause_time2)
        else:
            self.pause_grappled2_2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_grappled2, 0.5, self.threshold2), pause_time2)
                
        if self.effects_on:
            schedule_time = len(self.grappled2_text) * 0.05 + 6
        else:
            schedule_time = len(self.grappled2_text) * 0.05 + 0.5
        self.batted_options = Clock.schedule_once(self.evade_options, schedule_time)
        
    def skip_grappled2(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_write_grappled2.cancel()
            self.pause_grappled2_2.cancel()            
            if self.effects_on:
                self.play_grap.cancel()
                self.play_grapB.cancel()
            self.batted_options.cancel()
            try:
                self.resumption.cancel()
            except:
                pass
            self.char_index = 0
            Clock.schedule_once(self.evade_options, 0)
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
        
    def grappled(self, instance):
        self.layout.clear_widgets()
        self.grappled_text = "You fire the grapple gun. It attaches to the wall on the other side. You pull in and land safely. It's dark. You hear weird noises from afar. The noises are growing stronger and closer, BATS! A giant horde of bats is rushing toward you. You have to act fast, what do you do?"
        self.threshold = ""
        self.threshold2 = "You fire the grapple gun. It attaches to the wall on the other side."
        self.threshold3 =  "You fire the grapple gun. It attaches to the wall on the other side. You pull in and land safely."
        self.threshold4 = "You fire the grapple gun. It attaches to the wall on the other side. You pull in and land safely. It's dark. You hear weird noises from afar."
        self.threshold5 = "You fire the grapple gun. It attaches to the wall on the other side. You pull in and land safely. It's dark. You hear weird noises from afar. The noises are growing stronger and closer, BATS!"
        self.grappled_label = Label(
            text="",
            font_size="22sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        self.bat_attack = Image(
            source="assets/bat_attack.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.bat_attack.opacity = 0
            self.layout.add_widget(self.bat_attack)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.grappled_label)
        
        self.type_write_bat = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.grappled_text, self.grappled_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.15
        if self.effects_on:
            self.pause_bat = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_bat, 3.5, self.threshold), pause_time)
            self.usegrap = Clock.schedule_once(lambda dt: self.grapple.play(), pause_time)
        if self.effects_on:
            pause_time2 = len(self.threshold2) * 0.05 + 3.2
        else:
            pause_time2 = len(self.threshold2) * 0.05 - 0.15
        self.pause_bat2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_bat, 2.5, self.threshold2), pause_time2)
        if self.effects_on:
            self.grapB = Clock.schedule_once(lambda dt: self.grapple_back.play(), pause_time2)
        pause_time3 = len(self.threshold3) * 0.05 + 5.5
        if self.effects_on:
            self.pause_bat3 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_bat, 0.7, self.threshold3), pause_time3)
            self.bat_noises = Clock.schedule_once(self.play_bats, pause_time3)
        if self.effects_on:
            pause_time4 = len(self.threshold4) * 0.05 + 6
        else:
            pause_time4 = len(self.threshold4) * 0.05 + 2.15
        if self.effects_on:
            self.bat_amp = Clock.schedule_once(self.amp_bats, pause_time4)
        self.pause_bat4 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_bat, 0.7, self.threshold4), pause_time4)
        if self.images_on:
            Clock.schedule_once(lambda dt: self.make_appearance(dt, self.bat_attack, 0.5, 0.1), pause_time4)
        if self.effects_on:
            pause_time5 = len(self.threshold5) * 0.05 + 6.7
        else:
            pause_time5 = len(self.threshold5) * 0.05 + 2.8
        if self.images_on:
            Clock.schedule_once(lambda dt: self.make_appearance(dt, self.bat_attack, 1, 0.1), pause_time5)
        self.pause_bat5 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_bat, 1, self.threshold5), pause_time5)
        if self.effects_on:
            schedule_time = len(self.grappled_text) * 0.05 + 7.9
        else:
             schedule_time = len(self.grappled_text) * 0.05 + 4.5
        self.bat_situation = Clock.schedule_once(self.add_bat_options, schedule_time)
        self.cod = "eaten by bats"
        Clock.schedule_once(lambda dt: self.start_timer(dt, self.grappled, self.bat_sound), schedule_time)
        if self.effects_on:
            self.qtfu = Clock.schedule_once(self.bat_stop, schedule_time + 5.5)
                    
    def bat_stop(self, dt):
          try:
              self.bat_sound.stop()
          except:
              pass
          self.bat_sound2.stop()
          self.bat_sound3.stop()
              
    def add_bat_options(self, dt):
        self.fend_off = Button(
            text="Try to fend them off using the grapple gun",
            font_size="22sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=self.brown
        )
        self.fend_off.bind(on_press=self.fended)
        self.evade = Button(
            text="Try to avoid them",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_color=self.brown
        )
        self.evade.bind(on_press=self.evaded)
        
        self.layout.add_widget(self.fend_off)
        self.layout.add_widget(self.evade)
        
    def fended(self, instance):
        self.layout.clear_widgets()
        self.qte.cancel()
        if self.effects_on:
            self.qtfu.cancel()
        self.fended_text = "You try to use your grapple gun to fend them off. You fend off the first, second, and third bat successfully. The fourth bat latches onto your ear and rips it off. As you try to recover, a few more bats latch onto your shoulders, arms, and face. They bite and scratch multiple times, you are simply overwhelmed by their huge number. It hurt so much, your whole body feels numb now. You pass out."
        self.threshold = "You try to use your grapple gun to fend them off. You fend off the first, second, and third bat successfully."
        self.threshold2 = "You try to use your grapple gun to fend them off. You fend off the first, second, and third bat successfully. The fourth bat latches onto your ear and rips it off."
        self.threshold3 = "You try to use your grapple gun to fend them off. You fend off the first, second, and third bat successfully. The fourth bat latches onto your ear and rips it off. As you try to recover, a few more bats latch onto your shoulders, arms, and face."
        self.threshold4 = "You try to use your grapple gun to fend them off. You fend off the first, second, and third bat successfully. The fourth bat latches onto your ear and rips it off. As you try to recover, a few more bats latch onto your shoulders, arms, and face. They bite and scratch multiple times, you are simply overwhelmed by their huge number."
        self.threshold5 = "You try to use your grapple gun to fend them off. You fend off the first, second, and third bat successfully. The fourth bat latches onto your ear and rips it off. As you try to recover, a few more bats latch onto your shoulders, arms, and face. They bite and scratch multiple times, you are simply overwhelmed by their huge number. It hurt so much, your whole body feels numb now."
        self.fended_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.fended_label)
        
        self.type_write_fend = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.fended_text, self.fended_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.5
        self.pause_fend = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_fend, 0.5, self.threshold), pause_time) 
        pause_time2 = len(self.threshold2) * 0.05 - 0.15
        self.pause_fend2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_fend, 0.7, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3) * 0.05 + 0.45
        self.pause_fend3 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_fend, 0.5, self.threshold3), pause_time3)
        pause_time4 = len(self.threshold4) * 0.05 + 0.8
        self.pause_fend4 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_fend, 0.5, self.threshold4), pause_time4)
        pause_time5 = len(self.threshold5) * 0.05 + 1.25
        self.pause_fend5 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_fend, 0.5, self.threshold5), pause_time5)
        schedule_time = len(self.fended_text) * 0.05 + 3.75
        Clock.schedule_once(lambda dt: self.game_over(dt, self.grappled), schedule_time)
        if self.effects_on:
            Clock.schedule_once(self.bat_stop, schedule_time)          
    
    def amp_bats(self, dt):
        Clock.schedule_interval(lambda dt: self.amplification(dt, self.bat_sound, 0.8), 1)
        Clock.schedule_interval(lambda dt: self.amplification(dt, self.bat_sound2, 0.8), 1)
        Clock.schedule_interval(lambda dt: self.amplification(dt, self.bat_sound3, 0.8), 1)
        
                
    def evaded(self, instance):
        self.layout.clear_widgets()
        self.qte.cancel()
        self.batted = True
        if self.effects_on:
            self.qtfu.cancel()
        self.evaded_text = "You roll to the side and stay low. You watch as one, two, three bats fly by you. Soon after, a fourth bat passes by followed by the rest of them. They fly by you like a very fast gust of wind. You stand back up. There is a faint light from the area where the bats were, but you don't know what might await you there. Do you follow that, or head back towards the fork?"
        self.threshold = "You roll to the side and stay low. You watch as one,"
        self.threshold2 = "You roll to the side and stay low. You watch as one, two,"
        self.threshold3 = "You roll to the side and stay low. You watch as one, two, three bats fly by you."
        self.threshold4 = "You roll to the side and stay low. You watch as one, two, three bats fly by you. Soon after, a fourth bat passes by followed by the rest of them."
        self.threshold5 = "You roll to the side and stay low. You watch as one, two, three bats fly by you. Soon after, a fourth bat passes by followed by the rest of them. They fly by you like a very fast gust of wind."
        self.threshold6 = "You roll to the side and stay low. You watch as one, two, three bats fly by you. Soon after, a fourth bat passes by followed by the rest of them. They fly by you like a very fast gust of wind. You stand back up. There is a faint light from the area where the bats were, but you don't know what might await you there."
        self.evaded_label = Label(
            text="",
            font_size="22sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.evaded_label)
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_evaded)
        self.current_skip_func = self.skip_evaded
        
        self.type_write_evaded = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.evaded_text, self.evaded_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.2
        self.pause_evaded = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_evaded, 0.3, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.1
        self.pause_evaded2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_evaded, 0.3, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3) * 0.05 + 0.4
        self.pause_evaded3 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_evaded, 0.6, self.threshold3), pause_time3)
        pause_time4 = len(self.threshold4) * 0.05 + 0.9
        self.pause_evaded4 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_evaded, 0.5, self.threshold4), pause_time4)
        pause_time5 = len(self.threshold5) * 0.05 + 1.4
        self.pause_evaded5 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_evaded, 0.5, self.threshold5), pause_time5)
        pause_time6 = len(self.threshold6) * 0.05 + 1.7
        if self.effects_on:
            self.bats_pass = Clock.schedule_once(self.bat_stop, pause_time5 + 0.5)
        self.pause_evaded6 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_evaded, 1, self.threshold6), pause_time6)
        schedule_time = len(self.evaded_text) * 0.05 + 3
        self.evasion_option = Clock.schedule_once(self.evade_options, schedule_time)
        
    def evade_options(self, dt):
        self.forward = Button(
            text="Go towards the light",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color = self.brown
        )
        self.forward.bind(on_press=self.myroom)
        
        self.backward = Button(
            text="Go back",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_color = self.brown
        )
        self.backward.bind(on_press=self.head_back)
        
        self.layout.add_widget(self.forward)
        self.layout.add_widget(self.backward)    
    
    def skip_evaded(self, dt):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_write_evaded.cancel()
            self.pause_evaded.cancel()
            self.pause_evaded2.cancel()
            self.pause_evaded3.cancel()
            self.pause_evaded4.cancel()
            self.pause_evaded5.cancel()
            self.pause_evaded6.cancel()
            if self.effects_on:
                self.bats_pass.cancel()
                Clock.schedule_once(self.bat_stop, 0)
            self.evasion_option.cancel()
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            Clock.schedule_once(self.evade_options, 0)
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)    
    
    def head_back(self, instance):
        self.layout.clear_widgets()
        self.headed_text = "After a long moment of thought, you decide that it's not worth the risk. You turn back around and grapple back to the fork."
        self.headed_label = Label(
            text="",
            color=self.brown,
            font_size="28sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.headed_label)
        self.current_skip_func = self.skip_head
        self.skip_button.bind(on_press=self.skip_head)
        self.layout.add_widget(self.skip_button)
        
        self.type_write_head = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.headed_text, self.headed_label), 0.05)
        schedule_time = len(self.headed_text) * 0.05
        self.headcont = Clock.schedule_once(lambda dt: self.add_continue(dt, self.start_game), schedule_time)
    
    def skip_head(self, dt):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_write_head.cancel()
            self.headcont.cancel()
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.start_game), 0)
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
    
    def myroom(self, instance):
        self.layout.clear_widgets()
        self.myroom_text = """You walk towards the light. Your eyes open wide, your heart starts racing, you don't know what to make of the scene in front of you. "A room?" You ask yourself, "What's a room doing inside a cave??" You ponder. As you keep examining the room, it looks nothing short of an ordinary room, a sofa, two chairs, a table, and even a rug under the table. Your mind is jumbled, you are more confused than you've ever been. You step into the room, a big metal shutter closes the opening behind you. You try to lift it back up, bang on it, or even find a button next to it. Nothing, it appears you have been locked in here. On the table to the far western wall of the room, a tape recorder sits, with a tape labeled "play me". You take a moment to consider your actions. """
        self.threshold = """You walk towards the light. Your eyes open wide, your heart starts racing, you don't know what to make of the scene in front of you."""
        self.threshold2 = """You walk towards the light. Your eyes open wide, your heart starts racing, you don't know what to make of the scene in front of you. "A room?" You ask yourself, "What's a room doing inside a cave??" You ponder."""
        self.threshold3 = """You walk towards the light. Your eyes open wide, your heart starts racing, you don't know what to make of the scene in front of you. "A room?" You ask yourself, "What's a room doing inside a cave??" You ponder. As you keep examining the room, it looks nothing short of an ordinary room, a sofa, two chairs, a table, and even a rug under the table. """
        self.threshold4 = """You walk towards the light. Your eyes open wide, your heart starts racing, you don't know what to make of the scene in front of you. "A room?" You ask yourself, "What's a room doing inside a cave??" You ponder. As you keep examining the room, it looks nothing short of an ordinary room, a sofa, two chairs, a table, and even a rug under the table. Your mind is jumbled, you are more confused than you've ever been. You step into the room, """
        self.threshold5 = """You walk towards the light. Your eyes open wide, your heart starts racing, you don't know what to make of the scene in front of you. "A room?" You ask yourself, "What's a room doing inside a cave??" You ponder. As you keep examining the room, it looks nothing short of an ordinary room, a sofa, two chairs, a table, and even a rug under the table. Your mind is jumbled, you are more confused than you've ever been. You step into the room, a big metal shutter closes the opening behind you. """
        self.threshold6 = """You walk towards the light. Your eyes open wide, your heart starts racing, you don't know what to make of the scene in front of you. "A room?" You ask yourself, "What's a room doing inside a cave??" You ponder. As you keep examining the room, it looks nothing short of an ordinary room, a sofa, two chairs, a table, and even a rug under the table. Your mind is jumbled, you are more confused than you've ever been. You step into the room, a big metal shutter closes the opening behind you. You try to lift it back up, bang on it, or even find a button next to it. Nothing, it appears you have been locked in here."""
        self.threshold7 = """You walk towards the light. Your eyes open wide, your heart starts racing, you don't know what to make of the scene in front of you. "A room?" You ask yourself, "What's a room doing inside a cave??" You ponder. As you keep examining the room, it looks nothing short of an ordinary room, a sofa, two chairs, a table, and even a rug under the table. Your mind is jumbled, you are more confused than you've ever been. You step into the room, a big metal shutter closes the opening behind you. You try to lift it back up, bang on it, or even find a button next to it. Nothing, it appears you have been locked in here. On the table to the far western wall of the room, a tape recorder sits, with a tape labeled "play me". """
        self.myroom_label = Label(
            text="",
            font_size="17sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        self.myroom_image = Image(
            source="assets/roomimage.jpg",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch = True,
            keep_ratio = False
        )
        self.myroom_image.opacity = 0
        self.layout.add_widget(self.myroom_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.myroom_label)
        self.current_skip_func = self.skip_room
        self.skip_button.bind(on_press=self.skip_room)
        self.layout.add_widget(self.skip_button)
        
        self.type_write_room = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.myroom_text, self.myroom_label), 0.05)
        
        pause_time = len(self.threshold) * 0.05 - 0.5
        self.pause_room = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_room, 1.5, self.threshold), pause_time)
        if self.images_on:
            self.show_image = Clock.schedule_once(lambda dt: self.make_appearance(dt, self.myroom_image, 1, 0.1), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.85
        self.pause_room2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_room, 0.5, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3) * 0.05 + 0.95
        self.pause_room3 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_room, 0.5, self.threshold3), pause_time3)
        pause_time4 = len(self.threshold4) * 0.05 + 1.15
        self.pause_room4 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_room, 1, self.threshold4), pause_time4)
        if self.effects_on:
            self.slamshut = Clock.schedule_once(lambda dt: self.slamdoor.play(), pause_time4)
        if self.ambience_on:
            self.ambience.stop()
        pause_time5 = len(self.threshold5) * 0.05 + 1.95
        self.pause_room5 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_room, 0.5, self.threshold5), pause_time5)
        pause_time6 = len(self.threshold6) * 0.05 + 2.05
        self.pause_room6 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_room, 0.75, self.threshold6), pause_time6)
        pause_time7 = len(self.threshold7) * 0.05 + 2.35
        self.pause_room7 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_room, 0.5, self.threshold7), pause_time7)
        schedule_time = len(self.myroom_text) * 0.05 + 3.2
        self.roomcont = Clock.schedule_once(self.room_options, schedule_time)
        
    def skip_room(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_write_room.cancel()
            self.pause_room.cancel()
            self.pause_room2.cancel()
            self.pause_room3.cancel()
            self.pause_room4.cancel()
            self.pause_room5.cancel()
            self.pause_room6.cancel()
            self.pause_room7.cancel()
            if self.effects_on:
                self.slamshut.cancel()
            if self.images_on:
                self.show_image.cancel()
                self.myroom_image.opacity = 1
            self.roomcont.cancel()
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
            Clock.schedule_once(self.room_options, 0)
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
    
    def room_options(self, dt):
        self.search = Button(
            text="Try to find another exit",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=self.brown
        )
        self.search.bind(on_press=self.searched)
        
        self.playtape = Button(
            text="Play the tape",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_color=self.brown
        )
        self.playtape.bind(on_press=self.play_tape)
        
        self.layout.add_widget(self.playtape)
        self.layout.add_widget(self.search)
    
    def play_tape(self, instance):
        self.layout.clear_widgets()
        self.tape_text = """You put in the tape and press play, "Welcome to my room." A voice speaks, seemingly changed with a voice changer. Your heart starts racing, is this the man behind it all? "As you have probably figured out by now, this whole thing was set up by us" the tape pauses for a moment, a moment that felt like ages to you. "Who is *us*? Why was this set up? How did I get into this?" A storm of thoughts brews in your head. The tape continues, "As you can see, this... *cave* is special, the tape recorder you're listening to is special, and even YOU are special." The tape pauses again, it feels like the tape is trying to psychologically torment you, and it is succeeding."""
        self.threshold = """You put in the tape and press play, "Welcome to my room." A voice speaks, seemingly changed with a voice changer. Your heart starts racing, is this the man behind it all?"""
        self.threshold2 = """You put in the tape and press play, "Welcome to my room." A voice speaks, seemingly changed with a voice changer. Your heart starts racing, is this the man behind it all? "As you have probably figured out by now, this whole thing was set up by us" the tape pauses for a moment, a moment that felt like ages to you. "Who is *us*? Why was this set up? How did I get into this?" A storm of thoughts brews in your head."""
        self.threshold3 = """You put in the tape and press play, "Welcome to my room." A voice speaks, seemingly changed with a voice changer. Your heart starts racing, is this the man behind it all? "As you have probably figured out by now, this whole thing was set up by us" the tape pauses for a moment, a moment that felt like ages to you. "Who is *us*? Why was this set up? How did I get into this?" A storm of thoughts brews in your head. The tape continues, "As you can see, this... *cave* is special, the tape recorder you're listening to is special, and even YOU are special." """
        self.tape_label = Label(
            text="",
            font_size="18sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.tape_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_tape
        self.skip_button.bind(on_press=self.skip_tape)
        
        self.type_tape = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.tape_text, self.tape_label), 0.06)
        pause_time = len(self.threshold) * 0.06 - 0.5
        self.pause_tape = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_tape, 1, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.06  
        self.pause_tape2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_tape, 1, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3) * 0.06 + 0.5
        self.pause_tape3 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_tape, 1, self.threshold3), pause_time3)
        schedule_time = len(self.tape_text) * 0.06 + 1.5
        self.tapecont = Clock.schedule_once(lambda dt: self.add_continue(dt, self.conttape), schedule_time)    
        
    def skip_tape(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_tape.cancel()
            self.pause_tape.cancel()
            self.pause_tape2.cancel()
            self.pause_tape3.cancel()
            self.tapecont.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.conttape), 0)
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)            
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
    
    def conttape(self, instance):
        self.layout.clear_widgets()
        self.continuation_text = """The tape continues, "The tape recorder you are using right now is special because only the play button works, no other buttons function" you immediately test the pause, record, and stop recording button. Nothing happens, he is right. "This place is special because, well, I'm sure you already know." He is right, the place you woke up in, the conveniently-placed holes for light, the grapple gun on a pedestal, and eventually this room, all lead you to beleive that this place was man-made. "and you, you are special because you've been chosen for this project, so be proud." "Proud? What the hell is he talking about?" You start feeling rage filling your heart, you feel like you'd kill him the instant you get a chance to."""
        self.threshold = """The tape continues, "The tape recorder you are using right now is special because only the play button works, no other buttons function" you immediately test the pause, record, and stop recording button. Nothing happens, he is right."""
        self.threshold2  = """The tape continues, "The tape recorder you are using right now is special because only the play button works, no other buttons function" you immediately test the pause, record, and stop recording button. Nothing happens, he is right. "This place is special because, well, I'm sure you already know." He is right, the place you woke up in, the conveniently-placed holes for light, the grapple gun on a pedestal, and eventually this room, all lead you to beleive that this place was man-made."""
        self.threshold3 = """The tape continues, "The tape recorder you are using right now is special because only the play button works, no other buttons function" you immediately test the pause, record, and stop recording button. Nothing happens, he is right. "This place is special because, well, I'm sure you already know." He is right, the place you woke up in, the conveniently-placed holes for light, the grapple gun on a pedestal, and eventually this room, all lead you to beleive that this place was man-made. "and you,"""
        self.continuation_label = Label(
            text="",
            font_size="18sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.975},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )        
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.continuation_label)
        self.current_skip_func = self.skip_tape2
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_tape2)
        
        self.type_tape2 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.continuation_text, self.continuation_label), 0.07)
        pause_time = len(self.threshold) * 0.07 - 0.7
        self.pause_tape = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_tape2, 0.8, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.07 - 0.4 
        self.pause_tape2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_tape2, 0.8, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3)  * 0.07 + 0.4
        self.pause_tape3 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_tape2, 1.5, self.threshold3), pause_time3)
        schedule_time = len(self.continuation_text) * 0.07 + 1.9
        self.tape2cont = Clock.schedule_once(lambda dt: self.add_continue(dt, self.tape3), schedule_time) 
    
    def skip_tape2(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_tape2.cancel()
            self.pause_tape.cancel()
            self.pause_tape2.cancel()
            self.pause_tape3.cancel()
            self.tape2cont.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.tape3), 0)
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)            
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
    
    def tape3(self, instance):
        self.layout.clear_widgets()
        self.tape3_text = """ "There is another reason for why this recorder is special," the tape continues, "it might give you a way out." As soon as you hear that, your heart feels lightened. You don't quite understand the feeling you've just felt, but it's definitely good. "When this recording finishes, a puzzle shall reveal itself to you. Solve it correctly, and you shall survive; However," The tape pauses. The pause freaks you out. Your heart is racing rapidly, thinking about what the next sentence could be makes you feel sick. Just the thought of it torments you."""
        self.threshold = """ "There is another reason for why this recorder is special," the tape continues, "it might give you a way out." As soon as you hear that, your heart feels lightened. You don't quite understand the feeling you've just felt, but it's definitely good."""
        self.threshold2 = """ "There is another reason for why this recorder is special," the tape continues, "it might give you a way out." As soon as you hear that, your heart feels lightened. You don't quite understand the feeling you've just felt, but it's definitely good. "When this recording finishes, a puzzle shall reveal itself to you. Solve it correctly, and you shall survive; However," The tape pauses."""
        self.tape3_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.tape3_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_tape3
        self.skip_button.bind(on_press=self.skip_tape3)
        
        self.type_tape3 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.tape3_text, self.tape3_label), 0.07)
        pause_time = len(self.threshold) * 0.07 - 0.8
        self.pause_tape = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_tape3, 1, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.07
        self.pause_tape2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_tape3, 0.75, self.threshold2), pause_time2)
        schedule_time = len(self.tape3_text) * 0.07 + 1
        self.continue_tape = Clock.schedule_once(lambda dt: self.add_continue(dt, self.puzzle_reveal), schedule_time)
        
    def skip_tape3(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_tape3.cancel()
            self.pause_tape.cancel()
            self.pause_tape2.cancel()
            self.continue_tape.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.puzzle_reveal), 0)
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)            
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
        
    def puzzle_reveal(self, instance):
        self.layout.clear_widgets()
        self.puzzle_text = """ "May you solve it incorrectly, your survival is not guaranteed, in fact, your doom is almost certain." You feel your heart drop to your knees, that last sentence made you feel emminent danger. "Think hard, solve carefully. The puzzle is definitely solveable, and remember, only make your choice when you're sure of your answer. Good luck!" The tape finishes, and as soon as it does, the wall in front of you opens like an elevator door. Behind it is a screen with instructions, it appears that this is the puzzle he was referring to."""
        self.threshold=""" "May you solve it incorrectly, your survival is not guaranteed, in fact, your doom is almost certain." You feel your heart drop to your knees, that last sentence made you feel emminent danger."""
        self.threshold2 = """ "May you solve it incorrectly, your survival is not guaranteed, in fact, your doom is almost certain." You feel your heart drop to your knees, that last sentence made you feel emminent danger. "Think hard, solve carefully. The puzzle is definitely solveable, and remember, only make your choice when you're sure of your answer. Good luck!" The tape finishes, and as soon as it does, the wall in front of you opens like an elevator door."""
        self.puzzle_label = Label(
            text="",
            font_size="20sp",
            color=self.brown,
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.puzzle_label)
        self.current_skip_func = self.skip_puzzle
        self.skip_button.bind(on_press=self.skip_puzzle)
        self.layout.add_widget(self.skip_button)
        
        self.type_puzzle = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.puzzle_text, self.puzzle_label), 0.06)
        pause_time = len(self.threshold) * 0.06 - 0.7
        self.pause_puzzle = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_puzzle, 0.7, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.06 - 0.1
        self.pause_puzzle2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_puzzle, 0.7, self.threshold2), pause_time2)
        schedule_time = len(self.puzzle_text) * 0.06 + 0.85
        self.riddle_time = Clock.schedule_once(lambda dt: self.add_continue(dt, self.riddle), schedule_time)
    
    def skip_puzzle(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_puzzle.cancel()
            self.pause_puzzle.cancel()
            self.pause_puzzle2.cancel()
            self.riddle_time.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.riddle), 0)
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)            
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
        
    def riddle(self, instance):
        self.layout.clear_widgets()
        if self.ambience_on:
            try:
                self.ambience.stop()
            except:
                pass
        self.riddle_text = """You take a deep breath and start reading the instructions. "Below, is a riddle. Press the correct button, and you win. press the wrong button, and you lose. Press both buttons at once and you lose. Remember, only press when you're sure." You look down, you see two buttons labeled 'left' and 'right'. Between them lies a piece of paper that reads, "I may seem long, but I am short. If you walk with me, I rumble. Soon after that, I crumble. What am I?" At first this seems like a sick joke, but you decide to think about an actual solution anyway. Which button do you press?"""
        self.riddle_label = Label(
            text="",
            font_size="20sp",
            color=self.brown,
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.riddle_image = Image(
            source="assets/buttons.jpg",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.riddle_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.riddle_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_riddle
        self.skip_button.bind(on_press=self.skip_riddle)
        
        self.type_riddle = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.riddle_text, self.riddle_label), 0.05)
        schedule_time = len(self.riddle_text) * 0.05
        self.solving = Clock.schedule_once(self.solve_riddle, schedule_time)
    
    def skip_riddle(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_riddle.cancel()
            self.solving.cancel()
            Clock.schedule_once(self.solve_riddle, 0)
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)            
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
    
    def solve_riddle(self, dt):
        self.correct = False
        self.left_btn = Button(
            text="left",
            font_size="24sp",
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.1, 'center_y': 0.2},
            background_color=self.brown
        )
        self.left_btn.bind(on_press=self.solution)
        self.left_btn.bind(on_press=self.wrong)
        
        self.right_btn = Button(
            text="right",
            font_size="24sp",
            size_hint=(0.3, 0.2),
            pos_hint={'x': 0.6, 'center_y': 0.2},
            background_color=self.brown
        )
        self.right_btn.bind(on_press=self.solution)
        self.right_btn.bind(on_press=self.Ranswer)
        
        self.layout.add_widget(self.left_btn)
        self.layout.add_widget(self.right_btn)
    
    def Ranswer(self, instance):
        self.correct = True
        
    def wrong(self, instance):
        self.correct = False
    
    def solution(self, instance):
        self.layout.clear_widgets()
        if self.correct == True:
            self.solution_text = """You press the right button. Your heart feels like it's about to explode, the screen shows a response. "Correct! the exit shall be revealed!", A surge of extreme happiness and relief flow inside of you. You look around for the exit, you don't see anything. You start to worry, did he lie to you? Suddenly, the northern wall of the room opens up the same way the one to the west did. A great amount of sunlight rushes in through the opening. The happiness you feel at the moment is undescribable."""
            self.threshold = "You press the right button."
            self.threshold2 = """You press the right button. Your heart feels like it's about to explode, the screen shows a response. "Correct! the exit shall be revealed!", A surge of extreme happiness and relief flow inside of you. You look around for the exit, you don't see anything."""
            self.threshold3 = """You press the right button. Your heart feels like it's about to explode, the screen shows a response. "Correct! the exit shall be revealed!", A surge of extreme happiness and relief flow inside of you. You look around for the exit, you don't see anything. You start to worry, did he lie to you? Suddenly,"""
            self.solution_label = Label(
                text="",
                font_size="19sp",
                size_hint=(1, 0.6),
                pos_hint={'x': 0, 'top': 0.95},
                color=self.brown,
                text_size=(Window.width * 0.9, Window.height * 0.6),
                halign='left',
                valign='top',
                bold=True
            )
            self.layout.add_widget(self.text_background)
            self.layout.add_widget(self.solution_label)
            
            self.type_solution = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.solution_text, self.solution_label), 0.06)
            pause_time = len(self.threshold) * 0.06 - 0.1
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_solution, 2, self.threshold), pause_time)
            pause_time2 = len(self.threshold2) * 0.06 + 1
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_solution, 0.75, self.threshold2), pause_time2)
            pause_time3 = len(self.threshold3) * 0.06 + 1.7
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_solution, 0.6, self.threshold3), pause_time3)
            schedule_time = len(self.solution_text) * 0.06 + 3
            self.exit_num = "1"
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.victory_scene), schedule_time)
        else:
            self.solution_text = """You press the left button. Your heart feels like it's about to explode, the screen shows a response. "Incorrect" Your heart drops, you feel as if the whole world is ending. You hear a clicking sound behind you, you turn around. Before you get a chance to react, a burst of bullets pierce you like a piece of paper. The bullets came from three machine guns, hidden behind a door-like eastern wall, similar to the wall to the west. You are now as full of holes as a sponge."""
            self.threshold = "You press the left button."
            self.threshold2 = """You press the left button. Your heart feels like it's about to explode, the screen shows a response. "Incorrect" Your heart drops, you feel as if the whole world is ending. You hear a clicking sound behind you, you turn around."""
            self.solution_label = Label(
                text="",
                font_size="22sp",
                size_hint=(1, 0.6),
                pos_hint={'x': 0, 'top': 0.95},
                color=self.brown,
                text_size=(Window.width * 0.9, Window.height * 0.6),
                halign='left',
                valign='top',
                bold=True
            )
            self.layout.add_widget(self.text_background)
            self.layout.add_widget(self.solution_label)
            self.type_solution = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.solution_text, self.solution_label), 0.05)
            pause_time = len(self.threshold) * 0.05
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_solution, 2, self.threshold), pause_time)
            pause_time2 = len(self.threshold2) * 0.05 + 1.5
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_solution, 2, self.threshold2), pause_time2)
                Clock.schedule_once(lambda dt: self.shot.play(), pause_time2)
                schedule_time = len(self.solution_text) * 0.05 + 4
            else:
                Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_solution, 1, self.threshold2), pause_time2)
                schedule_time = len(self.solution_text) * 0.05 + 3
            self.cod = "shot to death"
            Clock.schedule_once(lambda dt: self.game_over(dt, self.riddle), schedule_time)
                
            
    
    def searched(self, instance):
        self.layout.clear_widgets()
        self.searched_text = "You decide to look around for other exits. You were too shocked to realize at first, but this room doesn't have any windows. You search under the rugs, the sofas, behind the walls, nothing. You tear apart the sofa's cloth, and start extracting its guts, nothing. You search every portion of the room, the room looks like a tornado hit it now, but still nothing. You stand one of the chairs back up and sit on it. You decide to play the tape."
        self.searched_label = Label(
            text="",
            font_size="22sp",
            size_hint=(1, 0.6),
            color=self.brown,
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        if self.images_on:
            self.layout.add_widget(self.myroom_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.searched_label)
        self.current_skip_func = self.skip_search
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_search)
        
        self.type_write_search = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.searched_text, self.searched_label), 0.05)
        schedule_time = len(self.searched_text) * 0.05
        self.aftersearch = Clock.schedule_once(lambda dt: self.add_continue(dt, self.play_tape), schedule_time)
    
    def skip_search(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_write_search.cancel()
            self.aftersearch.cancel()
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.play_tape), 0)
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
    
    def play_bats(self, dt):
        self.bat_sound.volume = 0.1
        self.bat_sound2.volume = 0.1
        self.bat_sound3.volume = 0.1
        self.bat_sound.play()
        self.bat_sound2.play()
        self.bat_sound3.play()
        
    def grapple_path(self, instance):
        self.layout.clear_widgets()
        if self.right_grnd_brkn and not self.havegrapple:
            self.right_text = "You walk back through the right. You reach the ground that was once there. You can't see the bottom of the ground where it once was. You can't think of a way across"
        elif self.right_grnd_brkn and self.havegrapple:
            self.right_text = "You walk back through the right. You reach the ground that was once there. You can't see the bottom of the ground where it once was. You can't think of a reason to go back across"    
        else:
            self.right_text = "You go through the right opening. A few steps in, the light from the fork behind you is almost dim. You can see a faint light from the end of this opening, you decide to follow it. Suddenly, the ground below you starts to shake and crack. You have to act fast. What do you do?"
        self.right_label = Label(
            text="",
            font_size="22sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        
        self.right_image = Image(
            source="assets/Cracking.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.right_label)
        
        self.char_index = 0
        self.type_write_right = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.right_text, self.right_label), 0.05)
        pause_timing = len("You go through the right opening.") * 0.05 - 0.05
        self.threshold = "You go through the right opening."
        if not self.right_grnd_brkn:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_right, 0.5, self.threshold), pause_timing)
        self.threshold2 = "You go through the right opening. A few steps in, the light from the fork behind you is almost dim."
        pause2_timing = len("You go through the right opening. A few steps in, the light from the fork behind you is almost dim.") * 0.05 + 0.1
        if not self.right_grnd_brkn:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_right, 0.5, self.threshold2), pause2_timing)
        self.threshold3 = "You go through the right opening. A few steps in, the light from the fork behind you is almost dim. You can see a faint light from the end of this opening, you decide to follow it. Suddenly,"
        pause3_timing = len("You go through the right opening. A few steps in, the light from the fork behind you is almost dim. You can see a faint light from the end of this opening, you decide to follow it. Suddenly,") * 0.05 + 0.3
        if not self.right_grnd_brkn:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_right, 2.5, self.threshold3), pause3_timing)
            Clock.schedule_once(self.start_cracking, pause3_timing)
        if not self.right_grnd_brkn:
            schedule_time = len(self.right_text) * 0.05 + 3.4
        else:
            schedule_time = len(self.right_text) * 0.05
        Clock.schedule_once(self.right_options, schedule_time)
        if not self.right_grnd_brkn:
            self.cod = "fell to doom"
            Clock.schedule_once(lambda dt: self.start_timer(dt, self.grapple_path, self.crack), schedule_time)
            self.qtfu = Clock.schedule_once(self.crumble, schedule_time + 5.5)
        
        
    def right_options(self, dt):
        self.return_attempt = Button(
            text="Try to go back, off of the cracking floor",
            font_size="22sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'y': 0},
            background_color=self.brown
        )
        self.return_attempt.bind(on_press=self.returned)
        if self.right_grnd_brkn:
            self.return_attempt.text = "Go back"
            self.return_attempt.pos_hint = {'center_x': 0.5, 'center_y': 0.2}
            self.return_attempt.size_hint = (0.5, 0.2)
            self.return_attempt.unbind(on_press=self.returned)
            self.return_attempt.bind(on_press=self.start_game)
            
        self.dash_across = Button(
            text="Try to dash across the cracking floor",
            font_size="22sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=self.brown
        )
        self.dash_across.bind(on_press=self.dashed)
        
        self.jump_over = Button(
            text="Try to jump over the cracking floor",
            font_size="22sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            background_color=self.brown
        )
        self.jump_over.bind(on_press=self.jumped)
        
        if not self.right_grnd_brkn:
            self.layout.add_widget(self.dash_across)
            self.layout.add_widget(self.jump_over)
            
        self.layout.add_widget(self.return_attempt)
        
    def jumped(self, instance):
        self.layout.clear_widgets()
        self.qte.cancel()
        self.qtfu.cancel()
        self.jumped_text = "You try to jump over the cracking ground. You look below you, the ground crumbles under your feet. You extend your arm forward trying to grab the ledge. Your fingers slip."
        self.jumped_label = Label(
            text="",
            font_size="25sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.jumped_label)
        
        self.threshold = "You try to jump over the cracking ground."
        pause_timing = len("You try to jump over the cracking ground.") * 0.05 - 0.2
        self.type_write_jumped = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.jumped_text, self.jumped_label), 0.05)
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_jumped, 1.2, self.threshold), pause_timing)
        Clock.schedule_once(self.crumble, pause_timing)
        self.threshold2 = "You try to jump over the cracking ground. You look below you, the ground crumbles under your feet."
        pause_timing2 = len("You try to jump over the cracking ground. You look below you, the ground crumbles under your feet.") * 0.05 + 0.85
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_jumped, 0.5, self.threshold2), pause_timing2)
        self.threshold3 = "You try to jump over the cracking ground. You look below you, the ground crumbles under your feet. You extend your arm forward trying to grab the ledge."
        pause_timing3 = (len(self.jumped_text) - len("your fingers slip")) * 0.05 + 1
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_jumped, 3.5, self.threshold3), pause_timing3)
        death_timing = pause_timing3 + len("your fingers slip.") * 0.05 + 5
        self.cod = "fell to doom"
        Clock.schedule_once(lambda dt: self.game_over(dt, self.grapple_path), death_timing)
        
    def dashed(self, instance):
        self.layout.clear_widgets()
        self.qte.cancel()
        self.qtfu.cancel()
        self.right_grnd_brkn = True
        self.dashed_text = "You dash forward as fast as you can. You're so certain you just broke the world record for sprinting. The ground behind you crumbles, you're just happy you're alive. You can see the light just up ahead, you continue onwards."
        self.dashed_label = Label(
            text="",
            font_size="24sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.dashed_label)
        
        self.type_write_dashed = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.dashed_text, self.dashed_label), 0.05)
        self.threshold = "You dash forward as fast as you can. You're so certain you just broke the world record for sprinting."
        pause_time = len("You dash forward as fast as you can. You're certain you just broke the world record for sprinting.") * 0.05 - 0.25
        self.pause_dashed = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_dashed, 1, self.threshold), pause_time)
        Clock.schedule_once(self.crumble, pause_time)
        self.threshold2 = "You dash forward as fast as you can. You're so certain you just broke the world record for sprinting. The ground behind you crumbles, you're just happy you're alive."
        pause_time2 = (len(self.dashed_text) - len("You can see the light just up ahead, you  continue onwards.")) * 0.05 + 0.35
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_dashed, 0.5, self.threshold2), pause_time2)
        schedule_time = len(self.dashed_text) * 0.05 + 1
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.grapple_scene), schedule_time)
        
    def grapple_scene(self, instance):
        self.layout.clear_widgets()
        self.get_grapple_text = "You reach the light source, a small hole similar to the two at the fork. The light shines brilliantly on a pedestal, you walk up to it. To your surprise, a grapple gun lies on top of it. Seeing as there is no way to keep going forward, you pick it up and head back towards the crumbled ground."
        self.get_grapple_label = Label(
            text="",
            font_size="22sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.pedestal_image = Image(
            source="assets/pedestal-GG.jpeg",
            size_hint = (1, 0.6),
            pos_hint = {'center_x': 0.5, 'center_y': 0.7},
            allow_stretch = True,
            keep_ratio = False
        )
        if self.images_on:
            self.layout.add_widget(self.pedestal_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.get_grapple_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_right
        self.skip_button.bind(on_press=self.skip_right)
                    
        self.type_write_gotG = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.get_grapple_text, self.get_grapple_label), 0.05)
        self.threshold = "You reach the light source, a small hole similar to the two at the fork."
        pause_time = len("You reach the light source, a small hole similar to the two at the fork.") * 0.05 - 0.25
        self.pause_gotG = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_gotG, 0.5, self.threshold), pause_time)
        self.threshold2 = "You reach the light source, a small hole similar to the two at the fork. The light shines brilliantly on a pedestal, you walk up to it."
        pause_time2 = len("You reach the light source, a small hole similar to the two at the fork. The ligh shines brilliantly on a pedestal, you walk up to it.") * 0.05 + 0.05
        self.pause_gotG2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_gotG, 0.5, self.threshold2), pause_time2)
        self.threshold3 = "You reach the light source, a small hole similar to the two at the fork. The light shines brilliantly on a pedestal, you walk up to it. To your surprise, a grapple gun lies on top of it."
        pause_time3 = pause_time2 + len("To your surprise, a grapple gun lies on top of it.") * 0.05 + 0.4
        self.pause_gotG3 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_gotG, 0.5, self.threshold3), pause_time3)
        schedule_time = len(self.get_grapple_text) * 0.05 + 1.3
        self.continue_G = Clock.schedule_once(lambda dt: self.add_continue(dt, self.grapple_over), schedule_time)
        self.havegrapple = True
                                  
    def skip_right(self, instance):
        if self.char_index < len(self.get_grapple_text):
            self.get_grapple_label.text = self.get_grapple_text
            self.type_write_gotG.cancel()
            self.pause_gotG.cancel()
            self.pause_gotG2.cancel()
            self.pause_gotG3.cancel()
            self.continue_G.cancel()
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.grapple_over), 0)
            self.skip_button.unbind(on_press=self.skip_right)
            self.layout.remove_widget(self.skip_button)
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.skip_right)
            self.layout.remove_widget(self.skip_button)    
    
    def grapple_over(self, instance):
        self.layout.clear_widgets()
        self.grappling_text = "You arrive back at the crumbled ground. All that's left of it is a pit whose bottom you can't see. You fire your grapple gun, it attaches to the wall on the other side. You land safely on the other side. You continue heading back towards the fork."
        self.grappling_label = Label(
            text="",
            font_size="26sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.8, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.grappling_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_grappling
        self.skip_button.bind(on_press=self.skip_grappling)
                
        self.type_write_G = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.grappling_text, self.grappling_label), 0.05)
        self.threshold = "You arrive back at the crumbled ground. All that's left of it is a pit whose bottom you can't see."
        pause_time = len("You arrive back at the crumbled ground. All that's left of it is a pit whose bottom you can't see.") * 0.05 - 0.45
        self.pause_G = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_G, 3.5, self.threshold), pause_time)
        if self.effects_on: 
            self.usegrap = Clock.schedule_once(lambda dt: self.grapple.play(), pause_time)
        self.threshold2 = "You arrive back at the crumbled ground. All that's left of it is a pit whose bottom you can't see. You fire your grapple gun, it attaches to the wall on the other side."
        pause_time2 = (len(self.grappling_text) - len("You land safely on the other side. You continue heading back towards the fork.")) * 0.05 + 2.8
        self.pause_G2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_G, 2.5, self.threshold2), pause_time2)
        if self.effects_on:
            self.grapover = Clock.schedule_once(lambda dt: self.grapple_back.play(), pause_time2)
        schedule_time = len(self.grappling_text) * 0.05 + 5.5
        self.continuation = Clock.schedule_once(lambda dt: self.add_continue(dt, self.start_game), schedule_time)
        
    def skip_grappling(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_write_G.cancel()
            self.pause_G.cancel()
            self.pause_G2.cancel()
            if self.effects_on:
                self.grapover.cancel()
                self.usegrap.cancel()
            self.continuation.cancel()
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.start_game), 0)
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)    
    
    def returned(self, instance):
        self.layout.clear_widgets()
        self.qte.cancel()
        self.qtfu.cancel()
        self.right_grnd_brkn = True
        self.returned_text = "You trace back your steps off of the cracking floor. The ground crumbles, you can no longer go that way."
        self.returned_label = Label(
            text="",
            font_size="27sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.returned_label)
         
        self.type_write_returned = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.returned_text, self.returned_label), 0.05)
        self.threshold = "You trace back your steps off of the cracking floor."
        pause_timing = len("You trace back your steps off of the cracking floor.") * 0.05 - 0.15
        self.pause_returned = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_write_returned, 1.2, self.threshold), pause_timing)
        Clock.schedule_once(self.crumble, pause_timing)
        schedule_time = len(self.returned_text) * 0.05 + 1.2
        self.schedule_continue = Clock.schedule_once(lambda dt: self.add_continue(dt, self.start_game), schedule_time)
        
    def crumble(self, dt):
        if self.effects_on == True:
            try:
                self.crack.stop()
                self.impact.play()
                Clock.schedule_once(self.fix_ambience, 0.5)
            except:
                Clock.schedule_once(self.fix_ambience, 0)
                pass
            
    def fix_ambience(self, dt):
        self.ambience.volume = 0.75
                        
    def start_cracking(self, dt):
        if self.images_on == True:
            self.right_image.opacity = 0
            self.layout.add_widget(self.right_image, index = 2)
            Clock.schedule_interval(lambda dt: self.image_appear(dt, self.right_image, 1), 0.2)
        if self.effects_on == True:
            self.ambience.volume = 0.2
            self.crack.play()
        
    def long_path(self, instance):
        self.stop()
        
    def option_menu(self, instance):
        self.layout.clear_widgets()
        self.ambience.stop()
        self.back_button = Button(
            text="back",
            font_size="24sp",
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            size_hint=(0.5, 0.09)
        )
        self.back_button.bind(on_press=self.main_menu)
        
        self.images_label = Label(
            text="Images:",
            font_size="24sp",
            pos_hint={'center_x': 0.2, 'center_y': 0.9}
        )
        self.yes_image = Button(
            text="On",
            font_size="24sp",
            size_hint=(0.15, 0.09),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        self.no_image = Button(
            text="Off",
            font_size="24sp",
            size_hint=(0.15, 0.09),
            pos_hint={'center_x': 0.8, 'center_y': 0.9}
        )
        self.yes_image.bind(on_press=self.turn_on_image)
        self.no_image.bind(on_press=self.turn_off_image)
        if self.images_on == True:
            self.yes_image.disabled = True
            self.yes_image.background_color = [0, 1, 0, 1]
        else:
            self.no_image.disabled = True
            self.no_image.background_color = [0, 1, 0, 1]
        self.ambience_label = Label(
            text="Ambience:",
            font_size="24sp",
            pos_hint={'center_x': 0.2, 'center_y': 0.55}
        )
        self.yes_ambience = Button(
            text="On",
            font_size="24sp",
            size_hint=(0.15, 0.09),
            pos_hint={'center_x': 0.5, 'center_y': 0.55}
        )
        self.no_ambience = Button(
            text="Off",
            font_size="24sp",
            size_hint=(0.15, 0.09),
            pos_hint={'center_x': 0.8, 'center_y': 0.55}
        )
        self.yes_ambience.bind(on_press=self.turn_on_ambience)
        self.no_ambience.bind(on_press=self.turn_off_ambience)
        if self.ambience_on == True:
            self.yes_ambience.disabled = True
            self.yes_ambience.background_color = [0, 1, 0, 1]
        else:
            self.no_ambience.disabled = True
            self.no_ambience.background_color = [0, 1, 0, 1]
        
        self.effects_label = Label(
            text="Effects:",
            font_size="24sp",
            pos_hint={'center_x': 0.2, 'center_y': 0.25}
        )
        self.yes_effect = Button(
            text="On",
            font_size="24sp",
            size_hint=(0.15, 0.09),
            pos_hint={'center_x': 0.5, 'center_y': 0.25}
        )
        self.no_effect = Button(
            text="Off",
            font_size="24sp",
            size_hint=(0.15, 0.09),
            pos_hint={'center_x': 0.8, 'center_y': 0.25}
        )
        self.yes_effect.bind(on_press=self.turn_on_effect)
        self.no_effect.bind(on_press=self.turn_off_effect)
        if self.effects_on == True:
            self.yes_effect.disabled = True
            self.yes_effect.background_color = [0, 1, 0, 1]
        else:
            self.no_effect.disabled = True
            self.no_effect.background_color = [0, 1, 0, 1]
        
        
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
        
    def  pause_typewrite(self, dt, typewrite_function, duration, pause_quota):
        self.typed_label.text = pause_quota
        self.char_index = len(pause_quota)
        typewrite_function.cancel()
        self.resumption = Clock.schedule_once(typewrite_function, duration)
    def typewrite(self, dt, target_text, label):
        self.typed_label = label
        self.targeted = target_text
        if self.char_index < len(self.targeted):
            self.typed_label.text += self.targeted[self.char_index] #The [] act as an index to determine which character to write.
            self.char_index += 1 #The addition makes it move from one character to the next.
        else:
            if self.skip_button.disabled == False:
                try:
                    self.layout.remove_widget(self.skip_button)
                    self.skip_button.unbind(on_press=self.current_skip_func)
                except:
                    pass
            self.char_index = 0
            return False # Returning False automatically stops the interval loop

    def start_timer(self, dt, previous_screen, SFX):
        self.timer_label = Label(
            text="",
            font_size="90sp",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=[1, 0, 0, 1],
            halign='center',
            valign='center'
        )
        self.timer_label.opacity = 0
        self.background_button = Image(
            source="assets/Timer_background.png",
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True,
            keep_ratio=False
        )
        self.background_button.opacity = 0
        self.layout.add_widget(self.background_button)
        self.layout.add_widget(self.timer_label)
        self.quick_timer = 5
        self.qte = Clock.schedule_interval(lambda dt: self.quick_time(dt, self.timer_label, previous_screen, SFX), 1)
        
    def quick_time(self, dt, label, previous_screen, SFX):
        if self.quick_timer > 0:
            label.text = str(self.quick_timer)
            label.opacity = 1
            Clock.schedule_once(self.appear, 0)
            self.quick_timer -= 1
            Clock.schedule_once(lambda dt: self.disappear(dt, label), 0.3)
        else:
            self.quick_timer = 5
            Clock.schedule_once(lambda dt: self.game_over(dt, previous_screen), 0)
            self.layout.remove_widget(label)
            self.layout.remove_widget(self.background_button)
            if self.effects_on:
                try:
                    SFX.stop()
                except:
                    pass
            return False
            
    def appear(self, dt):
        self.background_button.opacity=1
        Clock.schedule_once(lambda dt: self.disappear(dt, self.background_button), 0.3)
        
    def disappear(self, dt, label):
        label.opacity = 0
                               
    def game_over(self, dt, previous_screen):
        self.layout.clear_widgets()
        self.died_label = Label(
            text="You Died",
            font_size = "50sp",
            color=[1, 0, 0, 1],
            size_hint = (1, 0.25),
            text_size = (Window.width * 0.9, Window.height * 0.25),
            pos_hint = {'center_x': 0.5, 'top': 0.95},
            halign='center',
            valign='center'            
        )
        
        self.cod_label = Label(
            text=f"Cause of Death: {self.cod}",
            font_size="24sp",
            color=self.brown,
            size_hint=(1, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.75},
            text_size=(Window.width * 0.95, Window.height * 0.1),
            halign='center',
            valign='top'
        )
        
        self.main_menu_button = Button(
            text="Back to main menu",
            font_size="22sp",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0},
            background_color=self.brown
        )
        self.main_menu_button.bind(on_press=self.main_menu)
        
        self.retry_btn = Button(
            text="Retry from last screen",
            font_size="22sp",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            background_color=self.brown
        )
        self.retry_btn.bind(on_press=previous_screen)
        if self.ambience_on == True:
            self.retry_btn.bind(on_press=lambda instance: self.ambience.play())
        if self.effects_on == True:
            if self.cod == self.fall_death:
                self.death_sound.play()
            elif self.cod == self.bat_eaten:
                self.bat_death.play()
            elif self.cod == self.crush_death:
                self.crush_play()
        if self.ambience_on == True:
            self.ambience.stop() 
        self.died_label.opacity = 0
        self.cod_label.opacity = 0
        self.layout.add_widget(self.died_label)
        self.layout.add_widget(self.cod_label)
        self.death_count += 1
        
        Clock.schedule_interval(lambda dt: self.image_appear(dt, self.died_label, 1), 0.1)
        Clock.schedule_interval(lambda dt: self.image_appear(dt, self.cod_label, 1), 0.2)
        Clock.schedule_once(self.add_death_options, 2.5)
   
    def add_death_options(self, dt):
        self.layout.add_widget(self.main_menu_button)
        self.layout.add_widget(self.retry_btn)
        
    def victory_scene(self, instance):
        self.layout.clear_widgets()
        self.scenery_text = "You walk out the opening. You see the path going downwards. It appears that this *cave* is built on a mountain. You follow the path downwards towards the very beutiful sunshine. You embrace the sunlight as you walk downward, even the birds chirping sounds like music to your ears. So many unanswered questions remain, yet you stopped caring. You're just happy you're alive."
        self.scenery_label = Label(
            text="",
            font_size="24sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            color=[0, 0.5, 0.5, 1],
            bold=True
        )
        self.layout.add_widget(self.scenery_label)
        Clock.schedule_interval(lambda dt: self.typewrite(dt, self.scenery_text, self.scenery_label), 0.06)
        schedule_time = len(self.scenery_text) * 0.06 + 1.5
        Clock.schedule_once(self.victory, schedule_time)
    
    def victory(self, dt):
        self.layout.clear_widgets()
        if self.ambience:
            try:
                self.ambience.stop()
            except:
                pass
            self.vic_ambience.volume = 0
            self.vic_ambience2.volume = 0            
            self.vic_ambience.play()
            self.vic_ambience2.play()
            self.victorySFX = Clock.schedule_interval(lambda dt: self.amplification(dt, self.vic_ambience, 0.8), 0.5)
            self.victorySFX2 = Clock.schedule_interval(lambda dt: self.amplification(dt, self.vic_ambience2, 0.8), 0.5)
        
        self.vic_label = Label(
            text="You escaped",
            font_size="50sp",
            size_hint=(1, 0.25),
            pos_hint={'center_x': 0.5, 'top': 0.99},
            color=[0, 0.25, 1, 1],
            text_size=(Window.width * 0.9, Window.height * 0.25),
            halign='center',
            valign='top'
        )
        self.death_no = str(self.death_count)
        self.died_no = Label(
            text=f"Died {self.death_no} times",
            font_size="24sp",
            size_hint=(1, 0.1),
            color=[1, 0, 0, 1],
            pos_hint={'center_x': 0.5, 'top': 0.92},
            text_size=(Window.width * 0.9, Window.height * 0.1),
            halign='center',
            valign='top'
        )
        self.exit_no = Label(
            text=f"Exit {self.exit_num} of 3",
            font_size="24sp",
            size_hint=(1, 0.1),
            color=[1, 0.1, 0.1, 1],
            pos_hint={'center_x': 0.5, 'top': 0.87},
            text_size=(Window.width * 0.9, Window.height * 0.1),
            halign='center',
            valign='top'    
        )
        self.vic_image = Image(
            source="assets/Victory.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        self.main_menu_btn = Button(
            text="Back to main menu",
            font_size="22sp",
            size_hint=(0.6, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=self.brown
        )
        self.main_menu_btn.bind(on_press=self.main_menu)
        self.main_menu_btn.bind(on_press=self.resetdeaths)
        if self.ambience_on:
            self.main_menu_btn.bind(on_press=self.end_win)
        
        self.vic_label.opacity = 0
        self.died_no.opacity = 0
        self.exit_no.opacity = 0
        if self.images_on:
            self.vic_image.opacity = 0
            self.layout.add_widget(self.vic_image)
            self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.vic_label)
        self.layout.add_widget(self.died_no)
        self.layout.add_widget(self.exit_no)
        Clock.schedule_interval(lambda dt: self.image_appear(dt, self.vic_label, 1), 0.1)
        Clock.schedule_interval(lambda dt: self.image_appear(dt, self.died_no, 1), 0.2)
        Clock.schedule_interval(lambda dt: self.image_appear(dt, self.exit_no, 1), 0.2)
        if self.images_on:
            Clock.schedule_interval(lambda dt: self.image_appear(dt, self.vic_image, 1), 0.2)
        Clock.schedule_once(lambda dt: self.layout.add_widget(self.main_menu_button), 2.5)
        
    def resetdeaths(self, instance):
        self.death_count = 0
    
    def end_win(self, instance):
        self.victorySFX.cancel()
        self.victorySFX2.cancel()
        self.vic_ambience.stop()
        self.vic_ambience2.stop()
        
    
    def make_appearance(self, dt, target_image, target_opacity, interval):
        Clock.schedule_interval(lambda dt: self.image_appear(dt, target_image, target_opacity), interval)
        
    def image_appear(self, dt, target_image, target_opacity):
        if target_image.opacity < target_opacity:
            target_image.opacity += 0.1
        else:
            return False
            
    def amplification(self, dt, SFX, target_volume):
        if SFX.volume < target_volume:
            SFX.volume += 0.1
        else:
            return False

    def add_continue(self, dt, function):
        # 1. If a previous function was bound, unbind it first
        if hasattr(self, 'current_continue_func') and self.current_continue_func:
            self.continue_button.unbind(on_press=self.current_continue_func)
            
        # 2. Save the new function and bind it
        self.current_continue_func = function
        self.continue_button.bind(on_press=function)
        
        # 3. Only add the widget if it isn't already on screen
        if self.continue_button.parent is None:
            self.layout.add_widget(self.continue_button)

                
    def turn_on_image(self, instance):
        self.images_on = True
        self.yes_image.disabled = True
        self.no_image.disabled = False
        self.no_image.background_color = [1, 1, 1, 1]
        self.yes_image.background_color = [0, 1, 0, 1]
        
    def turn_off_image(self, instance):
        self.images_on = False
        self.yes_image.disabled = False
        self.no_image.disabled = True
        self.no_image.background_color = [0, 1, 0, 1]
        self.yes_image.background_color = [1, 1, 1, 1]

    def turn_on_ambience(self, instance):
        self.ambience_on = True
        self.yes_ambience.disabled = True
        self.no_ambience.disabled = False
        self.no_ambience.background_color = [1, 1, 1, 1]
        self.yes_ambience.background_color = [0, 1, 0, 1]

    def turn_off_ambience(self, instance):
        self.ambience_on = False
        self.yes_ambience.disabled = False
        self.no_ambience.disabled = True
        self.no_ambience.background_color = [0, 1, 0, 1]
        self.yes_ambience.background_color = [1, 1, 1, 1]

    def turn_on_effect(self, instance):
        self.effects_on = True
        self.yes_effect.disabled = True
        self.no_effect.disabled = False
        self.no_effect.background_color = [1, 1, 1, 1]
        self.yes_effect.background_color = [0, 1, 0, 1]

    def turn_off_effect(self, instance):
        self.effects_on = False
        self.yes_effect.disabled = False
        self.no_effect.disabled = True
        self.no_effect.background_color = [0, 1, 0, 1]
        self.yes_effect.background_color = [1, 1, 1, 1]
        
    def quit(self, instance):
        self.stop()
        
            
if __name__ == "__main__":
    AdventureApp().run()
