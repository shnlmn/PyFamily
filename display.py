from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import community
import colorsys
import person

from random import seed

# seed(a=12)



class FamDisplay(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.commune = community.Community().generate()
        self.rel_col = community.Community().relation_color
        self.cols = len(self.commune)

        for i, c in enumerate(self.commune):
            self.name = []
            self.name.append(Label(text=c.full_name+" ("+str(c.age)+")\n\n", markup=True, halign="center"))

            for r in c.relations:
                text = f"[color={self.rel_col[c.relations[r]]}]{r.full_name} {r.age}\n" \
                    f"{'-'*len(r.full_name)}\n" \
                    f"{c.relations[r]}[/color]\n\n"
                self.name.append(Label(text=text, markup=True, halign="center"))

            self.box = BoxLayout(orientation="vertical")
            for w in self.name:
                self.box.add_widget(w)

            self.add_widget(self.box)


class DisplayApp(App):
    def build(self):
        display = FamDisplay()
        return display



if __name__ == "__main__":
    DisplayApp().run()