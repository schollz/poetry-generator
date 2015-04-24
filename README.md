poetry-generator
================

A Python3 based Backus-Naur poetry generator.

This program works on the basis that every word in the English language is either "positive" or "negative." For instance "lovely" is positive and "thorn" is negative. A "poem" is a group of sentences that are structured in a way to have +1, -1 or 0 in terms of the positivity/negativity.  A "mushy poem" is strictly positive.

All the syntax and word choices are in the ```poem.bnf``` file. The main program is in ```poem.py``` and for web applications use the ```poem.php``` script to automatically generate a poem onload!

Try the [demo here](http://www.poetrygenerator.ninja)


Setup/installation
====================

This program now uses ```virtualenv``` so it can be deployed with ```gunicorn```. To use, install virtualenv

```
apt-get install virtualenv
``` 

then change to the directory

```
cd poetry-generator
```

Now startup virtualenv and install the packages

```
virtualenv ./
source bin/activate
(virtualenv) pip install gunicorn
```


To test out use

```bash
(virtualenv) ./bin/gunicorn -b 127.0.0.1:8002 -w 2 server:application
```

To exit virtualenv simply use

```
deactivate
```

Now move the UpStart configuration file to the /etc/init/ folder

```bash
sudo cp *.conf /etc/init/
```

And now start hosting on port 8002 with

```
sudo start poetrygenerator_ninja
```

You should now see it on 127.0.0.1:8002!!