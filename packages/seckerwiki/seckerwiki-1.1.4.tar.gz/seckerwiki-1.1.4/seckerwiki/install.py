"""
functions for installing the seckerwiki cli
"""
import os

EXAMPLE_CONTENTS = """wiki-root: /home/benjamin/Personal/personal
journal-path: Personal/Personal-Management/Journal
journal-password: password
courses:
  tri-1:
    - COMP424
    - NWEN438
    - ENGR401
  tri-2:
    - NWEN439
    - SWEN430
    - ENGR441
  full-year:
    - ENGR489
links:
  - https://trello.com/
  - https://mail.google.com/mail/?shva=1#inbox
  - https://calendar.google.com/calendar/r
  - https://clockify.me/tracker
browser-command: firefox
editor-command: code
"""

def setup():
    path=os.path.expanduser("~/.personal.yml")

    # Don't do anything if path exists
    if os.path.exists(path):
        print("Error: config file ~/.personal.yml exists")
        return False

    with open(path, 'w') as f:
        f.write(EXAMPLE_CONTENTS)
    os.chmod(path,0o600)

    print("Configuration file written to `~/.personal.yml`!")
    print("Edit this file to set the wiki root path and other settings")