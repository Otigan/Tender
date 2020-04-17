from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window

import pandas as pd
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

KV = '''
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
        text: "KivyMD library"
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

            OneLineListItem:
                text: "Analytics"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 2"
                    
            OneLineListItem:
                text: "About page"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 3"


Screen:

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "MDNavigationDrawer"
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
                    text: "Test"
                    id: file_path
                    pos_hint: {'center_x': .5, 'center_y': .3}

            Screen:
                name: "scr 2"

                MDLabel:
                    text: "Choose an analytics that you want"
                    halign: "center"
                 
                MDRoundFlatIconButton:
                    text: "Winners"
                    icon: "folder"
                    pos_hint: {'center_x': .5, 'center_y': .6}
                    on_release: app.winners()
                    
                BoxLayout:
                    id: box_graph
                    orientation: "vertical"
                    padding: dp(10)
                    size_hint: 1, 0.5
                    size: self.minimum_size
                    spacing: dp(10)
                    orientation: "vertical"
                    pos_hint: {"center_x": .5}
                
                    
            Screen:
                name: "scr 3"

                MDLabel:
                    text: "This is TenderAnalytics Bot"
                    halign: "center"

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
'''


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class TestNavigationDrawer(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            previous=True,
        )

    def build(self):
        return Builder.load_string(KV)

    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.root.ids.file_path.text = path
        self.exit_manager()
        toast(self.root.ids.file_path.text)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


    def winners(self):
        df = pd.read_csv('csv.csv')
        winners1 = df['Победитель1'].value_counts().plot.bar()
        self.root.ids.box_graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))

TestNavigationDrawer().run()