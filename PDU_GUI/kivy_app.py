from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')

import os
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
import main

class multilaterationWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(multilaterationWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
             
        # Initialize image widget without an image if file doesn't exist
        initial_source = "multilateration.png" if os.path.exists("multilateration.png") else ""
        self.img = Image(source=initial_source, allow_stretch=True, keep_ratio=True)
        self.add_widget(self.img)

        Clock.schedule_interval(self.run_multilateration, 1.0)

    def update_image(self):
        # Check if the file exists, and update the image widget accordingly
        if os.path.exists("multilateration.png"):
            self.img.source = "multilateration.png"
            self.img.reload()
        else:
            self.img.source = ""
            self.img.reload()
            
    def run_multilateration(self, dt):
        # Run the main function from main.py, which generates and saves the plot
        main.main()

        # Update the image widget to display the new plot (if the file exists)
        self.update_image()

class multilaterationApp(App):
    def build(self):
        return multilaterationWidget()

if __name__ == '__main__':
    multilaterationApp().run()
