class Participant:
    def __init__(self, id: int, attributes: list[str], desired_attributes: list[str]):
        self.id = id
        self.attributes = attributes
        self.desired_attributes = desired_attributes

    def __str__(self):
        return f"Participant(id={self.id}, attributes={self.attributes}, desired_attributes={self.desired_attributes})"

    __repr__ = __str__