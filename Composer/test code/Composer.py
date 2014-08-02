import music21
from music21 import instrument
from music21 import stream
import time
import random
import copy
from os import listdir
from os.path import isfile, join
from pprint import pprint

max_song_length = 8

def main():
	input_folder = "../input"
	output_folder = "../output"
	
	t1 = time.clock()
	last_time = t1;
	instrumentParts = {}
	# Extract instrument parts and names
	for filename in [ f for f in listdir(input_folder) if isfile(join(input_folder, f)) ]:
		print "Parsing", join(input_folder, filename)
		song = music21.converter.parse(join(input_folder, filename))
		print "Instruments in song: "
		for p in song.parts:
			instruments = p.getElementsByClass(instrument.Instrument)
			for i in instruments:
				print i.instrumentName
			if i.instrumentName != 'Piano':	# because drums
				if not i.instrumentName in instrumentParts.keys():
					instrumentParts[i.instrumentName] = []
				instrumentParts[i.instrumentName].append(p)
		# Print parse time info
		current_time = time.clock()
		print "Parsed", filename, "in", current_time - last_time, "sec"
		last_time = current_time
	t2 = time.clock()
	
	# Create output song
	print "Creating song"
	new_parts = []
	for key in instrumentParts.keys():
		parts = instrumentParts[key]
		new_part = stream.Part()
		longest_n = 0
		# Find longest track length
		for part in parts:
			n = len(part.getElementsByClass(stream.Measure))
			if n > longest_n:
				longest_n = n
		if longest_n > max_song_length:
			longest_n = max_song_length
		# Grab longest_n measures from different instrument tracks
		for part in parts:
			ms = part.getElementsByClass(stream.Measure)
			n = len(ms)
			for i in range(longest_n):
				measure = ms[random.randint(0, n-1)]
				new_part.append(copy.deepcopy(measure))
		# Add this new part to the song
		new_parts.append(new_part)
	
	output = stream.Score()
	for part in new_parts:
		output.insert(0, part)
	print "Writing MusicXML file"
	output.write('xml', join(output_folder, "composer.xml"))
	print "Writing MIDI file"
	output = music21.converter.parse(join(output_folder, "composer.xml"))
	output.write('midi', join(output_folder, "composer.mid"))
	
	t3 = time.clock()
	print "All done! \n"
	print "Time spent parsing input:", t2-t1, "sec"
	print "Time spent creating song:", t3-t2, "sec"
	#song.show()

if __name__ == '__main__':
	main()
