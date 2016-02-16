#!/usr/bin/env python

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.vkeyboard import VKeyboard


class KeyPadScreen(Screen):
    """ Screen containing keypad...
    """
    userInput = ObjectProperty()
    userAction = ObjectProperty()
    exit=None

    def __init__(self, **kwargs):
        super(KeyPadScreen, self).__init__(**kwargs)
        global kb
        kb = Window.request_keyboard(self._keyboard_close, self)
        if kb.widget:
            # If the current configuration supports Virtual Keyboards, this
            # widget will be a kivy.uix.vkeyboard.VKeyboard instance.
            self._keyboard = kb.widget
            self._keyboard.layout = "phone.json"
        else:
            self._keyboard = kb
        self._keyboard.bind(on_key_down=self.key_down, on_key_up=self.key_up)

    def _keyboard_close(self, *args):
        """ The active keyboard is being closed. """
        print "_keyboard_close"
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.key_down)
            self._keyboard.unbind(on_key_up=self.key_up)
            self._keyboard = None

    def key_down(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard down events.
        Note that this only fires for entries that return null for
        <text to put when the key is pressed>."""
        print u"Key pressed - {} {} {}".format(keycode, text, modifiers)
        self.userAction.text = u"{0} down".format(text)

    def key_up(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard up events. """
        print u"Key released - {} {} {}".format(keycode, text, modifiers)
        self.userAction.text = u"{0} up".format(text)

    def exit():
        print "Exiting..."
        

class KeyPadApp(App):
    sm = None
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(KeyPadScreen(name="keypad"))
        self.sm.current= "keypad"
        return self.sm

if __name__ == '__main__':
    KeyPadApp().run()
