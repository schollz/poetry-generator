# poetry-generator v. 1.1
_Updates: Uses "en" now_

```
verb-pr = hopes
verb-past = hoped
verb = hope
verb-inf = hoping
```
# TODO
 - Replace all the infinitive/present/past verbs with en.verb translator
 - Replace singular/plural nouns with en.noun

A Python3 based Backus-Naur poetry generator.

This program works on the basis that every word in the English language is either "positive" or "negative." For instance "lovely" is positive and "thorn" is negative. A "poem" is a group of sentences that are structured in a way to have +1, -1 or 0 in terms of the positivity/negativity.  A "mushy poem" is strictly positive.

All the syntax and word choices are in the `poem.bnf` file. The main program is in `poem.py` and for web applications use the `poem.php` script to automatically generate a poem onload!

Try the [demo here](http://www.poetrygenerator.ninja)

# Super simple setup!
Follow these commands to generate a poem if you have minimal experience coding/etc. Open up a terminal and use

```bash
git clone https://github.com/schollz/poetry-generator.git
cd poetry-generator
wget https://www.nodebox.net/code/data/media/linguistics.zip
unzip linguistics.zip
python3 poem.py
```

That's it!

# Simple server setup
Install gunicorn and then simply use

```bash
gunicorn server:application
```

Don't have gunicorn? Use waitress:

```bash
pip install waitress
waitress-serve --port=8000 server:application
```

Then open your browser to `localhost:8000` to see the poetry generator.

# Deployment
I wrote a deployment script for easy NGINX deployment (keep reading). This will install NGINX blocks, as well as a Linux `init.d` script to automatically start and stop gunicorn.

Edit deploy.py to change

```
APP_NAME = 'poetry-generator'
APP_URL = 'www.poetrygenerator.ninja'
APP_PORT = 8002
```

or leave the same - its up to you.

Then run

```
sudo python deploy.py install
```

This program now uses `virtualenv` so it can be deployed with `gunicorn`. The installation creates `virtualenv` and downloads the packages. Then it writes a new `init.d` script and sends that so that it can automatically start and stop. If you deploy, it will also generate a nginx server block so its already to go.

The program should be running and accessible on your LAN network at

```
YOURLOCALIP:8002/
```

## Common Error
When you run, you may see the following error:

```bash
[....] Reloading nginx configuration (via systemctl): nginx.serviceJob for nginx.service failed. See 'systemctl status nginx.service' and 'journalctl -xn' for details.
 failed!
```

To fix this, you just need to enable the server_names in nginx. First

```
sudo vim /etc/nginx/nginx.conf
```

And uncomment these lines:

```bash
server_names_hash_bucket_size 64;
server_name_in_redirect off;
```

and _now_ you should be good to go!

# Credits
Thanks to [nylen](https://github.com/nylen) for greatly improving Poetry Generator, by fixing code and adding permalinks to poems!
