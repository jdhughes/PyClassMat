import os
allfiles = os.listdir(os.getcwd())
for cfile in allfiles:
	if '.tex' in cfile.lower():
		indat = open(cfile,'r').readlines()
		ofp = open(cfile[:-4] + '_handout.tex', 'w')
		for line in indat:
			if '\pause' not in line:
				ofp.write(line)
		ofp.close()
