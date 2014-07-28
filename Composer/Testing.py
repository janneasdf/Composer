import music21
from music21 import instrument
from music21 import stream
import time
import random
import copy
from os import listdir
from os.path import isfile, join
from pprint import pprint
import numpy as np
import matplotlib as ml
import matplotlib.pyplot as plt

# Measures similarity of two measures, 1.0 means identical
def measureSimilarity(m1, m2):
  # Score for identical notes/chords timings
  same = 0
  different = 0
  for n1 in m1.notes:
    for n2 in m2.notes:
      if n1.offset == n2.offset:
        if n1.fullName == n2.fullName:
          same += 1
        else:
          different += 1
  if len(m1.notes) == 0 and len(m2.notes) == 0:
    return 1.0  # both are empty
  if same + different == 0:
    similarity = 0.0
  else:
    similarity = (1.0 * same) / (same + different)
  # Score for notes used TODO FIX THIS ITS NOT WORKING FOR m1 == m2 AT LEAST
  pitches1 = [x.nameWithOctave for x in m1.pitches] # dont use actual pitches coz refs
  pitches2 = [x.nameWithOctave for x in m2.pitches]
  pitches = pitches1
  for p in pitches2:
    if p not in pitches:
      pitches.append(p)
  diff = len(pitches) - min(len(pitches1), len(pitches2))
  if diff == 0:
    points = 1.0
  if diff == 1:
    points = 0.3
  else:
    points = 0.0
  sum_of_weights = 2.0
  return (similarity + points) / sum_of_weights

# Returns a self-similarity matrix of the measures
def similarityMatrix(measures):
  rows = []
  '''for m1 in measures:
    row = []
    for m2 in measures:
      similarity = measureSimilarity(m1, m2)
      row.append(similarity)
    rows.append(row)'''
  for i in range(len(measures)):
    rows.append([0] * len(measures))
  for i in range(len(measures)):
    for j in range(i, len(measures)):
      similarity = measureSimilarity(measures[i], measures[j])
      rows[i][j] = similarity
      rows[j][i] = similarity
  mat = np.matrix(rows)
  return mat


# Analyze song structure and find bounds.
# Mat = self similarity matrix. 
def calculateBounds(mat):
  min_seg_length = 4	# segment is at least 4 measures long
  threshold = 0.98		# min similarity between "same" measures
  n = mat.shape[0]
  if (mat.shape[0] != mat.shape[1]):
    print "Error: matrix shape is not square!"
  
  bounds = []     # measures where segments begin
  bounds.append(0)
  
  for i in range(n - min_seg_length):
    x = 0
    for j in range(i + min_seg_length, n):
      if (mat[i, j] > threshold):
        x += 1
      else:
        break
    if x > min_seg_length:
      # create segment
      bounds.append(i + x)
  return bounds

# Segment given file
def main():
  filename = 'input/' + raw_input('Enter song filename: ')
  # filename = 'input/oasis_morning_glory.xml'
  print 'Parsing song'
  song = music21.converter.parse(filename)
  final_mat = None
  print 'Song parsed'
  for p in song.parts:
    measures = p.getElementsByClass(stream.Measure)
    n = len(measures)
    mat = similarityMatrix(measures)
    if final_mat == None:
      final_mat = mat
    else:
      final_mat += mat
  print 'Similarity matrix created'
  final_mat *= 1.0 / len(song.parts)
  
  bounds = calculateBounds(final_mat)
  
  print bounds
  
  fig = plt.figure()
  ax = fig.add_subplot(1,1,1)
  ax.set_aspect('equal')
  ax.set_title('Song self-similarity')
  plt.imshow(final_mat, interpolation='nearest', cmap=plt.cm.ocean, extent=(0.5, n+0.5, 0.5, n+0.5))
  plt.colorbar()
  plt.show()


if __name__ == '__main__':
  main()