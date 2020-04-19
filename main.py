import matplotlib.pyplot as plt
import pandas as pd
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel

#This special KV language, that works like CSS, defining style for widgets
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
        text: "Tender Bot"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "sample_email@gmail.com"
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
                    id: greetings
                    text: ""
                    halign: "center"
                        
                MDLabel:
                    text: ""
                    id: file_path
                    halign: "center"
                    pos_hint: {'center_y': .3}

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
                    size_hint: 1, 0.7
                    ScatterLayout:
                        id: box
                        on_size: self.center = win.Window.center
                        do_rotation: False
                        do_translation: False
                    
        

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
                toolbar: toolbar
                           
'''

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()
    toolbar = ObjectProperty()

class TenderBot(MDApp):

    #This lines are class variables
    selection = ListProperty([])

    graph = ObjectProperty()

    clients = ObjectProperty()

    check_graph = ObjectProperty()

    check_clients = ObjectProperty()


    def build(self):
        return Builder.load_string(KV)

    #This method runs when app starts
    def on_start(self):
        #Greeting string that displayed on start screen
        self.root.ids.greetings.text = "Hi! This is tender analytics bot" + "\n\n" \
                                       + "At the moment app has two type of analytics:" \
                                       + "\n" + "1.Show potential competitors" + "\n" + "2.Show potential clients"

        #Filename, that currently loaded
        self.root.ids.file_path.text = "File loaded: csv.csv"

        #This variables used for tracking is there any result(plot of potential competitors
        # or list of potential clients) on result screen
        self.check_clients = False
        self.check_graph = False

    # This method runs when user clicks on corresponding button
    # Method adds scalabe image of plot to the screen
    def winners(self):
        # Checking if there are list of potential client on the result screent
        # and if there are, we are deleting this list from screen so that we can place plot on this screen
        if self.clients is not None:
            # Deleting list of potential clients
            self.root.ids.result_screen.remove_widget(self.clients)

            # Reseting flag
            self.check_clients = False

        # Checking if result screen already has a plot, and if not we are adding it
        if self.check_graph == False:

            # Dataframe that we get from .csv file
            df = pd.read_csv('csv.csv')

            # Counting winners from first column
            df1 = df['Победитель1'].value_counts()[df['Победитель1'].value_counts() >= 2]

            # Counting winners from second column
            df2 = df['Победитель2'].value_counts()[df['Победитель2'].value_counts() >= 2]

            # Adding dataframes into one dataframe
            frames = [df1, df2]
            df3 = pd.concat(frames)

            # Creating horizontal bar plot
            df3.plot.barh()

            plt.subplots_adjust(left=0.5)

            # Saving plot into image
            plt.savefig("image.png", bbox_inches='tight', dpi=150)

            # Creating image widget
            image = AsyncImage(source='image.png', )

            #Adding image to class variable
            self.graph = image

            self.root.ids.box.add_widget(image)

            # Adding button "Go to result"
            btn = MDRectangleFlatButton(text='Go to result screen',
                                        pos_hint={'center_x': .5, 'center_y': .4})

            # Binding button with method, which allows us go to result screen
            btn.bind(on_press=self.switch)

            # Adding button to screen
            self.root.ids.choice_screen.add_widget(btn)

            # Setting flag
            self.check_graph = True


    def switch(self, instance):

        # Getting screen manager, which do all work with screens
        screen_manager = self.root.ids.screen_manager

        self.root.ids.toolbar.title = 'Analytics result'

        # Go to result screen
        screen_manager.current = "scr 3"


    def potential_clients(self):
        # Checking if there are plot on result screen
        if self.graph is not None:
            self.root.ids.box.remove_widget(self.graph)

            # Reseting flag
            self.check_graph = False

        # Check if result screen already has clients list
        if self.check_clients == False:

            # Getting dataframe from .csv file
            df = pd.read_csv('csv.csv')

            # Formating data to object
            df['Дата'] = pd.to_datetime(df['Дата'])

            # Adding button, that leads to result screen
            btn = MDRectangleFlatButton(text='Go to result screen',
                                        pos_hint={'center_x': .5, 'center_y': .4})

            # Binding button with method
            btn.bind(on_press=self.switch)

            # Adding button
            self.root.ids.choice_screen.add_widget(btn)

            # Getting dataframe, with clients that made purchases in 2018 and 2019 years
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

            self.check_clients = True


TenderBot().run()