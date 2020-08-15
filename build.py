#!/usr/bin/python3

import feedparser, time, sys

print("Pulling blog posts...")
feed = feedparser.parse("https://patrik.kernstock.net/feed/")

blogPostsContent = ""

maxCount = 5
curCount = 1
for entry in feed.entries:
	if curCount > maxCount:
		break

	article_link = entry.link.split("/?")[0] + "/"
	blogPostsContent += ('- {}: ({})[{}]\n'.format(time.strftime("%Y-%m-%d %H:00 %Z", entry.published_parsed), entry.title, article_link))
	curCount += 1

blogPostsContent = blogPostsContent.strip()
if blogPostsContent == "":
	print("Blog content empty.")
	sys.exit(1)

print("Preparing files...")
# read template
tmplFile = open("README.tmpl.md", "r")
template = tmplFile.read()
tmplFile.close()

# replace placeholders
newREADME = template.replace("{{BLOG_POSTS}}", blogPostsContent)

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
