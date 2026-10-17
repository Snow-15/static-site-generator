from textnode import TextNode, TextType


# return a new list of text nodes
# "text" type nodes are split into multiple nodes
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for old_node in old_nodes:
        node_text = old_node.text

        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"invalid Markdown syntax, closing {delimiter} not found")
            
        # use a str as a reference to see where the inline parts are
        text_ref = node_text
        split_text = old_node.text.split(delimiter)

        for txt in split_text:
            if txt == "":
                continue

            # check if the index of the delimiter is 0 then the current txt is an inline element
            # after checking I remove txt from the start of text_ref after it has been processed
            # so i check the text_ref has a delimiter in the beginning
            if text_ref.find(delimiter) == 0:
                node = TextNode(txt, text_type)
                text_ref = text_ref.removeprefix(f"{delimiter}{txt}{delimiter}")
            else:
                node = TextNode(txt, TextType.TEXT)
                text_ref = text_ref.removeprefix(txt)

            new_nodes.append(node)

    return new_nodes
