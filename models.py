from constants import *


class Node:
  def __init__(self, *args, **kwargs):
    self.node_type = kwargs.get('node_type', NodeType.BOTH)
    self.tracks = kwargs.get('tracks', 1)

class Segment:
  def __init__(self, source: Node, sink: Node, **kwargs) -> None:
    self.directionality = kwargs.get('directionality',
        SegmentDirectionality.UNDIRECTED)

    self.source = source if source else kwargs.get('source')
    self.sink = sink if sink else kwargs.get('sink')

    if self.source is self.sink:
      raise ValueError("Can't have an empty segment")
