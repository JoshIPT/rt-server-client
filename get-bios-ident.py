#!/usr/bin/env python

from __future__ import print_function
import sys
import argparse
import pprint
import commands
import re

# Add to path to include paths
#sys.path.append('path')


# Classes definition {{{
class colors:
    NOC     = '\033[0m'
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    BLUE    = '\033[94m'

output = {}

#}}} Classes definition


# Print functions {{{
def pout(*objs):
    print('', *objs, file=sys.stdout)
    sys.stdout.flush()


def pwrn(*objs):
    print('WARNING: ', *objs, file=sys.stderr)


def perr(*objs):
    print(colors.RED + 'ERROR: ', *objs, end='', file=sys.stderr)
    print(colors.NOC, file=sys.stderr)


def pdeb(*objs):
    pprint.pprint(*objs)

def getServiceTag(output, dmidecode):
    # Vendor specific
    # HUAWEI
    if output['vendor'] == 'Huawei':
        if re.findall('Serial Number: .*', dmidecode):
            return re.findall('Serial Number: .*', dmidecode)[1].split()[2]
    elif output['vendor'] == 'Supermicro':
        if re.findall('UUID: .*', dmidecode):
            return re.findall('UUID: .*', dmidecode)[0].split("-")[-1]
    # DELL and others
    else:
        if re.findall('Serial Number: .*', dmidecode):    
            return re.findall('Serial Number: .*', dmidecode)[0].split()[2]

    return 'unknown' 

#}}} Print functions


# Exit functions {{{
def cleanup():
    return 0


def eexit(ecode, msg):
    cleanup()
    if msg:
        if ecode == 0:
            pout(colors.GREEN + msg + colors.NOC)
        else:
            perr(msg)
    sys.exit(ecode)
#}}} Exit functions


if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser(
        description= 'Script return service tag string based on vendor and others', 
        epilog='Created by Robert Vojcik <robert@vojcik.net>')
    
    # Example of sample arguments
    parser.add_argument('-v', action="store_true", dest="action_vendor", default=False, help='Print vendor name')
    parser.add_argument('-m', action="store_true", dest="action_model", default=False, help='Print model name')
    parser.add_argument('-t', action="store_true", dest="action_st", default=False, help='Print service tag')
    parser.add_argument('-s', action="store_true", dest="action_simple", default=False, help='Batch print, simple output')
    parser.add_argument('-u', action="store_true", dest="action_uuid", default=False, help='Print system UUID')
    
    args = parser.parse_args()

    dmidecode = commands.getstatusoutput('dmidecode -q')

    if dmidecode[0] == 0:

        # VENDOR
        if re.findall('Manufacturer:.*', dmidecode[1]):
            output['vendor'] = re.findall('Manufacturer:.*', dmidecode[1])[0].split()[1]
        else:
            output['vendor'] = 'unknown'

        # PRODUCT NAME
        if re.findall('Product Name:.*', dmidecode[1]):
            output['product_name'] = ' '.join(re.findall('Product Name:.*', dmidecode[1])[0].split()[2:])
        else:
            output['product_name'] = 'unknown'

        # UUID
        if re.findall('UUID:.*', dmidecode[1]):
            output['UUID'] = re.findall('UUID:.*', dmidecode[1])[0].split()[1]
        else:
            output['UUID'] = 'unknown'

        # SERIAL NUMBER
        output['servicetag'] = getServiceTag(output, dmidecode[1])


        if args.action_vendor:
            if args.action_simple:
                print(output['vendor'])
            else:
                print('vendor: %s' %(output['vendor']))

        if args.action_model:
            if args.action_simple:
                print(output['product_name'])
            else:
                print('model_name: %s' %(output['product_name']))

        if args.action_st:
            if args.action_simple:
                print(output['servicetag'])
            else:
                print('service_tag: %s' %(output['servicetag']))

        if args.action_uuid:
            if args.action_simple:
                print(output['UUID'])
            else:
                print('UUID: %s' %(output['UUID']))
     
    else:
        eexit(1, 'Problem during executing dmidecode')
