import requests
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.image import Image as CoreImage
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from io import BytesIO

class MyApp(App):
    loading = BooleanProperty(False)

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.background_color = (0.9, 0.9, 0.9, 1)
        self.layout.canvas.before.add(Color(rgb=self.background_color))
        self.layout.canvas.before.add(Rectangle(size=self.layout.size, pos=self.layout.pos))

        self.url_input = TextInput(
            hint_text='Enter the URL',
            size_hint=(1, None),
            height=50,
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.url_input)

        self.paste_button = Button(
            text='Paste',
            size_hint=(1, None),
            height=50,
            background_color=(0.5, 0.7, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.paste_button.bind(on_press=self.paste_from_clipboard)
        self.layout.add_widget(self.paste_button)
        
        self.button = Button(
            text='Fetch Image',
            size_hint=(1, None),
            height=50,
            background_color=(0.5, 0.7, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.button.bind(on_press=self.fetch_image)
        self.layout.add_widget(self.button)

        self.error_label = Label(
            text='',
            size_hint=(1, None),
            height=30,
            color=(1, 0, 0, 1)
        )
        self.layout.add_widget(self.error_label)
        
        self.img_widget = Image(
            allow_stretch=True,
            keep_ratio=True
        )
        self.layout.add_widget(self.img_widget)

        return self.layout

    def fetch_image(self, instance):
        if not self.loading:
            self.loading = True
            self.error_label.text = ''
            api_url = f"https://api.qewertyy.dev/webss?url={self.url_input.text}"
            response = requests.get(api_url)
            
            if response.status_code == 200:
                try:
                    image_data = BytesIO(response.content)
                    core_image = CoreImage(image_data, ext="png")
                    self.img_widget.texture = core_image.texture
                    self.error_label.text = ''
                except Exception as e:
                    self.error_label.text = f"Error loading image: {str(e)}"
            else:
                self.img_widget.texture = None
                self.error_label.text = f"Failed to retrieve image. Status code: {response.status_code}"

            self.loading = False

    def paste_from_clipboard(self, instance):
        self.url_input.text = Clipboard.paste()

if __name__ == '__main__':
    MyApp().run()
