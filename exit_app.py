from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

KV = '''
MDFloatLayout:

    MDLabel:
        text: "ВЫХОД"
        halign: 'center'
        pos_hint: {'center_x': .5, 'center_y': .5}  
'''


class Example(MDApp):
    dialog = None

    def build(self):
        Window.bind(on_keyboard=self.key_input)
        return Builder.load_string(KV)

    def show_exit_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Выйти из приложения?",
                buttons=[
                    MDFlatButton(
                        text="НЕТ",
                        on_press=lambda x: self.close_dialog(),
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color),
                    MDFlatButton(
                        text="ДА",
                        on_press=lambda x: self.close_app(),
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color),
                ],
            )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()

    def close_app(self):
        self.stop()

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            self.show_exit_dialog()
            return True
        else:
            return False


Example().run()
