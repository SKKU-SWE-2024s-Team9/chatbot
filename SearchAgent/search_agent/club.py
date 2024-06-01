import json
import re

class Club:
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

class ClubCollection:
    def __init__(self):
        self.clubs = []

    def add_club(self, club):
        if isinstance(club, Club):
            self.clubs.append(club)
        else:
            raise TypeError("Only instances of Club can be added")

    def to_json(self):
        clubs_dict = [club.to_dict() for club in self.clubs]
        return json.dumps(clubs_dict, indent=4)

    @classmethod
    def from_string(cls, string):
        pattern = re.compile(r'Name: (.*?)\nDescription: (.*?)\nReason to like it: (.*?)(?=\nName:|\Z)', re.DOTALL)
        matches = pattern.findall(string)

        if not matches:
            return string

        collection = cls()
        for match in matches:
            name, description, reason_to_like = match
            club = Club(name.strip(), description.strip(), reason_to_like.strip())
            collection.add_club(club)

        return collection
