from rich.text import Text

from textual import events
from textual.app import App
from textual.widgets import Header, Footer, Placeholder, ScrollView
from rich.console import Console
from textual_inputs import TextInput

console = Console()


class OutConsole(ScrollView):
    prev = Text("")

    async def eval(self, text_input):
        pre_y = self.y
        with console.capture() as capture:
            try:
                console.print(f"{text_input}")
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
        """Make a simple grid arrangement."""

        # Git code
        output = OutConsole()
        in_put = InConsole(out=output)


        grid = await self.view.dock_grid(edge="left", name="left")

        grid.add_column(fraction=1, name="left", min_size=20)
        grid.add_column(size=30, name="center")
        grid.add_column(fraction=1, name="right")

        grid.add_row(fraction=1, name="top", min_size=2)
        grid.add_row(fraction=2, name="middle")
        grid.add_row(fraction=1, name="bottom")

        grid.add_areas(
            area1="left, top",
            area2="center,top",
            area3="left-start|center-end,middle",
            area4="right,top-start|middle-end",
            area5="left-start|right-end,bottom"
        )

        grid.place(
            area1=Placeholder(name="area1"),
            area2=Placeholder(name="area2"),
            area3=output,
            area4=Placeholder(name="area4"),
            area5=in_put,
        )



GridTest.run(title="Grid Test", log="textual.log")
