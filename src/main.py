from textnode import TextNode, TextType


def main():
    new_node = TextNode("Utsav Deep's Portfolio",
                        TextType.LINKS, "https://utsavdeep.com")
    print(new_node)


if __name__ == "__main__":
    main()
