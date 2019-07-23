from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import community
import person

from random import seed

seed(a=12)

class Fam_Display(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.commune = community.Community().generate()
        self.cols = len(self.commune)

        for i, c in enumerate(self.commune):
            self.name = Label(text=c.full_name+" ("+str(c.age)+")\n\n")

            for r in c.relations:
                text = f"{r.full_name} {r.age}\n" \
                    f"{'-'*len(r.full_name)}\n" \
                    f"{c.relations[r]}\n\n"
                self.name.text += text
            self.name.halign = "center"
            self.box = BoxLayout()
            self.box.add_widget(self.name)
            self.add_widget(self.box)


class DisplayApp(App):
    def build(self):
        display = Fam_Display()
        return display



if __name__ == "__main__":
    DisplayApp().run()