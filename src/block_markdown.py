from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "headng"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []

    for i in range(len(blocks)):
        block = blocks[i].strip()
        if block == "":
            continue

        cleaned_blocks.append(block)

    return cleaned_blocks
