from enum import Enum
from enum import auto

class NodeType(Enum):
  SOURCE = auto()
  SINK = auto()
  BOTH = auto()

class SegmentDirectionality(Enum):
  DIRECTED = auto()
  UNDIRECTED = auto()

