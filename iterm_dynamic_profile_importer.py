#!/usr/bin/python

""" iTerm2 2.9.20140923 and later allows for the creation of Dynamic Profiles.
	
	I have a list of hosts that I would normally SSH into. This script was written to allow for simple creation of dynamic Profiles
	in iTerm2 for those individual hosts.

	https://iterm2.com/dynamic-profiles.html
"""

import argparse
import json
import os.path
import csv
from os.path import expanduser

# script options
parser = argparse.ArgumentParser(prog="SCRIPT", description="This script will allow you to automatically create dynamic profiles for iTerm2 version 2.9.20140923 or later.")

# Arguments
parser.add_argument("-f", "--file", dest="filename", default="my-dynamic-profiles.plist", help="Name of the dynamic profile plist file. File extension is not required.")
parser.add_argument("-i", "--import", dest="csvImport", help="CSV (comma separated) file. Two columns are accepted for hostnames/ip address and tags.")
parser.add_argument("-r", "--replace", dest="isReplace", action="store_true", default=False, help="If set the content of the dynamic profile will be replaced/overwritten.")
parser.add_argument("-t", "--tags", dest="tags", nargs="+", default=[], help="Tag(s) to apply to the profile.")
parser.add_argument("-l", "--hosts", dest="hosts", nargs="+", help="List of host names or IP addresses")
parser.add_argument("-c", "--command", dest="command", default="ssh {host}", help="The custom SSH command to run. The host name should be entered as '{host}'")

args = parser.parse_args()

""" DEFAULTS

	This is the location where iTerm2 will stores it's Dynamic Profiles
"""
itermDynamicProfilesFile 	= args.filename
iTermDynamicProfilesLoc		= os.path.expanduser("~") + "/Library/Application Support/iTerm2/DynamicProfiles"

#############################################
#############################################

dynamicProfLocation = iTermDynamicProfilesLoc + "/" + itermDynamicProfilesFile
emptyProfileData	= {"Profiles": []}
replaceProfiles 	= args.isReplace
allProfileEntries	= []
profileData = {};

fileExists = os.path.exists(dynamicProfLocation) 

if os.path.exists(iTermDynamicProfilesLoc) == False:
	raise RuntimeError("Missing iTerm2 Dynamic Profiles directory: " + iTermDynamicProfilesLoc + ". Make sure you have installed iTerm2 version 2.9.20140923 or later")

if fileExists:
	with open(dynamicProfLocation) as data_file:
		profileData = json.load(data_file)
else:
	profileData = emptyProfileData

if args.csvImport == None and args.hosts == None:
	raise RuntimeError("A file name (-i) or hosts (-l) is required")

if replaceProfiles == False:
	allProfileEntries = profileData['Profiles']
else:
	#TODO back up old plist in /tmp on replace
	pass

def getProfile(hostname, tags, command):
	""" Returns a profile dictionary. 

		This can be expanded to include other attributes allowed in the iTerm plist
	"""

	return {
       "Name": hostname,
       "Guid": hostname,
       "Custom Command" : "Yes",
       "Tags": tags,
       "Command" : command.replace("{host}", hostname)
	}

if args.csvImport != None:

	with open(args.csvImport, 'rb') as csvfile:
		csvReader = csv.reader(csvfile)

		for row in csvReader:
			host = row[0]

			tags = []
			
			if len(row) >= 2:
				# If the CSV has a second column, merge it with the tags argument values that were passed in
				# and then use that for the profile's tag
				tags = args.tags + row[1].strip().split(' ')

			allProfileEntries.append(getProfile(host, tags, args.command))

elif args.hosts != None:

	for host in args.hosts:
		allProfileEntries.append(getProfile(host, args.tags, args.command))

else:
	raise RuntimeError("A file name (-i) or hosts (-l) is required")

profileData['Profiles'] = allProfileEntries

with open(dynamicProfLocation, 'w') as f:
	f.write(unicode(json.dumps(profileData, ensure_ascii=False)))

