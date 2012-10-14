from __future__ import absolute_import, division, print_function, unicode_literals

import alsaaudio
import analyse
import numpy

from util import Util
from util import ThreadLoop

DEFAULT_CARD = 'sysdefault:CARD=AK5370'

def mic_input(config):
  conf = config['mic']
  card = conf.get('card', DEFAULT_CARD)
  mic = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
  mic.setchannels(1)
  if 'samplerate' in conf:
    mic.setrate(conf['samplerate'])

  if 'periodsize' in conf:
    mic.setperiodsize(conf['periodsize'])

  return mic

def get_mic_level(mic):
  length, data = mic.read()
  samps = numpy.fromstring(data, dtype=numpy.int16, count=length)
  return analyse.loudness(samps)

def run_mic_levels_thread(callback, config):
  mic = mic_input(config)
  cb_different = Util.call_if_different(callback)
  levels = config['mic']['levels']
  def cb():
    level = get_mic_level(mic)
    slot = Util.level_slot(level, levels)
    cb_different(slot)

  return ThreadLoop.ThreadLoop(cb)
