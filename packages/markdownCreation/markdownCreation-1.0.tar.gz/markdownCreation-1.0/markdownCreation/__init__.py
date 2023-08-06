"""
Markdown Creation by Anime no Sekai
2020
"""

class MarkdownFile():
    """
    A markdown file object
    """
    def __init__(self):
        """
        Initialize a new Markdown file
        """
        self.content = []
        self.headers = []
        self.footnotes = []

    def save(self, destination, appendToExistingFile=False):
        """
        Saves the MarkdownFile object to a markdown file
        """
        def writeToFile(fileInstance):
            for line in self.content:
                fileInstance.write(str(line) + '  \n\n')
            for note in self.footnotes:
                fileInstance.write(str(note) + '  \n\n')
        
        if appendToExistingFile:
            with open(destination, 'a+', encoding="utf-8") as outputFile:
                writeToFile(outputFile)
        else:
            with open(destination, 'w+', encoding="utf-8") as outputFile:
                writeToFile(outputFile)

    def add(self, object):
        """
        Add something to the markdown file
        """
        self.content.append(object)

    def tableOfContent(self, level):
        pastHeaders = []
        
        def _getLink(headerName):
            """
            Returns a markdown valid header link
            """
            temp = str(headerName).replace(" ", "-").lower()
            for replacing in ["/", ',', '"', "'", ".", ":", "`", "(", "[", "~", ")", "]", "°", "¨", "\\", "?", "!"]:
                temp = temp.replace(replacing, "")
            if temp in pastHeaders:
                number = 0
                while temp in pastHeaders:
                    number += 1
                    temp = temp + "-" + str(number)
            for hyphen in range(temp.count("-")):
                if hyphen > 1:
                    temp.replace("-" * hyphen, "-")
            pastHeaders.append(temp)
            temp = "#" + temp
            return temp

        results = ""
        iteration = 0
        levels = []
        currentHeader = 0
        for header in self.headers:
            if header.level in list(range(1, level + 1)):
                if header.level == 1:
                    headerLevel = 0
                    iteration += 1
                    headerTitle = header.content[header.level + 1:]
                    results += f"{str(iteration)}. [{headerTitle}]({_getLink(headerTitle)})\n"
                else:
                    headerTitle = header.content[header.level + 1:]
                    headerLevel = header.level
                    if currentHeader == 0:
                        headerLevel = 0
                    else:
                        if headerLevel > levels[currentHeader - 1]:
                            headerLevel = levels[currentHeader - 1] + 1
                    results += "    " * headerLevel + f"- [{headerTitle}]({_getLink(headerTitle)})\n"
            levels.append(headerLevel)
            currentHeader += 1
        return results


    def render(self):
        """
        Renders the file and outputs it as a string
        """
        result = ""
        for element in self.content:
            result += str(element) + '  \n\n'
        for element in self.footnotes:
            result += str(element) + '  \n\n'
        return result
    
    def html(self, title=None, onlyMarkdown=False, minify=False, destination=None):
        """
        Converts the Markdown file into an HTML file
        """
        import htmlmin
        from markdown import markdown
        from bs4 import BeautifulSoup

        extensions = ["nl2br", "def_list", "extra", "footnotes", "tables", "codehilite", "smarty"]

        if not onlyMarkdown:
            def getDocumentTitle():
                def _getHeader(currentLevel):
                    for header in self.headers:
                        if header.level == currentLevel:
                            return str(header)
                    return None

                for level in range(1, 7):
                    header = _getHeader(level)
                    if header is not None:
                        return header[level + 1:]
                    continue
                return "Markdown Render"

            htmlTitle = title
            if htmlTitle is None:
                htmlTitle = getDocumentTitle()

            htmlResult = """<!DOCTYPE html>
            <html>
                <head>
                    <title>{title}</title>
            """.format(title=htmlTitle)
            htmlResult += """<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
                    <link href="https://cdn.jsdelivr.net/gh/Animenosekai/markdown-creation/pygmentsOutput/styles/codeStyling.css" rel="stylesheet">
                    <style>
                        body { font-family: Helvetica, Arial, sans-serif; }
                        code, pre { font-family: monospace; }
                    </style>
                </head>
                <body>
                    <div class="markdownCreation-Render-Output">
            """
            htmlResult += """{content}
                    </div>
                </body>
            </html>
            """.format(content=markdown(self.render(), extensions=extensions))
        else:
            htmlResult = markdown(self.render(), extensions=extensions)
        
        if minify:
            try:
                htmlResult = htmlmin.minify(htmlResult, remove_comments=True, remove_empty_space=True)
            except:
                htmlResult = htmlResult
        else:
            htmlResult = BeautifulSoup(htmlResult, 'html.parser').prettify()

        if destination is not None:
            with open(destination, 'w+', encoding="utf-8") as outputFile:
                outputFile.write(htmlResult)

        return htmlResult

    def __repr__(self) -> str:
        numberOfLineBreak = self.render().count("\n")
        if numberOfLineBreak > 0:
            if len(self.content) > 1:
                numberOfLines = f'{str(numberOfLineBreak)} lines'
            else:
                numberOfLines = f'{str(numberOfLineBreak)} line'
        else:
            numberOfLines = "No line"
        if len(self.footnotes) > 0:
            if len(self.footnotes) > 1:
                return f"Markdown File | {str(numberOfLines)} with {str(len(self.footnotes))} footnotes"
            else:
                return f"Markdown File | {str(numberOfLines)} with {str(len(self.footnotes))} footnote"
        else:
            return f"Markdown File | {str(numberOfLines)}"




class Header():
    """
    A header element for the markdown file
    """
    def __init__(self, text, level, markdownObj=MarkdownFile()):
        self.text = text
        self.level = level
        self.content = "#" * level + " " + text
        markdownObj.headers.append(self)

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class Quote():
    """
    A blockquote element for the markdown file
    """
    def __init__(self, quotation, level=1) -> None:
        self.content = ">" * level + " " + quotation

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)
    
class OrderedList():
    """
    An ordered list element for the markdown file
    """
    def __init__(self, inputList) -> None:
        self.content = ""
        iteration = 0
        for element in inputList:
            iteration += 1
            if iteration == len(inputList):
                self.content += f"{str(iteration)}. {str(element)}"
            else:
                self.content += f"{str(iteration)}. {str(element)}\n"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class List():
    """
    An unordered list element for the markdown file
    """
    def __init__(self, inputList) -> None:
        self.content = ""
        iteration = 0
        for element in inputList:
            iteration += 1
            if iteration == len(inputList):
                self.content += "- " + element
            else:
                self.content += "- " + element + "\n"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class InlineCode():
    """
    An inline code element for the markdown file
    """
    def __init__(self, code) -> None:
        self.content = f"`{str(code)}`"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)
    
class Separator():
    """
    A separator (horizontal rule) element for the markdown file
    """
    def __init__(self) -> None:
        self.content = "---"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class Link():
    """
    A link element for the markdown file
    """
    def __init__(self, link, title=None, hoverTitle=None) -> None:
        putHoverTitle = ""
        if hoverTitle is not None:
            putHoverTitle = f' "{str(hoverTitle)}"'
        if title is None:
            self.content = f"[{str(link)}]({str(link)}{putHoverTitle})"
        else:
            self.content = f"[{str(title)}]({str(link)}{putHoverTitle})"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class Image():
    """
    An image element for the markdown file
    """
    def __init__(self, URL, alt_text=None) -> None:
        if alt_text is None:
            self.content = f"![{str(URL[str(URL).rfind('/'):])}]({str(URL)})"
        else:
            self.content = f"![{str(alt_text)}]({str(URL)})"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class Table():
    """
    A table element for the markdown file
    """

    class TableError(Exception):
        """
        When an error occured
        """
        def __init__(self, message):
            super().__init__(message)
    
    def __init__(self, headers, values, alignement="left") -> None:
        if isinstance(alignement, list):
            alignements = alignement
        else:
            alignements = [str(alignement)] * len(headers)
        
        iteration = 0
        for element in alignements:
            if str(element) == "left":
                alignements[iteration] = [":", ""]
            elif str(element) == "center":
                alignements[iteration] = [":", ":"]
            elif str(element) == "right":
                alignements[iteration] = ["", ":"]
            else:
                raise self.TableError(f"{str(element)} is not a valid alignement")


            iteration += 1

        if len(alignements) != len(headers) or len(values) != len(headers):
            def elementsNumber(inputList):
                if len(inputList) > 1:
                    return f"({str(len(inputList))} elements)"
                else:
                    return f"({str(len(inputList))} element)"

            raise self.TableError(f"The headers {elementsNumber(headers)}, the values {elementsNumber(values)} and the alignements {elementsNumber(alignements)} don't have the same number of elements")

        self.content = ""
        iteration = 0
        currentLine = ""
        for element in headers:
            if iteration == 0:
                currentLine += "| " + element + " |"
            else:
                currentLine += " " + element + " |"
            iteration += 1
        self.content += currentLine + "\n"

        currentLine = ""
        for iteration, _ in enumerate(headers):
            if iteration == 0:
                currentLine += f"| {str(alignements[iteration][0])}-----{str(alignements[iteration][1])} |"
            else:
                currentLine += f" {str(alignements[iteration][0])}-----{str(alignements[iteration][1])} |"
        self.content += currentLine + "\n"

        #print("New Table")
        for lineNumber, _ in enumerate(values[0]):
            currentLine = ""
            #print("Current line is: " + str(lineNumber))
            for iteration, hey in enumerate(headers):
                #print("Current column is: " + str(iteration))
                if iteration == 0:
                    currentLine += "| " + values[iteration][lineNumber] + " |"
                else:
                    currentLine += " " + values[iteration][lineNumber] + " |"
            self.content += currentLine + "\n"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class CodeBlock():
    """
    A code block element for the markdown file
    """
    def __init__(self, code, language=None) -> None:
        if language is None:
            self.content = "```"
            self.content += code
            self.content += "```"
        else:
            self.content = "```" + str(language).lower()
            self.content += code
            self.content += "```"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class Footnote():
    """
    A footnote element for the markdown file
    """
    def __init__(self, note, markdownObj) -> None:
        footnoteIndex = len(markdownObj.footnotes) + 1
        markdownObj.footnotes.append(f"[^{str(footnoteIndex)}]: " + note)
        self.content = f"[^{str(footnoteIndex)}]"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class HeadingID():
    """
    A heading ID element for the markdown file
    """
    def __init__(self, id, correctSyntax=True) -> None:
        if correctSyntax:
            self.content = "{#" + str(id).replace("/", "").replace(" ", "-").lower() + "}"
        else:
            self.content = "{#" + str(id) + "}"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class Definition():
    """
    A definition element for the markdown file
    """
    def __init__(self, word, definition) -> None:
        self.content = word
        if isinstance(definition, str):
            self.content += ": " + definition
        else:
            for element in definition:
                self.content += "\n: " + element

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)


class Strikethrough():
    """
    A strikethrough element for the markdown file
    """
    def __init__(self, text) -> None:
        self.content = "~~" + text + "~~"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class TaskList():
    """
    A task list element for the markdown file
    """
    def __init__(self, task, checked=False) -> None:
        if checked:
            self.content = f"- [x] {str(task)}"
        else:
            self.content = f"- [ ] {str(task)}"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)
    
    def addTask(self, task, checked=False) -> None:
        if checked:
            self.content += f"\n- [x] {str(task)}"
        else:
            self.content += f"\n- [ ] {str(task)}"

class Paragraph():
    """
    A paragraph element for the markdown file
    """
    def __init__(self, text) -> None:
        self.content = str(text).replace("\n", '  \n')

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class BoldText():
    """
    A bold text element for the markdown file
    """
    def __init__(self, text) -> None:
        self.content = "**" + str(text) + "**"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class ItalicText():
    """
    An italic text element for the markdown file
    """
    def __init__(self, text) -> None:
        self.content = "*" + str(text) + "*"

    def __repr__(self) -> str:
        return self.content 

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)

class BoldAndItalicText():
    """
    A bold and italic text element for the markdown file
    """
    def __init__(self, text) -> None:
        self.content = "***" + str(text) + "***"

    def __repr__(self) -> str:
        return self.content

    def __add__(self, other):
        return str(self.content) + str(other)
    
    def __radd__(self, other):
        return str(other) + str(self.content)


class TableOfContent:
    """
    A table of content element for the markdown file
    """
    class TableOfContent_Content:

        def __get__(self, obj, objtype=None):
            return obj.markdownObj.tableOfContent(obj.level)

    content = TableOfContent_Content()
    def __init__(self, markdownObj, level):
        self.markdownObj = markdownObj
        self.level = level

    def __repr__(self) -> str:
        return self.content