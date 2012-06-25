#!/usr/bin/python
"""Set eZPublish admin password, email and domain to serve

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=www.example.com

"""

import os
import re
import sys
import getopt
import hashlib

from dialog_wrapper import Dialog
from mysqlconf import MySQL
from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_DOMAIN="www.example.com"

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    domain = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "eZPublish Password",
            "Enter new password for the eZPublish 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "eZPublish Email",
            "Enter email address for the eZPublish 'admin' account.",
            "admin@example.com")

    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "eZPublish Domain",
            "Enter the domain to serve eZPublish.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    def sed(var, val, conf):
        system("sed -i \"s|%s.*|%s%s|\" %s" % (var, var, val, conf))

    # tweak configuration files
    conf = "/var/www/ezpublish/settings/siteaccess/eng/site.ini.append.php"
    sed("SiteURL=", "%s/index.php/eng" % domain, conf)
    sed("ActionURL=", "http://%s/index.php/site_admin/user/login" % domain, conf)
    sed("AdminEmail=", email, conf)

    conf = "/var/www/ezpublish/settings/siteaccess/site/site.ini.append.php"
    sed("SiteURL=", domain, conf)
    sed("ActionURL=", "http://%s/index.php/site_admin/user/login" % domain, conf)
    sed("AdminEmail=", email, conf)

    conf = "/var/www/ezpublish/settings/siteaccess/site_admin/site.ini.append.php"
    sed("SiteURL=", domain, conf)
    sed("AdminEmail=", email, conf)

    conf = "/var/www/ezpublish/settings/override/site.ini.append.php"
    sed("AdminEmail=", email, conf)
    
    # calculate password hash and tweak database
    hash = hashlib.md5("admin\n%s" % password).hexdigest()

    m = MySQL()
    m.execute('UPDATE ezpublish.ezuser SET password_hash=\"%s\" WHERE login=\"admin\";' % hash)
    m.execute('UPDATE ezpublish.ezuser SET email=\"%s\" WHERE login=\"admin\";' % email)

    m.execute('UPDATE ezpublish.ezcontentobject_attribute SET data_text=\"%s\" WHERE id=175;' % email)
    m.execute('UPDATE ezpublish.ezcontentobject_attribute SET data_text=\"%s\" WHERE id=176;' % domain)

    # clear cache
    system("cd /var/www/ezpublish; su www-data -c \"php5 bin/php/ezcache.php --quiet --clear-all --purge\"")

if __name__ == "__main__":
    main()

