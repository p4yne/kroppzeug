kroppzeug
=========

Helps you to manage your server kindergarten!


About
-----

Kroppzeug helps you to manage your server kindergarten by parsing your
SSH config file and providing shortcuts for connecting to a server or
updating one or all servers. Kroppzeug is perfect for managing a few to
a dozent servers but may be no fun when you have to orchestrate hundreds
or thousands of servers. It requires that you use a terminal multiplexer
like screen or tmux after connecting to a server.
Trivia: 'Kroppzeug' is an often lovingly and sometimes snidely used
low-german term for ones offspring.


Configuration
-------------

Just annotate you SSH config file with comments starting with '#kroppzeug_'.

* ``#kroppzeug_autocmd`` Commands to execute after the connection has been made. If value is ``false`` no command is executed. Mandatory.
* ``#kroppzeug_group`` This allows grouping of hosts, to e.g. update whole groups. Default value is``ǹone``. Optional.
* ``#kroppzeug_description`` A description of the server. Optional.
* ``#kroppzeug_update`` Commands to execute when using the update function. Optional.
* ``#kroppzeug_ssh`` Default is to use ssh, but setting this to e.g. mosh will use mosh to connect to the server. Optional.
* ``#kroppzeug_managed`` Set to 'true' to allow kroppzeug to list this server. Mandatory.

The default behaviour is to use ``ssh`` and ``ssh -v`` when updating. But ``#kroppzeug_ssh`` allows changing of ssh command for a normal connection, like changing it to ``mosh`` or to ``ssh -vvv``.
If no ``#kroppzeug_group`` is specified the host is added to the default group called ``none``. Otherwise hosts with corresponding groups a group together an can be e.g. updated by using the ``update_group <group_name>`` command.
``#kroppzeug_managed`` must be true if a host entry should be used and it also must be the last comment for a host entry, only this ensures correct parsing of the config file and host entries.

````
Host cloud
    Hostname                cloud.nonattached.net
    User                    user1
    Port                    2222
    #kroppzeug_autocmd      tmux attach || tmux
    #kroppzeug_description  OwnCloud Server
    #kroppzeug_update       apt-get update; apt-get upgrade
    #kroppzeug_managed      true
````

Additional Example snippets:

````
Host server
    Hostname                webserver.nonattached.net
    User                    user1
    Port                    2222
    #kroppzeug_autocmd      false
    #kroppzeug_description  OwnCloud Server
    #kroppzeug_update       sudo apt-get update; sudo apt-get upgrade
    #kroppzeug_managed      true
````

````
Host fun
    Hostname                lucky.nonattached.net
    User                    user1
    Port                    2222
    #kroppzeug_autocmd      false
    #kroppzeug_description  Happy Cats
    #kroppzeug_update       yaourt -Syua
    #kroppzeug_ssh          mosh
    #kroppzeug_managed      true
````

````
Host neo
    HostName                bluepill.example.com
    User                    apprentice
    Port                    6666
    IdentityFile            /home/path/to/priv-key
    IdentitiesOnly          yes
    #kroppzeug_autocmd      false
    #kroppzeug_description  VPN Server
    #kroppzeug_update       sudo apt-get update; sudo apt-get upgrade
    #kroppzeug_ssh          ssh -v
    #kroppzeug_group        matrix
    #kroppzeug_managed      true
````

Commands
--------

To connect to a server just type ``connect [server name]``.
To update a server use ``update [server name]`` or ``update all`` to update
all servers. If you are unsure from which host you are connecting, e.g.
because you own too many computers, type ``whereami`` to toggle the hostname
in the title area. The prompt is like a special purpose shell that supports
**TAB** completion and by typing ``help <command>`` a short description and usage examples are given.
The tab completion only works until special characters like ``!?-+*/|<>`` and so on are used in host or group names.

Screenshot
----------
````
                          ┬┌─┬─┐┌─┐┌─┐┌─┐┌─┐┌─┐┬ ┬┌─┐                           
                          ├┴┐├┬┘│ │├─┘├─┘┌─┘├┤ │ ││ ┬                           
                          ┴ ┴┴└─└─┘┴  ┴  └─┘└─┘└─┘└─┘                           
────────────────────────────────────────────────────────────────────────────────

             cell Testbed                        glados MCP                 

─| NaN |────────────────────────────────────────────────────────────────────────

               mail Mailserver                        www Webserver
           nethop Shell                             gws Gateway E.
          storage Storage E.                    sealand Backup
           nan-gw Gateway Frankfurt             nan-vpn VPN Terminator IPMI
           puppet Puppet Master                      ns Nameserver (master)
             dns1 RDNSS 1                          dns2 RDNSS 2
          irc IRC Server                          cloud OwnCloud Server
              git GIT Repository                    jmp VPN server
         workshop IPv6-Workshop

─| FunNet |─────────────────────────────────────────────────────────────────────

            cloud Owncloud                       valkyr Mailserver          
           oracle DNS Server                    wheatly Webserver           
          turrent Honeypot                          bit Firewall            
         morpheus Puppet Master                     neo VPN Server          

────────────────────────────────────────────────────────────────────────────────
(kroppzeug)$ 

````

License
-------

Copyright 2012-2014 Dan Luedtke <mail@danrl.de>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
