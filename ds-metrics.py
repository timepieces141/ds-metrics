'''
This module connects to Cassandra and records JMX metrics.
'''

# core libraries
import argparse
import logging
import os

# third party libraries
from cassandra.cluster import Cluster, NoHostAvailable

# setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] : %(message)s')

def status(args):
    '''
    Checks the running status of Cassandra.
    '''
    try:
        cluster = Cluster(args.hosts)
        session = cluster.connect()
        logging.info("Session connected to cluster at %s", args.hosts)
        return True
    except NoHostAvailable:
        logging.warning("The Cassandra service is not running on %s", args.hosts)
        return False


def collect(args):
    '''
    Begins the collection of metrics
    '''
    logging.debug("got here %s", args.jmxterm)


class ExistingFile(argparse.Action):
    '''
    An argparse action class for determining if a file exists.
    '''
    def __call__(self, parser, namespace, values, option_string=None):
        '''
        Determines if the value provided for the given option is an existing
        file.
        '''
        prospective = os.path.abspath(values)
        logging.debug("Validating the path '%s' given for the option '%s' exists", prospective, option_string)
        if not os.path.exists(prospective):
            raise argparse.ArgumentTypeError("Path '{}' given for option '{}' does not " \
                                             "exist!".format(prospective, option_string))
        setattr(namespace, self.dest, prospective)

# parse arguments/commands
parser = argparse.ArgumentParser(prog='ds-metrics')
subparsers = parser.add_subparsers(help='sub-command --help')

# the status command
status_command = subparsers.add_parser('status', help='Checks the running status of the Cassandra database')
status_command.add_argument('-H', '--hosts', nargs='+', default=["127.0.0.1"],
                            help='The host (or hosts) on which to check if Cassandra is running. Default: localhost')
status_command.set_defaults(func=status)

# start collection command
collect_command = subparsers.add_parser('collect', help='Starts collection of metrics, in case you want to ' \
                                                        'collect baseline metrics before the stress test.')
collect_command.add_argument('-j', '--jmxterm', default='/usr/lib/jmxterm/jmxterm-1.0-alpha-4-uber.jar',
                             action=ExistingFile, help='An override for providing the JMXTerm JAR file. Default: ' \
                                                       '/usr/lib/jmxterm/jmxterm-1.0-alpha-4-uber.jar')
collect_command.set_defaults(func=collect)

# other commands here

# parse
args = parser.parse_args()
args.func(args)
