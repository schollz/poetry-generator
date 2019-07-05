# A Python2 based Backus-Naur poetry generator.

This program works on the basis that every word in the English language is either "positive" or "negative." For instance "lovely" is positive and "thorn" is negative. A "poem" is a group of sentences that are structured in a way to have +1, -1 or 0 in terms of the positivity/negativity.  A "mushy poem" is strictly positive.

All the syntax and word choices are in the `brain.yaml` file (more info about this below).

Try the [demo here](http://www.poetrygenerator.ninja).

# Docker

```
$ docker run -p 8000:8000 schollz/poetry-generator
```

Now open your browser to localhost:8000!

### Changes in new version
 - Use YAML
 - Reverted to Python2 (to use Nodebox Linguistics)
 - Use Nodebox Linguistics for plurality and conjugations (saves much space)
 - Poem dictation (Chrome only)

# Setup
Follow these commands to generate a poem if you have minimal experience coding/etc. Open up a terminal and use

```bash
git clone https://github.com/schollz/poetry-generator.git
cd poetry-generator
```

Install Python requirements

```bash
pip install -r requirements.txt
```

Download and unzip the NodeBox linguistics package:

```bash
wget https://www.nodebox.net/code/data/media/linguistics.zip
unzip linguistics.zip
```

And then run using

```bash
waitress-serve --port=8000 poetrygenerator:application
```

Then open your browser to `localhost:8000` to see the poetry generator.

# About the brain file

Examples of the types of words:

```
verb-pr = hopes
verb-past = hoped
verb = hope
verb-inf = hoping
```

Currently you only need to put in the infinitive form, and the other forms will be determined automaticlaly.

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

### Common Error
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
