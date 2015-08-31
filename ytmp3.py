#**********LIBRARY IMPORTS************
#os for system calls , time for delays so user can read output
import os, time


#**********INSTALLATION AND UPDATES***************************
#This script utilizes ffmpeg, youtube-dl and cdrdao

print "Checking for youtube-dl and FFMpeg..."
time.sleep(3)

os.system("cd /usr/local/bin")
if not os.path.exists('/usr/local/bin/youtube-dl'):
	print "youtube-dl is not installed. Installing now."
	time.sleep(3)
	os.system("sudo wget https://yt-dl.org/downloads/2014.05.12/youtube-dl -O /usr/local/bin/youtube-dl")
	os.system("sudo chmod a+x /usr/local/bin/youtube-dl")
	os.system("sudo chmod rwx /usr/local/bin/youtube-dl")
	print "youtube-dl has been installed."
	print "Now updating youtube-dl..."
	os.system("sudo /usr/local/bin/youtube-dl -U")	
else:
	print "Checking for update to youtube-dl..."
	os.system("sudo /usr/local/bin/youtube-dl -U")
	
if not os.path.exists('/usr/local/bin/ffmpeg'):
	print("FFMpeg is not installed. Installing now.")
	time.sleep(3)
	os.system("sudo wget http://ffmpeg.gusari.org/static/32bit/ffmpeg.static.32bit.latest.tar.gz -O /usr/local/bin/ffmpeg.tar.gz")
	os.system("sudo tar -zxvf /usr/local/bin/*.tar.gz -C /usr/local/bin")
	os.system("sudo chmod a+x /usr/local/bin/ffmpeg")
	os.system("sudo chmod a+x /usr/local/bin/ffprobe")
	os.system("sudo rm ffmpeg.tar.gz")
	print "FFMpeg has been installed."
else:
	print "FFMpeg is already installed."
	
print "Installing/Updating cdrdao through apt-get. This is for burning to CD-R. Install \
manually if you do not use apt-get and wish to burn CDs with this program instead of an external one."
time.sleep(5)
os.system("sudo apt-get install cdrdao")
os.system("clear")


#*************DOWNLOADING VIDEOS/CONVERTING TO MP3**********************

urls = []
currenturl = "1"
while currenturl != "":
	currenturl = raw_input('Enter URL (just hit ENTER to stop and begin downloading): ')
	if currenturl == "":
		break
	urls.append(currenturl)
	
print "Done with queue entry. Downloading videos from YouTube:"
time.sleep(3)

count = 1
for i in urls:
	if count <= 9:
		os.system("/usr/local/bin/youtube-dl -o 'Track_0" + str(count) + "_-_%(title)s.%(ext)s' --restrict-filenames " + i)
	else:
		os.system("/usr/local/bin/youtube-dl -o 'Track_" + str(count) + "_-_%(title)s.%(ext)s' --restrict-filenames " + i)
	count = count + 1
	
print "Finished downloading queue. Finding downloaded videos: "

downloaded = []
for file in os.listdir('.'):
	if file.endswith(".mp4"):
		os.rename(file, file[:-4])
		print file[:-4]
		downloaded.append(file[:-4])
		print "Here are the found files: "
		
print '[%s]' % ', '.join(map(str, downloaded))

print "Now converting videos: "
time.sleep(3)
downloaded.sort()
for x in downloaded:
	os.system('/usr/local/bin/ffmpeg -i ' + x + " " + x + '.mp3')
	
print "Finished converting. Cleaning up: "
time.sleep(3)

for file in downloaded:
	print "Deleting file " + file + "..."
	os.system("rm " + file)
		

#*************BURNING TO CD-R*******************

switch = raw_input("Would you like to burn the downloaded MP3 to CD-R? \
'y' for yes or anything else for no: ")

if switch == "y":
	for file in os.listdir('.'):
		if file.endswith(".mp3"):
			os.system("/usr/local/bin/ffmpeg -i " + file + " " + file + ".wav")
	
	wave = []
	
	for file in os.listdir('.'):
		if file.endswith(".wav"):
			wave.append(file)
	
	wave.sort()
	
	os.system("touch cd.toc")
	os.system("sudo chmod 777 cd.toc")
	
	f = open('cd.toc', 'w')
	f.write('CD_DA\n\n')
	
	for z in wave:
		f.write('\n\nTRACK AUDIO\n')
		f.write('AUDIOFILE "' + z + '" 0')
	f.close()
	
	raw_input("Please place a blank CD-R into your CD drive, then hit ENTER:")
	print "Now burning CD..."
	
	os.system("cdrdao write cd.toc")
	
	for y in wave:
		print "Deleting file " + y + "..."
		os.system("rm " + y)
	
	os.system("rm cd.toc")

else:
	print "Skipping CD burning."
	
	
#*************POST-OPERATION ORGANIZATION*****************

name = raw_input("Give a name to the compilation you've made: ")
name = name.replace(" ", "_")
os.system("mkdir " + name)
os.system("mv *.mp3 " + name)
print "Moved MP3 into a folder called " + name + "."
print "All finished. Enjoy! Hit enter to terminate program."
raw_input("")
