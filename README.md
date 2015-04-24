poetry-generator
================

A Python3 based Backus-Naur poetry generator.

This program works on the basis that every word in the English language is either "positive" or "negative." For instance "lovely" is positive and "thorn" is negative. A "poem" is a group of sentences that are structured in a way to have +1, -1 or 0 in terms of the positivity/negativity.  A "mushy poem" is strictly positive.

All the syntax and word choices are in the ```poem.bnf``` file. The main program is in ```poem.py``` and for web applications use the ```poem.php``` script to automatically generate a poem onload!

Try the [demo here](http://www.poetrygenerator.ninja)

Installation
=================

Edit setup.py to change 

```
APP_NAME = 'poetry-generator'
APP_URL = 'www.poetrygenerator.ninja'
APP_PORT = 8002
```

or leave the same - its up to you.

Then run 

```
sudo python setup.py install
```

This program now uses ```virtualenv``` so it can be deployed with ```gunicorn```. The installation creates ```virtualenv``` and downloads the packages. Then it writes a new ```init.d``` script and sends that so that it can automatically start and stop. If you deploy, it will also generate a nginx server block so its already to go.

The program should be running and accessible on your LAN network at

```
YOURLOCALIP:8002/
```