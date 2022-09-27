from .save_mixin import SaveMixin

class SavableGroup(SaveMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.savables: list[SaveMixin] = []

    def to_dict(self):
        return {
            "savables": savable.to_dict() for savable in self.savables
        }

    def from_dict(self, source):
        for saved_dict in source["savables"]:
            ... # TODO