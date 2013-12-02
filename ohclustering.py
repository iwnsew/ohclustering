#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt
from treenode import treenode
import random

class ohclustering:
  def __init__(self):
    self.root = None

  def clustering(self, data):
    items = data.items()
    random.shuffle(items)
    for id, vec in items:
      #print id
      n = self.root
      sstack = [1]

      # First node
      if n is None:
        self.root = treenode(set([id]), vec, 1.0)
        continue

      # Down
      while n.left is not None:
        lscore = sqrt(self.updateSquare(n.left.square, n.left.vec, vec))
        rscore = sqrt(self.updateSquare(n.right.square, n.right.vec, vec))
        loldscore = sqrt(n.left.square)
        roldscore = sqrt(n.right.square)
        score = 0.0
        if lscore - loldscore >= rscore - roldscore:
          n = n.left
          score = lscore
        else:
          n = n.right
          score = rscore
        if score / (len(n.idset) + 1) > sqrt(n.parent.square) / len(n.parent.idset):
          sstack.append(1)
        else:
          sstack.append(0)
        pscore = score

      # Up
      while n is not None:
        if sstack.pop() > 0:
          d = treenode(set([id]), vec, 1.0)
          newidset = n.idset.union(d.idset)
          newvec = n.vec.copy()
          newsquare = self.updateSquareAndVec(n.square, newvec, vec)
          newnode = treenode(newidset, newvec, newsquare, n.parent, n, d)
          newnode.left.parent = newnode
          newnode.right.parent = newnode
          if newnode.parent is not None:
            if newnode.parent.left == n:
              newnode.parent.left = newnode
            else:
              newnode.parent.right = newnode
          n = newnode
          while n.parent is not None:
            n.parent.square = self.updateSquareAndVec(n.parent.square, n.parent.vec, vec)
            n.parent.idset.add(id)
            n = n.parent
          self.root = n
          break
        else:
          n = n.parent

    return self.root

  def updateSquare(self, square, vec, diffvec):
    newsquare = square
    for k, v in diffvec.items():
      diff = 0.0
      if vec.has_key(k):
        diff = (vec[k] + v) * (vec[k] + v) - vec[k] * vec[k]
      else:
        diff = v * v
      newsquare += diff
    return newsquare

  def updateSquareAndVec(self, square, vec, diffvec):
    newsquare = square
    for k, v in diffvec.items():
      diff = 0.0
      if vec.has_key(k):
        diff = (vec[k] + v) * (vec[k] + v) - vec[k] * vec[k]
        vec[k] = vec[k] + v
      else:
        diff = v * v
        vec[k] = v
      newsquare += diff
    return newsquare

  def showDendrogram(self, node, width=100, sstack=[], pos=0, det=0.01):
    score = sqrt(node.square) / len(node.idset)
    pscore = 1.0
    if node.parent is None: # Root node
      if width < 30:
        width = 30
      det = (1.0 - score) / (width - 3)
    else:
      pscore = sqrt(node.parent.square) / len(node.parent.idset)
    if node.left is not None:
      if pos < 0: # Left node
        self.showDendrogram(node.left, width, sstack, -1, det)
        sstack.append(pscore)
        sstack.append(score)
        self.printDendrogramLine('', sstack, width, det)
        sstack.pop()
        self.showDendrogram(node.right, width, sstack, 1, det)
        sstack.pop()
      elif pos > 0: # Right node
        sstack.append(pscore)
        self.showDendrogram(node.left, width, sstack, -1, det)
        sstack.append(score)
        self.printDendrogramLine('', sstack, width, det)
        sstack.pop()
        sstack.pop()
        self.showDendrogram(node.right, width, sstack, 1, det)
      else: # Root node
        self.showDendrogram(node.left, width, sstack, -1, det)
        sstack.append(score)
        self.printDendrogramLine('', sstack, width, det)
        sstack.pop()
        self.showDendrogram(node.right, width, sstack, 1, det)
    else:
      sstack.append(pscore)
      for id in node.idset:
        self.printDendrogramLine(id, sstack, width, det)
      sstack.pop()
    return

  def printDendrogramLine(self, id, sstack, width, det):
    space = ''
    s = 1.0
    flag = 1
    if id == '': # Inter node
      flag = 2
    for d in reversed(sstack):
      #print d,
      if s + det <= d:
        flag -= 1
        continue
      while s > d:
        if flag == 1:
          space = '-' + space
        else:
          space = ' ' + space
        s -= det
      if flag >= 1:
        space = '+' + space
      else:
        space = '|' + space
      s -= det
      flag -= 1
    while len(space) < width:
      space = ' ' + space
    print space, id
    return

  def showClusters(self, node):
    if node.left is not None:
      print '(',
      self.showClusters(node.left)
      print ',',
      self.showClusters(node.right)
      score = sqrt(node.square)/len(node.idset)
      print ', %.4f' % score,
      print ')',
    else:
      for id in node.idset:
        print id,
    return

