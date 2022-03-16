from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty


class MyTextInput(TextInput):
    max_characters = NumericProperty(0)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) + 1 > self.max_characters and self.max_characters \
                > 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)



class MyApp(App):
    def build(self):
        return MyTextInput(max_characters=4)



if __name__ == '__main__':
    MyApp().run()