FROM nimmis/apache-php5

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
COPY php.ini /etc/php5/apache2/php.ini

EXPOSE 80

WORKDIR /app

ADD . /app

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-client mysql-server libmysqlclient-dev build-essential python-dev python-pip
RUN pip install mysqlclient

CMD bash setup.sh