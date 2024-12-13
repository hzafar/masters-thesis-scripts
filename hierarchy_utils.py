import constants
import os

class HierarchyUtils:
  """A class containing utility methods for working with the OpenAlex concept hierarchy."""

  def __init__(self):
    pass

  def get_concept(self, path):
    """Given a path string of the form '[concept]->[ancestor]->[ancestor]->...->[ancestor],
       return the concept that is the base of the path."""

    first = path.find('->')
    return path[:first]
  
  def get_ancestor(self, path):
    """Given a path string of the form '[concept]->[ancestor]->[ancestor]->...->[ancestor],
       return the concept that is at the end of the path, i.e., the topmost ancestor."""

    last = path.rfind('->') + 2
    return path[last:]

  def related_ancestors(self, ancestors):
    """Checks whether the given set of ancestors are all related (i.e., all belong to the
       same L0 grouping)."""

    return any(ancestors.intersection(group) == ancestors for group in constants.L0_GROUPINGS)

  def common_tail(self, paths):
    """Returns the largest common tail of all the given paths."""

    return os.path.commonprefix(paths)
