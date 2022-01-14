import tkinter as tk
from resdisplay import ResDisplay
from rescalc import ResCal

window = tk.Tk()
window.geometry("800x600")

xpos = tk.DoubleVar()
ypos = tk.DoubleVar()
zpos = tk.DoubleVar()

#rect = Rectangle()
rc = ResCal("FATIMA_pos.txt", "FATIMA_intensities.txt")

def update_X (val):
  xpos.set(val)
  rc.update([xpos.get(), ypos.get(), zpos.get()])
  #window.update()
def update_Y (val):
  ypos.set(val)
  rc.update([xpos.get(), ypos.get(), zpos.get()])
  #window.update()
def update_Z (val):
  zpos.set(val)
  rc.update([xpos.get(), ypos.get(), zpos.get()])
  #window.update()
def reset():
  update_X(0)
  update_Y(0)
  update_Z(0)
  scl_Xvalue.set(0)
  scl_Yvalue.set(0)
  scl_Zvalue.set(0)

main_gui = tk.Frame(window, width=300)
main_display = tk.Frame(window, width=500)
#main_gui.grid_propagate(0)
main_gui.grid(row=0,column=0)
main_display.grid(row=0,column=1)

display1 = ResDisplay(main_display, 6)
display2 = ResDisplay(main_display, 12)
btn_reset_pos = tk.Button(main_gui, text="RESET", command=reset)
lbl_Sliders = tk.Label(main_gui,
                       text="Source position")
lbl_Xlbl = tk.Label(main_gui, text="Xpos")
lbl_Ylbl = tk.Label(main_gui, text="Ypos")
lbl_Zlbl = tk.Label(main_gui, text="Zpos")
scl_Xvalue = tk.Scale(main_gui, from_=-100, to=100,
                      orient=tk.HORIZONTAL,
                      width=20, length=200,
                      tickinterval=100,
                      command=update_X,
                      showvalue=0)
scl_Yvalue = tk.Scale(main_gui, from_=-100, to=100,
                      orient=tk.HORIZONTAL,
                      width=20, length=200,
                      tickinterval=100,
                      command=update_Y,
                      showvalue=0)
scl_Zvalue = tk.Scale(main_gui, from_=-100, to=100,
                      orient=tk.HORIZONTAL,
                      width=20, length=200,
                      tickinterval=100,
                      command=update_Z,
                      showvalue=0)
xpos.set(scl_Xvalue.get())
ypos.set(scl_Yvalue.get())
zpos.set(scl_Zvalue.get())
lbl_Xval = tk.Label(main_gui, textvariable=xpos, anchor="e", width=4)
lbl_Yval = tk.Label(main_gui, textvariable=ypos, anchor="e", width=4)
lbl_Zval = tk.Label(main_gui, textvariable=zpos, anchor="e", width=4)

#lbl_Sliders.pack()
lbl_Sliders.grid(row=0, column=1)
lbl_Xlbl.grid(row=1, column=0)
lbl_Ylbl.grid(row=2, column=0)
lbl_Zlbl.grid(row=3, column=0)
scl_Xvalue.grid(row=1, column=1, pady=(15,0))
scl_Yvalue.grid(row=2, column=1, pady=(15,0))
scl_Zvalue.grid(row=3, column=1, pady=(15,0))
lbl_Xval.grid(row=1, column=2)
lbl_Yval.grid(row=2, column=2)
lbl_Zval.grid(row=3, column=2)
btn_reset_pos.grid(row=4, column=1)
display1.grid(row=0, column=1)
display2.grid(row=1, column=1)

#btn_increment.bind("<Button-1>", increment_lbl)

window.mainloop()
