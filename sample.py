#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt
from treenode import treenode
from ohclustering import ohclustering

def main():
  data = {}
  id = 1
  for line in open('dataset/iris/iris.data'):
    #if id % 10 != 0:
      #id += 1
      #continue
    ds = line.rstrip().split(',')
    if len(ds) < 2:
      break
    tag = str(id) + '-' + ds[4]
    data[tag] = {}
    square = 0.0
    for n in range(0, 4):
      d = float(ds[n])
      data[tag][n] = d
      square += d * d
    norm = sqrt(square)
    #print tag,
    for k, v in data[tag].items():
      data[tag][k] = v/norm
      #print data[tag][k],
    #print
    id += 1
    #if id > 100:
      #break

  ohc = ohclustering()
  root = ohc.clustering(data)
  
  ohc.showDendrogram(root, 100) # Width of dendrogram is 100
  #ohc.showClusters(root)

if __name__ == '__main__':
  main()
