
from kivy.core.text import Label as CoreLabel
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget

my_label = CoreLabel()
my_label.text = 'hello'
# the label is usually not drawn until needed, so force it to draw.
my_label.refresh()
# Now access the texture of the label and use it wherever and
# however you may please.
hello_texture = my_label.texture


class MyApp(App):
    def build(self):
        return Button(text='Hello')


if __name__ == "__main__":
    MyApp().run()
