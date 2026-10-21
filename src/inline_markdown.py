from textnode import TextNode, TextType
from extract_md_img_link import *


# return a new list of text nodes
# "text" type nodes are possibly split into multiple nodes
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        # use a str as a reference to see if the current txt is contains inline formatting
        node_text = old_node.text

        if node_text == "":
            continue
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if node_text.count(delimiter) % 2 != 0:
            raise ValueError(f"invalid Markdown syntax, closing {delimiter} not found")
            
        split_text = node_text.split(delimiter)

        for txt in split_text:
            if txt == "":
                continue

            # check if the index of the delimiter is 0 then the current txt is an inline element
            # after checking, remove the txt from the start of text_ref after it has been processed
            # so i check the text_ref has a delimiter in the beginning
            if node_text.find(delimiter) == 0:
                node = TextNode(txt, text_type)
                node_text = node_text.removeprefix(f"{delimiter}{txt}{delimiter}")
            else:
                node = TextNode(txt, TextType.TEXT)
                node_text = node_text.removeprefix(txt)

            new_nodes.append(node)

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        node_text = old_node.text
        if node_text == "":
            continue
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_images(node_text)
        if not matches:
            new_nodes.append(old_node)
            continue

        for alt_text, url in matches:
            image_format = f"![{alt_text}]({url})"
            txt, node_text = node_text.split(image_format, maxsplit=1)

            if txt != "":
                node = TextNode(txt, TextType.TEXT)
                new_nodes.append(node)

            node = TextNode(alt_text, TextType.IMAGE, url)
            new_nodes.append(node)

        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        node_text = old_node.text
        if node_text == "":
            continue
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_markdown_links(node_text)
        if not matches:
            new_nodes.append(old_node)
            continue

        for alt_text, url in matches:
            link_format = f"[{alt_text}]({url})"
            txt, node_text = node_text.split(link_format, maxsplit=1)

            if txt != "":
                node = TextNode(txt, TextType.TEXT)
                new_nodes.append(node)

            node = TextNode(alt_text, TextType.LINK, url)
            new_nodes.append(node)

        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def text_to_text_nodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.TEXT)
    text_nodes = split_nodes_image([node])
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)

    return text_nodes
