#!/usr/bin/env python
from cgi import parse_qs, escape
from time import sleep
import json
import os
import random
import re

from poem import *

html_template = """
<html>
 <head>
  <title>A simple poem generator</title>
    <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">
<script src=https://code.jquery.com/jquery-1.12.0.min.js"></script>
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
<script>
var msg = new SpeechSynthesisUtterance();
var voices = window.speechSynthesis.getVoices();
</script>
 </head>
 <body>

 <h1>Poetry generator</h1>

<div class="well center-block" style="max-width: 600px;">
   <form method="POST" action="/poem">
    <div class="row">
  <div class="col-md-6"><button type="submit"  class="btn btn-primary btn-lg btn-block" name='poemtype' value='poem'>Regular Poem</button></div>
  <div class="col-md-6"><button type="submit" class="btn btn-default btn-lg btn-block" name='poemtype' value='mushypoem'>Mushy poem</button></div>
</div>
    </form>
</div>

<div id="poem">%(poem)s <h2>%(url)s</h2></div>

<footer class="footer">
    <div class="container">
        <p class="text-muted">See how this code passed the turing test <a href="http://rpiai.com/2015/01/24/turing-test-passed-using-computer-generated-poetry/">here</a> and <a href="http://motherboard.vice.com/read/the-poem-that-passed-the-turing-test">here</a>. Also check out the <a href="https://github.com/schollz/poetry-generator">source code!</a></p>
    </div>
</footer>
<script src='https://code.responsivevoice.org/responsivevoice.js'></script>
<input onclick='partA();' type='button' value='Play' />
<script>
document.addEventListener("DOMContentLoaded", function(event) {
    msg = new SpeechSynthesisUtterance();
    voices = window.speechSynthesis.getVoices();
setTimeout(function () {
    msg.voice = voices[10]; // Note: some voices don't support altering params
    msg.voiceURI = 'native';
    msg.volume = 1; // 0 to 1
    msg.rate = 1; // 0.1 to 10
    msg.pitch = 0; //0 to 2
    msg.lang = 'en-US';
    messages = %(lines)s;
    var messageNumber = 0;
    msg.text = messages[messageNumber];
    msg.onend = function(e) {
      console.log('Finished in ' + event.elapsedTime + ' seconds.');
      messageNumber = messageNumber + 1;
      msg.text = messages[messageNumber];
      msg.voice = voices[10]; // Note: some voices don't support altering params
      msg.voiceURI = 'native';
      msg.rate = 1; // 0.1 to 10
      msg.pitch = 0; //0 to 2
      msg.lang = 'en-US';
      msg.volume = 1; // 0 to 1
      if (msg.text=="pause") {
        msg.volume = 0;
      } else {
      }
      if (messageNumber < messages.length) {
        speechSynthesis.speak(msg);
      }
    };
    speechSynthesis.speak(msg);
}, 1000);

});

</script>
 </body>
</html>

"""

pages = {
     'index' : html_template,
}

class Router():
    def __init__(self, url):
        self.url = url

    def match(self, pattern):
        match = re.search(pattern, self.url)
        if match:
            self.params = match.groupdict()
            return True
        else:
            return False

def application(environ, start_response):
    url = environ['PATH_INFO']
    router = Router(url)

    if router.match('^/(?P<type>poem|mushypoem)/(?P<seed>[0-9a-zA-Z]+)$'):
        return show_poem(environ, start_response, router)
    else: # '/' '/poem' or anything else
        return redirect_to_poem(environ, start_response)


def redirect_to_poem(environ, start_response):
    # We might have a POST body indicating the poem type; try to read it.

    # The environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    # Read and parse the HTTP request body which is passed by the WSGI server
    request_body = environ['wsgi.input'].read(request_body_size)
    poemtype = None
    qs = parse_qs(request_body)
    if qs:
        poemtype = qs.get('poemtype')[0]
    if poemtype != 'mushypoem':
        poemtype = 'poem'

    seed = os.urandom(8).encode('hex')

    start_response('302 Found', [
        ('Location', '/' + poemtype + '/' + seed)
    ])

    return []


def show_poem(environ, start_response, router):
    # Ensure that we can always get back to a given poem
    p,str_seed = bnf.generatePretty('<' + router.params['type'] + '>',router.params['seed'])
    filtered = []
    for line in re.sub("<.*?>", " ", p).split("\n"):
        if len(line.strip()) > 0:
            filtered.append(line.strip())
        else:
            filtered.append("pause")
    response_body = pages['index'] % {
        'poem': p,
        'url': router.url,
        'lines': json.dumps(filtered)
    }

    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ])

    return [response_body]
