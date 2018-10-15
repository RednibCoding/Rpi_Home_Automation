from kivy.uix.button import Button

class RfButton(Button):
    '''RfButton class'''
    
    def __init__(self, switch_code, **kwargs):
        super().__init__(**kwargs)
        self.switch_code = switch_code
        self.on_press = self.click

    def click(self):
        '''Click Event of button'''
        # TODO: Send code
        print(self.switch_code)

class WifiButton(Button):
    pass
