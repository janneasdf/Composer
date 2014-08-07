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
  
  def analyzeMeasuresKey(self, tracks, first_measure_index, last_measure_index):
    target = music21.stream.Stream()    # contains the measures to analyze for key
    # All measures are appended (since apparently order etc doesn't matter in K-S key analyzing algorithm)
    for track in tracks:
      for m in track.measures(first_measure_index, last_measure_index):
        target.append(m)
    
    key = None
    try:
      key = m.analyze('key')
    except:
      print "Couldn't identify key for measures", first_measure_index, "to", last_measure_index
    print "key: ", key
    return key
  
  # Extracts ideas from tracks of a single song.
  # tracks_with_names = dictionary, string (instrument name) -> part (instrument track)
  def extractIdeasFromTracks(self, tracks_with_names):
    # Extract ideas (idea = key, measures pair)
    parts_to_extract = [(0, 32)]    # Later probably determined by song structure
    keys_for_parts = []
    tracks = tracks_with_names.values()
    for start_end_pair in parts_to_extract:
      part_key = self.analyzeMeasuresKey(tracks, start_end_pair[0], start_end_pair[1])
      if part_key != None:
        
    
    new_ideas = []
    idea = music21.stream.Stream()
    for i in range(4):
      note = music21.note.Note()
      note.pitch.name = 'E4'
      note.duration.type = 'quarter'
      idea.append(note)
    idea_key = self.analyzeMeasuresKey(track, 0, 32) # test code
    new_ideas.append((music21.key.Key('E'), idea))
    #idea.show()
    
    # Add ideas to the bank
    if instrument_name not in self.ideas.keys():
      self.ideas[instrument_name] = {}
    for idea in new_ideas:
      length_in_eights = int(idea[1].duration.quarterLength * 2)  # todo check divisibility by eights
      print length_in_eights
      if length_in_eights not in self.ideas[instrument_name]:
        self.ideas[instrument_name][length_in_eights] = []
      self.ideas[instrument_name][length_in_eights].append(idea)
    
  
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
  song_name_words = []
  idea_bank = None
  
  def __init__(self):
    self.idea_bank = IdeaBank()

  def addSong(self, filename):
    print "-" * 10
    print "Adding song", filename
    song = music21.converter.parse(filename)
    
    song_name = song.metadata.title;
    song_name = song_name.replace("_", " ")
    if (song_name.replace(" ", "") != ""):
      for word in song_name.split(" "):
        self.song_name_words.append(word)
    
    # Analyze instrument tracks
    temp_tracks = {}    # used for analyzing this specific song's tracks
    for track in song.parts:
      instruments = track.getElementsByClass(music21.instrument.Instrument)
      if len(instruments) != 1:
        print "ERROR: more than one instrument in track"
      instrument = instruments[0]
      if instrument.instrumentName != "Piano":    # Drums turn into piano for some reason
        if instrument.instrumentName not in self.tracks.keys():
          self.tracks[instrument.instrumentName] = []
        self.tracks[instrument.instrumentName].append(track)
        if instrument.instrumentName not in temp_tracks.keys():
          temp_tracks[instrument.instrumentName] = []
        temp_tracks[instrument.instrumentName].append(track)
        #self.idea_bank.addTrack(instrument.instrumentName, track)
    
    self.idea_bank.extractIdeasFromTracks(temp_tracks)
    
    print "Song added"
    self.input_song_count += 1
    
  # Call this once, after adding all songs. Analyzes all input songs for song generating purposes.
  def analyzeInput(self):
    print "-" * 10
      
    print "Extracting ideas..."
    
    print "Extraction done"
  
  # Generates a new song using the ideas gathered from input songs
  def generateSong(self):
    print "-" * 10
    print "Generating song"
    song = music21.stream.Score()
    song.metadata = music21.metadata.Metadata(title = self.generateName())
    return song
  
  # Generates a new song name with words from input song titles
  def generateName(self):
    words = []
    for i in range(random.randint(1, 6)):
      words.append(random.choice(self.song_name_words))
    name = " ".join(words)
    print self.song_name_words
    return name


def main():
  composer = Composer()
  input_folder = 'input'
  output_folder = 'output'
  for filename in [f for f in listdir(input_folder) if isfile(join(input_folder, f))]:
    composer.addSong(join(input_folder, filename))
  composer.analyzeInput()
  song = composer.generateSong()
  output_name = song.metadata.title
  print "Writing MusicXML file (" + output_name + ".xml)"
  song.write('xml', join(output_folder, output_name + ".xml"))
  print "Writing MIDI file (" + output_name + ".mid)"
  song.write('mid', join(output_folder, output_name + ".mid"))
    
if __name__ == '__main__':
  main()