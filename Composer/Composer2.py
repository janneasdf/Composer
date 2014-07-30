import music21 

import time
import math
import random
from os import listdir
from os.path import isfile, join
from pprint import pprint

class Composer:
	input_song_count = 0			# amount of songs parsed
	tracks = {} 					# string -> list of tracks for instrument
	ideas = {}						# string -> list of ideas for instrument
	
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
			if instrument.instrumentName != "Piano":		# Drums turn into piano for some reason
				if instrument.instrumentName not in self.tracks:
					self.tracks[instrument.instrumentName] = []
				self.tracks[instrument.instrumentName].append(track)
		
		print "Song added"
		self.input_song_count += 1
		
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
				idea = music21.stream.Measure([note for note in measures[0].getElementsByClass(music21.note.Note)])
				self.ideas[instrument_name].append(idea)
				idea.show('text')		
		
		print "Extraction done"
	
	def generateSong(self):
		print "-" * 10
		print "Generating song"
		song = music21.stream.Score()
		
		# Add instrument tracks
		for instrument_name in self.tracks.keys():
			avg_amount = len(self.tracks[instrument_name]) / (1.0 * self.input_song_count)
			print "Average amount of", instrument_name + " per song:", avg_amount
			for i in range(int(round(avg_amount))):
				print "Adding", instrument_name, "track"
				track = music21.stream.Stream()
				song.insert(track)
		# Populate the tracks
		for track in song.parts:
			for j in range(8):
				print "adding note"
				note = music21.note.Note()
				note.pitch.name = 'E4'
				note.duration.type = 'quarter'
				track.append(note)
			
		
		print "Song generated"
		return song


def main():
	composer = Composer()
	input_folder = 'input'
	output_folder = 'output'
	for filename in [f for f in listdir(input_folder) if isfile(join(input_folder, f))]:
		composer.addSong(join(input_folder, filename))
	composer.analyzeInput()
	song = composer.generateSong()
	print "Writing MusicXML file"
	song.write('xml', join(output_folder, "composer.xml"))
		
if __name__ == '__main__':
	main()