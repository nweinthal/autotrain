import sys
import pygame
import pymunk
import random

from pygame.locals import *
from models import *
from constants import *
from collections import namedtuple
import pymunk.pygame_util


Coord = namedtuple('Coord', ['x', 'y'])

station_a = Node(node_type=NodeType.BOTH)
station_b = Node(node_type=NodeType.BOTH)

TRACK_WIDTH = 25
PLATFORM_LENGTH = 50
segment = Segment(station_a, station_b)
#def add_ball(space):
#  """Add a ball to the given space at a random position"""
#  mass = 1
#  radius = 14
#  inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
#  body = pymunk.Body(mass, inertia)
#  x = random.randint(120,380)
#  body.position = x, 550
#  shape = pymunk.Circle(body, radius, (0,0))
#  space.add(body, shape)
#  return shape
#
def add_platform(space, anchor):
  com = pymunk.Body(body_type = pymunk.Body.STATIC)
  com.position = anchor
  width = TRACK_WIDTH
  length = PLATFORM_LENGTH
  ul = Coord(-length/2, width/2)
  ur = Coord(length/2, width/2)
  lr = Coord(length/2, -width/2)
  ll = Coord(-length/2, -width/2)

  poly = pymunk.Poly(com, [ul, ur, lr, ll], radius=2)
  space.add(poly)
  return poly

def add_track(space, node1, node2):
  n1_com = node1.body.position
  n2_com = node2.body.position
  print(n1_com.x)
  com = Coord(
      (n1_com.x+n2_com.x)/2,
      (n1_com.y+n2_com.y)/2,
  )
  width = com.x - n1_com.x
  height = com.y - n1_com.y

  body = pymunk.Body(body_type = pymunk.Body.STATIC)
  body.position = com
  seg = pymunk.Segment(
      body,
      (-width, -height),
      (width, height),
      TRACK_WIDTH/2
  )

  print(com)
  space.add(seg)
  return seg

def main():
  pygame.init()
  screen = pygame.display.set_mode((900, 600))
  pygame.display.set_caption("Simulation")
  clock = pygame.time.Clock()

  space = pymunk.Space()
  p1 = add_platform(space, Coord(100,300))
  p2 = add_platform(space, Coord(800, 300))
  track = add_track(space, p1, p2)
  train = add_train(track)
  draw_options = pymunk.pygame_util.DrawOptions(screen)

  ticks_to_next_ball = 10
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        sys.exit(0)
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
        sys.exit(0)

    screen.fill((255,255,255))

    space.debug_draw(draw_options)

    space.step(1/50.0)

    pygame.display.flip()
    clock.tick(50)

if __name__ == '__main__':
  main()
