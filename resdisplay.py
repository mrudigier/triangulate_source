import tkinter as tk
from typing import List, Tuple

TypeVector = List[float]
TypeCoordinate = Tuple[float,float,float]

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
    self.c_width = 300+20
    self.x_offset = self.c_width/2
    self.c_height = 20*self.n_bars+20
    self.bars=[]
    self.scaling = self.x_offset/60
    self.zeroLine = self.canvas.create_line(self.x_offset, 10,
                                            self.x_offset, self.c_height-10,
                                            width=5)
    self.rect = self.canvas.create_rectangle(10,10, self.c_width-10,self.c_height-10,
                                        outline="black", width=2)

    for i in range (0, self.n_bars):
      self.bars.append(DiffBar(self.canvas, self.x_offset, 20*i+10+10,
                                            self.x_offset-10, 20))
    self.canvas.tag_raise(self.zeroLine)
    #self.bar_1.update(self.canvas, 20)

  def update(self, dvalues:TypeVector):
    if len(dvalues)!=self.n_bars:
      print("WARNING: Encountered wrong number of bar chart values...")
      return
    for i in range (0, self.n_bars):
      print("      {}/{} -- {}".format(i, self.n_bars, dvalues[i]))
      self.bars[i].update(self.canvas, dvalues[i]*self.scaling)
    self.canvas.tag_raise(self.zeroLine)
    self.canvas.tag_raise(self.rect)

class DiffBar:
  def __init__(self, canvas, xoffset:int, yoffset:int,
                             max_width:int, height:int):
    self.xoffset = xoffset
    self.yoffset = yoffset-height/2
    self.height = height
    self.max_width = max_width
    self.value = 0
    self.coarse_bar = canvas.create_rectangle(self.xoffset+self.value,
                                              self.yoffset-self.height/2,
                                              self.xoffset,
                                              self.yoffset+self.height/2,
                                              outline="#f50", fill="#f50")
    self.fine_bar = canvas.create_rectangle(self.xoffset+self.value,
                                              self.yoffset,
                                              self.xoffset,
                                              self.yoffset+self.height,
                                              outline="#f20", fill="#f20")

  def update(self, canvas, xvalue):
    self.value = min(xvalue, self.max_width)
    canvas.coords(self.coarse_bar, self.xoffset+self.value,
                                   self.yoffset,
                                   self.xoffset,
                                   self.yoffset+self.height )
    canvas.coords(self.fine_bar, self.xoffset+min(10*self.value,self.max_width),
                                   self.yoffset,
                                   self.xoffset,
                                   self.yoffset+self.height )
