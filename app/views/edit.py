from logging import getLogger
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanelItem


class EditView:
    '''Contains all functions for EditView's buttons'''

    def __init__(self, app):
        '''
        app - The Instance of the class creating this one
        '''
        self.log = getLogger()
        self.app = app
        #
        self.tpi = TabbedPanelItem(text="Edit")

        # Add functions
        self.tpi.reload = self.reload
        self.tpi.create = self.create

        self.build_edit_tab()

    def build_edit_tab(self):
        '''
        Build the tab where the user is able to select the button to edit

        '''
        # Clear
        self.tpi.clear_widgets()

        # ScrollView
        sv = ScrollView()
        self.tpi.add_widget(sv)

        # FloatLayout
        fl = FloatLayout()
        sv.add_widget(fl)

        # New button
        btn_new = Button(
            text='NEW', size_hint=(None, None),
            size=(50, 100), pos=(10, 10),
            id='btn_new', on_press=self.edit_button
        )
        fl.add_widget(btn_new)

        # Add existing buttons
        pos_x = 50
        pos_y = 50
        button_size = (20, 60)
        for button_key in self.app.cfg['Buttons']:
            buttoncfg = self.app.cfg['Buttons'][button_key]
            if buttoncfg['tab'] == 'buttons':
                btn = Button()
                btn.text = buttoncfg['text']
                btn.size_hint = (None, None)
                btn.pos = (pos_x, pos_y)
                btn.size = button_size
                fl.add_widget(btn)
                if pos_x == 50:
                    pos_x = 120
                else:
                    pos_x = 50
                    pos_y += 50


    # <<<<< Button fuctions >>>>>
    def edit_button(self, button):
        self.tpi.clear_widgets()
        if button.id == 'btn_new':
            self.edit_view = Builder.load_file('views/edit_view.kv')
            self.edit_view.reload = self.reload
            self.edit_view.create = self.create
            self.edit_view.back = self.build_edit_tab
            self.tpi.add_widget(self.edit_view)

    def reload(self):
        '''Function for reload button'''
        self.app.build_view()

    def create(self):
        ''''''
        props = self.edit_view.ids
        # Reset error_label
        props['error_label'].text = ''
        props['error_label'].opacity = 0

        # Check if all values can be converted to in
        error = False
        for prop in ('button_x', 'button_y'):
            try:
                int(props[prop].text)
            except ValueError:
                props['error_label'].text = 'Values X and Y have to be numbers'
                props['error_label'].opacity = 100
                error = True

        if not error:
            self.build_edit_tab()

