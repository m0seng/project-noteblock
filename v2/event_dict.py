from collections import UserDict
from event import Event

# modifying mutables within a dictionary does not go through the dict's __setitem__
# this code is therefore not very useful

class EventDict(UserDict):
    def __init__(self, initialdata, event: Event, **kwargs):
        self.event = event
        super().__init__(initialdata, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.event.trigger()

def main():
    test_event = Event()
    test_event.add_listener(lambda: print("event called"))
    test_dict = EventDict({"a": [1, 2, 3], "b": [2, 3, 4]}, test_event)
    
    print("test starts here")
    for key, value in test_dict.items():
        temp = test_dict[key]
        temp.append(6)
    print("test ends here")
    print(test_dict)

if __name__ == "__main__":
    main()