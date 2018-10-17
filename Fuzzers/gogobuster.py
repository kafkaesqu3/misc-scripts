#######################################################################
#######################################################################
###########                                                 ###########
########### GOGOBUSTER: Parallel directory bruteforcing     ###########
########### Scan multiple URLs concurrently with gobuster   ###########
###########                                                 ###########
#######################################################################
#######################################################################

# Gobuster was written by OJ Reeves @TheColonial
# https://github.com/OJ/gobuster

# Already have scanned a network with EyeWitness? https://github.com/FortyNorthSecurity/EyeWitness
# MiktoList.py can take the scan output and create a list of URLs with splash pages or 404
# https://github.com/FortyNorthSecurity/EyeWitness/blob/master/MiktoList.py

import multiprocessing
import argparse
import subprocess
import re
import sys

def runCommand(command):
    subprocess.call(command.split(' '))


def pool_function(command):
    try:
        return runCommand(command)
    except KeyboardInterrupt:
        return 'KeyboardException'

def main(): 
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-f", "--file", help="File with target URLs", required=True)
    argparser.add_argument("-w", "--wordlist", help="Wordlist to use across all URLs", required=True)
    argparser.add_argument("-o", "--output", help="Output directory", required=False)
    argparser.add_argument("-t", "--threads", type=int, help="# of threads (concurrent URLs to be scanned)", required=False)
    arguments = argparser.parse_args()

    file = arguments.file
    targets = open(file).read().splitlines()

    wordlist = arguments.wordlist
    output_folder = arguments.output

    if arguments.threads is None: 
        thread_count = 2
    else: 
        thread_count = arguments.threads

    pool = multiprocessing.Pool(thread_count)

    try:
        jobs = []
        for url in targets: 
            output_file = re.sub(r"https?://", '', url)
            command = "gobuster -m dir -e -l -k -u {0} -w {1} -o {2}/{3}_out".format(url, wordlist, output_folder, output_file)

            jobs.append(pool.apply_async(pool_function, args=([command])))
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        print 'parent received control-c'
        pool.terminate()

if __name__ == "__main__":
    main()