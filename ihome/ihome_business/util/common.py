from werkzeug.routing import BaseConverter

class ReConverter(BaseConverter):
    def __init__(self, url_map, regix):
        super().__init__(url_map)
        self.regix = regix
