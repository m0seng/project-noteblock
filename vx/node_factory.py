from node import Node
# TODO: import Node subclasses here

class NodeFactory:
    node_classes = {
        "Node": Node,
        # TODO: add entries for Node subclasses here
    }

    def create_node(self, source: dict):
        node_class = self.node_classes.get(source["class"], None)
        if node_class is None: return None
        node = node_class()
        node.properties = source["properties"]
        node.child_order = source["child_order"]
        for k, v in source["children"].items():
            child = self.create_node(v)
            node._add_child(child, id=int(k), index=None)
        return node