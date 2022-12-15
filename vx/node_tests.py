from node import Node
from node_events import NodeEventBus
from node_actions import AddChildAction, RemoveChildAction, SetPropertyAction
from undo_manager import UndoManager
from node_editor import NodeEditor

def main():
    uman = UndoManager()
    event_bus = NodeEventBus()
    ed = NodeEditor(uman, event_bus)

    root = Node()
    ed.set_property(root, "bruh", "lmao")
    ed.set_property(root, "wheeze", "hehehe ha")

    child = Node()
    ed.set_property(child, "ligma", "balls")
    ed.set_property(child, "please", "work")

    ed.add_child(root, child)

    print(root.to_string())

if __name__ == "__main__":
    main()