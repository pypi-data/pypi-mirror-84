class GameUnitError(Exception):
    def __init__(self,msg='',code=000):
        super().__init__(msg)
        self.padding = '~'*50+'\n'
        self.error_msg = msg


class HealthMeterException(GameUnitError):
    def __init__(self,msg=''):
        super().__init__(msg)
        self.error_msg = (self.padding + msg + '\n' + self.padding)
