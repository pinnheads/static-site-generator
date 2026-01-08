
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        NOTE: Child classes to override this method
        """
        raise NotImplementedError

    def props_to_html(self):
        """Return '' if props is none else return all props as a string"""
        if self.props is None:
            return ""

        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'

        return result

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
