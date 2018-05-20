From ubuntu:latest

RUN apt-get update && && apt-get upgrade -y && apt-get install -y apache2\
    libapache2-mod-wsgi-py3\
    python3\
    python3-pip\
    vim\
&& apt-get clean\
&& apt-get autoremove

# Copy over and install the requirements
RUN pip3 install pipenv
RUN pipenv freeze > ./requirements.txt
RUN pip3 install -r ./requirements.txt
RUN pip3 install flask-mysql

# Copy over the apache configuration file and enable the site
COPY ./flask_login.conf /etc/apache2/sites-available/
RUN a2ensite flask_login
RUN a2enmod headers

# Copy over the wsgi file
COPY ./flask_login.wsgi /var/www/apache-flask/

RUN a2dissite 000-default.conf
RUN a2ensite flask_login.conf

EXPOSE 80

WORKDIR /var/www/apache-flask

# CMD ["/bin/bash"]
CMD  /usr/sbin/apache2ctl -D FOREGROUND
# The commands below get apache running but there are issues accessing it online
# The port is only available if you go to another port first
# ENTRYPOINT ["/sbin/init"]
# CMD ["/usr/sbin/apache2ctl"]
