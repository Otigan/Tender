from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
from kivy.factory import Factory
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import ObjectProperty
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import pandas as pd
import matplotlib.pyplot as plt


class CustomLayout(BoxLayout):

    def show(self):
        df = pd.read_csv('csv.csv')
        winners1 = df['Победитель1'].value_counts().plot.bar()
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))



class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Tender analytics"
        self.theme_cls.primary_palette = "Blue"
        super().__init__(**kwargs)

    def build(self):
        return CustomLayout()




if __name__ == "__main__":
    MainApp().run()