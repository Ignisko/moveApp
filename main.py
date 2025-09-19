from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem

KV = '''
MDBoxLayout:
    orientation: "vertical"
    MDToolbar:
        title: "Training Planner"
    MDTabs:
        id: tabs
        on_tab_switch: app.switch_tab(*args)
        Tab:
            text: "Gym"
            MDBoxLayout:
                orientation: "vertical"
                MDScrollView:
                    MDList:
                        id: gym_list
                MDBoxLayout:
                    size_hint_y: None
                    height: "50dp"
                    MDFlatButton:
                        text: "Add Exercise"
                        on_release: app.add_exercise()
        Tab:
            text: "Capoeira"
            MDBoxLayout:
                orientation: "vertical"
                MDScrollView:
                    MDList:
                        id: capo_list
                MDBoxLayout:
                    size_hint_y: None
                    height: "50dp"
                    MDFlatButton:
                        text: "Add Move"
                        on_release: app.add_exercise()
'''

class PlannerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plans = {"Gym": [], "Capoeira": []}
        self.current_tab = "Gym"

    def build(self):
        return Builder.load_string(KV)

    def switch_tab(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.current_tab = tab_text

    def add_exercise(self):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivymd.uix.button import MDFlatButton

        box = BoxLayout(orientation='vertical', spacing=10)
        name = TextInput(hint_text="Exercise/Move name", multiline=False)
        duration = TextInput(hint_text="Duration (min)", multiline=False, input_filter='int')
        rest = TextInput(hint_text="Rest after (min)", multiline=False, input_filter='int')
        box.add_widget(name)
        box.add_widget(duration)
        box.add_widget(rest)

        def save(instance):
            if name.text and duration.text and rest.text:
                self.plans[self.current_tab].append({
                    "name": name.text,
                    "duration": int(duration.text),
                    "rest": int(rest.text)
                })
                self.update_display()
            popup.dismiss()

        popup = Popup(title="Add Exercise/Move", content=box,
                      size_hint=(0.8, 0.5), auto_dismiss=False)
        btn = MDFlatButton(text="Save", on_release=save)
        box.add_widget(btn)
        popup.open()

    def update_display(self):
        list_id = "gym_list" if self.current_tab == "Gym" else "capo_list"
        mdlist = self.root.ids[list_id]
        mdlist.clear_widgets()
        for ex in self.plans[self.current_tab]:
            mdlist.add_widget(OneLineListItem(
                text=f"{ex['name']} - {ex['duration']}min + rest {ex['rest']}min"))

PlannerApp().run()
