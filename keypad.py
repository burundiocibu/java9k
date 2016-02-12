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
    displayLabel = ObjectProperty()

    def __init__(self, **kwargs):
        super(KeyPadScreen, self).__init__(**kwargs)
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
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.key_down)
            self._keyboard.unbind(on_key_up=self.key_up)
            self._keyboard = None

    def key_down(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard events. """
        print "Foo"
        print u"Key pressed - {0}".format(text)
        self.displayLabel.text = u"Key pressed - {0}".format(text)

    def key_up(self, keyboard, keycode, foo4, foo5):
        """ The callback function that catches keyboard events. """
        print "Bar"
        print u"Key released - {} {} {}".format(keycode, foo4, foo5)
        self.displayLabel.text += u" (up {0[1]})".format(keycode)


class KeyPadApp(App):
    sm = None
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(KeyPadScreen(name="keypad"))
        self.sm.current= "keypad"
        return self.sm

if __name__ == '__main__':
    KeyPadApp().run()