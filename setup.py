import sys
import os

APP_NAME = 'poetry-generator'
APP_URL = 'www.poetrygenerator.ninja'
APP_PORT = 8002



## CONFIGURATION ##

curDir = os.getcwd()

init_conf = """
# This should be placed in /etc/init directory
# start with
# sudo start %(appname)s
# stop with
# sudo stop %(appname)s

description "%(appname)s"

start on (filesystem)
stop on runlevel [016]

respawn
setuid nobody
setgid nogroup
chdir %(dir)s

exec %(dir)s/bin/gunicorn -b localhost:%(port)s -w 4 server:application
""" % {'port':APP_PORT,'dir':curDir,'appname':APP_NAME.replace(' ','')}

nginx_block = """
server {
	# SERVER BLOCK FOR %(appname)s
	listen   80; ## listen for ipv4; this line is default and implied

	root %(dir)s;
	index index.html index.htm;

	access_log /etc/nginx/logs/access-%(appname)s.log;
	error_log /etc/nginx/logs/error-%(appname)s.log;

	server_name %(url)s;

	location / {
		proxy_pass http://127.0.0.1:%(port)s;
		proxy_redirect off;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		#proxy_set_header Host $http_host;
		proxy_set_header X-NginX-Proxy true;
	}

	location /logs {
		deny all;
	}
	location ~ /\.ht {
		deny all;
	}

}
""" % {'port':APP_PORT,'dir':curDir,'appname':APP_NAME.replace(' ',''),'url':APP_URL + ' ' + APP_URL.replace('www.','')}

####################


if sys.argv[1]=='install' or sys.argv[1]=='deploy':
	print 'installing...'

	apt_get_packages = ['virtualenv']

	for package in apt_get_packages:
		print 'getting ' + package
		os.system('apt-get install ' + package)

	os.system('virtualenv ./ && . bin/activate && pip install gunicorn && deactivate')


	apt_get_packages = ['nginx']

	for package in apt_get_packages:
		print 'getting ' + package
		os.system('apt-get install ' + package)
	print 'generating init.d configuration file'
	with open('/etc/init/'+APP_NAME+'.conf','w') as f:
		f.write(init_conf)
		
	print 'generating nginx server block'
	with open('/etc/nginx/sites-available/'+APP_NAME,'w') as f:
		f.write(nginx_block)

	os.system('mkdir /etc/nginx/logs/')
	os.system('rm /etc/nginx/sites-enabled/%(app)s' % {'app':APP_NAME})
	print('ln -s /etc/nginx/sites-available/%(app)s /etc/nginx/sites-enabled/%(app)s' % {'app':APP_NAME})
	os.system('ln -s /etc/nginx/sites-available/%(app)s /etc/nginx/sites-enabled/%(app)s' % {'app':APP_NAME})

	os.system('/etc/init.d/nginx reload && /etc/init.d/nginx restart')
else:
	print 'usage: sudo python setup.py [install|deploy|uninstall]'



	

	
