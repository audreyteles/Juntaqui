import os.path

from textual.app import App
from textual.containers import Container
from textual.widgets import Header, Footer, Label, Button, Input, SelectionList
from textual.widgets._selection_list import Selection
from textual._on import on

from module.main import sort_files


class MyApp(App):
    CSS_PATH = "style.tcss"
    TITLE = "JUNTAQUI"

    def __init__(self):
        super().__init__()
        self.label = None
        self.extensions = []
        self.path = None
        self.lists = None
        self.new_extension = None

    def compose(self):
        yield Header(show_clock=True)
        self.path = Input(placeholder=r"C:\Users\YourUser\Documents", type="text",
                          id="path-input")
        self.label = Label("")
        yield self.path

        with Container(classes="extensions"):
            with Container(classes="left"):
                self.lists = SelectionList[str](
                    Selection(".iso", ".iso"),
                    Selection(".pdf", ".pdf"),
                    Selection(".exe", ".exe"),
                    Selection(".txt", ".txt")
                )
                # self.query_one(SelectionList).border_title = "Chose your extensions!"
                self.lists.classes = "extension-list"
                yield self.lists

            with Container(classes="right"):
                with Container():
                    self.new_extension = Input(placeholder=r".php", type="text", id="input-extension")
                    yield self.new_extension
                    yield Button(label="+", variant="default", id="extension-button")
                    with Container(classes="buttons"):
                        yield Button(label="Sort", variant="success", id="sort-button")
                        yield Button(label="Close", variant="error", id="error-button")

        yield Footer()
        with Footer():
            yield self.label

    @on(Input.Changed)
    def valid_path(self, event: Input.Changed):
        valid = os.path.isdir(self.path.value)
        if not self.path.value == "":
            if valid:
                self.query("#path-input").only_one().styles.border = ("tall", "green")
            else:
                self.query("#path-input").only_one().styles.border = ("tall", "red")
        else:
            self.query("#path-input").only_one().styles.border = ("none", "white")

    @on(SelectionList.SelectionToggled)
    def pressed_op(self, event: SelectionList.SelectionToggled) -> None:
        extension = str(event.selection.prompt)
        if extension in self.extensions:
            self.extensions.remove(extension)
        else:
            self.extensions.append(extension)

    @on(Button.Pressed, "#extension-button")
    def extension_button(self):
        if not self.new_extension.value == "":
            self.lists.add_options([Selection(self.new_extension.value, self.new_extension.value)])

    @on(Button.Pressed, "#sort-button")
    def sort_button(self):
        try:
            sort_files(str(self.path.value), self.extensions)
            self.label.update("Done!")
        except OSError:
            self.label.update("There was an error!")

    @on(Button.Pressed, "#error-button")
    def error_button(self):
        self.exit()


MyApp().run()
