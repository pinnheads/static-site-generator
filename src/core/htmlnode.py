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


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"Tag is required in {self}")
        if self.children is None:
            raise ValueError(f"children cannot be {self.children}")

        parent = f"<{self.tag}{self.props if self.props is not None else ''}>"
        for child in self.children:
            parent += child.to_html()

        return f"{parent}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        """Returns the HTML representation of the leaf node of HTML tag"""
        # if value is none raise error
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        # if tag is none return value as raw text
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
