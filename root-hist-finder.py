#/**
 #* @file   root-hist-finder.py
 #* @author Akshay Katre <akshay.k@cern.ch>
 #* @date   Fri Nov 9, 2012
 #*
 #* @brief  This file helps search for histograms/TTree's in root files
 #*
 #*/

#!/usr/bin/env python

import ROOT
import argparse

parser = argparse.ArgumentParser(prog="prog1", description='')
parser.add_argument(type=str, dest="NAME", help="Name of the ROOT file")
parser.add_argument('-f', '--find', default='', dest="FINDNAME", help="Searches with this string")
parser.add_argument('-i', '--icase', dest="CASE",action='store_true',help="Sets cases insensitivity to true, default is false")
parser.add_argument('-p', '--partial', dest="PARTIAL", action="store_true", help="Searches strings which partially contain find name")

args = parser.parse_args()


if args.NAME[-4:] == "root":
  #print "works"
  print args.NAME
else:
  print "Enter a root file" 

filename = args.NAME
find = args.FINDNAME
case = args.CASE
partial = args.PARTIAL


def listdir(dirname):
  dir_keys = dirname.GetListOfKeys()
  return dir_keys

def listtree(treename, findname):
  tree_keys = treename.GetListOfBranches()
  return tree_keys

def compnames(obj, findname):
  directory = listdir(obj)
  for leng in directory:
    object1 = obj.Get(leng.GetName())
    if (object1.IsA().GetName() != 'TDirectoryFile' or object1.IsA().GetName() != 'TTree'):
      name = object1.GetName()
      if name == findname:
	print "found in ", obj.IsA().GetName() , " called ", obj.GetName() 
	#print findname

def PrintTree(obj, findname, casein):
  directory = listtree(obj, findname)
  check = 0
  checkcase = 0
  #print directory
  for ob1 in directory:
    object1 = obj.GetBranch(ob1.GetName())
    #print object1
    if (object1.IsA().GetName() != 'TDirectoryFile' or object1.IsA().GetName() != 'TTree'):
      name = object1.GetName()
      #print name
      for i in range(0, len(name)):
        if len(name[i:i+len(findname)]) == len(findname):
          if (not casein):
	    if (name[i:i+len(findname)] == findname):
	      if (check == 0):
	        print "In" , obj.IsA().GetName(), obj.GetName(), " match for ", find, " as : "
              print  name
              check = 1

          if (casein):
            if(name[i:i+len(findname)].lower() == findname.lower()):
	      #print checkcase
	      if (checkcase == 0):
	        print "In" , obj.IsA().GetName(), obj.GetName(), " match for ", find, " as : "
              print  "\t \t \t", name 
              checkcase = 1


def PrintDir(obj, findname, casein):
    directory = listdir(obj)
    check = 0 
    checkcase = 0 
    for ob1 in directory:
      object1 = obj.Get(ob1.GetName())
      if (object1.IsA().GetName() != 'TDirectoryFile' or object1.IsA().GetName() != 'TTree'):
        name = object1.GetName()
        for i in range(0, len(name)):
          if len(name[i:i+len(findname)]) == len(findname):

	    if (not casein):
	      if (name[i:i+len(findname)] == findname):
	        if check ==0:
		  print "In", obj.IsA().GetName(), obj.GetName(), " match for ", find, " as: "
	        #print "found matches for ", find, " as ", name, " in ", obj.GetName(), " which is : ", obj.IsA().GetName()
	        print name
	        check = 1

            if (casein):
		#print findname
		#print casein
                if(name[i:i+len(findname)].lower() == findname.lower()):
		  if checkcase ==0:
		    print "In", obj.IsA().GetName(), obj.GetName(), " match for ", find, " as: "
	          #print "found matches for ", find, " as ", name, " in ", obj.GetName(), " which is : ", obj.IsA().GetName()
	          print name
  

def partialfind(obj, findname, casein = 'False'):
  #print "Case: ", casein
  leng = len(findname)
  #if obj.IsA().GetName() == 'TDirectoryFile':
    #directory = listdir(obj)
  if obj.IsA().GetName() == 'TTree':
    PrintTree(obj, findname, casein)

	        
	        
  if obj.IsA().GetName() == 'TDirectoryFile':
    PrintDir(obj, findname, casein)


rfile = ROOT.TFile(filename)

#rfile.ls()

keys = rfile.GetListOfKeys()

for count in keys:
  obj = rfile.Get(count.GetName())
  if count.GetName()==find:
    print "It is a ", obj.IsA().GetName(), " in the top directory ", obj.GetMotherDir().GetName()
    obj.ls()
    break
  #if obj.IsA().GetName() == 'TDirectoryFile':
    #print count
    #print "hell0"
  #else:
    #print obj.IsA().GetName()
  if partial:
    partialfind(obj, find, case)
  else:
    compnames(obj,find)

print "searching for: ", find
print "Case: ", case

