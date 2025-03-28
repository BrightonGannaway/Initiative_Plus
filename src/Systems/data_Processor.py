import constants

class Data_Processor:
    def __init__(self):
        pass

    def get_Expected_Type(self, header, item):
        if header == "Name" or header == "Conditions":
            return item.text()
        try:
            return int(item.text())
        except ValueError:
            return None
        
    