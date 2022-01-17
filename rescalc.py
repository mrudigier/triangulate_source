from typing import List, Tuple
import math

TypeVector = List[float]
TypeCoordinate = Tuple[float,float,float]

class ResCal():
  """Calculates intensity ratios for FATIMA detectors. Can then calculate
     the difference to some reference value.

     _init_: Loads the detector positions from file given as argument.
             Loads reference intensity values for 36 FATIMA detectors.
             Initisalises the source position to (0,0,0)

     update: method updates the source position (and thus the intensities)
     update_ref: update reference intensity ratios
     get_res: (inner/outer)
              returns two lists of intensity ratio differences of opposite
              detectors (one for the inner ring and one for the outer rings)
              between calculated and reference intensity ratios.
              If a detector is missing or has intensity 0 in the ref list
              it will be ignored in the calculations and the difference value
              is set to zero.

     get_rms: returns rms of the differences (can be used for
                   optimisation)
 """

  def __init__(self, posfile:str, reffile:str):
    self.res_inner = []
    self.res_outer = []
    self.mean_dev = 1000000000

    self.det_pos = []
    for i in range(0,36):
      self.det_pos.append([0.0,0.0,0.0])

    self.ref_int = []
    self.cal_int = []

    self.ref_ratio_inner = []
    self.ref_ratio_outer = []
    self.cal_ratio_inner = []
    self.cal_ratio_outer = []

    self.dtof_inner = []
    self.dtof_outer = []
    self.c_air = 299.702547  # speed of light in air [mm/ns]

    self.source_pos = [0.0, 0.0, 0.0]
    print("Loading file ", posfile)
    self.loadDetPos(posfile)
    self.loadRefIntensities(reffile)


  def loadDetPos(self, posfile:str):
    with open(posfile, "r") as pf:
      for line in pf:
         if len(line) == 0 or line[0] == '#' or line[0] == '\n':
           continue
         content = line.split()
         if len(content) == 4:
           self.det_pos[int(content[0])] = [float(content[1]),
                                            float(content[2]),
                                            float(content[3])]
         else:
           print("ERROR reading file {}. Check formatting.".format(posfile))
           exit(1)
    print ("Reading detector positions from {}".format(posfile))
    #for i,x in enumerate(self.det_pos):
    #  print(i, self.det_pos[i][0], self.det_pos[i][1], self.det_pos[i][2])
    self.update_cal()

  def loadRefIntensities(self, reffile:str):
    self.ref_int = []
    for i in range(0,36):
      self.ref_int.append(0)

    with open(reffile, "r") as rf:
      for line in rf:
         if len(line) == 0 or line[0] == '#' or line[0] == '\n':
           continue
         content = line.split()
         if len(content) == 2:
           print(line)
           self.ref_int[int(content[0])] = float(content[1])
         else:
           print("line no good '{}'".format(line))
           print("ERROR reading file {}. Check formatting.".format(reffile))
           exit(1)
    #print ("Reading reference intensities from {}".format(reffile))
    #for i,x in enumerate(self.ref_int):
    #  print(i, x)
    self.update_ratio(self.ref_int, self.ref_ratio_inner, self.ref_ratio_outer)

  def update_ratio (self, int_array:TypeVector,
                          inner_array:TypeVector,
                          outer_array:TypeVector) -> TypeVector:
    inner_array.clear()
    for i in range(0,6):
      if (int_array[12+i]!=0 and int_array[18+i]!=0):
        inner_array.append(int_array[12+i]/int_array[18+i])
      else:
        inner_array.append(-1)

    outer_array.clear()
    for i in range(0,12):
      if i < 6:
        j = 30 + i
      else:
        j = 18 + i
      if (int_array[i]!=0 and int_array[j]!=0):
        outer_array.append(int_array[i]/int_array[j])
      else:
        outer_array.append(-1)
    #print("Inner ring:")
    #for i, x in enumerate(inner_array):
    #  print (i, inner_array[i])
    #print("Outer ring:")
    #for j, x in enumerate(outer_array):
    #  print (j, outer_array[j])

  def update_cal(self):
    self.cal_int.clear()
    for i in range(0,36):
      # correct the intensity by a factor depending on the projected area
      # of the detector (first order correction, not accounting for thickness
      # or geometry of the detector.)
      self.cal_int.append(self.cal_angle_corr(self.source_pos, self.det_pos[i])
                      /(self.cal_distance(self.source_pos, self.det_pos[i])**2))
      #self.cal_int.append(1/(self.cal_distance(self.source_pos, self.det_pos[i])**2))
      #print("corrected: ", self.cal_angle_corr(self.source_pos, self.det_pos[i]))
    self.update_ratio(self.cal_int, self.cal_ratio_inner, self.cal_ratio_outer)

  def update_diff(self):
    self.res_inner.clear()
    for i,x in enumerate(self.cal_ratio_inner):
      if (self.cal_ratio_inner[i] < 0 or self.ref_ratio_inner[i] < 0):
        self.res_inner.append(0)
      else:
        self.res_inner.append(self.cal_ratio_inner[i] - self.ref_ratio_inner[i])
    self.res_outer.clear()
    for i,x in enumerate(self.cal_ratio_outer):
      if (self.cal_ratio_outer[i] < 0 or self.ref_ratio_outer[i] < 0):
        self.res_outer.append(0)
      else:
        self.res_outer.append(self.cal_ratio_outer[i] - self.ref_ratio_outer[i])

  def update (self, newPos:TypeCoordinate):
    self.source_pos = newPos.copy()
    #self.update_cal()
    #self.update_diff()
    self.update_tof()
    print("Updated source pos. Current value: {}".format(self.source_pos))

  def get_res_inner(self):
    return self.res_inner

  def get_res_outer(self):
    return self.res_outer

  def get_rms(self):
    dev = 0
    n=len(self.res_inner)
    if (n>0):
      for x in self.res_inner:
        dev += x**2
    n+=len(self.res_outer)
    if (len(self.res_outer)>0):
      for x in self.res_outer:
        dev += x**2
    if n>0:
      return math.sqrt(dev/n)
    else:
      return 1000000000

  def cal_distance(self, sourcepos:TypeCoordinate, detpos:TypeCoordinate) -> float:
    xsqr = (sourcepos[0] - detpos[0])**2
    ysqr = (sourcepos[1] - detpos[1])**2
    zsqr = (sourcepos[2] - detpos[2])**2
    return math.sqrt(xsqr + ysqr + zsqr)

  def cal_angle_corr(self, sourcepos:TypeCoordinate, detpos:TypeCoordinate) -> float:
    scalarprod = ((detpos[0] - sourcepos[0])*detpos[0]
                 + (detpos[1] - sourcepos[1])*detpos[1]
                 + (detpos[2] - sourcepos[2])*detpos[2])
    length_a = self.cal_distance([0,0,0], detpos)
    length_b = self.cal_distance(sourcepos, detpos)
    if( length_a == 0 or length_b == 0):
      return 0
    else:
      return abs(scalarprod/(length_a*length_b))


  def update_tof () -> float:
    dt = 0.0
    self.dtof_inner.clear()
    for i in range(0,6):
      if (self.det_pos[12+i]!=[0,0,0] and self.det_pos[18+i]!=[0,0,0]):
        dt = self.cal_distance(self.source_pos, self.det_pos[12+i]
                               - self.source_pos, self.det_pos[18+i])/self.c_air
        self.dtof_inner.append(dt)
      else:
        self.dtof_inner.append(0.0)

    self.dtof_outer.clear()
    for i in range(0,12):
      if i < 6:
        j = 30 + i
      else:
        j = 18 + i
      if (self.det_pos[i]!=[0,0,0] and self.det_pos[j]!=[0,0,0]):
        dt = self.cal_distance(self.source_pos, self.det_pos[i]
                               - self.source_pos, self.det_pos[j])/self.c_air
        self.dtof_outer.append(dt)
      else:
        self.dtof_outer.append(0.0)

  def get_tof_inner():
    return self.dtof_inner

  def get_tof_outer():
    return self.dtof_outer
