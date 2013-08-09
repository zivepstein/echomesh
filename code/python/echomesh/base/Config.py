from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import six

from compatibility.weakref import WeakSet

from echomesh.base import Args
from echomesh.base import Join
from echomesh.base import Quit
from echomesh.base import Reconfigure

MERGE_CONFIG = None
CONFIGS_UNVISITED = None  # Report on config items that aren't used.

CLIENTS = WeakSet()

THROW_EXCEPTIONS = True

def reconfigure():
  global MERGE_CONFIG, CONFIGS_UNVISITED
  MERGE_CONFIG = Reconfigure.reconfigure()
  CONFIGS_UNVISITED = copy.deepcopy(MERGE_CONFIG.config)

def add_client(client):
  if not client in CLIENTS:
    CLIENTS.add(client)
    client.config_update(get)

def update_clients():
  for c in CLIENTS:
    c.config_update(get)

def get(*parts):
  config, unvisited = MERGE_CONFIG.config, CONFIGS_UNVISITED
  none = object()
  def get_part(config, part):
    if not isinstance(config, dict):
      raise Exception("Reached leaf configuration for %s: %s" %
                      ('.'.join(parts), config))
    value = config.get(part, none)
    if value is none:
      raise Exception('Couldn\'t find configuration "%s"' % '.'.join(parts))
    return value

  for part in parts[:-1]:
    config = get_part(config, part)
    if unvisited:
      unvisited = unvisited.get(part)

  last_part = parts[-1]
  value = get_part(config, last_part)

  try:
    del unvisited[last_part]
  except:
    pass

  return value

def assign(values):
  return MERGE_CONFIG.assign(values)

def get_unvisited():
  def fix(d):
    if isinstance(d, dict):
      for k, v in list(six.iteritems(d)):
        assert v is not None
        fix(v)
        if v == {}:
          del d[k]
    return d
  if not True:
    return CONFIGS_UNVISITED
  return fix(copy.deepcopy(CONFIGS_UNVISITED))

# Automatically save any changed variables on exit.
def _save_atexit():
  files = get('autosave') and MERGE_CONFIG.save()
  if files:
    from echomesh.util import Log
    Log.logger(__name__).info('Configuration automatically saved to %s.',
                              Join.join_file_names(files))

Quit.register_atexit(_save_atexit)
