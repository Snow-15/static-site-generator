from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "text (plain)"
    BOLD_TEXT = "bold text"
    ITALIC_TEXT = "italic text"
    CODE_TEXT = "code text"
    LINKS = "link"
    IMAGES = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        


