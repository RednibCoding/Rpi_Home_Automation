from logging import getLogger

from kivy.uix.button import Button


class DeviceButton(Button):
    '''
    Gets an dict and sets the properties of the button with it.
    Keys have to have same name as the property
    '''
    def __init__(self, **options):
        super().__init__()
        self.log = getLogger()
        for key in options:
            setattr(self, key, options[key])

class RfButton(DeviceButton):
    '''RfButton class'''

    def __init__(self, **options):
        self.switch_code = options['code']
        del(options['code'])
        super().__init__(**options)
        self.on_press = self.click

    def click(self):
        '''Click Event of button'''
        # TODO: Send code
        self.log.info(self.switch_code)

class WifiButton(Button):
    pass
