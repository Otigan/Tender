from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton

import pandas as pd
import matplotlib.pyplot as plt

Builder.load_string(
    """
<ExampleButtons@BoxLayout>:
    orientation: "vertical"

    MDToolbar:
        id: toolbar
        title: app.title
        md_bg_color: app.theme_cls.primary_color
        background_palette: "Primary"
        elevation: 10


    ScrollView:
        size_hint_x: None
        width: box.width
        pos_hint: {"center_x": .5}
        bar_width: 0

        BoxLayout:
            id: box
            padding: dp(10)
            size_hint: None, None
            size: self.minimum_size
            spacing: dp(10)
            orientation: "vertical"
            pos_hint: {"center_x": .5}

            MDRectangleFlatButton:
                text: "Winners 1"
                opposite_colors: True
                elevation_normal: 8 
                on_release: app.show()   
                
"""
)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Tender analytics"
        self.theme_cls.primary_palette = "Blue"
        super().__init__(**kwargs)

    def build(self):
        self.root = Factory.ExampleButtons()

    def show(self):
        df = pd.read_csv('csv.csv')
        winners1 = df['Победитель1'].value_counts().plot.bar()
        plt.show()


if __name__ == "__main__":
    MainApp().run()