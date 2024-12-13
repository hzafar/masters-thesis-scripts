from math import sqrt

L0_COLOURS_MAP = {
  'Business': (235, 120, 71),
  'Sociology': (235, 169, 71),
  'Psychology': (235, 218, 71),
  'Environmental science': (153, 235, 71),
  'Geography': (104, 235, 71),
  'Geology': (71, 235, 88),
  'Biology': (71, 235, 137),
  'Medicine': (71, 235, 186),
  'Chemistry': (71, 235, 235),
  'Engineering': (71, 186, 235),
  'Materials science': (71, 137, 235),
  'Physics': (71, 88, 235),
  'Mathematics': (104, 71, 235),
  'Computer science': (153, 71, 235),
  'Economics': (202, 71, 235),
  'Political science': (235, 71, 218),
  'History': (235, 71, 88),
  'Philosophy': (235, 71, 169),
  'Art': (235, 71, 71)
}

class VizUtils:
  """Class to hold utility methods used in visualizations."""

  def __init__(self):
    pass

  def average_rgb(self, colours):
    """Averages the RGB value of all the colours provided."""

    reds = sum([r**2 for r,g,b in colours])
    greens = sum([g**2 for r,g,b in colours])
    blues = sum([b**2 for r,g,b in colours])
  
    n = len(colours)
  
    return (round(sqrt(reds/n)), round(sqrt(greens/n)), round(sqrt(blues/n)))

  def get_colour(self, l0_concept):
    return L0_COLOURS_MAP[l0_concept]

