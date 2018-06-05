from datetime import datetime
from urllib.parse import urlparse
from . import utils
import requests
import argparse
import pkgutil
import base64
import json

DEFAULT_PROXY_RULE = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'


def parse():
    parser = argparse.ArgumentParser(description='Generate a simple pac')
    parser.add_argument('-p', '--proxy', required=True, dest='proxy',
                        help='pac proxy like "PROXY 127.0.0.1:8888","SOCKS 127.0.0.1:1080"')
    parser.add_argument('-o', '--output', dest='output', required=True,
                        help='output pac file')
    parser.add_argument('--proxy-rule', dest='proxy_rule',
                        help='proxy rule, Base64 or text, default use gfwlist')
    parser.add_argument('--user-rule', dest='user_rule',
                        help='user rule like proxy rule, support cidr like "IP-CIDR,91.108.4.0/22"')

    parser.add_argument('--ad-rule', dest='ad_rule', help='ad rule to block ads')

    return parser.parse_args()


def get_url_rule(url):
    try:
        content = requests.get(url).text
        if utils.is_base64(content):
            decode_data = base64.b64decode(content).decode('utf-8')
            return decode_data
        else:
            return content
    except BaseException as e:
        print(e)
        return None


def get_user_rule(rule_file):
    content = ''
    try:
        with open(rule_file, 'r', encoding='utf-8') as rule:
            content = rule.read()
    except BaseException as e:
        print(e)

    return content


def get_host(something):
    try:
        if not something.startswith(('http:', 'https:')):
            something = 'http://' + something
        hostname = urlparse(something).hostname
        return hostname
    except BaseException as e:
        print(e)
        return ''


def filter_rule(rule_text):
    host_match = set()
    cidr_match = []
    for line in rule_text.split('\n'):
        if line.startswith('@@||') \
                or line.startswith('[') \
                or line.startswith('!') \
                or line.startswith('%') \
                or line.startswith('search') \
                or line.strip() == '':
            continue

        elif line.startswith('IP-CIDR,'):
            cidr = line[8:].strip('\n')
            ip, end = cidr.split('/')
            mask = utils.get_mask(end)
            cidr_match.append([ip, mask])
        else:
            hostname = get_host(line.strip('|.@/').strip('|'))
            host_match.add(hostname)

    return list(host_match), cidr_match


def generate(proxy, host_json, cidr_json, path):
    update_time = datetime.now().strftime('%Y %m-%d %H:%M')

    pac_content = pkgutil.get_data(__package__, 'resources/proxy.pac').decode('utf-8')
    pac_content = pac_content.replace('__PROXY__', proxy)
    pac_content = pac_content.replace('__UPDATE__', update_time)
    pac_content = pac_content.replace('__CIDRS__', cidr_json)
    pac_content = pac_content.replace('__DOMAINS__', host_json)
    try:
        with open(path, 'w', encoding='utf-8') as pac:
            pac.write(pac_content)
    except BaseException as e:
        print(e)


def main(rule_url, proxy, pac_path, user_rule_path):
    print('getting rule from {}'.format(rule_url))
    url_rule_data = get_url_rule(rule_url)
    if url_rule_data:
        if user_rule_path:
            print('getting user rule...')
            user_rule_data = get_user_rule(user_rule_path)
        else:
            user_rule_data = ''
        print('generating pac...')
        rule_data = '\n'.join([url_rule_data, user_rule_data])
        host_lst, cidr_result_lst = filter_rule(rule_data)
        host_json = json.dumps(host_lst)
        cidr_json = json.dumps(cidr_result_lst)
        generate(proxy, host_json, cidr_json, pac_path)


def run():
    args = parse()
    proxy_opt = args.proxy
    output_opt = args.output
    proxy_rule_opt = args.proxy_rule
    user_rule_opt = args.user_rule
    ad_rule_opt = args.ad_rule
    if not proxy_rule_opt:
        proxy_rule_opt = DEFAULT_PROXY_RULE
    main(proxy_rule_opt, proxy_opt, output_opt, user_rule_opt)
