#!/usr/bin/python3
import sys
import shlex
import subprocess
import argparse
import codecs
import time

from .xml_reader import load_xml_file, XmlReader, get_node_location
from .timeout import Timeout


INIT_XML = '''<?xml version="1.0" encoding="UTF-8"?>
<doc>
    Каждый узел задает один процесс.

    Имя узла -  Роли не играет, используется только для логов.
                Должно быть уникальным в файле.

    cmd -       Обязательный атрибут, задает программу с аргументами
    
    pauseSec -  Необязательный атрибут (по умолчанию 0) - задержка перед запуском в сек. 
                Может быть полезен, чтобы дать ядру загрузиться перед запуском сателлитов.

    <volcano cmd="python -m volcano.core --demo" />
    
    <web cmd="python -m volcano.web" pauseSec="5" />
    
</doc>
'''


def configure_my_args(parser):
    parser.add_argument('--init', help='Create sample config file', action='store_true')


class MyProcess:
    def __init__(self, node, env):
        self.env = env
        
        nd = XmlReader(node)
        
        self.name_ = node.tag
        self.cmd_ = nd.get_str('cmd')
        self.restart_ = nd.get_bool('restart', default=True)
        
        pause_sec = nd.get_int('pauseSec', default=0)

        self.start_timeout_ = Timeout(expired=False, timeout_sec=pause_sec)
        self.process_ = None

    def name(self):
        return self.name_

    def safe_close(self):
        if self.process_:
            print(f'Killing {self.name_}...')
            self.process_.kill()
            print(f'Killing {self.name_} done')
            self.process_ = None

    def launch_(self):
        args=shlex.split(self.cmd_)
        
        self.start_timeout_.expire()
        try:
            if self.env.pipe_streams:
                self.process_ = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                self.process_ = subprocess.Popen(args)
        except Exception as ex:
            print(f'{self.name_}: Error launching "{self.cmd_}": {ex}')
            raise
            
    def communicate(self) -> (int, None):
        if self.process_ is None:   # not launched
            if self.start_timeout_.is_expired():
                self.launch_()
            else:
                print (f'{self.name_}: Launch postponed for {int(self.start_timeout_.remain_sec())} sec')
                
            return None
        
        ret_code = self.process_.poll()
        if ret_code is None:
            # Process still running
            if self.env.pipe_streams:
                line = self.process_.stdout.readline()
                while line:
                    msg = line.decode().rstrip()  # to prevent printing several newlines
                    print (f'{self.name_} {msg}')
                    line = self.process_.stdout.readline()
        else:
            if self.restart_:
                self.process_ = None
                print (f'{self.name_} failed with code {ret_code}. Relaunch scheduled')
                self.start_timeout_.start()
            else:
                print (f'{self.name_} failed with code {ret_code}. No restart, exiting')
                return ret_code
        return None


def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    configure_my_args(parser)
    env = parser.parse_args()

    if env.init:
        file_name = 'proc(demo).xml'
        with codecs.open(file_name, 'w', 'utf-8') as f:
            f.write(INIT_XML)
        
        print('Example config written to "{}". Rename it to "proc.xml" and use'.format(file_name))
        return 0

    env.pipe_streams = False

    #g_WorkingDir = os.getcwd()

    file_name = 'proc.xml'
    try:
        g_tree = load_xml_file(file_name)
    except Exception as ex:
        print(f'Error loading {file_name}: {ex}')
        return 1

    processes = []
    names_map = {}
        
    for node in g_tree.getroot():
        if node.tag in names_map:
            print(f'{get_node_location(node)}: Duplicated node name {node.tag}')
            return 1
        
        names_map[node.tag] = True
        processes.append ( MyProcess(node, env) )

    if not processes:
        print('No processes specified')
        return 1

    try:
        # if we dont pipe streams (processes just inherit stdout) we dont need to check very often
        sleep_time_sec = 0.1 if env.pipe_streams else 1.0

        stop = False
        while not stop:
            time.sleep(sleep_time_sec)
            for p in processes:
                ret_code = p.communicate ()
                if ret_code is not None:
                    stop = True     # exit while
                    break           # exit for
        return 0
        
    except KeyboardInterrupt:
        print ("\n\n << Keyboard interrupt >> \n\n")
    
    finally:
        print ("Stop all processes...")
        for p in processes:
            p.safe_close()

sys.exit(main())
