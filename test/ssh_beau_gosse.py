#! /opt/csw/bin/python3

# --------------------------------------------------------------------------------------------------
# Ssh with exporting personalized prompt
# -
# Quentin MARY
# -------------------------------------------------------------------------------------------------

import subprocess
import getopt
import signal
import time
import sys
import re
import os

import mysql.connector

class Tunnel():
    """Create an ssh redirection port between localhost and remote server."""
#{{{
    def __init__(self, hostname, local_port, remote_port):
        args = ['sudo', 'ssh', '-f', '-L', 
                '{}:localhost:{}'.format(str(local_port), str(remote_port)),
                hostname, '-N']
        self.process = subprocess.Popen(args, preexec_fn=os.setsid)

    def close(self):
        args = ['sudo', 'kill', str(self.process.pid + 1)]
        with open('/dev/null', 'wb') as dev_null:
            subprocess.Popen(args, stdout=subprocess.PIPE)
#}}}

class MySQLQuery():
    """This class perform a query on an mysql server."""
#{{{

    def __init__(self, server, database_='', user_='', password_='',
                 host_='127.0.0.1', port_='3306'):
#{{{
        self.database = database_
        self.user = user_
        self.password = password_
        self.host = host_
        self.port = port_
        self.server = server

        try:
            self.connection = mysql.connector.connect(user = self.user,
                                                      host = self.host,
                                                      port = self.port,
                                                      database = self.database,
                                                      password = self.password,
                                                      raise_on_warnings = True)
        except mysql.connector.Error as err:
            print(err)

        self.cursor_gen = self.connection.cursor()
        self.cursor_clu = self.connection.cursor()
#}}}


    def get_info(self):
#{{{
        # Weird behavior if the query is not one liner...
        query = ("SELECT servername, site, local, baie, env, dmzflag, os, version, type, modeles.vendor, modeles.modele, father FROM systeminfo LEFT JOIN environnement USING(servername) LEFT JOIN modeles USING(servername) WHERE servername = %s")

        self.cursor_gen.execute(query, (self.server,))

        for (servername, site, local, baie, env, dmzflag, os, version, 
                type_, vendor, modele, father) in self.cursor_gen:

            print("NOM      : {}".format(servername))
            print("SITE     : {} > {} > {}".format(site, local, baie))
            print("ENV      : {}".format(env))
            print("DMZ      : {}".format(dmzflag))
            print("OS       : {}-{}".format(os, version))

            if type_ == 'physical': 
                print("TYPE     : physique ({}: {})".format(vendor, modele))
                # Still weird behavior if the query is not one liner...
                query_cluster = ("SELECT IF(clusternodes.node1=systeminfo.servername, clusternodes.node2, clusternodes.node1) FROM systeminfo, clusternodes WHERE systeminfo.servername = %s AND (systeminfo.servername=clusternodes.node1 OR systeminfo.servername=clusternodes.node2) limit 1")
                self.cursor_clu.execute(query_cluster, (self.server,))
                for (node,) in self.cursor_clu:
                    print("CLUSTER  : en cluster avec {}".format(node))
            elif type_ == 'logicalserver': 
                print("TYPE     : {} (sur {})".format(type_, father))
                # One more query ;-)
                query_cluster = ("SELECT clusterinfos.type_bascule, clusterinfos.product, clusternodes.node1, clusternodes.node2 FROM systeminfo, clusterinfos, clusternodes WHERE systeminfo.servername = %s and systeminfo.servername=clusterinfos.servername and systeminfo.servername=clusternodes.servername")
                self.cursor_clu.execute(query_cluster, (self.server,))
                for (type_, product, node1, node2) in self.cursor_clu:
                    print("CLUSTER  : {} ({}) sur {} / {}".format(type_, product, 
                                                                 node1, node2))
            elif type_ in ('zone', 'virtualserver'): 
                print("TYPE     : {} (sur {})".format(type_, father))
            else: print("TYPE     : Unknown type")

    def close(self):
        self.cursor_gen.close()  
        self.cursor_clu.close()
        self.connection.close()

#}}}
#}}}


def opt_management(argv):
    """Manage options passed to script."""
#{{{
    if not len(argv) in [1, 2]: exception('Wrong number of arguments', 1)

    if len(argv) == 1 and re.match(r'^-',sys.argv[1]): 
        exception('Is a hostname was specified?', 3)
    elif len(argv) == 1: return '', sys.argv[1]

    if len(argv) == 2 and re.match(r'^-',sys.argv[1]):
        try: 
            opts, args = getopt.getopt(argv, 'hacgi', ['help', 'admin', 
                                                       'console', 'global', 
                                                       'info'])
        except getopt.GetoptError as error: exception(error, 2)

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                exit()
            elif opt in ('-a', '--admin'): 
                return 'admin', sys.argv[2]
            elif opt in ('-c', '--console'): 
                return 'console', sys.argv[2]
            elif opt in ('-g', '--global'): 
                return 'global', sys.argv[2]
            elif opt in ('-i', '--info'): 
                return 'info', sys.argv[2]
    else: exception('Only one hostname should be given', 4)
#}}}

def exception(exception, code):
    print ('''Error occured: ''' + str(exception))
    usage()
    exit(code)

def usage():
    print ('''To be continued...''')


if __name__ == '__main__':

    colors={'red':'\[\033[0;31m\]', 
            'green':'\[\033[0;32m\]', 
            'yellow':'\[\033[0;33m\]', 
            'blue':'\[\033[1;34m\]', 
            'magenta':'\[\033[0;35m\]', 
            'inverse':'\[\033[7m\]', 
            'default':'\[\033[0m\]'}
    rootCo='\`who | grep ^root | wc -l | sed \"s/ *//\"\`'

    opt, server = opt_management(sys.argv[1:])

    cockpit_tunnel = Tunnel('mscockpit', 15002, 3306)

    time.sleep(0.25)

    test = MySQLQuery(server='slpfir1a', database_='cockpit', user_='root', port_='15002')
    test.get_info()

    test.close()

    cockpit_tunnel.close()
