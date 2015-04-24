#!/usr/bin/env python
from cgi import parse_qs, escape
from time import sleep
from poem import *

										
html_template = """
<html>
 <head>
  <title>A simple poem generator</title>
	<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-62257429-1', 'auto');
  ga('send', 'pageview');

</script>
<style>
body {
background: #FFF;
color: #111;
font: 18px Baskerville, "Palatino Linotype", "Times New Roman", Times, serif;
text-align: center;
}

#poem div, h1, h2, p {
margin: 0;
padding: 0;
}

#poem { 
margin: auto;
padding: 20px 0;
text-align: left;
width: 650px;
}

#poem h1, h2 {
font-weight: normal;
text-align: center;
}

#poem h1 {
font-size: 34px;
line-height: 1.2;
margin-bottom: 10px;
}

#poem h2 {
color: #666;
font-size: 18px;
font-style: italic;
margin-bottom: 30px;
}

#poem p {
line-height: 1.5;
margin-bottom: 15px;
}

/* The magic of selectors begins... */

#poem h2:before {
content: '- ';
}

#poem h2:after {
content: ' -';
}

#poem h2 + p:first-letter {
	float: left;
	font-size: 38px;
	line-height: 1;
	margin: 2px 5px 0 0;
}

#poem p:first-line {
font-variant: small-caps;
letter-spacing: 1px;
}

#poem p:last-child {
margin-bottom: 30px;
padding-bottom: 30px;
}

#footer {
position: fixed;
bottom: 0;
}

</style>
 </head>
 <body>
 
 <h1>Poetry generator</h1>

<div class="well center-block" style="max-width: 600px;">
   <form method="POST" action='/'> 
    <div class="row">
  <div class="col-md-6"><button type="submit"  class="btn btn-primary btn-lg btn-block" name='poemtype' value='poem'>Regular Poem</button></div>
  <div class="col-md-6"><button type="submit" class="btn btn-default btn-lg btn-block" name='poemtype' value='mushypoem'>Mushy poem</button></div>
</div>
    </form>
</div>


%s




<footer class="footer">
	<div class="container">
		<p class="text-muted">See how this code passed the turing test <a href="http://rpiai.com/2015/01/24/turing-test-passed-using-computer-generated-poetry/">here</a> and <a href="http://motherboard.vice.com/read/the-poem-that-passed-the-turing-test">here</a>. Also check out the <a href="https://github.com/schollz/poetry-generator">source code!</a></p>
	</div>
</footer>



 </body>
</html>

"""
 
pages = {
	 'index' : html_template % (
			"""
			<div id="poem">%(poem)s</div>

			"""),
}

def application(environ, start_response):

	# the environment variable CONTENT_LENGTH may be empty or missing
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0

	# When the method is POST the query string will be sent
	# in the HTTP request body which is passed by the WSGI server
	# in the file like wsgi.input environment variable.
	request_body = environ['wsgi.input'].read(request_body_size)
	d = parse_qs(request_body)
	
	poemtype = d.get('poemtype') # Returns a list of hobbies.
	# Always escape user input to avoid script injection
	try:
		poemtype = escape(poemtype)
	except:
		pass
		
	if int(request_body_size) > 0:
		response_body = pages['index'] % {'poem':bnf.generatePretty('<'+poemtype[0]+'>')}
	else:
		response_body = pages['index'] % {'poem':''}
		
	status = '200 OK'

	response_headers = [('Content-Type', 'text/html'),
								('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)

	return [response_body]