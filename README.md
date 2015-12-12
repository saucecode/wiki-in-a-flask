# wiki-in-a-flask
a tiny markdown-based wiki server

### Installation & Running

	$ pip install flask
	$ pip install markdown

Download this repo and extract anywhere. Run *wiki-in-a-flask.py* to start the server.

### Introduction

**Wiki-in-a-flask** is a tiny, lightweight [Python](https://www.python.org/) based wiki software, which runs using the [flask webserver](http://flask.pocoo.org/) to render [Markdown](https://en.wikipedia.org/wiki/Markdown) files as articles. The wiki is not designed for high load (see: flask), but it will function fine for a number of collaborators.

It does not come with a built-in editing system, so collaborators will need access to the *wiki/* folder on the server's file system. This can be facilitated by FTP access, or putting the folder in a Dropbox.

### Motivation

Wiki-in-a-flask was inspired by the great brevity and detail of [Wookieepedia](https://starwars.wikia.com/wiki/Main_Page), the Star Wars fan wikia. I thought that the idea of mapping out an entire universe, its stories, and lore in encyclopedia fashion would be very helpful to worldbuilders and story-tellers. Lacking a simple and lightweight solution, I have written this server to make organising "articles" of information easy to do.

### Pictures!

So [here](https://i.imgur.com/471kHA8.png) and [here](https://i.imgur.com/cYj1o31.png) is what it looks like.

![Scarlett Johansson](https://i.imgur.com/cYj1o31.png)
