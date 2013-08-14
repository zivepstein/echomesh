from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

from echomesh.util import Log
from echomesh.util import Subprocess
from echomesh.element import Element

LOGGER = Log.logger(__name__)

_ARGS = {'stdin': subprocess.PIPE,
         'stdout': subprocess.PIPE,
         'stderr': subprocess.PIPE}

class Execute(Element.Element):
  def __init__(self, parent, description):
    super(Execute, self).__init__(parent, description)
    self.command_line = [description['binary']] + description.get('args', [])

  def _on_run(self):
    super(Execute, self)._on_run()
    self.process = subprocess.Popen(command, _ARGS)
    result = popen.stdout.read()
    if not popen.returncode:
      pass # Send out a message.
    self.process = None
    self.pause()

  def _on_pause(self):
    super(Execute, self)._on_pause()
    if self.process:
      self.process.kill()
      self.process = None


