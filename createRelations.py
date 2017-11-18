import os
import sys

relations = {}
with open("data/society-issues/uids", "r") as uidsFile:
	for uid in uidsFile:
		relations[uid[:-1]] = {
			'followings' : set(),
			'followers' : set()
		}
accepted = 0
discarded = 0
with open("data/society-issues/followings", "r") as followingsFile:
	with open("data/society-issues/followers", "r") as followersFile:
		for followingsRecord in followingsFile:
			followersRecord = followersFile.readline()
			uid, followings = followingsRecord.split("\n")[0].split("\t")
			mirror, followers = followersRecord.split("\n")[0].split("\t")
			try:
				assert uid
				assert uid == mirror
				assert followings
				assert followers
				assert relations[uid]
				for following in followings.split(","):
					try:
						assert relations[following]
						relations[uid]["followings"].add(following)
						accepted += 1
					except KeyError:
						discarded += 1
				for follower in followers.split(","):
					try:
						assert relations[follower]
						relations[uid]["followers"].add(follower)
						accepted += 1
					except KeyError:
						discarded += 1
			except AssertionError:
				sys.stderr.write("[" + uid + "] malformatted lines\n")
# sys.stderr.write(str(relations) + "\n")
for uid in relations:
	print uid + "\t" + ",".join(relations[uid]["followers"]) + "\t" + ",".join(relations[uid]["followings"])
sys.stderr.write("kept " + str(accepted) + " relations\n")
sys.stderr.write("discarded " + str(discarded) + " relations\n")
