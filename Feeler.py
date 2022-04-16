from __future__ import annotations


from textual import events
from textual.app import App
from textual.widget import Widget
from textual.widgets import Header, Footer, Placeholder, ScrollView

from rich.console import Console
from rich.text import Text
from textual_inputs import TextInput

import psutil
from datetime import datetime

from sys import version_info

from modules.tiptop.__about__ import __version__
from modules.tiptop._battery import Battery
from modules.tiptop._cpu import CPU
from modules.tiptop._disk import Disk
from modules.tiptop._info import InfoLine
from modules.tiptop._mem import Mem
from modules.tiptop._net import Net
from modules.tiptop._procs_list import ProcsList

import Client

def Message():

    message = Client.main()
    return message


class Clock(Widget):
    def on_mount(self):
        self.set_interval(1, self.refresh)

    def render(self):
        time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return time


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
        
        message = Message()
        
        await output.eval(message)
        
        grid = await self.view.dock_grid(edge="left", name="left")

        grid.add_column(fraction=1, name="left", min_size=20)
        grid.add_column(size=30, name="center")
        grid.add_column(fraction=1, name="right")

        grid.add_row(fraction=1, name="top", min_size=1)
        grid.add_row(fraction=2, name="stats")
        grid.add_row(fraction=2, name="middle")
        grid.add_row(fraction=1, name="bottom")
        

        grid.add_areas(
            area1="left, top",
            area2="center,top",
            area3="right, top",
            area4="left, stats",
            area5="center, stats",
            area6="center, stats",
            area7="right, middle-start|bottom-end",
            area8="left-start|center-end, middle",
            area9="left-start|center-end, bottom",
            area10="right, stats"
        )

        grid.place(
            area1=Clock(),
            area2=Battery(),
            area3=ProcsList(),
            area4=CPU(),
            area5=InfoLine(),
            area6=Mem(),
            area7=Net(),
            area8=output,
            area9=in_put,
            area10=Disk()
        )


if __name__ == "__main__":

	console = Console()
	
	GridTest.run(title="Grid Test", log="textual.log")
