from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty
import re

class MyTextInput(TextInput):
    max_characters = 6
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 2)
            )
        return super().insert_text(s, from_undo=from_undo)



class MyApp(App):
    def build(self):
        return MyTextInput()



if __name__ == '__main__':
    MyApp().run()