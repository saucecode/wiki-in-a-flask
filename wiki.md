# Test Wiki, Please Ignore

## Introduction

**Wiki-in-a-flask** is a tiny, lightweight [Python](https://www.python.org/) based wiki software, which runs using the [flask webserver](http://flask.pocoo.org/) to render [Markdown](https://en.wikipedia.org/wiki/Markdown) files as articles. This very page was generated from a Markdown file: wiki.md, in the server's working directory. While the wiki is not designed for high load, it will function fine for a number of collaborators.

It does not come with a built-in editing system, so collaborators will need access to the *wiki/* folder on the server's file system. This can be facilitated by FTP access, or putting the folder in a Dropbox.

## Motivation

Wiki-in-a-flask was inspired by the great brevity and detail of [Wookieepedia](https://starwars.wikia.com/wiki/Main_Page), the Star Wars fan wikia. I thought that the idea of mapping out an entire universe, its stories, and lore in encyclopedia fashion would be very helpful to worldbuilders and story-tellers.

## Examples

Here are some example pages copied from wikipedia into the Markdown format, and rendered by this program.

  - [ISO 8601](/wiki/ISO_8601)
  - [Scarlett Johansson](/wiki/Scarlett_Johansson)

And here is the source to those same pages in Markdown. You should be able to understand the Markdown format very quickly. More simplified usage of Markdown is available [here](https://en.wikipedia.org/wiki/Markdown#Example).

  - [ISO 8601 Source](/wiki/ISO_8601/md)
  - [Scarlett Johansson Source](/wiki/Scarlett_Johansson/md)
  - [Scarlett Johansson Sidebar Source](/wiki/Scarlett_Johansson_Detail/md)

Take note of the table format in the sidebar source.
