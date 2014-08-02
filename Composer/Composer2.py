import music21 

import time
import math
import random
from os import listdir
from os.path import isfile, join
from pprint import pprint

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
    # Create stats etc from data
    print "Instruments and track counts: "
    for instrument_name in self.tracks.keys():
      print instrument_name, len(self.tracks[instrument_name])
      
    print "Extracting ideas..."
    for instrument_name in self.tracks.keys():
      self.ideas[instrument_name] = []
      for track in self.tracks[instrument_name]:
        measures = track.getElementsByClass(music21.stream.Measure)
        for i in range(0, 4):   # grab four random four-measure sequences
          idea = music21.stream.Measure()
          rand_i = random.randint(0, len(measures) - 4)
          for j in range(0, 4):   # four measures
            idea.append(music21.stream.Measure(measures[rand_i + j].getElementsByClass(music21.note.Note)))
          #idea = music21.stream.Measure([note for note in random.choice(measures).getElementsByClass(music21.note.Note)])
          self.ideas[instrument_name].append(idea)
        #idea.show('text')   
    
    print "Extraction done"
  
  def generateSong(self):
    print "-" * 10
    print "Generating song"
    song = music21.stream.Score()
    
    # Initialize instrument tracks
    tracks = []
    for instrument_name in self.tracks.keys():
      avg_amount = len(self.tracks[instrument_name]) / (1.0 * self.input_song_count)
      #print "Average amount of", instrument_name + " per song:", avg_amount
      for i in range(int(round(avg_amount))):
        print "Adding", instrument_name, "track"
        track = music21.stream.Stream()
        instrument = music21.instrument.Instrument()
        instrument.instrumentName = instrument_name
        track.insert(instrument)
        tracks.append(track)
    
    # Populate the tracks
    for track in tracks:
      track_ideas = self.ideas[track.getElementsByClass(music21.instrument.Instrument)[0].instrumentName]
      for j in range(8):
        idea = random.choice(track_ideas)
        tries = 0
        while idea.duration.quarterLength != 4 * 4 and tries < 20:    # only choose 4/4 measures
          idea = random.choice(track_ideas)
          tries += 1
        for i in range(4):              # add some repetition
          for measure in idea:
            for note in measure:
              note_copy = music21.note.Note(note.name)
              note_copy.duration = note.duration
              track.append(note_copy)
    
    # Insert tracks into song
    for track in tracks:
      song.insert(track)
    
    print "Song generated"
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