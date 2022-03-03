from rich.text import Text

from textual import events
from textual.app import App
from textual.widgets import Header, ScrollView
from rich.console import Console
from textual_inputs import TextInput

console = Console()


class OutConsole(ScrollView):
    prev = Text("")

    async def eval(self, text_input):
        pre_y = self.y
        with console.capture() as capture:
            try:
                console.print(text_input)

                if text_input == "Test1":
                    console.print("Test2")



            except Exception:
                console.print_exception(show_locals=True)
        self.prev.append(Text.from_ansi(capture.get() + "\n"))
        await self.update(self.prev)
        self.y = pre_y
        self.animate("y", self.window.virtual_size.height, duration=1, easing="linear")


class InConsole(TextInput):
    def __init__(self, out):
        super(InConsole, self).__init__()
        self.out = out

    async def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            await self.out.eval(self.value)
            self.value = ""


class GridTest(App):
    async def on_mount(self) -> None:
        output = OutConsole()
        in_put = InConsole(out=output)

        grid = await self.view.dock_grid(edge="left", name="left")
        grid.add_column(fraction=1, name="u")
        grid.add_row(fraction=1, name="top", min_size=3)
        grid.add_row(fraction=20, name="middle")
        grid.add_row(fraction=1, name="bottom", min_size=3)
        grid.add_areas(area1="u,top", area2="u,middle", area3="u,bottom")
        grid.place(area1=Header(), area2=output, area3=in_put, )


GridTest.run(title="Brain")
