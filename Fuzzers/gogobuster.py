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
from random import randint
from time import sleep

dryrun = False

def runCommand(command):
    try: 
        if dryrun: 
            print(' '.join(command))
            sleep(randint(10,20))
        else: 
            subprocess.call(command)    
    except KeyboardInterrupt, e:
        pass

def main(): 
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-u", "--url", help="Single target URLs", required=False)
    argparser.add_argument("-U", "--url-list", help="File with all URLs to test", required=False)
    argparser.add_argument("-w", "--wordlist", help="Wordlist to use across all URLs", required=False)
    argparser.add_argument("-W", "--wordlist-file", help="Path to file containing 1 path per line of all the wordlists to use", required=False)
    argparser.add_argument("-o", "--output", help="Output directory", required=False)
    argparser.add_argument("-t", "--threads", type=int, help="# of threads (concurrent URLs to be scanned)", required=False)
    argparser.add_argument("-d", "--dryrun", action='store_true', help="Print gobuster commands that will be run, but do not execute", required=False)
    arguments = argparser.parse_args()

    global dryrun
    dryrun = arguments.dryrun
    
    targets = []
    if arguments.url: 
        targets.append(arguments.url)    
    elif arguments.url_list: 
        targets_file = open(arguments.url_list).read().splitlines()
        for target in targets_file: 
            targets.append(target)
    else: 
        print("You need either a single URL (-u) or a file containing URLs (-U)")    


    wordlists = []
    if arguments.wordlist: 
        wordlists.append(arguments.wordlist)    
    elif arguments.wordlist_file: 
        wordlist_file = open(arguments.wordlist_file).read().splitlines()
        for wordlist in wordlist_file: 
            wordlists.append(wordlist)
    else: 
        print("You need either a wordlist (-w) or a file containing wordlists (-W)")

    output_folder = arguments.output

    # Gobuster uses 10 threads by default, 
    if arguments.threads is None: 
        thread_count = 2
    else: 
        thread_count = arguments.threads
        if thread_count > 4: 
            print("WARNING: Gobuster runs with 10 threads; you're about to run {0}*10={1} threads\n".format(thread_count, 10*thread_count))
            print("That's a lot of threads, be careful!\n")
            input("Press Enter to continue, press Ctrl-C to cancel")
    pool = multiprocessing.Pool(thread_count)
    try: 
        for url in targets: 
            if not url: continue
            for wordlist in wordlists: 
                if not wordlist: continue
                # no slashes in our output file name!
                output_file = re.sub(r"https?://", '', url)
                if output_file[-1] == "/": 
                    output_file = output_file[:-1]
                command = "gobuster -m dir -e -l -k -u {0} -w {1} -o {2}/{3}_out".format(url, wordlist, output_folder, output_file)

                #map_asyc will only take a single argument, so we must pass it a list. subprocess requires a list too so this is no problem
                p = pool.map_async(runCommand, [command.split(' ')])

        
            results = p.get()
    except KeyboardInterrupt: 
        print('Received control-c, cya!')
        return

if __name__ == "__main__":
    main()
