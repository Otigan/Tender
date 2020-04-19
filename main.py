import matplotlib.pyplot as plt
import pandas as pd
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.graphics.transformation import Matrix
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.scatter import Scatter, ScatterPlane
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from plyer import filechooser
import ntpath
import time
import functools
from jnius import autoclass
from kivy.logger import Logger
from pythonforandroid.recipes.android.src.android.permissions import request_permissions, Permission, check_permission
import sys

KV = '''
#:import kivy kivy
#:import win kivy.core.window
<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "data/logo/kivy-icon-256.png"

    MDLabel:
        text: "TenderBot"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "kivydevelopment@gmail.com"
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:

        MDList:

            OneLineListItem:
                text: "Starting page"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 1"
                    root.toolbar.title = "Starting page"

            OneLineListItem:
                text: "Analytics type"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 2"
                    root.toolbar.title = "Analytics type"
                    
            OneLineListItem:
                text: "Analytics result"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 3"
                    root.toolbar.title = "Analytics result"
                    
            OneLineListItem:
                text: "About page"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 4"
                    root.toolbar.title = "About page"


Screen:

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        size_hint: 1, 0.1
        elevation: 10
        title: "Starting page"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    NavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager

            Screen:
                name: "scr 1"

                MDLabel:
                    text: "To start an analytics, please, choose a xlxs/csv file"
                    halign: "center"
                    
                MDRoundFlatIconButton:
                    text: "Open manager"
                    icon: "folder"
                    pos_hint: {'center_x': .5, 'center_y': .6}
                    on_release: app.file_manager_open()
                                
                    
                MDLabel:
                    text: ""
                    id: file_path
                    halign: "center"
                    pos_hint: {'center_y': .2}

            Screen:
                id: choice_screen
                name: "scr 2"

                MDLabel:
                    text: "Choose an analytics that you want"
                    halign: "center"
                    pos_hint: {'center_y': .7}
                 
                MDRoundFlatIconButton:
                    id: btn_competitors
                    text: "Potential competitors"
                    icon: "folder"
                    pos_hint: {'center_x': .5, 'center_y': .6}
                    width: 200
                    on_release: app.winners()
                    
                MDRoundFlatIconButton:
                    id: btn_clients
                    text: "Potential client"
                    icon: "folder"
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    on_release: app.potential_clients()
                    
                MDLabel:
                    id: text_no_file
                    halign: "center"
                    text: 
                    pos_hint: {'center_y': .2}   

                
                
            Screen:
                name: "scr 3"
                id: result_screen
            
                BoxLayout:
                    size_hint: 1, 0.9
                    ScatterLayout:
                        id: box
                        on_size: self.center = win.Window.center
                        do_rotation: False
                        do_translation: False
                    
        
            Screen:
                name: "scr 4"

                MDLabel:
                    text: "This is TenderAnalytics Bot"
                    halign: "center"

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
                toolbar: toolbar
                           
'''


class ResultBox(BoxLayout):
    pass



class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    toolbar = ObjectProperty()



class Picture(Scatter):
    source = StringProperty(None)


class ImageWidget(Widget):
    pass

class MyButton(MDRectangleFlatButton, ScreenManager):
    def __init__(self, **kwargs):
        super(MyButton, self, ScreenManager).__init__(**kwargs)
        self.screen_manager = ScreenManager

    def on_release(self):
        self.screen_manager.switch_to(self.ids.result)


class TenderBot(MDApp):


    selection = ListProperty([])

    graph = ObjectProperty()

    clients = ObjectProperty()

    def build(self):
        return Builder.load_string(KV)

    def file_manager_open(self):

        if(sys.platform == "linux"):
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, ])
            # For requesting permission you can pass a list with all the permissions you need
            if (check_permission('android.permission.WRITE_EXTERNAL_STORAGE')):
                filechooser.open_file(on_selection=self.handle_selection,
                                      title="Pick a CSV file",
                                      filters=[("*.csv")])
        else:
            filechooser.open_file(on_selection=self.handle_selection,
                                  title="Pick a CSV file",
                                  filters=[("*.csv")])

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        #self.root.ids.file_path.text = str(self.selection)


        self.root.ids.file_path.text = 'Opened file:' + "\n" + str(self.path_leaf(self.selection[0]))

        self.root.ids.text_no_file.text = ''


    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)


    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def winners(self):

        if self.clients is not None:
            self.root.ids.result_screen.remove_widget(self.clients)


        if self.selection:

            #Reading csv file
            df = pd.read_csv(self.selection[0])


            df['Победитель1'].value_counts()[df['Победитель1'].value_counts() >= 2].plot.barh()


            #plt.subplots_adjust(left=0.5)

            #plt.tight_layout()


            plt.savefig("image.png", bbox_inches='tight', dpi=150)

            #self.root.ids.box.add_widget(self.graph)

            #scatter = Picture(source='image.png')

            image = AsyncImage(source='image.png', size_hint=(1, 0.9))

            self.graph = image

            self.root.ids.box.add_widget(image)

            btn = MDRectangleFlatButton(text='Go to result screen',
                                        pos_hint={'center_x': .5, 'center_y': .4})

            btn.bind(on_press=self.switch)

            self.root.ids.choice_screen.add_widget(btn)

        else:
            self.root.ids.text_no_file.text = "No csv file selected, please, " \
                                              "select csv file"

    def switch(self, instance):
        screen_manager = self.root.ids.screen_manager

        self.root.ids.toolbar.title = 'Analytics result'

        screen_manager.current = "scr 3"

    def potential_clients(self):

        if self.selection:

            if self.graph is not None:
                self.root.ids.box.remove_widget(self.graph)

            df = pd.read_csv(self.selection[0])

            df['Дата'] = pd.to_datetime(df['Дата'])

            btn = MDRectangleFlatButton(text='Go to result screen',
                                        pos_hint={'center_x': .5, 'center_y': .4})



            btn.bind(on_press=self.switch)

            self.root.ids.choice_screen.add_widget(btn)

            sr = df[df['Дата'].dt.year == 2018]
            sr1 = df[df['Дата'].dt.year == 2019]

            srr = sr[['Наименование']]
            srr1 = sr1[['Наименование']]

            ch = srr.values.tolist()
            ch1 = srr1.values.tolist()

            for name in ch:
                df.drop(df[df['Наименование'] == name[0]].index, inplace=True)

            for name in ch1:
                df.drop(df[df['Наименование'] == name[0]].index, inplace=True)

            abc = df['Наименование'].tolist()

            s = set(abc)

            text = 'Список потенциальных заказчиков:'

            for name in s:
                text += '\n\n' + name + ","

            # self.root.ids.result_text.text = text

            self.clients = MDLabel(text=text,
                                   halign='center')

            self.root.ids.result_screen.add_widget(self.clients)

            print(self.clients.text)

        else:
            self.root.ids.text_no_file.text = "No csv file selected, please, " \
                                              "select csv file"


TenderBot().run()