#!/usr/bin/python3
# -*- coding: utf-8 -*-

# kroppzeug: Helps you to manage your server kindergarten!
#
# Copyright 2012-2014 Dan Luedtke <mail@danrl.de>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import string
import os
import time
import sys
import signal
from subprocess import call
from socket import gethostname

# global variables
hosts           = []
whereami        = False
ssh_config_file = os.getenv("HOME") + '/.ssh/config'

# colors, control sequences
TERM_RED        = '\033[91m'
TERM_GREEN      = '\033[92m'
TERM_YELLOW     = '\033[93m'
TERM_BLUE       = '\033[94m'
TERM_MAGENTA    = '\033[95m'
TERM_BOLD       = '\033[1m'
TERM_RESET      = '\033[0m'


# catch SIGINT (e.g. ctrl+c)
def signal_handler(signal, frame):
    print()
    print(TERM_RESET + 'Life tasted so good, dude!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# get terminal size
def get_termsize():
    y, x = os.popen('stty size', 'r').read().split()
    y = int(y)
    x = int(x)
    return y, x
# terminal dimensions and sizes
TERM_SIZEY, TERM_SIZEX = get_termsize()

# fine grained layouting
# bss,shortcut_width,bs,about_width,aas,ms
bss = 1     # before_shortcut_space
sw  = 16    # shortcut_width
bs  = 1     # between_space
aas = 1     # after_about_space
ms  = 0     # middle_space
nc  = 2     # number of columns
shortcut_width = sw
about_width = (TERM_SIZEX - ((((bss + sw + bs + aas) * nc) + ms))) // nc


# read ssh hosts from config file
def parse_hosts(filename):
    i = -1
    inputfile = open(filename, 'r')
    for line in inputfile.readlines():
        # strip whitespaces
        line = line.strip()
        # extract options
        line = line.split(None, 1)
        # parse options
        if len(line) < 2:
            continue
        option = line[0]
        value = line[1]
        if option.lower() == 'host':
            shortcut = value
            about = 'no description'
            update = False
            autocmd = False
            shell = 'ssh'
            i += 1
        elif option.lower() == '#kroppzeug_ssh' and value.lower() != 'ssh':
            shell = value
        elif option.lower() == '#kroppzeug_description':
            about = value
        elif option.lower() == '#kroppzeug_update' and len(value) > 0:
            update = value
        elif option.lower() == '#kroppzeug_autocmd' and value.lower() != 'false':
            autocmd = value
        elif option.lower() == '#kroppzeug_managed' and value.lower() == 'true':
            hosts.append([shortcut, about, update, autocmd, shell])
    inputfile.close()


# print header
def print_header():
    os.system('clear')
    print(TERM_BOLD + TERM_RED, end='')
    if whereami is True:
        print()
        print(gethostname().center(TERM_SIZEX))
        print()
    else:
        print('┬┌─┬─┐┌─┐┌─┐┌─┐┌─┐┌─┐┬ ┬┌─┐'.center(TERM_SIZEX))
        print('├┴┐├┬┘│ │├─┘├─┘┌─┘├┤ │ ││ ┬'.center(TERM_SIZEX))
        print('┴ ┴┴└─└─┘┴  ┴  └─┘└─┘└─┘└─┘'.center(TERM_SIZEX))
    print(TERM_GREEN + '─' * TERM_SIZEX)


# print a list of available hosts
def print_hosts():
    i = -1
    for host in hosts:
        i += 1
        host_shortcut = host[0][:shortcut_width]
        if host[1] is not False:
            host_about = ' ' + host[1][:about_width] + ' '
        else:
            host_about = ' '
        out = ' '
        out = out + TERM_BOLD + TERM_BLUE + host_shortcut.rjust(shortcut_width)
        out = out + TERM_RESET + host_about.ljust(about_width)
        if i % 2 == 0:
            print(out, end='')
        else:
            print(out)


def print_rest_screen():
    # position
    posx = str(TERM_SIZEY - 2)
    print('\033[' + posx + ';0f')
    # horizontal line
    print(TERM_BOLD + TERM_GREEN + '─' * TERM_SIZEX + TERM_RESET)


def build_screen():
    # build screen
    TERM_SIZEY, TERM_SIZEX = get_termsize()
    print_header()
    print_hosts()
    print_rest_screen()


def connect_host(i):
    auto_command = hosts[i][3]
    shortcut = hosts[i][0]
    # craft shell command
    shell_command = hosts[i][4] + ' ' + shortcut
    if auto_command is not False:
        shell_command += ' -t "' + auto_command + '"'
    # go!
    os.system('clear')
    print(TERM_YELLOW + shell_command + TERM_RESET)
    call(shell_command, shell=True)


def update_host(i):
    update_command = hosts[i][2]
    shortcut = hosts[i][0]
    # craft shell command
    shell_command = 'ssh -v ' + shortcut
    if update_command is not False:
        shell_command += ' -t "' + update_command + '"'
        # go!
        os.system('clear')
        print(TERM_YELLOW + shell_command + TERM_RESET)
        call(shell_command, shell=True)


def shortcut_to_id(shortcut):
    i = -1
    for host in hosts:
        i += 1
        if host[0] == shortcut:
            return i
    return False


def startswith(text):
    return [host[0] for host in hosts if host[0].startswith(text)]


parse_hosts(ssh_config_file)


import cmd


class KroppzeugShell(cmd.Cmd):
    prompt = TERM_BOLD + TERM_YELLOW + '(kroppzeug)$ ' + TERM_RESET
    build_screen()

    def __init__(self):
        super(KroppzeugShell, self).__init__()

    #--------------commands---------------#
    def do_whereami(self, arg):
        'Toggle if current hostname sould be displayed instead of the '\
        'Kroppzeug logo: whereami'
        global whereami
        if whereami is True:
            whereami = False
        else:
            whereami = True

    def do_connect(self, arg):
        'Connect to specified host: connect valkyr'
        i = shortcut_to_id(arg)
        if i is not False:
            connect_host(i)
            time.sleep(1)
            build_screen()
        else:
            print(TERM_BOLD + TERM_RED + 'unknown/'\
            'undefined shortcut' + TERM_RESET)

    def do_update(self, arg):
        'Update specified host: update painkiller \n' \
        'Update all hosts:      update all '
        if arg == 'all':
            for i in range(len(hosts)):
                update_host(i)
                print(TERM_BOLD + TERM_GREEN + '─' * TERM_SIZEX + TERM_RESET)
                build_screen()
        else:
            i = shortcut_to_id(arg)
            if i is not False:
                update_host(i)
                print(TERM_BOLD + TERM_GREEN + '─' * TERM_SIZEX + TERM_RESET)
                time.sleep(3)
                build_screen()
            else:
                print(TERM_BOLD + TERM_RED + 'unknown/'\
                'undefined shortcut' + TERM_RESET)

    def do_list(self, arg):
        'List all available shortcuts for managed hosts: list'
        build_screen()

    def do_exit(self, arg):
        'Exit/quit the Kroppzeug shell: exit'
        print('Thank you for using Kroppzeug to manage you digital offspring!')
        return True

    #--------------tab completion---------------#
    def complete_connect(self, text, line, begidx, endidx):
        return startswith(text)

    def complete_update(self, text, line, begidx, endidx):
        return startswith(text)


if __name__ == '__main__':
    KroppzeugShell().cmdloop()
