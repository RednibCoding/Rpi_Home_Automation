from kivy.uix.tabbedpanel import TabbedPanelItem

class EditView(TabbedPanelItem):
    ''''Handels the Edit tabi'''

    def __init__(self, tpi):
        '''tpi - TabbedPanelItem'''
        self = tpi
        self.build()

    def build(self):
        '''Build view'''

