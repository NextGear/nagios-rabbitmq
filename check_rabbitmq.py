#!/usr/bin/env python
import argparse
import json
import requests


parser = argparse.ArgumentParser(
    description='Check a RabbitMQ host via its management HTTP API.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument('-H', '--host', dest='host', metavar='HOST', default='localhost', help="host that runs RabbitMQ")
parser.add_argument('-P', '--port', dest='port', metavar='PORT', type=int, default='15672', help="port to use")
parser.add_argument('-u', '--user', dest='user', default='guest', help="username of an admin user")
parser.add_argument('-p', '--pass', dest='pass', default='guest', help="password of your admin user")
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="show some extra information")
parser.add_argument('-V', '--vhost', dest='vhost', metavar='VIRTUAL_HOST', default='/', help="virtual host")
parser.add_argument('-q', '--queue', dest='queue', required=True, help="virtual host")
parser.add_argument('-c', '--check', dest='check', default='vhosts', choices=['alive', 'consumers', 'queue', 'vhosts'], help="what check to run")
parser.add_argument('-W', '--warning', dest='warning', type=int, required=True)
parser.add_argument('-C', '--critical', dest='critical', type=int, required=True)
args = vars(parser.parse_args())

API = 'http://%(host)s:%(port)d/api/' % args


class RabbitMQ(object):

    @staticmethod
    def get(module):
        try:
            r = requests.get(API + module, auth=(args['user'], args['pass']))
        except requests.exceptions.ConnectionError:
            print("Could not connect to " + API)
            exit(3)
        if args['verbose']:
            print("[HTTP %d] %s" % (r.status_code, API + module))
        response = json.loads(r.text)
        if type(response) is dict and response.has_key('reason'):
            print("%(reason)s: %(error)s" % response)
            exit(3)
        if type(response) is list:
            print("Multiple results for %(queue)s" % args)
            exit(3)
        return response

    @staticmethod
    def alive():
        alive = RabbitMQ.get('aliveness-test/%(vhost)s' % args)
        print("Status: %(status)s" % alive)
        if alive['status'] != 'ok':
            return 2

    @staticmethod
    def consumers():
        queue = RabbitMQ.get('queues/%(vhost)s/%(queue)s' % args)
        if not queue.has_key('active_consumers'):
            queue['active_consumers'] = 0
        print("Consumers: %(consumers)d (%(active_consumers)d active)") % queue
        if queue['consumers'] <= args['critical']:
            return 2
        elif queue['consumers'] <= args['warning']:
            return 1

    @staticmethod
    def queue():
        queue = RabbitMQ.get('queues/%(vhost)s/%(queue)s' % args)
        print("Messages: %(messages)d (%(messages_ready)d ready, %(messages_unacknowledged)d unacknowledged)" % queue)
        if queue['messages'] >= args['critical']:
            return 2
        elif queue['messages'] >= args['warning']:
            return 1

    @staticmethod
    def vhosts():
        vhosts = []
        for vhost in RabbitMQ.get('vhosts'):
            vhosts.append(vhost['name'])
        print("Vhosts: " + ', '.join(vhosts))
        if len(vhosts) <= args['critical']:
            return 2
        elif len(vhosts) <= args['warning']:
            return 1

check = getattr(RabbitMQ, args['check'])
exit(check())
