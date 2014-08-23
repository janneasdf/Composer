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
    target = target.notesAndRests
    target.show('text')
    key = None
    try:
      #key = m.analyze('key')
      key = m.analyze('AardenEssen')
      print "Key for measures", first_measure_index, "to", last_measure_index, ":", key, key.tonic, key.mode
    except:
      print "Couldn't identify key for measures", first_measure_index, "to", last_measure_index
    return key
  
  # Extracts ideas from tracks of a single song.
  # tracks_with_names = dictionary, string (instrument name) -> LIST of parts (instrument track)
  def extractIdeasFromTracks(self, tracks_with_names):
    # Analyze locations to choose ideas from
    track_length_in_measures = len(tracks_with_names.values()[0][0].getElementsByClass('Measure'))
    parts_to_extract = []   # Later probably determined by song structure
    #for i in range(track_length_in_measures / 8):
    #  parts_to_extract.append((i * 8, (i + 1) * 8))
    for i in range((track_length_in_measures / 16) - 1):
      if i > 3:
        break
      parts_to_extract.append((i * 16, (i + 1) * 16))
    
    # Extract keys for of the ideas
    keys_for_parts = []
    tracks = []
    for track_list in tracks_with_names.values():
      for track in track_list:
        tracks.append(track)
    
    for start_end_pair in parts_to_extract:
      part_key = self.analyzeMeasuresKey(tracks, start_end_pair[0], start_end_pair[1])
      keys_for_parts.append(part_key)           # This can be None
    
    if len(parts_to_extract) != len(keys_for_parts):
        print "Error occured while extracting ideas, returning"
        return
    
    # Extract the actual ideas
    print "Extracting ideas"
    new_ideas = {}
    for instrument_name in tracks_with_names.keys():
        new_ideas[instrument_name] = []
    for i in range(len(parts_to_extract)):
        for instrument_name in tracks_with_names.keys():
            for start_end_pair in parts_to_extract:
                if keys_for_parts[i] != None:
                    for track in tracks_with_names[instrument_name]:
                      idea = music21.stream.Stream()
                      for m in track.measures(start_end_pair[0], start_end_pair[1]):
                          idea.append(m)
                      new_ideas[instrument_name].append((keys_for_parts[i], idea))
    
    '''idea = music21.stream.Stream()
    for i in range(4):
      note = music21.note.Note()
      note.pitch.name = 'E4'
      note.duration.type = 'quarter'
      idea.append(note)
    idea_key = self.analyzeMeasuresKey(track, 0, 32) # test code
    new_ideas.append((music21.key.Key('E'), idea))'''
    # idea.show()
    
    # Add ideas to the bank     TODO modify to support the diff. instruments change
    print "Storing ideas"
    for instrument_name in tracks_with_names.keys():
        if instrument_name not in self.ideas.keys():
            self.ideas[instrument_name] = {}
        for idea in new_ideas[instrument_name]:
            length_in_eighths = int(idea[1].duration.quarterLength * 2)
            if length_in_eighths not in self.ideas[instrument_name].keys():
                self.ideas[instrument_name][length_in_eighths] = []
            self.ideas[instrument_name][length_in_eighths].append(idea)
  
  # Returns certain length ideas for instrument, and transposes them to the target key
  def getIdea(self, instrument_name, length_in_eighths, target_key):
    fitting_ideas = self.ideas[instrument_name][length_in_eighths]
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
    try:
        song = music21.converter.parse(filename)
    except:
        print "Something went wrong when parsing " + filename + "; skipping song"
        return
    
    song_name = song.metadata.title;
    song_name = song_name.replace("_", " ")
    if (song_name.replace(" ", "") != ""):
      for word in song_name.split(" "):
        if word.replace(" ", "") != "":
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
    
    self.idea_bank.extractIdeasFromTracks(temp_tracks)
    
    print "Song added"
    self.input_song_count += 1
    
  # Call this once, after adding all songs. Analyzes all input songs for song generating purposes.
  def analyzeInput(self):
    print "-" * 10
      
    print "Analyzing input..."
    # note: no use for this currently since ideas are extracted when adding songs,
    # this function will eventually probably create statistics or something
    print "Analyzing done"
  
  # Generates a new song using the ideas gathered from input songs
  def generateSong(self):
    print "-" * 10
    print "Generating song"
    song = music21.stream.Score()
    song.metadata = music21.metadata.Metadata(title = self.generateName())
    
    # Initialize instrument tracks
    tracks = []
    for instrument_name in self.tracks.keys():
      avg_amount = len(self.tracks[instrument_name]) / (1.0 * self.input_song_count)
      for i in range(int(round(avg_amount))):
        print "Adding", instrument_name, "track"
        track = music21.stream.Stream()
        instrument = music21.instrument.Instrument()
        instrument.instrumentName = instrument_name
        track.insert(instrument)
        tracks.append(track)
    
    # Populate the tracks
    for track in tracks:
      instrument_name = track.getElementsByClass('Instrument')[0].instrumentName
      key = music21.key.Key('C')
      for i in range(4):
        idea = self.idea_bank.getIdea(instrument_name, 16 * 8, key)
        notes = idea[1].notesAndRests
        for note in notes:
          note_copy = music21.note.Note(note.name)
          note_copy.duration = note.duration
          track.append(note_copy)
    
    # Insert tracks to song
    for track in tracks:
      song.insert(track)
    
    return song
  
  # Generates a new song name with words from input song titles
  def generateName(self):
    words = []
    for i in range(random.randint(1, 6)):
      words.append(random.choice(self.song_name_words))
    name = " ".join(words)
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
  if output_name == "":
    output_name = "composer"
  print "Writing MusicXML file (" + output_name + ".xml)"
  song.write('xml', join(output_folder, output_name + ".xml"))
  print "Writing MIDI file (" + output_name + ".mid)"
  song.write('mid', join(output_folder, output_name + ".mid"))
    
if __name__ == '__main__':
  main()