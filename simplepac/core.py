from datetime import datetime
from . import utils
import requests
import argparse
import base64
import json

DEFAULT_PROXY_RULE = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'


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


def filter_rule(rule_text):
    url_match = set()
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
            icdr = line[8:].strip('\n')
            ip, end = icdr.split('/')
            mask = utils.get_mask(end)
            cidr_match.append([ip, mask])
        else:
            url_match.add(line.strip('|.@/').strip('|'))

    return list(url_match), cidr_match


def generate(proxy, url_json, cidr_json, path):
    update_time = datetime.now().strftime('%Y %m-%d %H:%M')

    pac_content = '''/*
 * Last Update: %s
 * https://github.com/Taosky/simplepac
 */
var Proxy = '%s; DIRECT;';

var urlList = %s;

var cidrList = %s;

function isMatchProxy(url, pattern) {
    try {
        return new RegExp(pattern.replace('.', '\\.')).test(url);
    } catch (e) {
        return false;
    }
}
function FindProxyForURL(url, host) {
    for(var i=0, l=cidrList.length; i<l; i++) {
        if (isInNet(host, cidrList[i][0], cidrList[i][1])){
            return Proxy;
        }
    }

    for(var j=0, m=urlList.length; j<m; j++) {
        if (isMatchProxy(url, urlList[j])) {
            return Proxy;
        }
    }
    return 'DIRECT';
}
    ''' % (update_time, proxy, url_json, cidr_json)
    try:
        with open(path, 'w', encoding='utf-8') as pac:
            pac.write(pac_content)
    except BaseException as e:
        print(e)


def main(rule_url, proxy, pac_path, user_rule_path):
    url_rule_data = get_url_rule(rule_url)
    if url_rule_data:
        user_rule_data = get_user_rule(user_rule_path)
        rule_data = '\n'.join([url_rule_data, user_rule_data])
        url_lst, cidr_result_lst = filter_rule(rule_data)
        url_json = json.dumps(url_lst)
        cidr_json = json.dumps(cidr_result_lst)
        generate(proxy, url_json, cidr_json, pac_path)


def run():
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
    args = parser.parse_args()
    proxy_opt = args.proxy
    output_opt = args.output
    proxy_rule_opt = args.proxy_rule
    user_rule_opt = args.user_rule
    ad_rule_opt = args.ad_rule

    if not proxy_rule_opt:
        proxy_rule_opt = DEFAULT_PROXY_RULE

    main(proxy_rule_opt, proxy_opt, output_opt, user_rule_opt)
