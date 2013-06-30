eZ publish - Enterprise Content Management System
=================================================

`eZ publish`_ is a web content management system that supports the
development of customized web applications. It features professional and
secure development of web applications, content versioning, media
library, role-based rights management, mobile development, sitemaps,
search and printing.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- eZ publish configurations:
   
   - Installed from upstream source code to /var/www/ezpublish

- SSL support out of the box.
- `PHPMyAdmin`_ administration frontend for MySQL (listening on port
  12322 - uses SSL)
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2, PHP, MySQL and Postfix.

Credentials *(passwords set at first boot)*
-------------------------------------------

- Webmin, SSH, MySQL, phpMyAdmin: username **root**
- eZ publish: username **admin@example.com**


.. _eZ publish: http://ez.no/
.. _TurnKey Core: http://www.turnkeylinux.org/core
.. _PHPMyAdmin: http://www.phpmyadmin.net
