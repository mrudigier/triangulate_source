import tkinter as tk

class RmsDisplay(tk.Frame):
  """Displays the root mean square (rms) value given. It stores then
     best value and the corresponding settings. This way they can be
     restored later from the main app"""
  n_bars = 1
  def __init__(self, tkroot):
    #self.padding = 10
    #self.width = 300+2*self.padding
    #self.height = 100
    super().__init__(tkroot)
    self.rms_curr = 1000000000.0
    self.rms_best = 1000000000.0
    self.best_x = 0.0
    self.best_y = 0.0
    self.best_z = 0.0
    self.s_rms_curr = tk.StringVar()
    self.s_rms_best = tk.StringVar()
    self.s_best_coord = tk.StringVar()

    self.initFrame()

  def initFrame(self):
    self.lbl_rms_curr = tk.Label(self,
                               textvariable=self.s_rms_curr, anchor="e",
                               width=30)
    self.lbl_rms_best = tk.Label(self,
                               textvariable=self.s_rms_best, anchor="e",
                               width=30)
    self.lbl_pos_best = tk.Label(self,
                               textvariable=self.s_best_coord, anchor="e", width=40)
    self.lbl_rms_curr.grid(row=1, column=0)
    self.lbl_rms_best.grid(row=0, column=0)
    self.lbl_pos_best.grid(row=2, column=0)
    self.update_labels(self.rms_curr, self.best_x, self.best_y, self.best_z)



  def update_labels(self, curr_rms, curr_x, curr_y, curr_z):
    print ("UPDATING labels\n {} {} {}".format(self.best_x, self.best_y, self.best_z))
    self.rms_curr = curr_rms
    if (self.rms_curr < self.rms_best):
      self.rms_best = curr_rms
      self.best_x = curr_x
      self.best_y = curr_y
      self.best_z = curr_z
    self.s_rms_curr.set("RMS current {:10.4f}".format(self.rms_curr))
    self.s_rms_best.set("RMS best    {:10.4f}".format(self.rms_best))
    self.s_best_coord.set("Best source pos [{:8.2f},{:8.2f},{:8.2f}]".format(self.best_x,
                                                                    self.best_y,
                                                                    self.best_z))

  def reset(self):
    self.rms_curr = 1000000000.0
    self.rms_best = 1000000000.0
    self.best_x = 0.0
    self.best_y = 0.0
    self.best_z = 0.0
    self.update_labels(self.rms_curr, self.best_x, self.best_y, self.best_z)
