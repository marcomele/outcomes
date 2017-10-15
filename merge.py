import os

categories = {
	"health" : {
		"diseases" : 4,
		"mental" : 45,
		"pharmacy" : 3
	},
	"society" : {
		"issues" : 1,
		"law" : 9,
		"relationships" : 2
	},
	"business" : {
		"construction-and-maintenance" : 1,
		"financial-services" : 4,
		"investing" : 76
	}
}
folder = "mergedData"
os.system("rm -rf " + folder)
os.system("mkdir " + folder)

for category in categories:
	for subcat in categories[category]:
		with open(folder + "/" + category + "-" + subcat + "_ids.txt", "w") as outFile:
			print "merging files for " + category + "/" + subcat + "..."
			for n in xrange(categories[category][subcat]):
				filename = "previous-data/" + category + "/twitter_" + category + "_" + subcat + "_2014-03-01_2014-05-31_tweetids_" + str(n) + ".txt"
				with open(filename, "r") as infile:
					for line in infile:
						outFile.write(line)
print "done"
