from tkinter import *
from PIL import Image
import random


class Sketchpad:
    def __init__(self, parent, **args):
        self.canvas = Canvas(parent, width=280, height=280, borderwidth=0, highlightthickness=0, **args)
        self.canvas.focus_set()

        self.drawing_x = None
        self.drawing_y = None

        self.drawing = False

        self.canvas.bind("<ButtonPress-1>", self.enable_drawing)
        self.canvas.bind("<B1-ButtonRelease>", self.disable_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

        # Note: canvas object needs keyboard focus to respond keyboard key presses and releases
        self.canvas.bind("<KeyRelease-Return>", self.save_and_clear)

    def enable_drawing(self, event):
        self.drawing = True
        self.update_drawing_position(event)

        tile_x, tile_y = event.x, event.y
        if len(self.canvas.find_overlapping(tile_x * 10, tile_y * 10, tile_x * 10 + 9, tile_y * 10 + 9)) == 0:
            self.canvas.create_rectangle(tile_x * 10, tile_y * 10, tile_x * 10 + 9, tile_y * 10 + 9, tags='rect', fill='black')

    def disable_drawing(self, event):
        self.drawing = False

    def draw(self, event):
        if not self.drawing:
            return

        self.update_drawing_position(event)

        # TODO: relax assumption of width = 280 and height = 280
        for tile_y in range(28):
            for tile_x in range(28):
                if tile_x * 10 <= self.drawing_x < (tile_x + 1) * 10 and tile_y * 10 <= self.drawing_y < (tile_y + 1) * 10:
                    if len(self.canvas.find_overlapping(tile_x * 10, tile_y * 10, tile_x * 10 + 9, tile_y * 10 + 9)) == 0:
                        self.canvas.create_rectangle(tile_x * 10, tile_y * 10, tile_x * 10 + 9, tile_y * 10 + 9, tags='rect', fill='black')
                    break

    def save_and_clear(self, event):
        items = self.canvas.find_withtag('rect')[1:]

        image = Image.new(mode="L", size=(28, 28), color=255)

        for item in items:
            pixel_x, pixel_y = int(self.canvas.coords(item)[0] // 10), int(self.canvas.coords(item)[1] // 10)
            image.putpixel((pixel_x, pixel_y), 0)

        image.save(f"{random.randint(1, 100000000)}.png", "PNG")

        self.canvas.delete('rect')

    def update_drawing_position(self, event):
        self.drawing_x, self.drawing_y = event.x, event.y

    def grid(self, **args):
        self.canvas.grid(**args)


root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

sketch = Sketchpad(root)
sketch.grid(column=0, row=0, sticky="NWES")

root.mainloop()
