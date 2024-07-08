# Demonstrate Python Binary Tree Treap implmenentation
# Using star dataset from:
# http://www.projectrho.com/public_html/starmaps/catalogues.php

# based on:
# https://www.javatpoint.com/treap-data-structure

import csv
import time
import random
from datetime import datetime

import tree_print as tp

# Data on one star
class Star():
    def __init__( self, habhvg, name, mag, spectral, habit, dist):
        self.habhvg = habhvg
        self.display_name = name
        self.magnitude = mag
        self.spectral_class = spectral
        self.habitable = habit
        self.distance_parsecs = dist

    def print_me(self):
        print("display_name=" + self.display_name + ", magnitude =" + self.magnitude)
        print("habhvg="+ self.habhvg + ", spectral="+ self.spectral_class+ ", habitable="+ self.habitable)

    def print_name(self):
        print(self.display_name)

# Wrap info for one star in a node suitable for placing in the treap
# Based very loosely on https://www.javatpoint.com/treap-data-structure
class TreapNode():
    def __init__(self, star ):
        self.left = None
        self.right = None
        self.star_info = star
        self.name = "N" + str(self.star_info.habhvg)
        self.key = star.display_name
        self.priority = random.randint(0, 5000)

    def print_key( self ):
        print( self.key)
        
    def print_me(self):
        print( "node name =" + self.name)
    
        if self.left is None:
            print( "left is None")
        else:
            print( "left child:", end="")
            self.left.print_me()
            
        if self.right is None:
            print("right is None")
        else:
            print( "right child:", end="")
            self.right.print_me()

        if self.star_info is None:
            print("value is None", end="")
        else:
           self.star_info.print_me()

# Utilites based on:
# # Based on: https://www.techiedelight.com/implementation-treap-data-structure-cpp-java-insert-search-delete/
def rotateLeft( root):

    R = root.right
    X = root.right.left
 
    # rotate
    R.left = root
    root.right = X
 
    # set a new root
    return R


''' Function to right-rotate a given treap
 
        r                        L
       / \     Right Rotate     / \
      L   R       ———>         X   r
     / \                          / \
    X   Y                        Y   R
'''


def rotateRight( root):
 
    L = root.left
    Y = root.left.right
 
    # rotate
    L.right = root
    root.left = Y
 
    # set a new root
    return L


# Recursive function to insert a given key with a priority into treap
# Based on: https://www.techiedelight.com/implementation-treap-data-structure-cpp-java-insert-search-delete/
def insertNode(root, star):
 
    # base case
    if root is None:
        return TreapNode(star)
 
    # if the given data is less than the root node, insert in the left subtree;
    # otherwise, insert in the right subtree
    if star.display_name < root.key:
        root.left = insertNode(root.left, star)
 
        # rotate right if heap property is violated
        if root.left and root.left.priority > root.priority:
            pass
            # uncomment this roateRight() line and the line with rotateLeft()
            # below to see the effect of the Treap algorithm
            #root = rotateRight(root)
    else:
        root.right = insertNode(root.right, star)
 
        # rotate left if heap property is violated
        if root.right and root.right.priority > root.priority:
            pass
            # uncomment this rotateLeft() line and the rotateRight() line
            # above to see the effect of the Treap algorithm
            #root = rotateLeft(root)
 
    return root

# Binary Search Tree, augmented with a random priority to make a Treap
class Treap():
    def __init__(self, name):
        self.name = name
        self.node_num = 0
        self.node_list= []
        self.root = None
        # seed random number generator to get a different sequne
        # every time
        random.seed(datetime.now())
            
    def preorder_print( self, root ):
        if root is None:
            return

        self.preorder_print(root.left)
        root.print_key()
        self.preorder_print(root.right)

    
    def search( self, key):
        current_node = self.root
        while current_node is not None:
            if current_node.key == key:
                return current_node
            elif key <current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return None

# 
# main starts here
#
def main():

    # Instantiate Binary Searcj Tree (Treap) to hold the stars
    star_treap = Treap( "Star Catalog")
    
    # Load the CSV with the star info, assuming first row is labels
    #with open('./data/HabHyg_short.csv','r') as csvfile:
    #with open('./data/HabHYG_shuffled.csv','r') as csvfile:
    with open('./data/HabHYG_sorted.csv','r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')

        # skip header row
        next(csvfile)
            
        obs_processed = 0

        # Create a new star and then insert it into the star_treap
        for row in lines:
            # habhvg, name, mag, spectral, habit, dist)
            this_star = Star(row[0], row[3], row[16], row[11], row[2], row[12] ) 
            star_treap.root = insertNode( star_treap.root, this_star )
            obs_processed = obs_processed + 1

    print("obs_processed = " + str(obs_processed))

    # Your test and debug code here...
    #star_treap.preorder_print( star_treap.root)

    # print the tree
    tp.printTree(star_treap.root, None, False)
    print()

    # get time in nanoseconds -- maybe OS-specific?
    # See https://docs.python.org/3/library/time.html
    t0 = time.perf_counter_ns() 
    
    # test search Procyon
    node_found = star_treap.search( "Procyon")
    if node_found is None:
        print( "Not found")
    else:
        node_found.star_info.print_me()

    # test search Kapteyn's Star
    node_found = star_treap.search( "Kapteyn's Star")
    if node_found is None:
        print( "Not found")
    else:
        node_found.star_info.print_me()

    # test search for Barnard's star
    node_found = star_treap.search( "Barnard's Star")
    if node_found is None:
        print( "Not found")
    else:
        node_found.star_info.print_me()  

    # test search for Gl 406 star
    node_found = star_treap.search( "Gl 406")
    if node_found is None:
        print( "Not found")
    else:
        node_found.star_info.print_me()  

    t1 = time.perf_counter_ns() - t0
    print( "elapsed ms = " + str(t1 / 1000))
    
if __name__ == "__main__":
    main()
