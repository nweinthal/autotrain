import numpy as np
import curses
from curses import wrapper
import time

NUMBER_OF_TRAINS = 10
NUMBER_OF_TRACKS = 2
EAST = 1
WEST = -1
MIN_HEADWAY = 0
SIMULATION_LENGTH = 3
TIMESTEP = 0.1

class Train:
  """
  A Train comes from a source and goes to a sink, with some maximum speed.
  For now let's assume instantaneous acceleration.
  """
  def __init__(self, source, sink, speed):
    self.source = source
    self.sink   = sink
    self.max_speed  = speed
    self.location = source.location
    self.velocity = 0
    source.enqueue(self)

  def set_velocity(self, speed):
    self.velocity = speed*source.direction

  def get_direction(self):
    return np.sign(self.velocity)

class Branch:
  """
  A Train is sourced at one branch and is sunk at another.  An eastbound branch
  sources westbound trains, (negative velocity) and sinks eastbound trains.
  """

  def __init__(self, direction, location):
    self.direction = direction
    self.location  = location
    self.queue = []

  def enqueue(self, train):
    self.queue.append(train)

  def dequeue(self):
    return self.queue.pop(0)

  def trains_waiting(self):
    return len(self.queue)

class Trunk:
  """
  A Trunk has a number of bidirectional tracks, and a set of branches along
  its length.
  """
  class Track:
    def __init__(self):
      self.trains = []

    def can_join(self, train):
      direction = train.get_direction()
      return all(t.get_direction() == direction for t in self.trains)

    def add_train(self, train):
      if not self.can_join(train):
        raise ValueError('Train is in wrong direction for track')

    def running_speed(self):
      if self.trains:
        return min(np.abs(train.max_speed) for train in self.trains)
      return 0

    def is_empty(self):
      return len(self.trains) is 0

  def __init__(self, tracks, length, branches):
    self.tracks = [Trunk.Track() for i in range(tracks)]
    self.length = length
    self.branches = branches

  def run_step(self, timestep):
    for track in self.tracks:
      running_speed = track.running_speed()

      # Block Signal Case
      if track.is_empty():
        for branch in self.branches:
          if branch.trains_waiting():
            track.add_train(branch.dequeue())

      for train in track.trains:
        train.set_velocity(running_speed)
        train.location += train.velocity*timestep
        if train.location >= train.sink.location:
          track.remove(train)

def main(stdscr):
  height, width = stdscr.getmaxyx()
  MESSAGE_LINE = height-1

  simulation_time = 0.0
  branch1 = Branch(EAST, 0)
  branch2 = Branch(WEST, 10)
  branches = [branch1, branch2]
  trunk = Trunk(NUMBER_OF_TRACKS, 10, branches)
  train = Train(branch1, branch2, 1)

  # Simulation TUI
  num = min(height,width)
  buffer = []
  while True:
    c = stdscr.getch()
    if c == ord('q'):
      break
    if c == ord('r'):
      stdscr.addstr(MESSAGE_LINE, 0, "Running Simulation, q to quit",
          curses.A_REVERSE)

      stdscr.addstr(0, 0, "Trunk Line:")
      for num, track in enumerate(trunk.tracks):
        stdscr.addstr(num+1, 2, "Track {}:".format(num))

      for num, branch in enumerate(trunk.branches):
        stdscr.addstr(
      for t in np.arange(0, SIMULATION_LENGTH+TIMESTEP, TIMESTEP):
        trunk.run_step(TIMESTEP)
        timestr = "{0:.3f}".format(t)
        stdscr.addstr(MESSAGE_LINE, width-len(timestr)-1, timestr,
            curses.A_REVERSE)
        stdscr.refresh()
        time.sleep(TIMESTEP)

      stdscr.move(MESSAGE_LINE, 0)
      stdscr.clrtoeol()
      stdscr.addstr(MESSAGE_LINE, 0, "Ran simulation")
    time.sleep(0.1)
wrapper(main)
