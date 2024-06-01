import json
import re

class Lab:
    def __init__(self, name, description, reason_to_like):
        self.name = name
        self.description = description
        self.reason_to_like = reason_to_like

    def to_dict(self):
        return {
            "Name": self.name,
            "Description": self.description,
            "Reason to like it": self.reason_to_like
        }

class LabCollection:
    def __init__(self):
        self.labs = []

    def add_lab(self, lab):
        if isinstance(lab, Lab):
            self.labs.append(lab)
        else:
            raise TypeError("Only instances of Lab can be added")

    def to_json(self):
        labs_dict = [lab.to_dict() for lab in self.labs]
        return json.dumps(labs_dict, indent=4)

    @classmethod
    def from_string(cls, string):
        pattern = re.compile(r'Name: (.*?)\nDescription: (.*?)\nReason to like it: (.*?)(?=\nName:|\Z)', re.DOTALL)
        matches = pattern.findall(string)

        if not matches:
            return string

        collection = cls()
        for match in matches:
            name, description, reason_to_like = match
            lab = Lab(name.strip(), description.strip(), reason_to_like.strip())
            collection.add_lab(lab)

        return collection
