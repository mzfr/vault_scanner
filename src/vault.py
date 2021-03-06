#!/usr/bin/env python

import argparse
import sys


""" This is the beginning point for VAULT Scanner.

    OPTIONS ->

    1. Scan a website for the following - 1. XSS
                                          2. LFI
                                          3. RFI
                                          4. SQLi

    2. Common header erros : 1. Clickjacking
                             2. jQuery
                             3. Insecure cookie flags
                             4. Session fixation through a cookie injection
                             5. Spoofing Agents
                             6. Brute force login through authorization header
                             7. Testing HTTP methods
                             8. Insecure headers

    3. Collecting data 1. Port scanning
                       2. Header grabbing
                       3. Banner grabbing
                       4. Finding comments in source code
                       5. Smartwhois scan
                       6. Check if error handling is done or not and extract the site data using that information
                       7. OS Scanning

    4. SSL scanner

    5. Crawl a website and collect all the url related fields

    6. Scrap a website and collect all the images

    7. URL fuzzing

    8. Shellsock checking
"""

if __name__ == '__main__':

    print('\nWelcome to VAULT Scanner...\n')

    # Taking in arguments
    parser = argparse.ArgumentParser(description="VAULT Scanner")

    parser.add_argument('-u', '--url', help='URL for scanning')
    parser.add_argument('-p', '--port', action='store_true', help='Port for scanning')
    parser.add_argument('-sp', '--start_port', action='store_true', help='Start port for scanning')
    parser.add_argument('-ep', '--end_port', action='store_true', help='End port for scanning')
    parser.add_argument('-ssl', action='store_true', help='perform SSL scan')
    parser.add_argument('-info', action='store_true', help='Gather information')
    parser.add_argument('-comment', action='store_true', help='Finding comments')
    parser.add_argument('-fuzz', action='store_true', help='Fuzzing URL')

    # Print help message if no argumnents are supplied
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.ssl:
        if not args.url:
            print('[-] Please enter an URL for SSL scanning')
            sys.exit(1)
        try:
            from ssl_scanner import ssl_scanner
            print('\n--SSL scan using SSL Labs API--\n')

            data = ssl_scanner.analyze(args.url)
            ssl_scanner.vulnerability_parser(data)
        except ImportError:
            print('[-] Could not import the required module.')
        except Exception as e:
            print(e)

    if args.info:
        if not args.url:
            print('[-] Please enter an URl for information gathering')
            sys.exit(1)
        try:
            from info_gathering import header_vuln
            print('[+] Performing informatio gathering over : {}'.format(args.url))

            infoGatherObj = header_vuln.HeaderVuln(args.url)
            infoGatherObj.gather_header()
            infoGatherObj.insecure_cookies()
            infoGatherObj.test_http_methods()
        except ImportError:
            print('[-] Could not import the required module.')
        except Exception as e:
            print(e)

    if args.comment:
        if not args.url:
            print('[-] Please enter an URL for finding comments')
            sys.exit(1)
        try:
            from info_gathering import finding_comment
            print('[+] Performing comment gathering over : {}'.format(args.url))

            findCommnentObj = finding_comment.FindingComments(args.url)
            findCommnentObj.parse_comments()

        except ImportError:
            print('[-] Could not import the required module.')
        except Exception as e:
            print(e)

    if args.fuzz:
        if not args.url:
            print('[-] Please enter an URL for fuzzing')
            sys.exit(1)
        try:
            from fuzzer import fuzzer
            print('[+] Performing fuzzing on : {}'.format(args.url))
            fuzzObj = fuzzer.Fuzzer(base_url=args.url)
            fuzzObj.initiate()

        except ImportError:
            print('[-] Could not import the required module.')
        except Exception as e:
            print(e) 
