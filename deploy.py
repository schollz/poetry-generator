import sys
import os
import socket

APP_NAME = 'poetry-generator'
APP_URL = 'www.poetrygenerator.ninja'
APP_PORT = 8002

try:
	print "working to " + sys.argv[1]
except:
	print 'usage: sudo python setup.py [install|deploy|uninstall]'
	sys.exit()

## CONFIGURATION ##
mainIP = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
curDir = os.getcwd()

init_conf = """
# This should be placed in /etc/init.d directory
# start with
# sudo /etc/init.d/%(appname)s start
# stop with
# sudo /etc/init.d/%(appname)s start

dir="%(dir)s"
user="nobody"
cmd="%(dir)s/bin/gunicorn -b %(ip)s:%(port)s -w 4 server:application"

name=`basename $0`
pid_file="/var/run/$name.pid"
stdout_log="/var/log/$name.log"
stderr_log="/var/log/$name.err"

get_pid() {
    cat "$pid_file"
}

is_running() {
    [ -f "$pid_file" ] && ps `get_pid` > /dev/null 2>&1
}

case "$1" in
    start)
    if is_running; then
        echo "Already started"
    else
        echo "Starting $name"
        cd "$dir"
        sudo -u "$user" $cmd >> "$stdout_log" 2>> "$stderr_log" &
        echo $! > "$pid_file"
        if ! is_running; then
            echo "Unable to start, see $stdout_log and $stderr_log"
            exit 1
        fi
    fi
    ;;
    stop)
    if is_running; then
        echo -n "Stopping $name.."
        kill `get_pid`
        for i in {1..10}
        do
            if ! is_running; then
                break
            fi

            echo -n "."
            sleep 1
        done
        echo

        if is_running; then
            echo "Not stopped; may still be shutting down or shutdown may have failed"
            exit 1
        else
            echo "Stopped"
            if [ -f "$pid_file" ]; then
                rm "$pid_file"
            fi
        fi
    else
        echo "Not running"
    fi
    ;;
    restart)
    $0 stop
    if is_running; then
        echo "Unable to stop, will not attempt to start"
        exit 1
    fi
    $0 start
    ;;
    status)
    if is_running; then
        echo "Running"
    else
        echo "Stopped"
        exit 1
    fi
    ;;
    *)
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
    ;;
esac

exit 0
""" % {'port':APP_PORT,'dir':curDir,'appname':APP_NAME.replace(' ',''),'ip':mainIP}

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
		proxy_pass http://%(ip)s:%(port)s;
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
""" % {'port':APP_PORT,'dir':curDir,'appname':APP_NAME.replace(' ',''),'url':APP_URL + ' ' + APP_URL.replace('www.',''),'ip':mainIP}

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
	with open('/etc/init.d/'+APP_NAME,'w') as f:
		f.write(init_conf)
	os.system('chmod +x /etc/init.d/'+APP_NAME)
	print "starting server..."
	os.system('/etc/init.d/' + APP_NAME + ' restart')

	print 'generating nginx server block'
	with open('/etc/nginx/sites-available/'+APP_NAME,'w') as f:
		f.write(nginx_block)

	os.system('mkdir /etc/nginx/logs/')
	os.system('rm /etc/nginx/sites-enabled/%(app)s' % {'app':APP_NAME})
	print('ln -s /etc/nginx/sites-available/%(app)s /etc/nginx/sites-enabled/%(app)s' % {'app':APP_NAME})
	os.system('ln -s /etc/nginx/sites-available/%(app)s /etc/nginx/sites-enabled/%(app)s' % {'app':APP_NAME})

	os.system('/etc/init.d/nginx reload && /etc/init.d/nginx restart')

	print "-"*30
	print "To activate:"
	print '/etc/init.d/' + APP_NAME + ' [start|stop|restart]'
	print 'Currently running on ' + str(mainIP) + ':'+str(APP_PORT)
	print "-"*30
else:
	print 'usage: sudo python setup.py [install|deploy|uninstall]'
