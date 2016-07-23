#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading


class read_stdout_thread(threading.Thread):

    def __init__(self, dictionary):
        threading.Thread.__init__(self)

        self.daemon = True
        self.dictionary = dictionary

    def run(self):
        while True:
            chat_proc_dict = self.dictionary.copy()
            for key, value in chat_proc_dict.iteritems():
                # stderr_line = value['proc'].stderr.readline()
                # stderr_line = value['proc'].stderr.readline()
                # if stderr_line != '':
                #     value['bot'].sendMessage(key, text=stderr_line)
                
                stdout_line = value['proc'].stdout.readline()
                if stdout_line != '':
					value['bot'].sendMessage(key, text=stdout_line)