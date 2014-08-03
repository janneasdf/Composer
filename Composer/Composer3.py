import music21 

import time
import math
import random
from os import listdir
from os.path import isfile, join
from pprint import pprint

# Parses tracks for ideas and stores them as well as analyzes the key they are in
class IdeaBank:
  ideas = {}            # string (instrument name) -> (string (length) -> list of (key, stream) pairs)
  
  def __init__(self):
    pass
  
  def addTrack(self, measure):
    # Extract ideas
    pass
  
  # Returns certain length ideas for instrument, and transposes them to the target key
  def getIdea(instrument_name, length_in_eighths, target_key):
    fitting_ideas = self.ideas[instrument_name][length_in_eights]
    if len(fitting_ideas) == 0:
      raise Exception('No fitting idea found')
    idea = random.choice(fitting_ideas)
    return idea
  
class Composer:
  input_song_count = 0      # amount of songs parsed
  tracks = {}           # string -> list of tracks for instrument
  ideas = {}            # string -> list of ideas for instrument
  
  def __init__(self):
    pass

  def addSong(self, filename):
    print "-" * 10
    print "Adding song", filename
    song = music21.converter.parse(filename)
    
    # Analyze instrument tracks
    for track in song.parts:
      instruments = track.getElementsByClass(music21.instrument.Instrument)
      if len(instruments) != 1:
        print "ERROR: more than one instrument in track"
      instrument = instruments[0]
      if instrument.instrumentName != "Piano":    # Drums turn into piano for some reason
        if instrument.instrumentName not in self.tracks.keys():
          self.tracks[instrument.instrumentName] = []
        self.tracks[instrument.instrumentName].append(track)
    
    print "Song added"
    self.input_song_count += 1
    
  # Call this once, after adding all songs. Analyzes all input songs for song generating purposes.
  def analyzeInput(self):
    print "-" * 10
      
    print "Extracting ideas..."
    
    print "Extraction done"
  
  def generateSong(self):
    print "-" * 10
    print "Generating song"
    song = music21.stream.Score()
    
    return song


def main():
  composer = Composer()
  input_folder = 'input'
  output_folder = 'output'
  output_name = 'composer'
  for filename in [f for f in listdir(input_folder) if isfile(join(input_folder, f))]:
    composer.addSong(join(input_folder, filename))
  composer.analyzeInput()
  song = composer.generateSong()
  print "Writing MusicXML file (" + output_name + ".xml)"
  song.write('xml', join(output_folder, output_name + ".xml"))
  print "Writing MIDI file (" + output_name + ".mid)"
  song.write('mid', join(output_folder, output_name + ".mid"))
  key = song.analyze('key')
    
if __name__ == '__main__':
  main()