# wiki-in-a-flask.py
# requires: python3, flask, markdown, gnupg
from flask import *
import os, mimetypes, time, gnupg, subprocess
import markdown as MD

GNUPGHOME = '/home/julian/.gnupg'

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

@app.route('/wiki/<article>/edit', methods=['POST', 'GET'])
def editArticle(article=None):
	if not article: return abort(404)
	
	if request.method == 'POST':
		with open('trusted_keys','r') as f: trusted = f.read().strip().split('\n')
		
		gpg = gnupg.GPG(gnupghome=GNUPGHOME)
		verification = gpg.verify(request.data)
		if not verification:
			return f'Error: Signature failed to verify.\n', 403
			
		if verification.fingerprint not in trusted:
			return f'ERROR: The fingerprint {verification.fingerprint} is not trusted.\nPlease contact the administrator.\n', 403
		
		# save the signed changes to disk
		changename = time.strftime('%Y%m%dT%H%M%S_') + article + '.md.sig'
		with open(f'changes/{changename}', 'wb') as f:
			f.write(request.data)
		
		# write the actual new page to disk
		with open(f'changes/{changename}.tmp', 'wb') as f:
			f.write(gpg.decrypt(request.data).data)
		
		# generate a patch file
		patchname = changename.replace('.sig', '.patch')
		with open(f'changes/{patchname}', 'wb') as f:
			subprocess.call(['diff', f'wiki/{article}.md', f'changes/{changename}.tmp'], stdout=f)
		
		# remove the tmp file
		os.remove(f'changes/{changename}.tmp')
		
		# apply the patch
		subprocess.call(['patch', f'wiki/{article}.md', f'changes/{patchname}'])
		
		return 'Ok!\n'
		
	else:
		return Response('''To edit this page you will need:
	- wget or curl
	- a gpg key

Download the page with
	$ wget -O {article}.md https://{host}/wiki/{article}/md

Edit the page using your editor of choice
	$ nano {article}.md

Sign the modified page with your GPG key
	$ gpg --output {article}.md.sig --clearsign {article}.md

Send it to the wiki, with an optional comment
	$ cat {article}.md.sig | curl -X POST -H "Comment: YOUR COMMENT HERE" -H "Content-Type: text/plain" --data-binary "@-" https://{host}/wiki/{article}/edit
'''.format(host=request.headers.get('Host'), article=article), mimetype='text/plain')

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
