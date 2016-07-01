import json


class FileMaster(object):
    def __init__(self):
        pass

    def _load_file(self, file: str) -> str:
        with open(file) as data:
            read_data = data.read()

        return read_data

    def interpret_json_from_string(self, string: str) -> object:
        return json.loads(string)

    def load_traits(self):
        pass

    def load_skills(self):
        pass

    def load_colonies(self):
        pass

    def load_structures(self):
        pass

    def load_colonists(self):
        pass
