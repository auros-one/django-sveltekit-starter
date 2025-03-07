import bs4
from bs4.element import PageElement, Tag
from markdownify import ATX, markdownify

# REDUNDANT ELEMENTS
# Delete
GRAPHICS_ELEMENTS = [
    "defs",
    "svg",
    "g",
    "stop",
    "lineargradient",
    "path",
    "rect",
    "circle",
    "polygon",
    "symbol",
    "clippath",
    "mask",
]
ELEMENTS_TO_REMOVE = GRAPHICS_ELEMENTS + [
    "script",
    "link",
    "style",
    "iframe",
    "template" "button",
]
OPTIONAL_NAVIGATION_ELEMENTS = ["nav", "header", "footer"]
ELEMENTS_TO_REMOVE += OPTIONAL_NAVIGATION_ELEMENTS
ELEMENTS_TO_UNWRAP = ["main", "div", "span"]


def simplify_html(source_html) -> str:
    soup = bs4.BeautifulSoup(source_html, "html.parser")

    elements_to_decompose: list[PageElement] = []

    for elem in soup.descendants:
        """
        In this loop some elements are marked for deletion.
        We mark the elements for deletion instead of decomposing them right away
        because decomposing an element stops the `soup.descendants` iterator.
        """

        # Only analyze Tag
        if (
            isinstance(elem, bs4.Comment)
            or isinstance(elem, bs4.Script)
            or isinstance(elem, bs4.Stylesheet)
        ):
            elements_to_decompose.append(elem)
            continue
        if not isinstance(elem, bs4.Tag):
            continue

        # List of rules that can mark an element for deletion
        if (
            elem.name is None
            # Delete certain types of elements (svg, script, etc.)
            or elem.name in ELEMENTS_TO_REMOVE
            # Delete all img elements that have no or an empty alt attribute
            or (elem.name == "img" and (not elem.get("alt") or elem.get("alt").isspace()))  # type: ignore
            # Delete all elements with aria-hidden="true"
            or (elem.get("aria-hidden") == "true")
        ):
            elements_to_decompose.append(elem)

    for element in soup.find_all("img"):
        elements_to_decompose.append(element)

    # Delete the elements marked for deletion
    for elem in elements_to_decompose:
        # check hasattr because some elements don't have a decompose method
        if hasattr(elem, "decompose"):
            elem.decompose()  # type: ignore

    # #### Remove Useless HTML elements ####

    # Extract the contents of the body element
    html = soup.find("html")
    if html and isinstance(html, Tag):
        html.unwrap()
    head = soup.find("head")
    if head and isinstance(head, Tag):
        head.decompose()
    body = soup.find("body")
    if body and isinstance(body, Tag):
        body.unwrap()

    # Unwrap useless elements
    for elem in soup.find_all(ELEMENTS_TO_UNWRAP):
        if isinstance(elem, Tag):
            elem.unwrap()

    # Delete empty elements
    for elem in soup.find_all(True):
        if isinstance(elem, Tag) and (
            elem.text.isspace() or (elem.text == "" and not elem.name == "br")
        ):
            if hasattr(elem, "decompose"):
                elem.decompose()

    # Remove attributes except href
    for elem in soup.find_all(True):
        if isinstance(elem, Tag):
            for attr in list(elem.attrs):
                if attr != "href":
                    del elem[attr]

    for ul in soup.find_all("ul"):
        if isinstance(ul, Tag):
            ul["class"] = "list-disc"
    for ol in soup.find_all("ol"):
        if isinstance(ol, Tag):
            ol["class"] = "list-decimal"
    for li in soup.find_all("li"):
        if isinstance(li, Tag):
            li["class"] = "ml-4"

    for elem in soup.find_all("button"):
        if hasattr(elem, "decompose"):
            elem.decompose()

    return str(soup)


def html_to_markdown(source_html: str, simplify_first: bool = True) -> str:
    if simplify_first:
        source_html = simplify_html(source_html)

    markdown = markdownify(source_html, heading_style=ATX)

    # Remove spaces between newline characters & strip trailing whitespaces
    result = []
    for item in markdown.split("\n"):
        if not item.isspace():
            result.append(item.rstrip())
    markdown = "\n".join(result)

    # Remove triple newlines
    while "\n\n\n" in markdown:
        markdown = markdown.replace("\n\n\n", "\n\n")

    markdown = markdown.strip()

    return markdown
