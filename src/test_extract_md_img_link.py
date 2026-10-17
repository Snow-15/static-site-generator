import unittest
from extract_md_img_link import *


class TestExtractMDImgLink(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_with_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_with_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image1", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with an [link1](https://i.imgur.com/zjjcJKZ.png) and [link2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("link1", "https://i.imgur.com/zjjcJKZ.png"),
                ("link2", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches
        )

    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_links(
            "No links here"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_image(self):
        matches = extract_markdown_images(
            "No images here"
        )
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()
