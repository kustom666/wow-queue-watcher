"""WoW Queue Watcher. Watches your screen and texts you when your wait time is over!

Usage:
  watcher.py <account_sid> <auth_token> <from_number> <to_number>
  watcher.py --version
Options:
  -h --help     Show this screen.
  --version     Show version.
"""
import sys
import time
import numpy as np
import pyscreenshot as ImageGrab
from twilio.rest import Client
from docopt import docopt

if __name__ == '__main__':
  arguments = docopt(__doc__, version='WoW Watcher 1.0')
  client = Client(arguments["<account_sid>"], arguments["<auth_token>"])
  prev_im = np.array(ImageGrab.grab())
  try:
    while True:
      new_img = np.array(ImageGrab.grab())
      mse = ((prev_im - new_img)**2).mean(axis=None)
      if mse > 80:
        print("Difference, triggering text: ", mse)
        message = client.messages.create(
          body="WoW Classic queue watcher: Your wait in the queue is over, hop in!",
          from_=arguments["<from_number>"],
          to=arguments["<to_number>"]
        )
        print(message.sid)
        print("Watcher done, exiting")
        quit(0)
      prev_im = new_img
      time.sleep(5)
  except KeyboardInterrupt:
    print("Exiting")