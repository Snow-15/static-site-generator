class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> None:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        attributes = ""
        for key, value in self.props.items():
            attributes += f' {key}="{value}"'

        return attributes

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("node has no value")

        if self.tag is None:
            return self.value

        attributes = self.props_to_html()

        return f"<{self.tag}{attributes}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("node has no tag")

        if not self.children:
            raise ValueError("node has no children")

        attributes = self.props_to_html()
        converted_to_html = f"<{self.tag}{attributes}>"

        for node in self.children:
            converted_to_html += node.to_html()

        return converted_to_html + f"</{self.tag}>"
