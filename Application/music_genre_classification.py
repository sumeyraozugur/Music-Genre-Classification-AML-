from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
import os
from classification import Classifier

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

dir_path = os.path.dirname(os.path.realpath(__file__))

Builder.load_string("""
<MenuScreen>:
    id: my_widget
    BoxLayout:
        Button
            text: "Select"
            on_release: my_widget.open(filechooser.path, filechooser.selection)
        FileChooserListView:
            id: filechooser
            path:"./"
            on_selection: my_widget.selected(filechooser.selection)

<SettingsScreen>:
    id: settings
    BoxLayout:
        orientation : 'vertical'
        canvas.before:
            Color:
                rgba: .5, .5, .5, 1
            Line:
                width: 2
                rectangle: self.x, self.y, self.width, self.height
        BoxLayout:
            orientation : 'horizontal'
            size_hint: 1, 0.25
            canvas.before:
                Color:
                    rgba: .5, .5, .5, 1
                Line:
                    width: 2
                    rectangle: self.x, self.y, self.width, self.height
            Label:
                text: settings.filepath
                text_size: self.size
                color: 1,1,1,1
                halign: 'center'
                valign: 'middle'   
        
        BoxLayout:
            orientation : 'horizontal'
            size_hint: 1, 0.5
            canvas.before:
                Color:
                    rgba: .5, .5, .5, 1
                Line:
                    width: 1
                    rectangle: self.x, self.y, self.width, self.height
            Button:  
                text: "K Nearest Neighbor "
                background_color: 0.1, 0.5, 0.6, 1
                size_hint: 0.25, 1
                pos_hint: {"x":0, "top":1}   
                on_press: settings.classifyKnn()
            
                    
            Button:  
                text:"Support Vector Machine"
                background_color: 0.4, 0.5, 0.6, 1
                size_hint: 0.25, 1
                pos_hint: {"x":1, "top":1}  
                on_press: settings.classifySvm()
            
            Button:  
                text:"Neural Network"
                background_color: 0, 0, 1, 1
                size_hint: 0.25, 1
                pos_hint: {"x":2, "top":1}  
                on_press: settings.classifyNn()
            
            Button:  
                text:"Naive Bayes"
                background_color: 1, 0, 1, 1
                size_hint: 0.25, 1
                pos_hint: {"x":3, "top":1}  
                on_press: settings.classifyNb()

        BoxLayout:
            orientation : 'horizontal'
            canvas.before:
                Color:
                    rgba: .5, .5, .5, 1
                Line:
                    width: 2
                    rectangle: self.x, self.y, self.width, self.height
            Label:
                text: settings.hiphop
                text_size: self.size
                color: 1,1,1,1
                halign: 'center'
                valign: 'middle'  
            Label:
                text: settings.jazz
                text_size: self.size
                color: 1,1,1,1
                halign: 'center'
                valign: 'middle' 
            Label:
                text: settings.metal
                text_size: self.size
                color: 1,1,1,1
                halign: 'center'
                valign: 'middle' 
            Label:
                text: settings.pop
                text_size: self.size
                color: 1,1,1,1
                halign: 'center'
                valign: 'middle' 
            Label:
                text: settings.rock
                text_size: self.size
                color: 1,1,1,1
                halign: 'center'
                valign: 'middle' 
             
        
        BoxLayout:
            orientation : 'vertical'
            size_hint: 1, 0.25
            canvas.before:
                Color:
                    rgba: .5, .5, .5, 1
                Line:
                    width: 2
                    rectangle: self.x, self.y, self.width, self.height
            Button:
                text: 'Back to File Choose'
                size_hint: 0.25, 0.25
                pos_hint: {"x":0.37, "top":1} 
                on_press: root.manager.current = 'menu'
""")

# Declare both screens

filePath=""

class MenuScreen(Screen):
    def selected(self, filename):
        pass
    
    def open(self, path, filename):
        global filePath
        filePath = filename[0]
        sm.current = 'settings'

class SettingsScreen(Screen):
    filepath = StringProperty()
    hiphop = StringProperty()
    jazz = StringProperty()
    rock = StringProperty()
    pop = StringProperty()
    metal = StringProperty()
    classifier = object
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.filepath=""
        self.classifier = Classifier()
    
    def on_enter(self):
        global filePath
        self.filepath=os.path.basename(filePath)
        self.hiphop = "Hiphop"
        self.jazz = "Jazz"
        self.metal = "Metal"
        self.pop = "Pop"
        self.rock = "Rock"
        self.classifier.setMusic(filePath)
        print("Music Set")

    def classifyKnn(self):
        results = self.classifier.kNN()
        self.hiphop = "Hiphop: %s " % results[0]
        self.jazz = "Jazz: %s " % results[1]
        self.metal = "Metal: %s " % results[2]
        self.pop = "Pop: %s " % results[3]
        self.rock = "Rock: %s " % results[4]

    def classifySvm(self):
        results = self.classifier.svma()
        self.hiphop = "Hiphop: %s " % results[0]
        self.jazz = "Jazz: %s " % results[1]
        self.metal = "Metal: %s " % results[2]
        self.pop = "Pop: %s " % results[3]
        self.rock = "Rock: %s " % results[4]


    def classifyNn(self):
        results = self.classifier.nn()
        self.hiphop = "Hiphop: %s " % results[0]
        self.jazz = "Jazz: %s " % results[1]
        self.metal = "Metal: %s " % results[2]
        self.pop = "Pop: %s " % results[3]
        self.rock = "Rock: %s " % results[4]


    def classifyNb(self):
        results = self.classifier.bnb()
        self.hiphop = "Hiphop: %s " % results[0]
        self.jazz = "Jazz: %s " % results[1]
        self.metal = "Metal: %s " % results[2]
        self.pop = "Pop: %s " % results[3]
        self.rock = "Rock: %s " % results[4]


    


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()