#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2008-07, Erik Svensson <erik.public@gmail.com>

import sys, os, os.path, re, itertools
import urllib.request, base64, shlex
from optparse import OptionParser
try:
    import readline
except:
    pass
import cmd
import transmissionrpc
from transmissionrpc.utils import *
from transmissionrpc.constants import DEFAULT_PORT

__author__    = 'Erik Svensson <erik.public@gmail.com>'
__version__   = '0.2'
__copyright__ = 'Copyright (c) 2008 Erik Svensson'
__license__   = 'MIT'

class Helical(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = 'Helical %s' % (__version__)
        self.doc_leader = '''
Helical is a command line interface that communicates with Transmission
bittorent client through json-rpc. To run helical in interactive mode
start without a command.
'''

    def connect(self, address=None, port=None, username=None, password=None):
        self.tc = transmissionrpc.Client(address, port, username, password)
        self.prompt = 'Helical %s:%d> ' % (address, port)

    def arg_tokenize(self, argstr):
        return [token for token in shlex.split(argstr)] or ['']

    def word_complete(self, text, words):
        suggestions = []
        for word in words:
            if word.startswith(text):
                suggestions.append(word)
        return suggestions

    def _complete_torrent(self, name, offset):
        words = [torrent.name for id, torrent in self.tc.torrents.items()]
        suggestions = []
        cut_index = len(name) - offset
        for word in words:
            if word.startswith(name):
                suggestions.append(word[cut_index:])
        return suggestions

    def _complete_torrent_command(self, text, line, begidx, endidx):
        args = self.arg_tokenize(line)
        item = args[-1] if len(args) > 1 else ''
        return self._complete_torrent(item, endidx - begidx)

    def help_quit(self):
        print('quit|exit\n')
        print('Exit to shell.\n')

    def do_quit(self, line):
        sys.exit('')
    #Alias
    do_exit = do_quit
    help_exit = help_quit
    do_EOF = do_quit

    def help_add(self):
        print('add <torrent file or url> [<target dir> paused=(yes|no) peer-limit=#]\n')
        print('Add a torrent to the transfer list.\n')

    def do_add(self, line):
        args = self.arg_tokenize(line)

        if len(args) == 0:
            print('Specify a torrent file or url')
            return

        torrent_url = args[0]
        args = args[1:]
        torrent_file = None
        if os.path.exists(torrent_url):
            torrent_file = open(torrent_url, 'r')
        else:
            try:
                torrent_file = urllib.request.urlopen(torrent_url)
            except:
                torrent_file = None
        if not torrent_file:
            print('Couldn\'t find torrent "%s"' % torrent_url)
            return

        add_args = {}
        if len(args) > 0:
            for arg in args:
                try:
                    (k,v) = arg.split('=')
                    add_args[str(k)] = str(v)
                except:
                    if 'download_dir' not in add_args:
                        try:
                            os.mkdir(arg)
                            add_args['target'] = arg
                            continue
                        except:
                            pass
                    print('Unknown argument: "%s"' % arg)

        torrent_data = base64.b64encode(torrent_file.read())
        try:
            self.tc.add(torrent_data, **add_args)
        except transmissionrpc.TransmissionError as e:
            print('Failed to add torrent "%s"' % e)

    def complete_remove(self, text, line, begidx, endidx):
        return self._complete_torrent_command(text, line, begidx, endidx)

    def help_remove(self):
        print('remove <torrent id> [,<torrent id>, ...]\n')
        print('Remove one or more torrents from the transfer list.\n')

    def do_remove(self, line):
        args = self.arg_tokenize(line)
        if len(args) == 0:
            raise ValueError('No torrent id')
        self.tc.remove(args)

    def complete_start(self, text, line, begidx, endidx):
        return self._complete_torrent_command(text, line, begidx, endidx)

    def help_start(self):
        print('start <torrent id> [,<torrent id>, ...]\n')
        print('Start one or more queued torrent transfers.\n')

    def do_start(self, line):
        args = self.arg_tokenize(line)
        if len(args) == 0:
            raise ValueError('No torrent id')
        self.tc.start(args)

    def complete_stop(self, text, line, begidx, endidx):
        return self._complete_torrent_command(text, line, begidx, endidx)

    def help_stop(self):
        print('stop <torrent id> [,<torrent id>, ...]\n')
        print('Stop one or more active torrent transfers.\n')

    def do_stop(self, line):
        args = self.arg_tokenize(line)
        if len(args) == 0:
            raise ValueError('No torrent id')
        self.tc.stop(args)

    def complete_verify(self, text, line, begidx, endidx):
        return self._complete_torrent_command(text, line, begidx, endidx)

    def help_verify(self):
        print('verify <torrent id> [,<torrent id>, ...]\n')
        print('Verify one or more torrent transfers.\n')

    def do_verify(self, line):
        args = self.arg_tokenize(line)
        if len(args) == 0:
            raise ValueError('No torrent id')
        self.tc.verify(args)

    def complete_info(self, text, line, begidx, endidx):
        return self._complete_torrent_command(text, line, begidx, endidx)

    def help_info(self):
        print('info [<torrent id>, ...]\n')
        print('Get details for a torrent. If no torrent id is provided, all torrents are displayed.\n')

    def do_info(self, line):
        args = self.arg_tokenize(line)
        if len(args) == 0:
            raise ValueError('No torrent id')
        result = self.tc.info(args)
        for id, torrent in result.items():
            print(self._torrent_detail(torrent))

    def help_list(self):
        print('list\n')
        print('List all torrent transfers.\n')

    def do_list(self, line):
        args = self.arg_tokenize(line)
        result = self.tc.list()
        self._list_torrents(result)

    def help_files(self):
        print('files [<torrent id>, ...]\n')
        print('Get the file list for one or more torrents\n')

    def do_files(self, line):
        args = self.arg_tokenize(line)
        result = self.tc.get_files(args)
        for tid, files in result.items():
            print('torrent id: %d' % tid)
            for fid, file in files.items():
                print('  %d: %s' % (fid, file['name']))

    def do_set(self, line):
        args = self.arg_tokenize(line)
        set_args = {}
        ids = []
        add_ids = True

        if len(args) > 0:
            for arg in args:
                try:
                    (k,v) = arg.split('=')
                    set_args[str(k)] = str(v)
                    add_ids = False
                except:
                    if add_ids:
                        ids.append(arg)
                    else:
                        print('Unknown argument: "%s"' % arg)
        if len(ids) > 0:
            result = self.tc.change(ids, **set_args)

    def complete_session(self, text, line, begidx, endidx):
        return self.word_complete(text, ['get', 'set', 'stats'])

    def help_session(self):
        print('session (get|stats)\n')
        print('Get session parameters or session statistics.\n')

    def do_session(self, line):
        args = self.arg_tokenize(line)
        if len(args[0]) == 0 or args[0] == 'get':
            self.tc.get_session()
            print(self.tc.session)
        elif args[0] == 'stats':
            print(self.tc.session_stats())

    def do_request(self, line):
        (method, sep, args) = line.partition(' ')
        try:
            args = eval(args)
        except SyntaxError:
            args = {}
        if not isinstance(args, dict):
            args = {}
        verbose = self.tc.verbose
        self.tc.verbose = True
        self.tc._request(method, args)
        self.tc.verbose = verbose

    def _list_torrents(self, torrents):
        if len(torrents) > 0:
            print(self._torrent_brief_header())
            for tid, torrent in torrents.items():
                print(self._torrent_brief(torrent))

    def _torrent_brief_header(self):
        return ' Id  Done   ETA           Status       Download    Upload      Ratio  Name'

    def _torrent_brief(self, torrent):
        s = '% 3d: ' % (torrent.id)
        try:
            s += '%5.1f%%' % torrent.progress
        except:
            pass
        try:
            if torrent.fields['eta'] > 0:
                s += ' %- 13s' % torrent.format_eta()
            else:
                s += ' -            '
        except:
            pass
        try:
            s += ' %- 12s' % torrent.status
        except:
            s += ' -status     '
            pass
        try:
            s += ' %5.1f %- 5s' % format_speed(torrent.rateDownload)
            s += ' %5.1f %- 5s' % format_speed(torrent.rateUpload)
        except:
            s += ' -rate     '
            s += ' -rate     '
            pass
        try:
            s += ' %6.2f' % torrent.ratio
        except:
            s += ' -ratio'
            pass
        s += ' ' + torrent.name
        return s

    def _torrent_detail(self, torrent):
        s = ''
        s +=   '            id: ' + str(torrent.fields['id'])
        s += '\n          name: ' + torrent.fields['name']
        s += '\n          hash: ' + torrent.fields['hashString']
        s += '\n'
        try: # size
            f = ''
            f += '\n      progress: %.2f%%' % torrent.progress
            f += '\n         total: %.2f %s' % format_size(torrent.totalSize)
            f += '\n      reqested: %.2f %s' % format_size(torrent.sizeWhenDone)
            f += '\n     remaining: %.2f %s' % format_size(torrent.leftUntilDone)
            f += '\n      verified: %.2f %s' % format_size(torrent.haveValid)
            f += '\n  not verified: %.2f %s' % format_size(torrent.haveUnchecked)
            s += f + '\n'
        except KeyError:
            pass
        try: # activity
            f = ''
            f += '\n        status: ' + str(torrent.status)
            f += '\n      download: %.2f %s' % format_speed(torrent.rateDownload)
            f += '\n        upload: %.2f %s' % format_speed(torrent.rateUpload)
            f += '\n     available: %.2f %s' % format_size(torrent.desiredAvailable)
            f += '\ndownload peers: ' + str(torrent.peersSendingToUs)
            f += '\n  upload peers: ' + str(torrent.peersGettingFromUs)
            s += f + '\n'
        except KeyError:
            pass
        try: # history
            f = ''
            f += '\n         ratio: %.2f' % torrent.ratio
            f += '\n    downloaded: %.2f %s' % format_size(torrent.downloadedEver)
            f += '\n      uploaded: %.2f %s' % format_size(torrent.uploadedEver)
            f += '\n        active: ' + format_timestamp(torrent.activityDate)
            f += '\n         added: ' + format_timestamp(torrent.addedDate)
            f += '\n       started: ' + format_timestamp(torrent.startDate)
            f += '\n          done: ' + format_timestamp(torrent.doneDate)
            s += f + '\n'
        except KeyError:
            pass
        return s

def main(args=None):
    """Main entry point"""
    if args is None:
        args = sys.argv[1:]
    parser = OptionParser(usage='Usage: %prog [options] [[address]:[port]] [command]')
    parser.add_option('-', '--username', dest='username',
                    help='Athentication username.')
    parser.add_option('-p', '--password', dest='password',
                    help='Athentication password.')
    (values, args) = parser.parse_args(args)
    commands = [cmd[3:] for cmd in itertools.ifilter(lambda c: c[:3] == 'do_', dir(Helical))]
    address = 'localhost'
    port = DEFAULT_PORT
    command = None
    for arg in args:
        if arg in commands:
            command = arg
            break
        try:
            (address, port) = inet_address(arg, DEFAULT_PORT)
        except INetAddressError:
            pass
    helical = Helical()
    try:
        helical.connect(address, port, values.username, values.password)
    except transmissionrpc.TransmissionError as error:
        print(error)
        parser.print_help()
        return

    if command:
        command_args = ' '.join(['"%s"' % arg for arg in args[args.index(command)+1:]])
        helical.onecmd(command + command_args)
    else:
        try:
            helical.cmdloop()
        except KeyboardInterrupt:
            helical.do_quit('')

if __name__ == '__main__':
    sys.exit(main())
