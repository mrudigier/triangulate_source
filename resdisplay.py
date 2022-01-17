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
    self.padding = 10
    self.barheight = 20
    self.c_width = 300+2*self.padding
    self.x_offset = self.c_width/2
    self.c_height = self.barheight*self.n_bars+2*self.padding
    self.bars=[]
    self.scaling = 1
    self.zeroLine = self.canvas.create_line(self.x_offset, self.padding,
                                            self.x_offset,
                                            self.c_height-self.padding,
                                            width=5)
    self.rect = self.canvas.create_rectangle(self.padding, self.padding,
                                             self.c_width-self.padding,
                                             self.c_height-self.padding,
                                        outline="black", width=2)

    for i in range (0, self.n_bars):
      self.bars.append(DiffBar(self.canvas, self.x_offset,
                                            self.barheight*i+self.padding,
                                            self.x_offset-self.padding,
                                            self.barheight))
    self.canvas.tag_raise(self.zeroLine)
    self.canvas.tag_raise(self.rect)

  def update(self, dvalues:TypeVector):
    if len(dvalues)!=self.n_bars:
      print("WARNING: Encountered wrong number of bar chart values...")
      return
    for i in range (0, self.n_bars):
      #print("      {}/{} -- {} scl {}".format(i, self.n_bars, dvalues[i], self.scaling))
      self.bars[i].update(self.canvas, dvalues[i]*self.scaling)
    self.canvas.tag_raise(self.zeroLine)
    self.canvas.tag_raise(self.rect)

class DiffBar:
  def __init__(self, canvas, xoffset:int, yoffset:int,
                             max_width:int, height:int):
    self.xoffset = xoffset
    self.yoffset = yoffset
    self.height = height
    self.max_width = max_width
    self.value = 0
    self.value_scaled = 0
    # Have two bars, a coarse and a fine bar. The coarse bar is 10 timest
    # less sensitive than the fine one. For better discrimination, the
    # coarse bar is made thinner and a different colour.
    self.fine_bar = canvas.create_rectangle(self.xoffset+self.value+0,
                                              self.yoffset,
                                              self.xoffset,
                                              self.yoffset+self.height,
                                              outline="#2d7", fill="#2d7")
    self.coarse_bar = canvas.create_rectangle(self.xoffset+self.value_scaled+0,
                                              self.yoffset+self.height/4,
                                              self.xoffset,
                                              self.yoffset+3*self.height/4,
                                              outline="#f50", fill="#f50")


  def update(self, canvas, xvalue:float):
    if xvalue>0:
      self.value = min(xvalue, self.max_width)
      self.value_scaled = min(10*xvalue, self.max_width)
    else:
      self.value = max(xvalue, -self.max_width)
      self.value_scaled = max(10*xvalue, -self.max_width)
    canvas.coords(self.fine_bar, self.xoffset+self.value_scaled,
                                 self.yoffset,
                                 self.xoffset,
                                 self.yoffset+self.height )
    canvas.coords(self.coarse_bar, self.xoffset+self.value,
                                   self.yoffset+self.height/4,
                                   self.xoffset,
                                   self.yoffset+3*self.height/4 )
