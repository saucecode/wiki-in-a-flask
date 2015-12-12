# wiki-in-a-flask.py
# requires: python2.7, flask (pip), markdown (pip)
from flask import *
import os, mimetypes
import markdown as MD

app = Flask(__name__)
guessType = lambda x:mimetypes.guess_type(x)[0] or 'application/octet-stream'

def loadResource(fname):
	with open(fname,'rb') as f: return f.read()

def render_markdown(md):
	return MD.markdown(md, extensions=['markdown.extensions.tables'])

INDEX_HTML = loadResource('index.html')
TEMPLATE_HTML = '''<!DOCTYPE html>
<html>
	<head>
		<title>{{ title }}</title>
		<style>
			html {
				font-family:Arial;
			}
			a {
				text-decoration:none;
				color:#44f;
			}
			a:hover {
				text-decoration:underline;
			}
			h1, h2 {
				border-bottom:1px solid #aaa;
			}
			#sidebar {
				width:200px;
				vertical-align:top;
			}
			#detail {
				width:250px;
				max-width:250px;
				margin-left:auto;
				margin-right:auto;
				text-align:center;
				vertical-align:top;
				background-color:#dfdfdf;
			}
			#detail table {
				text-align:left;
				border-collapse: collapse;
				font-size:10pt;
				width:100%;
			}
			#detail table tr td, th {
				border:0px solid black;
				padding-top:5px;
				padding-bottom:5px;
				padding-left:3px;
				padding-right:3px;
				vertical-align:top;
			}
			#detail img {
				width:250px;
				height:auto;
			}
			#content {
				vertical-align:text-top;
				width:800px;
				max-width:800px;
				font-size:11pt;
			}
			p {
				font-size:11pt;
			}
			blockquote {
				color:#555;
				background-color:#dfdfdf;
				border-left:4px solid #bbb;
				padding-left:12px;
				padding-top:3px;
				padding-bottom:3px;
				margin:0px;
				margin-right:16px;
				line-height:150%;
			}
			blockquote p {
				font-size:12pt;
			}
			li ul {
				padding-left:20px;
				list-style-type:disc;
			}
		</style>
	</head>
	<body>
		<table style="border:0px solid black;">
			<tr>
				<td id="sidebar">
					<img src="https://upload.wikimedia.org/wikipedia/en/e/ed/Nyan_cat_250px_frame.PNG" width="200" height="200" /><br/>
					<a href="/wiki/">Main page</a>
				</td>
				<td id="content">
					{{ contenthtml }}
				</td>
				<td id="detail">
					{{ detailhtml }}
				</td>
			</tr>
		</table>
	</body>
</html>
'''

@app.route('/')
def indexPage():
	return render_template_string(INDEX_HTML, pagetext="<strong>It works!</strong><br/>wiki-in-a-flask is now running!<br/></br><a href='/wiki/'>Click here to enter the wiki.</a>")

@app.route('/static/<fname>')
def getStaticResource(fname=None):
	if not fname: return abort(404)
	with open('./static/'+fname, 'rb') as f: return Response(f.read(), mimetype=guessType(fname))

@app.route('/wiki/')
def wikiIndexPage():
	return render_template_string(TEMPLATE_HTML,
		title='Wiki Index',
		contenthtml=render_markdown(loadResource('wiki.md'))
	)

@app.route('/wiki/<article>')
def viewArticle(article=None):
	if not article or not os.path.exists('./wiki/%s.md' % (article,)):
		return abort(404)
	detailhtml = ''
	if os.path.exists('./wiki/%s_Detail.md' % (article,)):
		detailhtml = render_markdown(loadResource('./wiki/%s_Detail.md' % (article,)))
	return render_template_string(TEMPLATE_HTML,
		title=article.replace('_',' '),
		contenthtml=render_markdown(loadResource('./wiki/%s.md' % (article,))),
		detailhtml=detailhtml
	)

@app.route('/wiki/<article>/md')
def viewArticleMarkdown(article=None):
	if not article: return abort(404)
	with open('./wiki/%s.md' % (article,), 'rb') as f:
		return Response(f.read(), mimetype='text/plain')


if __name__ == '__main__':
	app.run(threaded=True, debug=True, host='localhost', port=8080)
