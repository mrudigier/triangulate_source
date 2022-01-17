import tkinter as tk
from resdisplay import ResDisplay
from rescalc import ResCal
from rms_display import RmsDisplay

window = tk.Tk()
window.geometry("900x700")

xpos = tk.DoubleVar()
ypos = tk.DoubleVar()
zpos = tk.DoubleVar()

#rect = Rectangle()
reffile = "FATIMA_intensities.txt"
posfile = "FATIMA_pos.txt"
rc = ResCal(posfile, reffile)

def update_X (val):
  xpos.set(float(val))
  update()
def update_Y (val):
  ypos.set(float(val))
  update()
def update_Z (val):
  zpos.set(float(val))
  update()

def update():
  # first calculate the new intensity and ratio values
  rc.update([xpos.get(), ypos.get(), zpos.get()])
  # update the bar displays
  display1.update(rc.get_tof_inner())
  display2.update(rc.get_tof_outer())
  # update the rms display
  rmsdisplay.update_labels(rc.get_rms(), xpos.get(), ypos.get(), zpos.get())
  #this is probably not necessary
  window.update()

def reset():
  update_X(0)
  update_Y(0)
  update_Z(0)
  # set scaler to rest value [0,0,0]
  scl_Xvalue.set(0)
  scl_Yvalue.set(0)
  scl_Zvalue.set(0)

def load_best():
  reset()
  update_X(rmsdisplay.best_x)
  update_Y(rmsdisplay.best_y)
  update_Z(rmsdisplay.best_z)
  scl_Xvalue.set(rmsdisplay.best_x)
  scl_Yvalue.set(rmsdisplay.best_y)
  scl_Zvalue.set(rmsdisplay.best_z)

def load_ref():
  reset()
  rmsdisplay.reset()
  reffile = ent_load_ref.get()
  rc.loadRefIntensities(reffile)
  update()


main_gui = tk.Frame(window, width=300, height=700)
main_display = tk.Frame(window, width=500, height=700)
#main_gui.grid_propagate(0)
main_gui.grid(row=0,column=0, sticky=tk.N)
main_display.grid(row=0,column=1, sticky=tk.N)

title1 = tk.Label(main_display, text="Inner ring")
display1 = ResDisplay(main_display, 6)
title2 = tk.Label(main_display, text="Outer ring")
display2 = ResDisplay(main_display, 12)
rmsdisplay = RmsDisplay(main_display)
btn_reset_pos = tk.Button(main_gui, text="RESET", command=reset, width = 14)
#btn_load_ref = tk.Button(main_gui, text="LOAD REF.", command=load_ref, width = 14)
#ent_load_ref = tk.Entry(main_gui, width = 30)
#btn_load_best = tk.Button(main_gui, text="LOAD BEST", command = load_best, width = 14)
lbl_Sliders = tk.Label(main_gui,
                       text="Source position")
lbl_Xlbl = tk.Label(main_gui, text="Xpos")
lbl_Ylbl = tk.Label(main_gui, text="Ypos")
lbl_Zlbl = tk.Label(main_gui, text="Zpos")
scl_Xvalue = tk.Scale(main_gui, from_=-100, to=100,
                      orient=tk.HORIZONTAL,
                      width=20, length=200,
                      resolution = 0.2,
                      tickinterval=100,
                      command=update_X,
                      showvalue=0)
scl_Yvalue = tk.Scale(main_gui, from_=-100, to=100,
                      orient=tk.HORIZONTAL,
                      width=20, length=200,
                      resolution = 0.2,
                      tickinterval=100,
                      command=update_Y,
                      showvalue=0)
scl_Zvalue = tk.Scale(main_gui, from_=-100, to=100,
                      orient=tk.HORIZONTAL,
                      width=20, length=200,
                      resolution = 0.2,
                      tickinterval=100,
                      command=update_Z,
                      showvalue=0)
xpos.set(scl_Xvalue.get())
ypos.set(scl_Yvalue.get())
zpos.set(scl_Zvalue.get())
lbl_Xval = tk.Label(main_gui, textvariable=xpos, anchor="e", width=6)
lbl_Yval = tk.Label(main_gui, textvariable=ypos, anchor="e", width=6)
lbl_Zval = tk.Label(main_gui, textvariable=zpos, anchor="e", width=6)

#lbl_Sliders.pack()
lbl_Sliders.grid(row=0, column=1, pady=(30,0), sticky = tk.N)
lbl_Xlbl.grid(row=1, column=0, padx=(15.0))
lbl_Ylbl.grid(row=2, column=0, padx=(15.0))
lbl_Zlbl.grid(row=3, column=0, padx=(15.0))
scl_Xvalue.grid(row=1, column=1, pady=(15,0))
scl_Yvalue.grid(row=2, column=1, pady=(15,0))
scl_Zvalue.grid(row=3, column=1, pady=(15,0))
lbl_Xval.grid(row=1, column=2)
lbl_Yval.grid(row=2, column=2)
lbl_Zval.grid(row=3, column=2)
btn_reset_pos.grid(row=4, column=1)
#btn_load_best.grid(row=5, column=1)
#btn_load_ref.grid(pady=(30,0), row=6, column=1)
#ent_load_ref.grid(row=7, column=1)
#ent_load_ref.delete(0, 'end')
#ent_load_ref.insert(0, reffile)


title1.grid(padx=(20,0), pady=(30,0), sticky=tk.W, row=0, column=1)
display1.grid(padx=(20,0),stick=tk.N, row=1, column=1)
title2.grid(padx=(20,0),sticky=tk.W+tk.N, row=2, column=1)
display2.grid(padx=(20,0),stick=tk.N, row=3, column=1)
rmsdisplay.grid(padx=(20,0), row=4, column=1)
#btn_increment.bind("<Button-1>", increment_lbl)

window.mainloop()
