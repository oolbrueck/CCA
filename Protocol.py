from datetime import datetime


#Die Klasse Protocol dient zum Sammen relervanter Versuchsdaten
class Protocol:
    def __init__(self):
        self.time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.program_parameters = {}
protocol_obj = Protocol()