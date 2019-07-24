import numpy as np
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)
print("parentdir=", parentdir)

from pybullet_envs.deep_mimic.env.pybullet_deep_mimic_env import PyBulletDeepMimicEnv
from pybullet_envs.deep_mimic.learning.rl_world import RLWorld
from pybullet_utils.logger import Logger
from pybullet_envs.deep_mimic.testrl import update_world, update_timestep, build_world
import pybullet_utils.mpi_util as MPIUtil
from mpi4py import MPI

args = []
world = None


def run():
  global update_timestep
  global world
  rank = MPI.COMM_WORLD.Get_rank()
  name = "timings"+str(rank)+".json"
  slot = world.env._pybullet_client.startStateLogging(world.env._pybullet_client.STATE_LOGGING_PROFILE_TIMINGS,name)
  count=1000
  done = False
  while not (done):
    count-=1
    if (count<0):
      world.env._pybullet_client.stopStateLogging(slot)
    update_world(world, update_timestep)

  return


def shutdown():
  global world

  Logger.print2('Shutting down...')
  world.shutdown()
  return


def main():
  global args
  global world

  # Command line arguments
  args = sys.argv[1:]
  enable_draw = False
  world = build_world(args, enable_draw)

  run()
  shutdown()

  return


if __name__ == '__main__':
  main()
