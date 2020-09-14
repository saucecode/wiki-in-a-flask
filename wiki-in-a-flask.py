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

INDEX_HTML = loadResource('index.html').decode()
with open('template.html','r') as f: TEMPLATE_HTML = f.read()

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
		contenthtml=render_markdown(loadResource('wiki.md').decode())
	)

@app.route('/wiki/<article>')
def viewArticle(article=None):
	if not article:
		return abort(404)
	if not os.path.exists('./wiki/%s.md' % (article,)):
		return "This page does not yet exist!<br/><a href='/createpage/%s'>Create!</a>" % article
	detailhtml = ''
	if os.path.exists('./wiki/%s_Detail.md' % (article,)):
		detailhtml = render_markdown(loadResource('./wiki/%s_Detail.md' % (article,)).decode())
	return render_template_string(TEMPLATE_HTML,
		title=article.replace('_',' '),
		contenthtml=render_markdown(loadResource('./wiki/%s.md' % (article,)).decode()),
		detailhtml=detailhtml
	)

@app.route('/wiki/<article>/md')
def viewArticleMarkdown(article=None):
	if not article: return abort(404)
	with open('./wiki/%s.md' % (article,), 'r') as f:
		return Response(f.read(), mimetype='text/plain')

@app.route('/createpage/<article>')
def createArticle(article=None):
	if not article: return abort(404)
	if os.path.exists('./wiki/%s.md' % article): return "<a href='/wiki/%s'>This page already exists!</a>" % article
	with open('./wiki/%s.md'%article ,'w') as f: f.write(article.replace('_',' ') + '\n=======')
	return "<a href='/wiki/%s'>Article created.</a>" % article

@app.route('/search/')
def searchWiki():
	query = request.args.get('query').replace(' ','_')
	files = [x for x in os.listdir('./wiki/') if not x.endswith('_Detail.md')]
	results = ['<a href="/wiki/'+x[:-3]+'">'+x[:-3].replace('_',' ')+'</a>' for x in files if query.lower() in x.lower()]
	return 'Found %i results!<br/>' % len(results) + '<br/>'.join(results)

if __name__ == '__main__':
	app.run(threaded=True, debug=True, host='localhost', port=8080)
