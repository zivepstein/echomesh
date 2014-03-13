from __future__ import absolute_import, division, print_function, unicode_literals

import itertools

from echomesh.pattern.Pattern import Pattern

class Choose(Pattern):
  SETTINGS = {
    'choose': {'default': 0},
  }

  def _evaluate(self):
    length = len(self._patterns)
    def restrict(size):
      return int(max(0, min(length - 1, size)))
    choose = self.get('choose')
    return self._patterns[restrict(choose)].evaluate()

