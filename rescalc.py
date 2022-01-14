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
     get_res: returns two lists of intensity ratio differences of opposite
              detectors (one for the inner ring and one for the outer rings)
              between calculated and reference intensity ratios.
              If a detector is missing or has intensity 0 in the ref list
              it will be ignored in the calculations and the difference value
              is set to zero.
 """

  def __init__(self, posfile:str, reffile:str):
    self.res_inner = []
    self.res_outer = []

    self.det_pos = []
    for i in range(0,36):
      self.det_pos.append([0.0,0.0,0.0])

    self.ref_int = []
    self.cal_int = []

    self.ref_ratio_inner = []
    self.ref_ratio_outer = []
    self.cal_ratio_inner = []
    self.cal_ratio_outer = []

    self.source_pos = [0.0, 0.0, 0.0]

    self.loadDetPos(posfile)
    self.loadRefIntensities(reffile)


  def loadDetPos(self, posfile:str):
    with open(posfile, "r") as pf:
      for line in pf:
         if len(line) == 0 or line[0] == '#':
           continue
         content = line.split()
         if len(content) == 4:
           self.det_pos[int(content[0])] = [float(content[1]),
                                            float(content[2]),
                                            float(content[3])]
         else:
           print("ERROR reading file {}. Check formatting.".format(posfile))
           exit(1)
    #print ("Reading detector positions from {}".format(posfile))
    #for i,x in enumerate(self.det_pos):
    #  print(i, self.det_pos[i][0], self.det_pos[i][1], self.det_pos[i][2])
    self.update_cal()

  def loadRefIntensities(self, reffile:str):
    for i in range(0,36):
      self.ref_int.append(0)

    with open(reffile, "r") as rf:
      for line in rf:
         if len(line) == 0 or line[0] == '#':
           continue
         content = line.split()
         if len(content) == 2:
           self.ref_int[int(content[0])] = float(content[1])
         else:
           print("ERROR reading file {}. Check formatting.".format(posfile))
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
      self.cal_int.append(1/(self.cal_distance(self.source_pos, self.det_pos[i])**2))
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
    self.update_cal()
    self.update_diff()
    print("Updated source pos {}".format(self.source_pos))

  def get_res_inner(self):
    return self.res_inner
  def get_res_outer(self):
    return self.res_outer

  def cal_distance(self, sourcepos:TypeCoordinate, detpos:TypeCoordinate) -> float:
    xsqr = (sourcepos[0] - detpos[0])**2
    ysqr = (sourcepos[1] - detpos[1])**2
    zsqr = (sourcepos[2] - detpos[2])**2
    return math.sqrt(xsqr + ysqr + zsqr)
