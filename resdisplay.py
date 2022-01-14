import tkinter as tk

class ResDisplay(tk.Frame):
  """Displays the residual between two values for a given number
     of inputs using rectangle charts
     Inherits from tkinter.Frame and calles its constructor via super"""
  n_bars = 1
  def __init__(self, tkroot, n_bars):
    super().__init__(tkroot)
    self.n_bars = n_bars
    self.initCanvas()

  def initCanvas(self):
    self.canvas = tk.Canvas(self)
    self.canvas.pack(fill=tk.BOTH, expand=1)
    self.c_width = 500
    self.x_offest = self.c_width/2
    self.c_height = 30*self.n_bars
    self.zeroLine = self.canvas.create_line(self.x_offest, 0,
                                            self.x_offest, self.c_height,
                                            width=5)
