from os.path import join

from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
import sys

import os
import pandas as pd
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from plyer import filechooser

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
                    pos_hint: {'center_x': 1, 'center_y': .2}

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
                    
                MDLabel:
                    id: text_no_file
                    text: 
                    pos_hint: {'center_x': 1, 'center_y': .4}   
                
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

    selection = ListProperty([])

    def build(self):
        return Builder.load_string(KV)

    def file_manager_open(self):
        filechooser.open_file(on_selection=self.handle_selection,
                              title="Pick a CSV file",
                              filters=[("*.csv")])

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        self.root.ids.file_path.text = str(self.selection)

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

        if self.selection:
            self.root.ids.text_no_file.text = ''
            df = pd.read_csv(self.selection[0])
            winners1 = df['Победитель1'].value_counts().plot.bar()
            self.root.ids.box_graph.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        else:
            self.root.ids.text_no_file.text = "No csv file selected,please," \
                                              "select csv file"


TestNavigationDrawer().run()