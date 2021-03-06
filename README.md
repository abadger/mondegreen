My current need for these is work related.  I use Finito to upload what I'm
working on and have accomplished.  Mondegreen is used to pass idonethis
messages on to a centralized channel on slack.

Currently, Finito has a minimal set of working functions but mondegreen is
currently not functioning.  Work is ongoing to fix this.

Mondegreen
==========

Mondegreen is a simple application to read messages from one web service and
repeat them to another.  It can centralize information you care about in one
service.

Finito
======
Finito is a little command line application for posting to idonethis.  It is
written in a similar style to mondegreen so with a trivial amount of work it
could be changed to post to any of the services that mondegreen supports.


Requirements
============

These programs are written in python3 and require the asyncio library.  asyncio
is included in the python3.4 distribution or may be downloaded separately for
python3.3.  It also needs python3-configobj

* Python3.3 or later: https://www.python.org/downloads/
* Asyncio: https://pypi.python.org/pypi/asyncio
* ConfigObj: https://pypi.python.org/pypi/configobj

You'll need at least one plugin to post messages with finito and a second one
to retrieve messages if you're using mondegreen.  Most of these plugins require
the aiohttp library to transfer this data over http.

* Aiohttp: https://pypi.python.org/pypi/aiohttp

The IRC plugin (Vaporware) needs the irc library along with its dependencies

* irc: https://pypi.python.org/pypi/irc

Author
======

Mondegreen and all other included files are written by Toshio Kuratomi
<toshio@fedoraproject.org> and licensed under the terms of the GNU Public
License v3 or later.  When Mondegreen matures a little it may relicense to
AGPLv3 with additional permissions similar to:

http://fedoraproject.org/wiki/Infrastructure_Licensing#AGPL_Discussion_Item
