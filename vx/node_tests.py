import json
from node import Node
from node_events import NodeEventBus
from node_actions import AddChildAction, RemoveChildAction, SetPropertyAction
from undo_manager import UndoManager
from node_editor import NodeEditor
from node_factory import NodeFactory

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

    sibling = Node()
    ed.set_property(sibling, "idk", "lol")
    ed.set_property(sibling, "who", "asked")

    grandchild = Node()
    ed.set_property(grandchild, "me", "when")
    ed.set_property(grandchild, "the", "imposter")

    ed.add_child(root, child)
    ed.add_child_at_index(root, sibling, 0)
    ed.add_child(child, grandchild)

    print(uman.past)

    # factory = NodeFactory()
    # tree_dict = root.to_dict()
    # new_root = factory.create_node(tree_dict)
    # new_tree_dict = new_root.to_dict()
    # new_tree_string = json.dumps(new_tree_dict, indent=4)
    # print(new_tree_string)

if __name__ == "__main__":
    main()