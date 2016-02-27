#!/usr/bin/env python

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.label import Label
from kivy.lang import Builder


class PhonePad(VKeyboard):
    def draw_keys(self):
        """ This is to fix what I would call a bug in the drawing
        of the keyboards. It computes the font size as the width/46
        without regard to how many keys there are..."""
        super(PhonePad, self).draw_keys()
        for i in self.walk():
            if isinstance(i, Label):
                i.font_size=self.font_size


class KeyPadScreen(FloatLayout):
    """ Layout that has keypad & other widgets"""
    
    userInput = ObjectProperty()
    feedback = ObjectProperty()
    userInputText=""

    def __init__(self, **kwargs):
        super(KeyPadScreen, self).__init__(**kwargs)
        self.userInputText=""
        self._keyboard = PhonePad()
        self._keyboard.bind(on_key_down=self.key_down, on_key_up=self.key_up)
        self._keyboard.layout = "phone.json"
        self._keyboard.size=(380,430)
        self._keyboard.pos=(410,5)
        self._keyboard.key_margin=([10, 10, 10, 10])
        self._keyboard.font_size=24
        self.add_widget(self._keyboard)
        self.userInputText=""
        
    def key_down(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard down events.
        Note that this only fires for entries that return null for
        <text to put when the key is pressed>."""
        print u"Key pressed - {} {} {}".format(keycode, text, modifiers)
        if keycode=='backspace' and len(self.userInput.text)>0:
            self.userInputText = self.userInputText[:-1]
        elif keycode=='return' and len(self.userInput.text)>0:
            self.processNumber(self.userInputText)
            self.userInputText = ""
        self.userInput.text = self.userInputText

        
    def key_up(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard up events. """
        print u"Key released - {} {} {}".format(keycode, text, modifiers)
        if keycode in ['backspace','return']:
            pass
        else:
            if len(self.userInputText) < 40:
                self.userInputText += text
                self.userInput.text = self.userInputText
                
    def processNumber(self, num):
        self.feedback.text = "Drink on {}".format(num)
        # set timer to erase text in 3 seconds...
        pass
        

class KeyPadApp(App):
    kps = None
    def build(self):
        self.root = FloatLayout()
        self.kps=KeyPadScreen()
        self.root.add_widget(self.kps)
        return self.root

if __name__ == '__main__':
    app=KeyPadApp()
    app.run()
