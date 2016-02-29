#!/usr/bin/env python

import ipdb

from kivy.app import App
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.animation import Animation


class PhonePad(VKeyboard):

    def draw_keys(self):
        """ This is to fix what I would call a bug in the drawing
        of the keyboards. It computes the font size as the width/46
        without regard to how many keys there are..."""
        super(PhonePad, self).draw_keys()
        for i in self.walk():
            if isinstance(i, Label):
                i.font_size=self.font_size
                if i.text == u"\u21a9":
                    self.enterKey = i


class KeyPadScreen(FloatLayout):
    """ Layout that has keypad & other widgets"""
    
    userInput = ObjectProperty()
    feedback = ObjectProperty()
    userPrompt = ObjectProperty()
    userInputText=""

    def __init__(self, **kwargs):
        super(KeyPadScreen, self).__init__(**kwargs)
        self.userInputText=""
        self._keyboard = PhonePad()
        self._keyboard.bind(on_key_down=self.key_down, on_key_up=self.key_up)
        self._keyboard.layout = "phone.json"
        self._keyboard.size=(380,470)
        self._keyboard.pos=(410,5)
        self._keyboard.key_margin=([10, 10, 10, 10])
        self._keyboard.font_size=24
        self.add_widget(self._keyboard)
        self.userInputText=""

    def key_down(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard down events.
        Note that this only fires for entries that return null for
        <text to put when the key is pressed>."""
        #print u"Key pressed - {} {} {}".format(keycode, text, modifiers)
        if keycode=='backspace' and len(self.userInput.text)>0:
            self.userInputText = self.userInputText[:-1]
        elif keycode=='return' and len(self.userInput.text)>0:
            self.processNumber(self.userInputText)
            self.userInputText = ""
        self.userInput.text = self.userInputText
    
        
    def key_up(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard up events. """
        #print u"Key released - {} {} {}".format(keycode, text, modifiers)
        if keycode in ['backspace','return']:
            pass
        else:
            if len(self.userInputText) < 7:
                self.userInputText += text
                self.userInput.text = self.userInputText
            if len(self.userInputText) == 4:
                animation = Animation(color=(1,0,0,1), t='in_out_quad', duration=0.5)
                animation += Animation(color=(1,1,1,1), t='in_out_quad', duration=0.5)
                animation += Animation(color=(1,0,0,1), t='in_out_quad', duration=0.5)
                animation += Animation(color=(1,1,1,1), t='in_out_quad', duration=0.5)
                animation.start(self._keyboard.enterKey)
                
                
    def clearFeedback(self, dt):
        self.feedback.text = "..."
        self.feedback.canvas.opacity  = 0;
        
    def processNumber(self, num):
        if len(num) != 4 or not num.isnumeric():
            self.feedback.text = "Not a valid extension."
        else:
            self.feedback.text = "Drink on {}".format(num)
        self.feedback.canvas.opacity  = 1;
        #Clock.schedule_once(self.clearFeedback, 3)
        animation = Animation(opacity=0, t='in_out_quad', duration=3)
        animation.start(self.feedback.canvas)

    def debugme(self):
        ipdb.set_trace()
        

class KeyPadApp(App):
    kps = None
    def build(self):
        self.root = FloatLayout()
        self.kps=KeyPadScreen()
        self.root.add_widget(self.kps)
        return self.root
        #
        

if __name__ == '__main__':
    global app
    app=KeyPadApp()
    app.run()
