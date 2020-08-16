#!/usr/bin/python3

import sys, os, time, datetime
import feedparser

os.environ['TZ'] = 'UTC'

print("Pulling blog posts...")
feed = feedparser.parse("https://patrik.kernstock.net/feed/")

blogPostsContent = ""

maxCount = 5
curCount = 1
for entry in feed.entries:
	if curCount > maxCount:
		break

	article_link = entry.link.split("/?")[0] + "/"
	blogPostsContent += ('- {}: <a href="{}" target="_blank">{}</a>\n'.format(time.strftime("%Y-%m-%d %H:00 %Z", entry.published_parsed), article_link, entry.title))
	curCount += 1

blogPostsContent = blogPostsContent.strip()
if blogPostsContent == "":
	print("Blog content empty.")
	sys.exit(1)

currentTime = datetime.datetime.now(tz=datetime.timezone.utc)
lastUpdate = currentTime.strftime("%Y-%m-%d %H:%m %Z")

print("Preparing files...")
# read template
tmplFile = open("README.tmpl.md", "r")
newREADME = tmplFile.read()
tmplFile.close()

# replace placeholders
newREADME = newREADME.replace("{{BLOG_POSTS}}", blogPostsContent)
newREADME = newREADME.replace("{{BLOG_POSTS_LASTUPDATE}}", lastUpdate)

# load current file
oldFile = open("README.md", "r")
oldREADME = oldFile.read()
oldFile.close()

# write when different.
if oldREADME != newREADME:
	print("Writing...")
	# write new file
	newFile = open("README.md", "w")
	newFile.write(newREADME)
	newFile.close()
else:
	print("Nothing to update.")
