nagios-rabbitmq
===============

nagios check for RabbitMQ that uses the HTTP API

Commands
--------
* $USER2$ - the dir for this plugin
* $ARG1$ - username
* $ARG2$ - password
* $ARG3$ - vhost
* $ARG4$ - queue
* $ARG5$ - warning level
* $ARG6$ - critical level

##### check_rabbitmq_consumers
$USER2$/check_rabbitmq.py -H $HOSTADDRESS$ --user=$ARG1$ --pass=$ARG2$ --vhost=$ARG3$ --queue=$ARG4$ --check=consumers --warning $ARG5$ --critical $ARG6$

##### check_rabbitmq_queue
$USER2$/check_rabbitmq.py -H $HOSTADDRESS$ --user=$ARG1$ --pass=$ARG2$ --vhost=$ARG3$ --queue=$ARG4$ --check=queue --warning $ARG5$ --critical $ARG6$

##### check_rabbitmq_vhosts
$USER2$/check_rabbitmq.py -H $HOSTADDRESS$ --user=$ARG1$ --pass=$ARG2$ --vhost=$ARG3$ --queue=$ARG4$ --check=vhosts --warning $ARG5$ --critical $ARG6$
