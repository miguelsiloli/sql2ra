from typing import List, Optional, Union

# class ASTNode:
#     def __init__(self, node_type: str, children: Optional[List[Union[str, 'ASTNode']]] = None):
#         self.node_type = node_type
#         self.children = children if children is not None else []

#     def repr(self, indent: int = 3) -> str:
#         return str(self.to_dict())

#     def to_dict(self) -> dict:
#         return {
#             "node_type": self.node_type,
#             "children": [child.to_dict() if isinstance(child, ASTNode) else child for child in self.children]
#         }

#     def __repr__(self) -> str:
#         return self.repr(indent=2)


class ASTNode:
    def __init__(self, node_type: str, children: Optional[List[Union[str, "ASTNode"]]] = None):
        """
        Initializes an instance of the ASTNode class.

        Args:
            node_type (str): The type of the node.
            children (Optional[List[Union[str, 'ASTNode']]], optional): The children of the node. Defaults to None.

        Returns:
            None
        """
        self.node_type = node_type
        self.children = children if children is not None else []

    def to_dict(self) -> dict:
        """
        Converts the current ASTNode object into a dictionary representation.

        The dictionary contains the node type and its children. If the node has children,
        they are recursively converted into dictionaries or kept as strings if they are not ASTNode objects.

        Returns:
            dict: A dictionary representation of the ASTNode object.
        """
        result = {"node_type": self.node_type}
        if self.children:
            result["children"] = [
                child.to_dict() if isinstance(child, ASTNode) else child for child in self.children
            ]
        return result

    def __repr__(self) -> str:
        return str(self.to_dict())
