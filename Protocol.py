from datetime import datetime


#Die Klasse Protocol dient zum Sammen relervanter Versuchsdaten
class Protocol:
    def __init__(self):
        self.time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.program_parameters = {}

    def __str__(self):
        attributes = ', '.join(f'{key}={value}' for key, value in vars(self).items())
        return f'{self.__class__.__name__}({attributes})'


protocol_obj = Protocol()