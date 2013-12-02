#!/usr/bin/python
# -*- coding: utf-8 -*-

class treenode:
  def __init__(self, idset=set([]), vec={}, square=0.0, parent=None, left=None, right=None):

    # Data
    self.idset = idset # nodesize = len(self.idset)
    self.vec = vec
    self.square = square # score = sqrt(self.square) / nodesize

    # Tree structure
    self.parent = parent
    self.left = left
    self.right = right

