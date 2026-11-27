__version__ = "0.1.0"
import os
import platform
from kivy.config import Config

os.environ['KIVY_CLOCK'] = 'interrupt'
# Force Windows environments to use ANGLE/DirectX to prevent OpenGL 1.1 crashes
if platform.system() == 'Windows':
    Config.set('graphics', 'fullscreen', 'auto')
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
from kivy.storage.jsonstore import JsonStore
from pathlib import Path

class AdventureApp(App):
    def build(self):
        self.ambience = SoundLoader.load("assets/ambience.mp3")
        self.collapse = SoundLoader.load("assets/collapse.mp3")
        self.crack = SoundLoader.load("assets/crack_sound.mp3")
        self.death_sound = SoundLoader.load("assets/Death.mp3")
        self.ambience_2 = SoundLoader.load("assets/eyes.mp3")
        self.grapple = SoundLoader.load("assets/grapple.mp3")
        self.grapple_back = SoundLoader.load("assets/grapple_back.mp3")        
        self.impact = SoundLoader.load("assets/hit_ground.wav")
        self.vic_ambience = SoundLoader.load("assets/victory_ambience.mp3")
        self.vic_ambience2 = SoundLoader.load("assets/victory_ambience_2.mp3")
        self.bat_sound = SoundLoader.load("assets/Bat_sounds.mp3")            
        self.bat_sound2 = SoundLoader.load("assets/bat_sounds2.mp3")            
        self.bat_sound3 = SoundLoader.load("assets/bat_sounds3.mp3")
        self.boulder_sound = SoundLoader.load("assets/boulder_rolling.mp3")        
        self.bat_death = SoundLoader.load("assets/bat_eat.mp3")            
        self.crush = SoundLoader.load("assets/bone_break.mp3")
        self.shot = SoundLoader.load("assets/guntrap.mp3")            
        self.slamdoor = SoundLoader.load("assets/slamdoor.mp3")           
        self.bouldercrash = SoundLoader.load("assets/Bouldercrash.mp3")            
        self.click = SoundLoader.load("assets/click.mp3")           
        self.headbutt = SoundLoader.load("assets/headbutt.mp3")
        self.elevator_open = SoundLoader.load("assets/elevator_open.mp3")
        self.elevator_close = SoundLoader.load("assets/elevator_close.mp3")
        self.alarm = SoundLoader.load("assets/alarm.mp3")
        self.lift_fall = SoundLoader.load("assets/lift_fall.mp3")
        self.elevator_ride = SoundLoader.load("assets/elevator_victory.mp3")
        self.electrocuted = SoundLoader.load("assets/electrocution.mp3")
        self.elevator_crash = SoundLoader.load("assets/lift_crash.mp3")
        self.oneshot = SoundLoader.load("assets/oneshot.mp3")
        self.dead_electricity = SoundLoader.load("assets/electric_death.mp3")
            
        self.layout = FloatLayout()
        
        #(set all default values here:-
        self.images_on = True 
        self.ambience_on = True
        self.effects_on = True
        self.brown = get_color_from_hex("B3865B")
        self.bat_eaten = "eaten by bats"
        self.fall_death = "fell to doom"
        self.crush_death = "crushed to death"
        self.electric_death = "electrocuted"
        self.spilled = False
        save_path = Path(self.user_data_dir) / "save.json"
        self.store = JsonStore(str(save_path))
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
        #default values:{
        self.havegrapple = False
        self.started = False
        self.right_grnd_brkn = False
        self.batted = False
        self.quick_timer = 5
        self.counter = 1
        self.upped = False
        self.op_no = 0
        self.returned = False
        self.not_ambience = False
        if self.headbutt:
            self.headbutt.volume = 1
            self.headbutt.loop = False
        if self.elevator_open:
            self.elevator_open.volume = 1
            self.elevator_open.loop = False
        if self.elevator_close:
            self.elevator_close.volume = 1
            self.elevator_close.loop = False
        if self.alarm:
            self.alarm.volume = 1
            self.alarm.loop = False
        if self.lift_fall:
            self.lift_fall.volume = 1
            self.lift_fall.loop = False
        if self.elevator_ride:
            self.elevator_ride.volume = 1
            self.elevator_ride.loop = False
        if self.electrocuted:
            self.electrocuted.volume = 1
            self.electrocuted.loop = True
        if self.elevator_crash:
            self.elevator_crash.volume = 1
            self.elevator_crash.loop = False
        if self.oneshot:
            self.oneshot.volume = 1
            self.oneshot.loop = False    
        if self.dead_electricity:
            self.dead_electricity.volume = 1
            self.dead_electricity.loop = False
        if self.click:
            self.click.volume = 1
            self.click.loop = False
        if self.bouldercrash:
            self.bouldercrash.volume = 1
            self.bouldercrash.loop = False
        if self.slamdoor:
            self.slamdoor.volume = 1
            self.slamdoor.loop = False
        if self.shot:
            self.shot.volume = 1
            self.shot.loop = False
        if self.crush:
            self.crush.volume = 1
            self.crush.loop = False
        if self.bat_death:
            self.bat_death.volume = 1
            self.bat_death.loop = False
        if self.boulder_sound:
            self.boulder_sound.volume = 1
            self.boulder_sound.loop = True
        if self.bat_sound3:
            self.bat_sound3.volume = 1
            self.bat_sound3.loop = True
        if self.bat_sound2:
            self.bat_sound2.volume = 1
            self.bat_sound2.loop = True
        if self.bat_sound:
            self.bat_sound.volume = 1
            self.bat_sound.loop = True
        if self.vic_ambience2:
            self.vic_ambience2.volume = 0.75
            self.vic_ambience2.loop = True
        if self.vic_ambience:
            self.vic_ambience.volume = 1
            self.vic_ambience.loop = True
        if self.impact:
            self.impact.volume = 1
            self.impact.loop = False
        if self.grapple_back:
            self.grapple_back.volume = 1
            self.grapple_back.loop = False
        if self.grapple:
            self.grapple.volume = 1
            self.grapple.loop = False
        if self.ambience_2:
            self.ambience_2.volume = 0.6
            self.ambience_2.loop = True
        if self.death_sound:
            self.death_sound.volume = 1
            self.death_sound.loop = False
        if self.crack:
            self.crack.volume = 0.8
            self.crack.loop = True
        if self.collapse:
            self.collapse.volume = 1
            self.collapse.loop = False
        if self.ambience:
            self.ambience.volume = 0.75
            self.ambience.loop = True
        #}
        
        self.skip_button.pos_hint = {'right': 1, 'center_y': 0.425}
        if self.store.exists("exits"):
            self.exits = self.store.get("exits")
            self.found_exits = self.exits["found"]
        else:
            self.found_exits = []
            self.store.put("exits", found=self.found_exits)
        if self.store.exists("deaths"):
            self.deaths = self.store.get("deaths")
            self.death_count = self.deaths["count"]
        else:
            self.death_count = 0
            self.store.put("deaths", count=self.death_count)
        if self.store.exists("access"):
            self.access = self.store.get("access")
            self.hasaccess = self.access["has"]
        else:
            self.hasaccess = False
            self.store.put("access", has=self.hasaccess)
        #}
        
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
        
        self.archive_btn = Button(
            text="Enter\nThe\nArchive",
            font_size="24sp",
            size_hint=(0.25, 0.2),
            pos_hint={'x': 0, 'y': 0.1},
            background_color=[0.1, 1, 0.1, 1],
            color=[0.1, 0.1, 1, 1],
            text_size=(Window.width * 0.25, Window.height * 0.2),
            halign='center',
            valign='center'
        )
        self.archive_btn.bind(on_press=self.Rarchive)
        
        self.secret_btn = Button(
            text="secret code",
            font_size="10sp",
            size_hint=(0.2, 0.1),
            pos_hint={'right': 1, 'y': 0},
            background_color=[0, 0, 0, 0],
            color=[1, 1, 1, 1]
        )
        self.secret_btn.bind(on_press=self.revealed)
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
        if (self.death_count >= 10 or ("1" in self.found_exits and "2" in self.found_exits and "3" in self.found_exits)) and not self.spilled:
            self.layout.add_widget(self.secret_stroke)
            self.layout.add_widget(self.secret_btn) 
        self.layout.add_widget(self.title_background)
        self.layout.add_widget(self.option_button)
        self.layout.add_widget(self.quit_button)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.gamename)
        #REMOVE AFTER TESTING:(
        self.test_btn = Button(
            text="test",
            size_hint=(0.1, 0.05),
            pos_hint={'x': 0, 'top': 0.95},
            font_size="9sp"
        )
        self.test_btn.bind(on_press=self.traitor)
        self.layout.add_widget(self.test_btn)
        #)
                
        if hasattr(self, "hasaccess") and self.hasaccess:
            self.layout.add_widget(self.archive_btn)
        
        if self.ambience_on == True:
            self.ambience.play()

    def revealed(self, instance):
        self.layout.clear_widgets()
        self.secret_code = Label(
            text="The secret code is: book, chair, spatula, and spoon. Input it wherever you can for a secret.",
            font_size="27sp",
            size_hint=(1, 1),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.back_btn = Button(
            text="Back",
            font_size="24sp",
            size_hint=(0.3, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0.05}
        )
        self.back_btn.bind(on_press=self.main_menu)
        
        self.layout.add_widget(self.secret_code)
        self.layout.add_widget(self.back_btn)
        self.spilled = True
    
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
            font_size="20sp",
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
        pause_time2 = len(self.threshold2) * 0.06 - 0.55
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
        self.layout.clear_widgets()
        self.left_text = "You walk through the left opening. A few steps later, a boulder falls down behind you, blocking the opening. Your only choice is to keep going forward. A few steps later, you find yourself at a fork. The path to the left is well-lit with a bunch of holes like the ones at the first fork, but you don't see it's end at all. The path to the right is dark, but you see light coming from its end. Which path do you choose?"
        self.threshold = "You walk through the left opening. A few steps later,"
        self.threshold2 = "You walk through the left opening. A few steps later, a boulder falls down behind you, blocking the opening. Your only choice is to keep going forward."
        self.left_label = Label(
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
        if self.images_on:
            self.fork_image.opacity = 0
            self.layout.add_widget(self.fork_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.left_label)
        self.current_skip_func = self.skip_left
        self.skip_button.bind(on_press=self.skip_left)
        self.layout.add_widget(self.skip_button)
                
        self.type_left = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.left_text, self.left_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.2
        self.pause_left = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_left, 1, self.threshold), pause_time)
        if self.effects_on:
            self.lockout = Clock.schedule_once(lambda dt: self.bouldercrash.play(), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.55
        self.pause_left2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_left, 0.75, self.threshold2), pause_time2)
        if self.images_on:
            self.fork_image.source = "assets/fork2.jpg"
            self.arawareru = Clock.schedule_once(lambda dt: self.make_appearance(dt, self.fork_image, 0.8, 0.1), pause_time2)
            schedule_time = len(self.left_text) * 0.05 + 1.8
            self.left_options = Clock.schedule_once(self.lefty, schedule_time)
        
    def skip_left(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_left.cancel()
            self.pause_left.cancel()
            self.pause_left2.cancel()
            if self.effects_on:
                try:
                    self.lockout.cancel()
                except:
                    pass
            if self.images_on:
                try:
                    self.arawareru.cancel()
                except:
                    pass
                self.fork_image.opacity = 0.8
            self.left_options.cancel()
            self.char_index = 0
            try:
                self.resumption.cancel()
            except:
                pass
            Clock.schedule_once(self.lefty, 0) 
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)
        else:
            self.char_index = 0
            self.skip_button.unbind(on_press=self.current_skip_func)
            self.layout.remove_widget(self.skip_button)    
    
    def lefty(self, dt):
        self.Bpath = Button(
            text="Go left",
            font_size="24sp",
            size_hint=(0.5, 0.4),
            pos_hint={'x': 0, 'center_y': 0.2},
            background_color = self.brown
        )    
        self.Bpath.bind(on_press=self.boulder)
        self.dualroom = Button(
            text="Go right",
            font_size="24sp",
            size_hint=(0.5, 0.4),
            pos_hint={'right': 1, 'center_y': 0.2},
            background_color=self.brown
        )
        self.dualroom.bind(on_press=self.two_btns)
        self.layout.add_widget(self.Bpath)
        self.layout.add_widget(self.dualroom)
        
    def boulder(self, instance):
        self.layout.clear_widgets()
        self.ball_text = "You decide to follow the left path. After a few steps, you realize that the path is sloping upwards gradually. The slope feels natural until, you hear a clicking sound from below your feet. Almost immediately after that, you hear weird loud noises coming from the end of the slope. You look ahead. A BOULDER! You instinctively start running down the slope, there appears to be a small opening to the left that you may be able to hide in but you can't really tell. What do you do?"
        self.threshold = "You decide to follow the left path. After a few steps, you realize that the path is sloping upwards gradually. The slope feels natural until,"
        self.threshold2 = "You decide to follow the left path. After a few steps, you realize that the path is sloping upwards gradually. The slope feels natural until, you hear a clicking sound from below your feet. Almost immediately after that,"
        self.threshold3 = "You decide to follow the left path. After a few steps, you realize that the path is sloping upwards gradually. The slope feels natural until, you hear a clicking sound from below your feet. Almost immediately after that, you hear weird loud noises coming from the end of the slope. You look ahead."
        self.ball_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            color=self.brown,
            bold=True
        )
        self.ball_image = Image(
            source="assets/boulder_trap.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.ball_image.opacity = 0
            self.layout.add_widget(self.ball_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.ball_label)
        
        self.type_ball = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.ball_text, self.ball_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.5
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_ball, 0.5, self.threshold), pause_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.click.play(), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 - 0.1 
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_ball, 0.5, self.threshold2), pause_time2)
            self.boulder_sound.volume = 0
            Clock.schedule_once(lambda dt: self.boulder_sound.play(), pause_time2)
            Clock.schedule_once(lambda dt: self.Samplification(dt, self.boulder_sound, 1, 0.5), pause_time2)
        if self.effects_on:
            pause_time3 = len(self.threshold3) * 0.05 + 0.5
        else:
            pause_time3 = len(self.threshold3) * 0.05 - 0.15
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_ball, 0.5, self.threshold3), pause_time3)
        if self.images_on:
            Clock.schedule_once(lambda dt: self.make_appearance(dt, self.ball_image, 1, 0.1), pause_time3)
        if self.effects_on:
            schedule_time = len(self.ball_text) * 0.05 + 1.3
        else:
            schedule_time = len(self.ball_text) * 0.05 + 0.8
        Clock.schedule_once(self.ballopts, schedule_time)
        Clock.schedule_once(lambda dt: self.start_timer(dt, self.boulder, self.boulder_sound), schedule_time)
        self.cod = "crushed to death"
        
    def ballopts(self, dt):
        self.running = Button(
            text="Just keep running",
            font_size="22sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            background_color=self.brown   
        )
        self.running.bind(on_press=self.ran)
        
        self.grappling = Button(
            text="Try to grapple upwards, avoiding it",
            font_size="22sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=self.brown
        )
        self.grappling.bind(on_press=self.spidermanned)
        
        self.hide = Button(
            text="Try to hide in the opening to the left",
            font_size="22sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'y': 0},
            background_color=self.brown
        )
        self.hide.bind(on_press=self.hidden)
        self.layout.add_widget(self.running)
        self.layout.add_widget(self.hide)
        if self.havegrapple:
            self.layout.add_widget(self.grappling)
    
    def spidermanned(self, instance):
        self.layout.clear_widgets()
        self.qte.cancel()
        self.spiderman_text = "You take out your grapple gun and shoot it upwards. You pull yourself upwards, the boulder scrapes your feet as it passes by. The boulder crashes onto the wall, blocking off the path backwards. You drop back down, you see what appears to be a big area behind where the boulder was, it seems that's your only path, so you take it."
        self.threshold = "You take out your grapple gun and shoot it upwards."
        self.threshold2 = "You take out your grapple gun and shoot it upwards. You pull yourself upwards, the boulder scrapes your feet as it passes by."
        self.threshold3 = "You take out your grapple gun and shoot it upwards. You pull yourself upwards, the boulder scrapes your feet as it passes by. The boulder crashes onto the wall, blocking off the path backwards."
        self.spiderman_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.spiderman_label)
        
        self.type_spider = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.spiderman_text, self.spiderman_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.2
        if self.effects_on: 
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_spider, 3.2, self.threshold), pause_time)
            Clock.schedule_once(lambda dt: self.grapple.play(), pause_time)
            Clock.schedule_once(lambda dt: self.grapple_back.play(), pause_time + 3.2)
            Clock.schedule_once(lambda dt: self.grapple_back.stop(), pause_time + 5)
            pause_time2 = len(self.threshold2) * 0.05 + 2.75
            self.impact.volume = 0.05
            Clock.schedule_once(lambda dt: self.boulder_sound.stop(), pause_time2)
            Clock.schedule_once(lambda dt: self.impact.play(), pause_time2)
            Clock.schedule_once(lambda dt: self.bouldercrash.play(), pause_time2)
            pause_time3 = len(self.threshold3) * 0.05 + 3.15
            schedule_time = len(self.spiderman_text) * 0.05 + 4.2
        else:
            pause_time2 = len(self.threshold2) * 0.05 - 0.4
            pause_time3 = len(self.threshold3) * 0.05
            schedule_time = len(self.spiderman_text) * 0.05 + 0.8
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_spider, 0.5, self.threshold2), pause_time2)
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_spider, 0.5, self.threshold3), pause_time3)
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.puzzleroom), schedule_time)
    
    def puzzleroom(self, instance):
        self.layout.clear_widgets()
        self.bigroom_text = """You follow the path up the slope. You reach the end, it's a big empty space with a metal door directly in front of you. Next to the door is a small keypad. On the edge of the metal door, a small paper appears to be stuck. It reads, "Cave Layout De-". It appears that the paper was torn out of something. Your only choice seems to be to figure the code out, you don't even know where the door leads."""
        self.bigroom_label = Label(
            text="",
            color=self.brown,
            font_size="22sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.bigroom_image = Image(
            source="assets/puzzleroom.jpg",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.bigroom_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.bigroom_label)
        self.current_skip_func = self.skip_big
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_big)
        
        self.type_big = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.bigroom_text, self.bigroom_label), 0.05)
        schedule_time = len(self.bigroom_text) * 0.05
        self.start_solving = Clock.schedule_once(lambda dt: self.add_continue(dt, self.bigpuzzle), schedule_time)
    
    def skip_big(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_big.cancel()
            self.start_solving.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.bigpuzzle), 0)
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
    
    def bigpuzzle(self, instance): #(bent spoon, closed book, small chair, very thin spatula)
        self.layout.clear_widgets()
        self.bigpuzzle_text = """You look closer at the keypad. The screen reads, "enter the 4-digit code to continue." You look at the buttons, what you see confuses you. Instead of digits, the buttons have drawings carved into them. A closed door is carved into the first button usually having the number one on it, followed by a round table, a small chair, an un-even fork, a bent spoon, a cracked egg, a very thin spatula, a closed book, and a deep bowl carved into the remaining eight buttons respectively. Next to these buttons are a green button labeled 'SUBMIT', and a red button labeled 'RESET'. You are confused by what you see, yet you don't have a choice but to try solving it."""
        self.bigpuzzle_label = Label(
            text = "",
            font_size="19sp",
            color=self.brown,
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.bigpuzzle_image = Image(
            source="assets/Puzzle.jpg",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.bigpuzzle_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.bigpuzzle_label)
        self.current_skip_func = self.skip_solving
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_solving)
        
        self.type_bigpuzzle = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.bigpuzzle_text, self.bigpuzzle_label), 0.05)
        schedule_time = len(self.bigpuzzle_text) * 0.05 - 0.5
        self.solvenow = Clock.schedule_once(self.solveopts, schedule_time)        
    
    def skip_solving(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_bigpuzzle.cancel()
            self.solvenow.cancel()
            Clock.schedule_once(self.solveopts, 0)
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
    
    def solveopts(self, dt):
        self.code = ""
        self.firstinput = ""
        self.pressed_no = 0
        self.have_reset = False
        self.wasdumb = True
        self.door_btn = Button(
            text="door",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.025, 'top': 0.375},
            color=[0, 0, 0, 1]
        )
        self.door_btn.bind(on_press=self.pressed)
        self.table_btn = Button(
            text="table",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.275, 'top': 0.375},
            color=[0, 0, 0, 1]
        )
        self.table_btn.bind(on_press=self.pressed)
        self.chair_btn = Button(
            text="chair",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.525, 'top': 0.375},
            color=[0, 0, 0, 1]
        )
        self.chair_btn.bind(on_press=self.pressed)
        self.submit_btn = Button(
            text="SUBMIT",
            font_size="16sp",
            size_hint=(0.2, 0.15),
            pos_hint={'right': 0.975, 'top': 0.365},
            background_color=[0, 1, 0, 1],
            color=[0, 1, 0, 1]
        )
        self.submit_btn.bind(on_press=self.submitted)
        self.fork_btn = Button(
            text="fork",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.025, 'top': 0.25},
            color=[0, 0, 0, 1]
        )
        self.fork_btn.bind(on_press=self.pressed)
        self.spoon_btn = Button(
            text="spoon",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.275, 'top': 0.25},
            color=[0, 0, 0, 1]
        )
        self.spoon_btn.bind(on_press=self.pressed)
        self.egg_btn = Button(
            text="egg",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.525, 'top': 0.25},
            color=[0, 0, 0, 1]
        )
        self.egg_btn.bind(on_press=self.pressed)
        self.reset_btn = Button(
            text="RESET",
            font_size="16sp",
            size_hint=(0.2, 0.15),
            pos_hint={'right': 0.975, 'top': 0.185},
            background_color=[1, 0, 0, 1],
            color=[1, 0, 0, 1]
        )
        self.reset_btn.bind(on_press=self.reset_btns)
        self.spatula_btn = Button(
            text="spatula",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.025, 'top': 0.125},
            color=[0, 0, 0, 1]
        )
        self.spatula_btn.bind(on_press=self.pressed)
        self.book_btn = Button(
            text="book",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.275, 'top': 0.125},
            color=[0, 0, 0, 1]
        )
        self.book_btn.bind(on_press=self.pressed)
        self.bowl_btn = Button(
            text="bowl",
            font_size="20sp",
            size_hint=(0.2, 0.1),
            pos_hint={'x': 0.525, 'top': 0.125},
            color=[0, 0, 0, 1]
        )
        self.bowl_btn.bind(on_press=self.pressed)
        
        self.layout.add_widget(self.door_btn)
        self.layout.add_widget(self.table_btn)
        self.layout.add_widget(self.chair_btn)
        self.layout.add_widget(self.submit_btn)
        self.layout.add_widget(self.fork_btn)
        self.layout.add_widget(self.spoon_btn)
        self.layout.add_widget(self.egg_btn)
        self.layout.add_widget(self.reset_btn)
        self.layout.add_widget(self.spatula_btn)
        self.layout.add_widget(self.book_btn)
        self.layout.add_widget(self.bowl_btn)
            
    def pressed(self, instance):
        if self.pressed_no < 4:
            instance.disabled = True
            self.pressed_no += 1
            if self.firstinput == "":
                self.firstinput = instance.text
                self.extra_text = f"You press the {instance.text} button. An asterisk appears on the screen. It seems the keypad does actually work."
                if not self.have_reset:
                    self.bigpuzzle_label.text = ""
                    self.extra = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.extra_text, self.bigpuzzle_label), 0.05)
            else:
                self.code += f", {instance.text}"
        elif self.wasdumb:
            self.dumb_text = "You press a fifth button. Nothing happens. When the screen said 4-digit code, it meant it. You feel like an idiot now."
            self.bigpuzzle_label.text = ""
            self.char_index = 0
            try:
                self.extra.cancel()
            except:
                pass
            try:
                self.rip.cancel()
            except:
                pass
            self.dumb = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.dumb_text, self.bigpuzzle_label), 0.05)
            self.wasdumb = False
        else:
            try:
                self.dumb.cancel()
            except:
                pass
            try:
                self.extra.cancel()
            except:
                pass
            try:
                self.rip.cancel()
            except:
                pass
            self.char_index = 0
            self.bigpuzzle_label.text="The buttons are: A closed book, a round table, a small chair, an un-even fork, a bent spoon, a cracked egg, a very thin spatula, a closed book, and a deep bowl." 
                
    
    def reset_btns(self, instance):
        self.reset_text="You press the reset button. All asterisks are erased. It seems this keypad functions properly."
        if not self.have_reset:
            self.char_index = 0
            self.bigpuzzle_label.text=""
            try:
                self.extra.cancel()
            except:
                pass
            try:
                self.dumb.cancel()
            except:
                pass
            self.rip = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.reset_text, self.bigpuzzle_label), 0.05)
            self.have_reset = True
        else:
            self.char_index = 0
            try:
                self.rip.cancel()
            except:
                pass
            try:
                self.extra.cancel()
            except:
                pass
            try:
                self.dumb.cancel()
            except:
                pass
            self.bigpuzzle_label.text="The buttons are: A closed book, a round table, a small chair, an un-even fork, a bent spoon, a cracked egg, a very thin spatula, a closed book, and a deep bowl."
        self.code = ""
        self.firstinput = ""
        self.pressed_no = 0
        self.door_btn.disabled = False
        self.table_btn.disabled = False
        self.chair_btn.disabled = False
        self.fork_btn.disabled = False
        self.spoon_btn.disabled = False
        self.egg_btn.disabled = False
        self.spatula_btn.disabled = False
        self.book_btn.disabled = False
        self.bowl_btn.disabled = False
    
    def submitted(self, instance):
        self.layout.clear_widgets()
        try:
            self.rip.cancel()
        except:
            pass
        try:
            self.extra.cancel()
        except:
            pass
        try:
            self.dumb.cancel()
        except:
            pass
        self.char_index = 0
        self.submitted_label = Label(
            text="",
            font_size="25sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True,
            color=self.brown
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.submitted_label)
        if self.firstinput == self.fork_btn.text and self.egg_btn.disabled and self.bowl_btn.disabled and self.door_btn.disabled:
            self.submitted_text = f"""You input: {self.firstinput}{self.code}, and press the submit button. The screen responds, "Access granted", and the door opens. A big amount of sunlight rushes in, the happiness and relief you feel at the moment is undescribable. Behind the door is an opening that leads outside."""
            self.threshold = f"You input: {self.firstinput}{self.code}, and press the submit button."
            self.threshold2 = f"""You input: {self.firstinput}{self.code}, and press the submit button. The screen responds, "Access granted", and the door opens."""
            self.type_submitted = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.submitted_text, self.submitted_label), 0.05)
            pause_time = len(self.threshold) * 0.05 - 0.4
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_submitted, 1, self.threshold), pause_time)
            pause_time2 = len(self.threshold2) * 0.05 + 0.45
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_submitted, 0.5, self.threshold2), pause_time2)
            schedule_time = len(self.submitted_text) * 0.05 + 2
            self.exit_num = "2"
            Clock.schedule_once(self.victory_scene, schedule_time)
        elif self.chair_btn.disabled and self.spoon_btn.disabled and self.book_btn.disabled and self.spatula_btn.disabled:
            self.submitted_text = f"""You input: {self.firstinput}{self.code}, and press the submit button. The screen responds, "Secret code detected. Initiating secret sequence". You are confused as what that means, but before you get a chance to react, everything goes black."""
            self.threshold = f"You input: {self.firstinput}{self.code}, and press the submit button."
            self.threshold2 = f"""You input: {self.firstinput}{self.code}, and press the submit button. The screen responds, "Secret code detected. Initiating secret sequence". """
            
            self.type_submit = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.submitted_text, self.submitted_label), 0.05)
            pause_time = len(self.threshold) * 0.05 - 0.4
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_submit, 1, self.threshold), pause_time)
            pause_time2 = len(self.threshold2) * 0.05 + 0.35
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_submit, 0.5, self.threshold2), pause_time2)
            schedule_time = len(self.submitted_text) * 0.05 + 1.2
            Clock.schedule_once(self.secrecy, schedule_time)
        else:
            self.submitted_text = f"""You input: {self.firstinput}{self.code}, and press the submit button. The screen responds, "Error. Self destruction initiated", then immediately, the whole cave is shaking. You see debris and dust falling from the roof, the ground below you also starts cracking. You start running back. You reach the opening that is now blocked off with the boulder, it seems impossible to keep going that way. The ground below you crumbles."""
            self.threshold = f"""You input: {self.firstinput}{self.code}, and press the submit button."""
            self.threshold2 = f"""You input: {self.firstinput}{self.code}, and press the submit button. The screen responds, "Error. Self destruction initiated", then immediately, """
            self.threshold3 = f"""You input: {self.firstinput}{self.code}, and press the submit button. The screen responds, "Error. Self destruction initiated", then immediately, the whole cave is shaking. You see debris and dust falling from the roof, the ground below you also starts cracking."""
            self.threshold4 = f"""You input: {self.firstinput}{self.code}, and press the submit button. The screen responds, "Error. Self destruction initiated", then immediately, the whole cave is shaking. You see debris and dust falling from the roof, the ground below you also starts cracking. You start running back. You reach the opening that is now blocked off with the boulder, it seems impossible to keep going that way."""
            self.submitted_label.font_size = "24sp"
            self.type_submitted = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.submitted_text, self.submitted_label), 0.05)
            pause_time = len(self.threshold) * 0.05 - 0.4
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_submitted, 1, self.threshold), pause_time)
            pause_time2 = len(self.threshold2) * 0.05 + 0.25
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_submitted, 0.5, self.threshold2), pause_time2)
            if self.effects_on:
                self.boulder_sound.volume = 0.3
                Clock.schedule_once(lambda dt: self.boulder_sound.play(), pause_time2)
            pause_time3 = len(self.threshold3) * 0.05 + 0.5
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_submitted, 1, self.threshold3), pause_time3)
            if self.effects_on:
                if self.ambience_on:
                    self.ambience.volume = 0.2
                self.crack.volume = 0.7
                Clock.schedule_once(lambda dt: self.crack.play(), pause_time3)
            pause_time4 = len(self.threshold4) * 0.05 + 1.1
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_submitted, 1, self.threshold4), pause_time4)
            if self.effects_on:
                Clock.schedule_once(self.crumble, pause_time4)
            schedule_time = len(self.submitted_text) * 0.05 + 3
            Clock.schedule_once(lambda dt: self.game_over(dt, self.bigpuzzle), schedule_time)
            self.cod = "fell to doom"
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.boulder_sound.stop(), schedule_time)          
        
    def secrecy(self, dt):
        self.layout.clear_widgets()
        Clock.schedule_once(self.archive, 10)
    
    def archive(self, dt):
        self.layout.clear_widgets()
        self.archive_text = "Welcome to the lore archive. Here, you can read the whole story behind Cave Adventures. Most of the story can be understood via gameplay, so if you want to try figuring it out yourself, you can click 'return to main menu' to go back to the main menu; or click 'return to puzzle' to go back to the puzzle room you were just in. If you want to read the whole story, click 'access the archive'. The archive is a multi-page story that you can read at your own pace."
        self.archive_label = Label(
            text=self.archive_text,
            font_size="22sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=[0.5, 0.5, 0.5, 1],
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True,
            markup=True
        )
        self.main_menu_button = Button(
            text="return to main menu",
            font_size="22sp",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0},
            background_color=self.brown
        )
        self.main_menu_button.bind(on_press=self.main_menu)
        self.repuzzle = Button(
            text="return to puzzle",
            font_size="22sp",
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'y': 0.1},
            background_color=self.brown
        )
        self.repuzzle.bind(on_press=self.bigpuzzle)
        if self.ambience_on:
            self.ambience.stop()
            self.repuzzle.bind(on_press=lambda instance: self.ambience.play())
        self.read_btn = Button(
            text="access the archive",
            font_size="26sp",
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0.2},
            background_color=self.brown
        )
        self.read_btn.bind(on_press=self.story)
        
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.archive_label)
        self.layout.add_widget(self.main_menu_button)
        if not self.no_puzzle:
            self.layout.add_widget(self.repuzzle)
        self.layout.add_widget(self.read_btn)
    
    def story(self, instance):
        self.layout.clear_widgets()
        self.hasaccess = True
        self.store.put("access", has=self.hasaccess)
        self.story_label = Label(
            text="DISCLAIMER\n\nThis game's story, names, and locations are entirely fictional. Any similarity to real-life objects or people is entirely coincidential..",
            font_size="27sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        self.page_no = 0
        self.next_btn = Button(
            text="next page -->",
            size_hint=(0.2, 0.4),
            pos_hint={'right': 1, 'top': 0.4},
            font_size="19sp",
            text_size=(Window.width * 0.2, Window.height * 0.4),
            valign='center',
            halign='center'
        )
        self.next_btn.bind(on_press=self.next_page)
        self.prev_btn = Button(
            text="prev. page <--",
            font_size="18sp",
            size_hint=(0.2, 0.4),
            pos_hint={'x': 0, 'top': 0.4},
            text_size=(Window.width * 0.2, Window.height * 0.4),
            valign='center',
            halign='center'
        )
        if self.page_no == 0:
            self.prev_btn.text = "Back"
            self.prev_btn.bind(on_press=self.archive)
        else:
            self.prev_btn.bind(on_press=self.prev_page)
        
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.story_label)
        self.layout.add_widget(self.next_btn)
        self.layout.add_widget(self.prev_btn)
           
    def Rarchive(self, instance):
        if instance == self.archive_btn:
            self.no_puzzle = True
        else:
            self.no_puzzle = False
        Clock.schedule_once(self.archive, 0)
    
    def next_page(self, instance):
        self.page_no += 1
        if self.page_no > 1:
            try:
                self.prev_btn.unbind(on_press=self.archive)
            except:
                pass
            self.prev_btn.bind(on_press=self.prev_page)
            self.prev_btn.text = "prev. page <--"
        Clock.schedule_once(self.loadstory, 0)
        
    
    def prev_page(self, instance):
        self.page_no -= 1
        if self.page_no == 1:
            self.prev_btn.unbind(on_press=self.prev_page)
            self.prev_btn.bind(on_press=self.archive)   
            self.prev_btn.text = "Back"
        Clock.schedule_once(self.loadstory, 0)
    
    def loadstory(self, dt):
        if self.page_no == 0:
            self.story_label.text = "DISCLAIMER\n\nThis game's story, names, and locations are entirely fictional. Any similarity to real-life objects or people is entirely coincidential."
            self.story_label.font_size = "27sp"
        elif self.page_no == 1:
            self.story_label.text = "You are an ordinary office worker, with extraordinary friends. Your friends include a scientist, his assistants, and a person who works with the governement. One day, you had a meeting with your friends, and talked about interesting stuff. The scientist mentioned a project they're working on that tests people's reactions in a life-or-death simulation, but they know that they are in a simulation. You protest against the idea, as you think it's wrong to put poeple's lives in danger, even if it is just a simulation."
            self.story_label.font_size="20sp"
        elif self.page_no == 2:
            self.story_label.text = "What you didn't know is that this scientist friend of yours and his assistants are all a part of a much larger organization known as the HRRO. The HRRO is an organization that conducts research in human reactions in different situations with different stimuli. However, the HRRO has a dark secret. As an organization that tests human reactions, they are legally limited to simulation, or low danger levels with willing volunteers, but for a full in-depth research, it was necessary to test the reactions of non-willing people, and thus, the HRIT project was initiated."
            self.story_label.font_size="19sp"
        elif self.page_no == 3:
            self.story_label.text = "The HRIT project, is an illegal project where humans are put through REAL life-or-death situations without their consent. The *cave* you were put in is one of the many sites of the HRIT project. The HRIT project's targets are usually not random. After your protest against the simulation idea, the HRRO was scared of you doing research into them since you have a friend working in the government. The HRRO put you through this test for two major reasons. The first, is to simply remove a threat. In other words, to kill you. The second reason is, even if you do survive, they had needed a test subject for this site anyway."
            try:
                self.next_btn.unbind(on_press=self.archive)
            except:
                pass
            self.next_btn.text = "next page -->"
            self.next_btn.bind(on_press=self.next_page)
        elif self.page_no == 4:
            self.story_label.text = "As a test subject within the HRIT project, they give you drugs that cause memory loss, which is why you barely remember anything when you first wake up. The other thing they do to you is plant chips inside of you for tracking. These chips act as vitals trackers tracking your Bp, heart rate, and other vitals. They also act as location trackers, allowing them to continuously know where you are and what you're doing. The HRIT started many years ago, when the head of the HRRO realized their research was too limited and needed to expand. Each HRIT testing site's records and findings are recorded and stored in a database hidden within the many databases in the HRRO's base of operations.\nTHE    END" 
            self.oii_label = Label(
                text="or is it?",
                font_size="11sp",
                size_hint=(1, 0.1),
                pos_hint={'right': 1, 'y': 0.41},
                text_size=(Window.width * 0.4, Window.height * 0.1),
                halign='left',
                valign='bottom',
                italic=True,
                color=self.brown
            )
            if "1" in self.found_exits and "2" in self.found_exits and "3" in self.found_exits:
                self.layout.add_widget(self.oii_label)
            self.next_btn.text = "done reading"
            self.next_btn.unbind(on_press=self.next_page)
            self.next_btn.bind(on_press=self.archive)
    
    def ran(self, instance):
        self.qte.cancel()
        self.layout.clear_widgets()
        self.ran_text="You keep running as fast as you can. You soon find yourself going towards the right opening in the fork you were just in. the boulder crashes into the wall in front of you, it was really close. The dust settles, the boulder appears to have blocked off the path to the left and back, your only choice is to follow this path to the right."
        self.threshold = "You keep running as fast as you can. You soon find yourself going towards the right opening in the fork you were just in."
        self.threshold2 = "You keep running as fast as you can. You soon find yourself going towards the right opening in the fork you were just in. the boulder crashes into the wall in front of you, it was really close."
        self.ran_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            color=self.brown,
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.ran_label)
        
        self.type_ran = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.ran_text, self.ran_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.4
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_ran, 1, self.threshold), pause_time)
            Clock.schedule_once(lambda dt: self.boulder_sound.stop(), pause_time)
            Clock.schedule_once(lambda dt: self.bouldercrash.play(), pause_time)
            self.impact.volume = 0.05
            Clock.schedule_once(lambda dt: self.impact.play(), pause_time)
        if self.effects_on:
            pause_time2 = len(self.threshold2) * 0.05 + 0.1
        else:
            pause_time2 = len(self.threshold2) * 0.05 - 0.6
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_ran, 0.5, self.threshold2), pause_time2)
        if self.effects_on:
            schedule_time = len(self.ran_text) * 0.05 + 0.5
        else:
            schedule_time = len(self.ran_text) * 0.05 + 0.2
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.two_btns), schedule_time)
    
    def hidden(self, instance):
        self.qte.cancel()
        self.layout.clear_widgets()
        self.hidden_text="You run towards the opening and shove yourself in it. You get stuck. The hole is too small for your whole body, so you attempt to pull yourself out. You succeed; However, it's too late."
        self.threshold = "You run towards the opening and shove yourself in it."
        self.threshold2 = "You run towards the opening and shove yourself in it. You get stuck. The hole is too small for your whole body, so you attempt to pull yourself out."
        self.hidden_label = Label(
            text="",
            font_size="25sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True,
            color=self.brown
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.hidden_label)
        
        self.type_hidden = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.hidden_text, self.hidden_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.2
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_hidden, 0.5, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_hidden, 1, self.threshold2), pause_time2)
        schedule_time = len(self.hidden_text) * 0.05 + 1.5
        Clock.schedule_once(lambda dt: self.game_over(dt, self.boulder), schedule_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.boulder_sound.stop(), schedule_time)
    
    def two_btns(self, instance):
        self.layout.clear_widgets()
        self.two_text = "You follow the right path. You reach the light source, a small hole in the ceiling similar to the ones at the first fork. This hole is lighting a big empty square area. In the center of the eastern and western walls are two small holes, each of which has a button in it. Neither button has a label on it, and both of them look exactly the same. Which button do you press?"
        self.threshold="You follow the right path."
        self.two_label = Label(
            text="",
            font_size="23sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        self.two_image = Image(
            source="assets/two_btns.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.two_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.two_label)
        self.current_skip_func = self.skip_two
        self.skip_button.bind(on_press=self.skip_two)
        self.layout.add_widget(self.skip_button)
        
        self.type_two = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.two_text, self.two_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.1
        self.pause_two = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_two, 0.5, self.threshold), pause_time)
        schedule_time = len(self.two_text) * 0.05 + 0.5
        self.pick_one = Clock.schedule_once(self.twopiece, schedule_time)
        
    def twopiece(self, dt):
        self.western = Button(
            text="Western",
            font_size="24sp",
            size_hint=(0.4, 0.4),
            pos_hint={'x': 0, 'center_y': 0.2},
            background_color=self.brown
        )
        self.western.bind(on_press=self.trap)
        self.eastern = Button(
            text="Eastern",
            font_size="24sp",
            size_hint=(0.4, 0.4),
            pos_hint={'right': 1, 'center_y': 0.2},
            background_color=self.brown
        )
        self.eastern.bind(on_press=self.longer)
        self.layout.add_widget(self.western)
        self.layout.add_widget(self.eastern)    
    
    def skip_two(self, dt):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_two.cancel()
            self.pause_two.cancel()
            self.pick_one.cancel()
            Clock.schedule_once(self.twopiece, 0)
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
        
    
    def longer(self, instance):
        self.layout.clear_widgets()
        self.long_text = "You press the eastern button. Before you get a chance to react, the ground below you shatters, and you fall."
        self.threshold = "You press the eastern button."
        self.threshold2 = "You press the eastern button. Before you get a chance to react, the ground below you shatters,"
        self.long_label = Label(
            text="",
            font_size="28sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True,
            color=self.brown
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.long_label)
        
        self.type_long = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.long_text, self.long_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.1
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_long, 2, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 1.6
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_long, 0.5, self.threshold2), pause_time2)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.death_sound.play(), pause_time2)
        schedule_time = len(self.long_text) * 0.05 + 4
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.prepstair), schedule_time)
    
    def prepstair(self, instance):
        self.layout.clear_widgets()
        self.prep_text = "You land on a matress. It seems it was set up to cushion your fall. There is only one path for you to follow, it appears there is light at the end of this tunnel. You follow the light."
        self.prep_label = Label(
            text="",
            font_size="28sp",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.prep_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_prep
        self.skip_button.bind(on_press=self.skip_prep)
        
        self.type_prep = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.prep_text, self.prep_label), 0.05)
        schedule_time = len(self.prep_text) * 0.05
        self.contprep = Clock.schedule_once(lambda dt: self.add_continue(dt, self.stair), schedule_time)
        
    def skip_prep(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_prep.cancel()
            self.contprep.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.stair), 0)
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
    
    def stair(self, instance):
        self.layout.clear_widgets()
        if self.upped:
            self.stair_text = """You go back down the spiraling path. You are back in front of the two spiraling path. Which one do you take?"""
        else:
            self.stair_text = """You reach the light source, it doesn't surprise you anymore. Two holes, just like the ones you've seen before. You can see two paths, but they don't look natural. The path to your right spirals downwards, just like a spiral saircase. The path to your left spirals upwards, just like the one to the right. Which path will you take?"""
        self.threshold = """You reach the light source, it doesn't surprise you anymore. Two holes, just like the ones you've seen before. You can see two paths, but they don't look natural."""
        self.threshold2 = """You reach the light source, it doesn't surprise you anymore. Two holes, just like the ones you've seen before. You can see two paths, but they don't look natural. The path to your right spirals downwards, just like a spiral saircase"""
        self.threshold3 = """You reach the light source, it doesn't surprise you anymore. Two holes, just like the ones you've seen before. You can see two paths, but they don't look natural. The path to your right spirals downwards, just like a spiral saircase. The path to your left spirals upwards, just like the one to the right."""
        self.stair_label = Label(
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
        self.stair_image = Image(
            source="assets/stairway.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.stair_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.stair_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_stair
        self.skip_button.bind(on_press=self.skip_stair)
        
        if self.upped:
            self.stair_label.font_size = "27sp"
        self.type_stair = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.stair_text, self.stair_label), 0.05)
        if not self.upped:
            pause_time = len(self.threshold) * 0.05 - 0.6
            self.pause_stair = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_stair, 0.5, self.threshold), pause_time)
            pause_time2 = len(self.threshold2) * 0.05 - 0.2
            self.pause_stair2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_stair, 0.5, self.threshold2), pause_time2)
            pause_time3 = len(self.threshold3) * 0.05 + 0.25
            self.pause_stair3 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_stair, 0.5, self.threshold3), pause_time3)
            schedule_time = len(self.stair_text) * 0.05 + 1
        else:
            schedule_time = len(self.stair_text) * 0.05 - 0.1
        self.stairopts = Clock.schedule_once(self.stairway, schedule_time)
    
    def skip_stair(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_stair.cancel()
            if not self.upped:
                self.pause_stair.cancel()
                self.pause_stair2.cancel()
                self.pause_stair3.cancel()
            self.stairopts.cancel()
            Clock.schedule_once(self.stairway, 0)
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
    
    def stairway(self, dt):
        self.up_btn = Button(
            text="\n\n\nGo upwards",
            font_size="20sp",
            size_hint=(0.3, 0.4),
            pos_hint={'x': 0.1, 'center_y': 0.2},
            background_color=self.brown,
            text_size=(Window.width * 0.3, Window.height * 0.4),
            halign='center',
            valign='top',
            bold=True
        )
        self.up_btn.bind(on_press=self.upward)
        self.down_btn = Button(
            text="Go downwards\n\n\n",
            size_hint=(0.3, 0.4),
            font_size="20sp",
            pos_hint={'right': 0.9, 'center_y': 0.2},
            background_color=self.brown,
            text_size=(Window.width * 0.3, Window.height * 0.4),
            halign='center',
            valign='bottom',
            bold=True
        )
        self.down_btn.bind(on_press=self.downward)
        self.layout.add_widget(self.up_btn)
        self.layout.add_widget(self.down_btn)
    
    def upward(self, instance):
        self.layout.clear_widgets()
        self.up_text = """You follow the spiral upwards. Moments later, you reach a dead end. It seems there might not be anything here, but you can take a closer look."""
        self.up_label = Label(
            text="",
            font_size="27sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            color=self.brown,
            bold=True
        )
        self.up_image = Image(
            source="assets/dead_end.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.up_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.up_label)
        
        self.type_up = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.up_text, self.up_label), 0.05)
        schedule_time = len(self.up_text) * 0.05
        Clock.schedule_once(self.upopts, schedule_time)
    
    def upopts(self, dt):
        self.inspect_btn = Button(
            text="Try to inspect the wall",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            background_color=self.brown
        )
        self.inspect_btn.bind(on_press=self.inspected)
        self.backdown_btn = Button(
            text="Go back down",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=self.brown
        )
        self.backdown_btn.bind(on_press=self.stairagain)
   
        self.layout.add_widget(self.inspect_btn)
        self.layout.add_widget(self.backdown_btn)
    
    def stairagain(self, instance):
        self.layout.clear_widgets()
        self.stair_text = """You go back down the spiraling path. You are back in front of the two spiraling paths. Which one do you take?"""
        self.stair_label = Label(
            text="",
            font_size="27sp",
            color=self.brown,
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        if self.images_on:
            self.layout.add_widget(self.stair_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.stair_label)
        
        self.type_stair = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.stair_text, self.stair_label), 0.05)
        schedule_time = len(self.stair_text) * 0.05 - 0.2
        Clock.schedule_once(self.stairway, schedule_time)  
    
    def inspected(self, instance):
        self.layout.clear_widgets()
        self.inspected_text = """You put your hands on the wall. You start touching around on it. The wall gets pushed in, like a button. Then, before you get a chance to react, a burst of bullets pierce you like a piece of paper. The bullets came from machine guns behind the wall which opened like an elevator door. You are now as full of holes as a sponge.""" 
        self.threshold = """You put your hands on the wall. You start touching around on it."""
        self.threshold2 = """You put your hands on the wall. You start touching around on it. The wall gets pushed in, like a button. Then, before you get a chance to react,"""
        self.inspected_label = Label(
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
        self.layout.add_widget(self.inspected_label)
        
        self.type_inspected = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.inspected_text, self.inspected_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.2
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_inspected, 1, self.threshold), pause_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.click.play(), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.7
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_inspected, 2.5, self.threshold2), pause_time2)
            Clock.schedule_once(lambda dt: self.shot.play(), pause_time2)
            schedule_time = len(self.inspected_text) * 0.05 + 4.5
        else:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_inspected, 1, self.threshold2), pause_time2)
            schedule_time = len(self.inspected_text) * 0.05 + 3.2
        self.cod = "shot to death"
        Clock.schedule_once(lambda dt: self.game_over(dt, self.stair), schedule_time)
    
    def downward(self, instance):
        self.layout.clear_widgets()
        self.op_no += 1
        if self.op_no == 1:
            self.down_text = """You follow the right spiral downwards. As you are walking downwards, you see an opening to your left. Do you take the opening or keep heading down?"""
        else:
            self.down_text = """You keep heading downwards. You see another opening to your left. Do you want to take the opening or keep heading down?"""
        self.down_label = Label(
            text="",
            font_size="27sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            bold=True,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top'
        )
        self.down_image = Image(
            source="assets/spiral_down.png",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.down_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.down_label)
        self.current_skip_func = self.skip_down
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_down)
        
        self.type_down = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.down_text, self.down_label), 0.05)
        schedule_time = len(self.down_text) * 0.05
        self.op_opts = Clock.schedule_once(self.downopts, schedule_time)
    
    def skip_down(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_down.cancel()
            self.op_opts.cancel()
            Clock.schedule_once(self.downopts, 0)
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
    
    def downopts(self, dt):
        self.take_btn = Button(
            text="Take the opening",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            background_color=self.brown
        )
        if self.op_no == 5:
            self.take_btn.bind(on_press=self.SE)
        else:
            self.take_btn.bind(on_press=self.wrong_turn)
        self.keep_btn = Button(
            text="Keep going down",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0},
            background_color=self.brown
        )
        if self.op_no == 9:
            self.keep_btn.bind(on_press=self.password)
        else:
            self.keep_btn.bind(on_press=self.downward)
        self.layout.add_widget(self.take_btn)
        self.layout.add_widget(self.keep_btn)
    
    def wrong_turn(self, instance):
        self.layout.clear_widgets()
        self.wrong_text = """You take the opening to your left. A few steps in, a boulder blocks the opening behind you. Then, before you get a chance to react, a burst of bullets pierce you like a piece of paper. It seems the walls to your left and right were set up to open up and reveal a set of machine guns arranged across them. You are now as full of holes as a sponge."""
        self.threshold = """You take the opening to your left. A few steps in,"""
        self.threshold2 = """You take the opening to your left. A few steps in, a boulder blocks the opening behind you. Then, before you get a chance to react,"""
        self.wrong_label = Label(
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
        self.layout.add_widget(self.wrong_label)
        
        self.type_wrongturn = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.wrong_text, self.wrong_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.1
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_wrongturn, 0.5, self.threshold), pause_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.bouldercrash.play(), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.2
        if self.effects_on:
            self.duration = 2.5
            Clock.schedule_once(lambda dt: self.shot.play(), pause_time2)
            schedule_time = len(self.wrong_text) * 0.05 + 3
        else:
            self.duration = 1
            schedule_time = len(self.wrong_text) * 0.05 + 1.5
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_wrongturn, self.duration, self.threshold2), pause_time2)
        self.cod = "shot to death"
        Clock.schedule_once(lambda dt: self.game_over(dt, self.stair), schedule_time)
        self.op_no = 0
    
    def password(self, instance):
        self.layout.clear_widgets()
        if not hasattr(self, 'passed1') or not self.returned:
            self.password_hint = "How many openings did you pass by?"
            self.passed1= True
            self.returned = True
            self.passed2 = False
        elif self.passed1 == True and not self.passed2:
            self.password_hint = "What was the button you pressed last time?"
            self.passed2 = True
        else:
            self.password_hint = "Solve: x - y\n where: x = The number of openings you passed by, y = The button you pressed last."
            self.returned = False
        self.pass_text = f"""You keep heading down. The spiral finally reaches an end, and the path is now straight. A few steps forward, you now stand directly in front of a metal door with what appears to be an elevator's keypad numbered zero through nine next to it. There is a note attached to it, it reads, "{self.password_hint}". What do you input?"""
        self.threshold = f"""You keep heading down. The spiral finally reaches an end, and the path is now straight. A few steps forward, you now stand directly in front of a metal door with what appears to be an elevator's keypad numbered zero through nine next to it."""
        self.pass_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.pass_image = Image(
            source="assets/second_puzzle.png",
            size_hint=(1, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.pass_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.pass_label)
        self.current_skip_func = self.skip_pass
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_pass)
         
        self.type_pass = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.pass_text, self.pass_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.8
        self.pause_pass = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_pass, 0.5, self.threshold), pause_time)
        schedule_time = len(self.pass_text) * 0.05
        self.buttons = Clock.schedule_once(self.lift_btns, schedule_time)
    
    def skip_pass(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_pass.cancel()
            try:
                self.pause_pass.cancel()
            except:
                pass
            self.buttons.cancel()
            Clock.schedule_once(self.lift_btns, 0)
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
    
    def lift_btns(self, dt):
        self.one_btn = Button(
            text="1",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.025, 'top': 0.39}
        )
        self.one_btn.bind(on_press=self.elevated)
        self.two_btn = Button(
            text="2",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.35, 'top': 0.39}
        )
        self.two_btn.bind(on_press=self.elevated)
        self.three_btn = Button(
            text="3",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.675, 'top': 0.39}
        )
        self.three_btn.bind(on_press=self.elevated)
        self.four_btn = Button(
            text="4",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.025, 'top': 0.29} 
        )
        self.four_btn.bind(on_press=self.elevated)
        self.five_btn = Button(
            text="5",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.35, 'top': 0.29}
        )
        self.five_btn.bind(on_press=self.elevated)
        self.six_btn = Button(
            text="6",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.675, 'top': 0.29}
        )
        self.six_btn.bind(on_press=self.elevated)
        self.seven_btn = Button(
            text="7",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.025, 'top': 0.19}
        )
        self.seven_btn.bind(on_press=self.elevated)
        self.eight_btn = Button(
            text="8",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.35, 'top': 0.19}
        )
        self.eight_btn.bind(on_press=self.elevated)
        self.nine_btn = Button(
            text="9",
            font_size="24sp",
            size_hint=(0.3, 0.09),
            pos_hint={'x': 0.675, 'top': 0.19}
        )
        self.nine_btn.bind(on_press=self.elevated)
        self.zero_btn = Button(
            text="0",
            font_size="24sp",
            size_hint=(0.4, 0.08),
            pos_hint={'center_x': 0.5, 'top': 0.09}
        )
        self.zero_btn.bind(on_press=self.elevated)
        
        self.layout.add_widget(self.one_btn)
        self.layout.add_widget(self.two_btn)
        self.layout.add_widget(self.three_btn)
        self.layout.add_widget(self.four_btn)
        self.layout.add_widget(self.five_btn)
        self.layout.add_widget(self.six_btn)
        self.layout.add_widget(self.seven_btn)
        self.layout.add_widget(self.eight_btn)
        self.layout.add_widget(self.nine_btn)
        self.layout.add_widget(self.zero_btn)
    
    def elevated(self, instance):
        self.layout.clear_widgets()
        if self.password_hint == "How many openings did you pass by?":
            self.correct_answer = 9
        elif self.password_hint == "What was the button you pressed last time?":
            self.correct_answer = self.pressed_btn_no
        else:
            self.correct_answer = 9 - self.pressed_btn_no
        self.pressed_btn_no = int(instance.text)
        self.elevated_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.elevated_label)
        if self.correct_answer == self.pressed_btn_no:
            self.elevated_text = f"""You press {self.pressed_btn_no}. The metal door opens just like an elevator door. You walk in, you don't see the usual keypad in the elevator, but the door closes automatically after a moment. The elevator starts moving, it feels like it's going downwards. The elevator stops, and its door starts to open, you see sunlight rushing in. The elevator door opens to an opening leading outside."""
            self.threshold = f"""You press {self.pressed_btn_no}. The metal door opens just like an elevator door. You walk in, you don't see the usual keypad in the elevator, but the door closes automatically after a moment."""
            self.threshold2 = f"""You press {self.pressed_btn_no}. The metal door opens just like an elevator door. You walk in, you don't see the usual keypad in the elevator, but the door closes automatically after a moment. The elevator starts moving, it feels like it's going downwards."""
            self.type_elevated = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.elevated_text, self.elevated_label), 0.05)
            open_time = len(f"You press {self.pressed_btn_no}") * 0.05
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.elevator_open.play(), open_time)
            pause_time = len(self.threshold) * 0.05 - 0.65
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_elevated, 0.5, self.threshold), pause_time)
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.elevator_ride.play(), pause_time - 2)
            pause_time2 = len(self.threshold2) * 0.05 - 0.25
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_elevated, 4, self.threshold2), pause_time2)
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.elevator_ride.stop(), pause_time2 + 4)
                Clock.schedule_once(lambda dt: self.elevator_open.play(), pause_time2 + 4.1)
            schedule_time = len(self.elevated_text) * 0.05 + 3.75
            self.exit_num = "3"
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.victory_scene), schedule_time)
        else:
            self.elevated_text = f"""You press {self.pressed_btn_no}. The metal door opens just like an elevator door. You walk in, you don't see the usual keypad in the elevator, but the door closes automatically after a moment. The elevator starts moving, it feels like it's going downwards. The elevator malfunctions, you can feel your legs lift up from the floor as the elevator plummets faster than you could catch your breath. The elevator crashes with you inside it. Your body feels numb, your vision is blurry, you can barely see the color red. Your mind fades away."""
            self.threshold = f"""You press {self.pressed_btn_no}. The metal door opens just like an elevator door. You walk in, you don't see the usual keypad in the elevator, but the door closes automatically after a moment."""
            self.threshold2 = f"""You press {self.pressed_btn_no}. The metal door opens just like an elevator door. You walk in, you don't see the usual keypad in the elevator, but the door closes automatically after a moment. The elevator starts moving, it feels like it's going downwards."""
            self.threshold3 = f"""You press {self.pressed_btn_no}. The metal door opens just like an elevator door. You walk in, you don't see the usual keypad in the elevator, but the door closes automatically after a moment. The elevator starts moving, it feels like it's going downwards. The elevator malfunctions, you can feel your legs lift up from the floor as the elevator plummets faster than you could catch your breath."""
            
            self.type_elevated = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.elevated_text, self.elevated_label), 0.05)
            open_time = len(f"You press {self.pressed_btn_no}") * 0.05
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.elevator_open.play(), open_time)
            pause_time = len(self.threshold) * 0.05 - 0.65
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_elevated, 0.5, self.threshold), pause_time)
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.elevator_ride.play(), pause_time - 2)
            pause_time2 = len(self.threshold2) * 0.05 - 0.25
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_elevated, 1, self.threshold2), pause_time2)
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.elevator_ride.stop(), pause_time2 + 1)
                Clock.schedule_once(lambda dt: self.lift_fall.play(), pause_time2 + 1)
            pause_time3 = len(self.threshold3) * 0.05 + 0.45
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_elevated, 3, self.threshold3), pause_time3)
            if self.effects_on:
                Clock.schedule_once(lambda dt: self.lift_fall.stop(), pause_time3 + 2.9)
                Clock.schedule_once(lambda dt: self.elevator_crash.play(), pause_time3 + 2.9)
            schedule_time = len(self.elevated_text) * 0.05 + 6
            self.cod = "crashed out"
            Clock.schedule_once(lambda dt: self.game_over(dt, self.stair), schedule_time)
            self.op_no = 0
            
    def SE(self, instance):
        self.layout.clear_widgets()
        self.SE_text = """You take the opening to your left. A few steps in, a boulder blocks the opening. You see a light ahead of you, so you follow it."""
        self.threshold = """You take the opening to your left. A few steps in, """
        self.SE_label = Label(
            text="",
            font_size="27sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            color=self.brown,
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.SE_label)
        self.current_skip_func = self.skip_SE
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_SE)
        
        self.type_SE = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.SE_text, self.SE_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.1
        self.pause_SE = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_SE, 0.5, self.threshold), pause_time)
        if self.effects_on:
            self.blockme = Clock.schedule_once(lambda dt: self.bouldercrash.play(), pause_time)
        schedule_time = len(self.SE_text) * 0.05 + 0.35
        self.protest = Clock.schedule_once(lambda dt: self.add_continue(dt, self.traitor), schedule_time)
    
    def skip_SE(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_SE.cancel()
            try:
                self.pause_SE.cancel()
            except:
                pass
            if self.effects_on:
                self.blockme.cancel()
            self.protest.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.traitor), 0)
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
    
    def traitor(self, instance):
        self.layout.clear_widgets()
        self.traitor_text = """You reach the light, your mind is blown, you are too shocked to even show emotion. "What am I doing here?" is the first question that comes to your mind, and you're not wrong. Directly in front of you is a photo of yourself. You walk forward to it, your leg bumps into one of three completely metal levers. As you take a closer look at the image, it appears there is writing engraved on the frame, "Protestor" is what it says."""
        self.threshold = """You reach the light, your mind is blown, you are too shocked to even show emotion."""
        self.threshold2 = """You reach the light, your mind is blown, you are too shocked to even show emotion. "What am I doing here?" is the first question that comes to your mind, and you're not wrong. Directly in front of you is a photo of yourself. You walk forward to it, your leg bumps into one of three completely metal levers."""
        self.traitor_label = Label(
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
        self.traitor_image = Image(
            source="assets/lever_puzzle.png",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.traitor_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.traitor_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_traitor
        self.skip_button.bind(on_press=self.skip_traitor)
        
        if self.ambience_on:
            self.ambience.stop()
            self.not_ambience = True
        self.type_traitor = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.traitor_text, self.traitor_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.2
        self.pause_traitor = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_traitor, 1, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05
        self.pause_traitor2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_traitor, 0.5, self.threshold2), pause_time2)
        schedule_time = len(self.traitor_text) * 0.05 + 1
        self.memory_flash = Clock.schedule_once(lambda dt: self.add_continue(dt, self.protestor), schedule_time)
        
    def skip_traitor(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_traitor.cancel()
            self.pause_traitor.cancel()
            self.pause_traitor2.cancel()
            self.memory_flash.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.protestor), 0)
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
    
    def protestor(self, instance):
        self.layout.clear_widgets()
        self.protestor_text = """That word causes a memory flash. You can vaguely remember protesting against a certain idea, but you can't remember what or why. You take a closer look at the levers, all of them are pulled towards the opening you entered, so if you move them you'll' be pulling them towards your photo. It appears that each lever has a note next to it. The notes read, "I regret what I've done.", "I was right.", and "I don't care anymore." Which lever do you pull?"""
        self.threshold = """That word causes a memory flash. You can vaguely remember protesting against a certain idea, but you can't remember what or why."""
        self.threshold2 = """That word causes a memory flash. You can vaguely remember protesting against a certain idea, but you can't remember what or why. You take a closer look at the levers, all of them are pulled towards the opening you entered, so if you move them you'll' be pulling them towards your photo."""
        self.protestor_label = Label(
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
        if self.images_on:
            self.layout.add_widget(self.traitor_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.protestor_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_protestor
        self.skip_button.bind(on_press=self.skip_protestor)
        
        self.type_protesting = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.protestor_text, self.protestor_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.5
        self.pause_protesting = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_protesting, 0.5, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 - 0.3
        self.pause_protesting2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_protesting, 0.5, self.threshold2), pause_time2)
        schedule_time = len(self.protestor_text) * 0.05 + 0.6
        self.protest_opts = Clock.schedule_once(self.protest_options, schedule_time)
    
    def skip_protestor(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_protesting.cancel()
            self.pause_protesting.cancel()
            self.pause_protesting2.cancel()
            self.protest_opts.cancel()
            Clock.schedule_once(self.protest_options, 0)
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
               
    def protest_options(self, dt):
        self.regret_btn = Button(
            text="I regret what I've done",
            font_size="24sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            background_color=self.brown
        )
        self.regret_btn.bind(on_press=self.simulate)
        self.insist_btn = Button(
            text="I was right",
            font_size="24sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'top': 0.27},
            background_color=self.brown
        )
        self.insist_btn.bind(on_press=self.shocked)
        self.idc_btn = Button(
            text="I don't care anymore",
            font_size="24sp",
            size_hint=(1, 0.13),
            pos_hint={'center_x': 0.5, 'top': 0.14},
            background_color=self.brown
        )
        self.idc_btn.bind(on_press=self.shocked)
        self.layout.add_widget(self.regret_btn)
        self.layout.add_widget(self.insist_btn)
        self.layout.add_widget(self.idc_btn)
    
    def shocked(self, instance):
        self.layout.clear_widgets()
        self.shocked_text = f"""You pull the "{instance.text}" lever. The moment it reaches the other side, a surge of high-voltage electricity zaps your whole body. You can feel your body shaking and getting numb, but you can't get your hand off of it. The electric surge slams you onto the wall, but your mind has already faded away."""
        self.threshold = f"""You pull the "{instance.text}" lever. The moment it reaches the other side, """
        self.threshold2 = f"""You pull the "{instance.text}" lever. The moment it reaches the other side, a surge of high-voltage electricity zaps your whole body. You can feel your body shaking and getting numb, but you can't get your hand off of it."""
        self.shocked_label = Label(
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
        if self.images_on:
            self.layout.add_widget(self.traitor_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.shocked_label)
        
        self.type_shock = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.shocked_text, self.shocked_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.35
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_shock, 0.5, self.threshold), pause_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.electrocuted.play(), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 - 0.2
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_shock, 0.5, self.threshold2), pause_time2)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.electrocuted.stop(), pause_time2)
            Clock.schedule_once(lambda dt: self.headbutt.play(), pause_time2 + 0.1)
        schedule_time = len(self.shocked_text) * 0.05 + 1.5
        self.cod = "electrocuted"
        Clock.schedule_once(lambda dt: self.game_over(dt, self.protestor), schedule_time)
        
    def simulate(self, instance):
        self.layout.clear_widgets()
        self.simulate_text = f"""You pull the "{instance.text}" lever. The moment it reaches the other side, the wall to your left crumbles, revealing a small opening. There is light coming from the other side of the opening, so you decide to follow it."""
        self.threshold = f"""You pull the "{instance.text}" lever. The moment it reaches the other side, """
        self.simulate_label = Label(
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
        self.layout.add_widget(self.simulate_label)
        
        self.type_simulate = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.simulate_text, self.simulate_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.4
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_simulate, 0.5, self.threshold), pause_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.impact.play(), pause_time)
        schedule_time = len(self.simulate_text) * 0.05
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.simulation), schedule_time)
    
    def simulation(self, instance):
        self.layout.clear_widgets()
        self.simulation_text = """You reach the light, it's another room. In this room you see a table with a laptop on it directly ahead of you. The laptop's screen shows, "press Enter to continue". To your left is a wooden door with a metal handle. There is nothing else, except a ceiling lamp, in this room. What do you do?"""
        self.simulation_label = Label(
            text="",
            font_size="27sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            color=self.brown,
            bold=True
        )
        self.simulation_image = Image(
            source="assets/laptop_puzzle.png",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.simulation_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.simulation_label)
        self.layout.add_widget(self.skip_button)
        self.skip_button.bind(on_press=self.skip_simulation)
        self.current_skip_func = self.skip_simulation
        
        self.type_simulation = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.simulation_text, self.simulation_label), 0.05)
        schedule_time = len(self.simulation_text) * 0.05
        self.laptop = Clock.schedule_once(self.keyboard, schedule_time)
    
    def skip_simulation(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_simulation.cancel()
            self.laptop.cancel()
            Clock.schedule_once(self.keyboard, 0)
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
    
    def keyboard(self, dt):
        self.ENTER = Button(
            text="Press Enter on the laptop's keyboard",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'y': 0},
            background_color=self.brown
        )
        self.ENTER.bind(on_press=self.started_simulation)
        self.open_door = Button(
            text="Go through the door.",
            font_size="24sp",
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            background_color=self.brown
        )
        self.open_door.bind(on_press=self.electric_door)
        
        self.layout.add_widget(self.ENTER)
        self.layout.add_widget(self.open_door)
    
    def electric_door(self, instance):
        self.layout.clear_widgets()
        self.electric_door_text = """You put your hand on the door's handle. A surge of high-voltage electricity zaps your whole body. You can feel your body going numb, but your hand won't let go. The electriciy slams you on the floor, but your mind has already faded away."""
        self.threshold = """You put your hand on the door's handle."""
        self.threshold2 = """You put your hand on the door's handle. A surge of high-voltage electricity zaps your whole body. You can feel your body going numb, but your hand won't let go."""
        self.electric_door_label = Label(
            text="",
            font_size="27sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True,
            color=self.brown
        )
        if self.images_on:
            self.layout.add_widget(self.simulation_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.electric_door_label)
        
        self.type_electric_door = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.electric_door_text, self.electric_door_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.1
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_electric_door, 0.5, self.threshold), pause_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.electrocuted.play(), pause_time)
        pause_time2 = len(self.threshold2) * 0.05
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_electric_door, 0.5, self.threshold2), pause_time2)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.electrocuted.stop(), pause_time2)
            Clock.schedule_once(lambda dt: self.headbutt.play(), pause_time2 + 0.1)
        schedule_time = len(self.electric_door_text) * 0.05 + 1.5
        self.cod = "electrocuted"
        Clock.schedule_once(lambda dt: self.game_over(dt, self.simulation), schedule_time)
    
    def started_simulation(self, instance):
        self.layout.clear_widgets()
        self.begun_text = """You press Enter on the laptop's keyboard. The screen changes and now displays, "The simulation has begun."' The word 'simulation' strikes you like lightining. You remember the thing you protested against was a life-risking simulation of some kind. Your head hurts, it feels like it's being drilled. Your thought is interrupted with a clicking sound coming from the door. You go towards the door."""
        self.threshold = """You press Enter on the laptop's keyboard. The screen changes and now displays, "The simulation has begun."' The word 'simulation' strikes you like lightining."""
        self.threshold2 = """You press Enter on the laptop's keyboard. The screen changes and now displays, "The simulation has begun."' The word 'simulation' strikes you like lightining. You remember the thing you protested against was a life-risking simulation of some kind. Your head hurts, it feels like it's being drilled."""
        self.begun_label = Label(
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
        if self.images_on:
            self.layout.add_widget(self.simulation_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.begun_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_beginning
        self.skip_button.bind(on_press=self.skip_beginning)
        
        self.type_begun = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.begun_text, self.begun_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.6
        self.pause_begun = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_begun, 0.5, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 - 0.2
        self.pause_begun2 = Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_begun, 0.5, self.threshold2), pause_time2)
        if self.effects_on:
            self.turn_off = Clock.schedule_once(lambda dt: self.click.play(), pause_time2)
        schedule_time = len(self.begun_text) * 0.05 + 0.5
        self.lastSE = Clock.schedule_once(lambda dt: self.add_continue(dt, self.two_doors), schedule_time) 
    
    def skip_beginning(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_begun.cancel()
            self.pause_begun.cancel()
            self.pause_begun2.cancel()
            self.lastSE.cancel()
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.two_doors), 0)
            if self.effects_on:
                self.turn_off.cancel()
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
    
    def two_doors(self, instance):
        self.layout.clear_widgets()
        self.two_doors_text = """You open the door and walk through. You find yet another room; However, the room this time is mostly empty. The only thing you see are two doors, one to the left and one to the right. In between the two doors is a big sign that reads, "Do you think you'll survive?" You notice two small signs above each door, one reading "Yes" and the other reading "No". Do you think you'll survive?"""
        self.two_doors_label = Label(
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
        self.two_doors_image = Image(
            source="assets/two_door.png",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'center_y': 0.7},
            allow_stretch=True,
            keep_ratio=False
        )
        if self.images_on:
            self.layout.add_widget(self.two_doors_image)
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.two_doors_label)
        self.layout.add_widget(self.skip_button)
        self.current_skip_func = self.skip_two_doors
        self.skip_button.bind(on_press=self.skip_two_doors)
        
        self.type_two_doors = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.two_doors_text, self.two_doors_label), 0.05)
        schedule_time = len(self.two_doors_text) * 0.05 -  0.2
        self.survival_chance = Clock.schedule_once(self.potentialSE, schedule_time)
                               
    def skip_two_doors(self, instance):
        if self.char_index < len(self.targeted):
            self.typed_label.text = self.targeted
            self.type_two_doors.cancel()
            self.survival_chance.cancel()
            Clock.schedule_once(self.potentialSE, 0)
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
       
    def potentialSE(self, dt):
        self.I_do = Button(
            text="Yes",
            font_size="24sp",
            size_hint=(0.45, 0.4),
            pos_hint={'x': 0, 'center_y': 0.2},
            background_color=self.brown
        )
        self.I_do.bind(on_press=self.failed)
        self.I_dont = Button(
            text="No",
            font_size="24sp",
            size_hint=(0.45, 0.4),
            pos_hint={'right': 1, 'center_y': 0.2},
            background_color=self.brown
        )
        self.I_dont.bind(on_press=self.failed)
        self.idk = Button(
            text="I don't know",
            font_size="24sp",
            size_hint=(0.3, 0.4),
            pos_hint={'x': 0.3, 'center_y': 0.2},
            background_color=self.brown
        )
        self.idk.bind(on_press=self.secret_ending)
        
        if "1" in self.found_exits and "2" in self.found_exits and "3" in self.found_exits:
            self.I_do.size_hint = (0.3, 0.4)
            self.I_dont.size_hint = (0.3, 0.4)
            self.layout.add_widget(self.idk)
        self.layout.add_widget(self.I_do)
        self.layout.add_widget(self.I_dont)
    
    def failed(self, instance):
        self.layout.clear_widgets()
        if instance.text == "Yes":
            self.answer = "Think again."
        else:
            self.answer = "Correct."
        self.failed_text = f"""You walk toward the door with the "{instance.text}" sign. You squeeze the handle downward and open it. Before you get a chance to react, a singular shot square in your forehead. With the last bit of your blurry vision, your eyes scroll over a sign that reads, "{self.answer}" that is stuck to the ceiling. You hit the ground, your mind fades away."""
        self.threshold = f"""You walk toward the door with the "{instance.text}" sign. You squeeze the handle downward and open it. Before you get a chance to react,"""
        self.threshold2 = f"""You walk toward the door with the "{instance.text}" sign. You squeeze the handle downward and open it. Before you get a chance to react, a singular shot square in your forehead. With the last bit of your blurry vision, your eyes scroll over a sign that reads, "{self.answer}" that is stuck to the ceiling."""
        self.failed_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.failed_label)
        
        self.type_failed = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.failed_text, self.failed_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.4
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_failed, 0.5, self.threshold), pause_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.oneshot.play(), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 - 0.15
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_failed, 3, self.threshold2), pause_time2)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.collapse.play(), pause_time2 + 3)
        schedule_time = len(self.failed_text) * 0.05 + 4
        self.cod = "headshot"
        Clock.schedule_once(lambda dt: self.game_over(dt, self.two_doors), schedule_time)
        
    def secret_ending(self, instance):
        self.layout.clear_widgets()
    
    def trap(self, instance):
        self.layout.clear_widgets()
        self.trap_text = "You press the western button. Before you get a chance to react, the ground below you shatters, and you fall into what seems to be a bottomless pit."
        self.threshold = "You press the western button."
        self.threshold2 = "You press the western button. Before you get a chance to react, the ground below you shatters,"
        self.trap_label = Label(
            text="",
            font_size="28sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True,
            color=self.brown
        )
        self.layout.add_widget(self.text_background)
        self.layout.add_widget(self.trap_label)
        
        self.type_trap = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.trap_text, self.trap_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.1
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_trap, 2, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 1.6
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_trap, 0.5, self.threshold2), pause_time2)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.death_sound.play(), pause_time2)
        schedule_time = len(self.trap_text) * 0.05 + 4
        Clock.schedule_once(self.stuck, schedule_time)
    
    def stuck(self, dt):
        self.layout.clear_widgets()
        if self.ambience_on:
            self.ambience.stop()
        Clock.schedule_once(self.awaken, 5)
    
    def awaken(self, dt):
        self.awaken_text = """You wake up. It's pitch black. You survived the fall, you don't know how. The ground below you. It's soft. A mattress, thick enough to cushion your fall. You stand up, extend your hand upwards. Nothing. Your hand fails to feel anything, no ceiling, no rocks, no wind, just darkness. You walk around on the mattress, you feel the pieces of the ground you once stood on - tiny rocks, scattered in a million pieces, too tiny to even hurt your feet."""
        self.threshold = "You wake up. It's pitch black. You survived the fall, you don't know how."
        self.threshold2 = "You wake up. It's pitch black. You survived the fall, you don't know how. The ground below you. It's soft."
        self.threshold3 = "You wake up. It's pitch black. You survived the fall, you don't know how. The ground below you. It's soft. A mattress, thick enough to cushion your fall. You stand up, extend your hand upwards."
        self.threshold4 = "You wake up. It's pitch black. You survived the fall, you don't know how. The ground below you. It's soft. A mattress, thick enough to cushion your fall. You stand up, extend your hand upwards. Nothing. Your hand fails to feel anything, no ceiling, no rocks, no wind, just darkness."
        self.awaken_label = Label(
            text="",
            font_size="20sp",
            size_hint=(1, 0.6),
            pos_hint={'x': 0, 'top': 0.95},
            color=self.brown,
            text_size=(Window.width * 0.9, Window.height * 0.6),
            halign='left',
            valign='top',
            bold=True
        )
        self.layout.add_widget(self.awaken_label)
        
        self.type_awaken = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.35
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken, 0.5, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.1
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken, 0.5, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3) * 0.05 + 0.25
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken, 0.5, self.threshold3), pause_time3)
        pause_time4 = len(self.threshold4) * 0.05 + 0.45
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken, 0.5, self.threshold4), pause_time4)
        schedule_time = len(self.awaken_text) * 0.05 + 1.1
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken2), schedule_time)
    
    def awaken2(self, instance):
        self.awaken_label.text = ""
        self.awaken_label.font_size="18sp"
        self.layout.remove_widget(instance)
        self.awaken_text = """A few steps forward, you bump into a wall. A wall, too smooth to even be a part of a cave. Suddenly, all previous encounters in this cave flash through your brain. The layout, the spot you woke up in, your memory loss of how you got here, and even the conveniently and almost too neatly placed lighting holes in the roof. "Was this a set-up?" You think to yourself, "Was I trapped here by someone?" \n"Who? Why? When? For what? I never did anything to anyone to deserve this!" So many unanswered questions echo through your hollow skull. "I don't have time to think about that!" You shout, desperately. "I have to find a way out." """
        self.threshold = "A few steps forward, you bump into a wall."
        self.threshold2 = """A few steps forward, you bump into a wall. A wall, too smooth to even be a part of a cave. Suddenly, all previous encounters in this cave flash through your brain."""
        self.threshold3 = """A few steps forward, you bump into a wall. A wall, too smooth to even be a part of a cave. Suddenly, all previous encounters in this cave flash through your brain. The layout, the spot you woke up in, your memory loss of how you got here, and even the conveniently and almost too neatly placed lighting holes in the roof. "Was this a set-up?" You think to yourself, "Was I trapped here by someone?" """
        self.threshold4 = """A few steps forward, you bump into a wall. A wall, too smooth to even be a part of a cave. Suddenly, all previous encounters in this cave flash through your brain. The layout, the spot you woke up in, your memory loss of how you got here, and even the conveniently and almost too neatly placed lighting holes in the roof. "Was this a set-up?" You think to yourself, "Was I trapped here by someone?" \n"Who? Why? When? For what? I never did anything to anyone to deserve this!" So many unanswered questions echo through your hollow skull."""
        
        self.type_awaken2 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.15
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken2, 0.5, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.05
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken2, 0.7, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3) * 0.05 + 0.1
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken2, 1, self.threshold3), pause_time3)
        pause_time4 = len(self.threshold4) * 0.05 + 0.7
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken2, 2, self.threshold4), pause_time4)
        schedule_time = len(self.awaken_text) * 0.05 + 2.7
        if self.havegrapple:
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken25), schedule_time)
        else:
            Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken3), schedule_time)
        
        
    def awaken25(self, instance):
        self.awaken_label.text = ""
        self.awaken_label.font_size = "24sp"
        self.layout.remove_widget(instance)
        self.awaken_text = """You look around for your grapple gun. You lean down towards the ground and start feeling it. After scavenging in the dark for a while, you manage to finally find it. You pick it up, aim upwards, and shoot. It hits nothing, you can feel the rope coming back down. It seems the ceiling is too high up for you to grapple."""
        self.threshold = "You look around for your grapple gun. You lean down towards the ground and start feeling it."
        self.threshold2 = "You look around for your grapple gun. You lean down towards the ground and start feeling it. After scavenging in the dark for a while, you manage to finally find it. You pick it up, aim upwards, and shoot."
        self.type_awaken25 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.4
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken25, 2.5, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 1.8
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken25, 3, self.threshold2), pause_time2)
            Clock.schedule_once(lambda dt: self.grapple.play(), pause_time2)
            Clock.schedule_once(lambda dt: self.grapple.stop(), pause_time2 + 2.2)
            schedule_time = len(self.awaken_text) * 0.05 + 5
        else:
            Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken25, 1, self.threshold2), pause_time2)
            schedule_time = len(self.awaken_text) * 0.05 + 3
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken3), schedule_time)
    
    def awaken3(self, instance):
        self.awaken_label.text = ""
        self.layout.remove_widget(instance)
        self.awaken_label.font_size = "19sp"
        self.awaken_text = """You closely follow and touch the wall, hoping to find an opening, or a rougher surface that could be climbable. Nothing. You halt your examination of the wall when you realize that you've already went in a circle. "NO... This just.... Can't.... Be true... I can't die in a place like this!" But hope isn't all lost. You quickly lie down on the mattress, "If this was indeed a set-up, an exit could be below this thing." You hoped, "Come on, come on!" You start tearing apart the cloth on the mattress, you can feel the cotton stuffed inside it, you start removing it. "Just a little more," you encourage yourself, "I can do this!" """
        self.threshold = "You closely follow and touch the wall, hoping to find an opening, or a rougher surface that could be climbable."
        self.threshold2 = """You closely follow and touch the wall, hoping to find an opening, or a rougher surface that could be climbable. Nothing. You halt your examination of the wall when you realize that you've already went in a circle. "NO... This just.... Can't.... Be true... I can't die in a place like this!" But hope isn't all lost."""
        self.type_awaken3 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.35
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken3, 1.5, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.6
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken3, 1, self.threshold2), pause_time2)
        schedule_time = len(self.awaken_text) * 0.05 + 2
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken4), schedule_time)
        
    
    def awaken4(self, instance):
        self.layout.remove_widget(instance)
        self.awaken_label.text = ""
        self.awaken_label.font_size = "20sp"
        self.awaken_text = """Moments later, you touch the ground. A touch, that shrouds you completely in despair. "NO, NO! There has to be an exit" you desperately try to convince yourself. "I just have to check other areas."  Moments later, you're too exhausted. you've removed most - if not all - of the mattress's cotton, and yet you've found nothing, like a child who's piñata was empty after working so hard to break it. You are filled with despair."""
        self.threshold = """Moments later, you touch the ground. A touch, that shrouds you completely in despair. "NO, NO! There has to be an exit" you desperately try to convince yourself. "I just have to check other areas." """
        
        self.type_awaken4 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.3 - len("Moments") * 0.05
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken4, 2, self.threshold), pause_time)
        schedule_time = len(self.awaken_text) * 0.05 + 2
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken5), schedule_time)
    
    def awaken5(self, instance):
        self.layout.remove_widget(instance)
        self.awaken_label.text = ""
        self.awaken_text = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" "Help" "Exit" "somebody" "death" "exit" "somebody" "help" A surge of endless thoughts drowns your brain.... Until suddenly, your brain goes blank."""
        self.tick1 = """ "NO!" """
        self.tick2 = """ "NO!" "I can't die here!" """
        self.tick3 = """ "NO!" "I can't die here!" "I must find a way out" """
        self.tick4 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" """
        self.tick5 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" """
        self.tick6 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" """
        self.tick7 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" """
        self.tick8 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" """
        self.tick9 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" """
        self.tick10 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" """
        self.tick11 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" """
        self.tick12 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" """
        self.tick13 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" "Help" """
        self.tick14 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" "Help" "Exit" """
        self.tick15 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" "Help" "Exit" "somebody" """
        self.tick16 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" "Help" "Exit" "somebody" "death" """
        self.tick17 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" "Help" "Exit" "somebody" "death" "exit" """
        self.tick18 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" "Help" "Exit" "somebody" "death" "exit" "somebody" """
        self.tick19 = """ "NO!" "I can't die here!" "I must find a way out" "There just has to be a way out" "Is there a way out?" "I've looked everywhere, haven't I?" "There is just no exit" "I'm gonna die here" "I don't want to die" "Somebody help!" "I don't want to die" "I'm gonna die" "Help" "Exit" "somebody" "death" "exit" "somebody" "help" """
        self.counter = 1
        self.remaining_text = (len(self.awaken_text) - len(self.tick19)) * 0.05
        self.tickthresh = 20
        Clock.schedule_interval(lambda dt: self.ticking(dt, self.awaken_label, self.awaken_text), 1)
        schedule_time = self.remaining_text + self.tickthresh
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken6), schedule_time)             
    
    def awaken6(self, instance):
        self.layout.remove_widget(instance)
        self.awaken_label.text = ""
        self.awaken_text = """Your head feels hollow, like an egg missing its insides. Your body feels numb, too numb to even raise a finger. You collapse. Your life flashes before your eyes. Your family, your pet, your job, all the sweet memories, all the bad memories. You miss it all, you miss your normal life. "How did this happen?" One thought clears your brain, almost too loud and clear to be a thought. "How did I end up in this place? What led to this? Whe-." your thoughts are interrupted with a memory. A memory, clear as day."""
        self.threshold = """Your head feels hollow, like an egg missing its insides. Your body feels numb, too numb to even raise a finger. You collapse."""
        self.threshold2 = """Your head feels hollow, like an egg missing its insides. Your body feels numb, too numb to even raise a finger. You collapse. Your life flashes before your eyes. Your family, your pet, your job, all the sweet memories, all the bad memories. You miss it all, you miss your normal life."""
        self.threshold3 = """Your head feels hollow, like an egg missing its insides. Your body feels numb, too numb to even raise a finger. You collapse. Your life flashes before your eyes. Your family, your pet, your job, all the sweet memories, all the bad memories. You miss it all, you miss your normal life. "How did this happen?" One thought clears your brain, almost too loud and clear to be a thought."""
        self.type_awaken6 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        pause_time = len(self.threshold) * 0.05 - 0.3
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken6, 1, self.threshold), pause_time)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.collapse.play(), pause_time - len("You collapse") * 0.05)
        pause_time2 = len(self.threshold2) * 0.05 + 0.6
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken6, 3, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3) * 0.05 + 3.2
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_awaken6, 0.7, self.threshold3), pause_time3)
        schedule_time = len(self.awaken_text) * 0.05 + 3.9
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken7), schedule_time)
    
    def awaken7(self, instance):
        self.layout.remove_widget(instance)
        self.awaken_label.text = ""
        self.awaken_label.font_size = "17sp"
        self.awaken_text = """A group of people, in what appears to be a diner. A scientist you seem to know but can't remember, his assistants, a friendly face you recall to be a neighbour, a friend of yours, and finally, you. "I have been thinking about an experiment," the scientist says, "a simulation, where people put their lives in danger, and their survival skills are tested." "How interesting," you remark, "What's the idea behind this experiment?" "Simple," the scientist replies, "people in this experiment KNOW they are in a simulation, we want to see how much the human body prepares for survival, even when knowing their lives aren't in any real danger." "How intriguing," your friend remarks, "What type of danger are you simulating though?" "A dark cave was our first thought." An assistant replies, "We thought it was an easy scenario to deal with for a starting prototype. It can change later" """
        self.type_awaken7 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        schedule_time = len(self.awaken_text) * 0.05
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.awaken8), schedule_time)
    
    def awaken8(self, instance):
        self.layout.remove_widget(instance)
        self.awaken_label.text = ""
        self.awaken_label.font_size = "20sp"
        self.awaken_text = """The memory stops there, you can't bring yourself to recall anything after that memory, as your mind is stuck on one question, like a tape that is put on repeat. "Is this a simulation?" "Is this a simulation?" "Is this a simulation?" You pick yourself up, barely able to get to your feet that can barely handle your weight. Swaying, stumbling your way over to the wall, you pull your head as far up and back as you can while maintaining balance."""
        self.tick1= """The memory stops there, you can't bring yourself to recall anything after that memory, as your mind is stuck on one question, like a tape that is put on repeat. "Is this a simulation?" """
        self.tick2 = """The memory stops there, you can't bring yourself to recall anything after that memory, as your mind is stuck on one question, like a tape that is put on repeat. "Is this a simulation?" "Is this a simulation?" """
        self.tick3 = """The memory stops there, you can't bring yourself to recall anything after that memory, as your mind is stuck on one question, like a tape that is put on repeat. "Is this a simulation?" "Is this a simulation?" "Is this a simulation?" """
        self.tickthresh = 4
        self.textthreshold = """The memory stops there, you can't bring yourself to recall anything after that memory, as your mind is stuck on one question, like a tape that is put on repeat."""
        self.type_awaken8 = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        pause_time = len(self.textthreshold) * 0.05 - 0.55
        Clock.schedule_once(lambda dt: self.tick_prep(dt, self.type_awaken8, self.textthreshold, self.awaken_label, self.awaken_text, 1.5), pause_time)
        self.remaining_text = (len(self.awaken_text) - len(self.tick3)) * 0.05
        schedule_time = len(self.awaken_text) * 0.05 + self.tickthresh + 2
        Clock.schedule_once(lambda dt: self.add_continue(dt, self.Fawaken), schedule_time) 
    
    def Fawaken(self, instance):
        self.layout.remove_widget(instance)
        self.awaken_label.text = ""
        self.awaken_label.markup = True
        self.awaken_text = """*CRACK* A loud sound, coming straight from your head that you've rammed to the wall. Blood, drips over your face, like water washing down a window after heavy rain. The pain, you can feel it, even though your whole body is numb. "This is not a simulation." A simple yet very cruel realization, all your hope is gone, your body, number than ever, fails you. You collapse. Your mind, fades away, like light getting sucked into a vacuum. Despair, consumes you, like a savage beast eating at your body."""
        self.threshold = """*CRACK*"""
        self.threshold2 = """*CRACK* A loud sound, coming straight from your head that you've rammed to the wall."""
        self.threshold3 = """*CRACK* A loud sound, coming straight from your head that you've rammed to the wall. Blood, drips over your face, like water washing down a window after heavy rain. The pain, you can feel it, even though your whole body is numb."""
        self.threshold4 = """*CRACK* A loud sound, coming straight from your head that you've rammed to the wall. Blood, drips over your face, like water washing down a window after heavy rain. The pain, you can feel it, even though your whole body is numb. "This is not a simulation." A simple yet very cruel realization, all your hope is gone, your body, number than ever, fails you. You collapse."""
        if self.effects_on:
            self.headbutt.volume = 0.8
            self.headbutt.play()
        self.type_Fawaken = Clock.schedule_interval(lambda dt: self.typewrite(dt, self.awaken_text, self.awaken_label), 0.05)
        pause_time = len(self.threshold) * 0.05
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_Fawaken, 0.5, self.threshold), pause_time)
        pause_time2 = len(self.threshold2) * 0.05 + 0.25
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_Fawaken, 0.5, self.threshold2), pause_time2)
        pause_time3 = len(self.threshold3) * 0.05 + 0.65
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_Fawaken, 0.5, self.threshold3), pause_time3)
        pause_time4 = len(self.threshold4) * 0.05 + 0.95
        Clock.schedule_once(lambda dt: self.pause_typewrite(dt, self.type_Fawaken, 0.5, self.threshold4), pause_time4)
        if self.effects_on:
            Clock.schedule_once(lambda dt: self.collapse.play(), pause_time4)
        schedule_time = len(self.awaken_text) * 0.05 + 3
        self.cod = "trapped forever"
        Clock.schedule_once(lambda dt: self.game_over(dt, self.two_btns), schedule_time)
    
    def make_true(self, variable):
        variable = True
    
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
    
    def tick_prep(self, dt, typewrite_method, pause_quota, label, full_text, interval):
        self.typed_label.text = pause_quota
        try:
            typewrite_method.cancel()
        except:
            pass
        Clock.schedule_interval(lambda dt: self.ticking(dt, label, full_text), interval)
    
    def ticking(self, dt, label, full_text):
        if self.counter < self.tickthresh:
            label.text = getattr(self, f"tick{self.counter}")
            self.counter += 1
        else:
            self.char_index = len(label.text)
            Clock.schedule_interval(lambda dt: self.typewrite(dt, full_text, label), 0.05)
            self.counter = 1
            return False
                
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
        if self.ambience_on == True and not self.not_ambience:
            self.retry_btn.bind(on_press=lambda instance: self.ambience.play())
        if self.effects_on == True:
            if self.cod == self.fall_death:
                self.death_sound.play()
            elif self.cod == self.bat_eaten:
                self.bat_death.play()
            elif self.cod == self.crush_death:
                self.crush.play()
            elif self.cod == self.electric_death:
                self.dead_electricity.play() 
        if self.ambience_on == True:
            self.ambience.stop() 
        self.died_label.opacity = 0
        self.cod_label.opacity = 0
        self.layout.add_widget(self.died_label)
        self.layout.add_widget(self.cod_label)
        self.death_count += 1
        self.store.put("deaths", count=self.death_count)
        
        Clock.schedule_interval(lambda dt: self.image_appear(dt, self.died_label, 1), 0.1)
        Clock.schedule_interval(lambda dt: self.image_appear(dt, self.cod_label, 1), 0.2)
        Clock.schedule_once(self.add_death_options, 2.5)
   
    def add_death_options(self, dt):
        self.layout.add_widget(self.main_menu_button)
        self.layout.add_widget(self.retry_btn)
        
    def victory_scene(self, instance):
        self.layout.clear_widgets()
        self.scenery_text = "You walk out the opening. You see the path going downwards. It appears that this *cave* is built on a mountain. You follow the path downwards towards the very beautiful sunshine. You embrace the sunlight as you walk downward, even the birds chirping sounds like music to your ears. So many unanswered questions remain, yet you stopped caring. You're just happy you're alive."
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
        
        if not self.exit_num in self.found_exits:
            self.found_exits.append(self.exit_num)
            self.store.put("exits", found=self.found_exits)
        
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
        Clock.schedule_once(lambda dt: self.layout.add_widget(self.main_menu_btn), 2.5)
        
    def resetdeaths(self, instance):
        self.death_count = 0
        self.store.put("deaths", count=self.death_count)
    
    def end_win(self, instance):
        try:
            self.victorySFX.cancel()
            self.victorySFX2.cancel()
        except:
            pass
        self.vic_ambience.stop()
        self.vic_ambience2.stop()
        
    
    def make_appearance(self, dt, target_image, target_opacity, interval):
        Clock.schedule_interval(lambda dt: self.image_appear(dt, target_image, target_opacity), interval)
        
    def image_appear(self, dt, target_image, target_opacity):
        if target_image.opacity < target_opacity:
            target_image.opacity += 0.1
        else:
            return False
            
    def Samplification(self, dt, SFX, target_volume, interval):
        Clock.schedule_interval(lambda dt: self.amplification(dt, SFX, target_volume), interval)
        
    
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
