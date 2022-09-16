from processor import Processor

class Channel(Processor):
    default_props = {}
    default_state = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)