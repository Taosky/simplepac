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


def filter_rule(rule_text):
    result = set()
    for line in rule_text.split('\n'):
        if line.startswith('@@||') \
                or line.startswith('[') \
                or line.startswith('!') \
                or line.startswith('%') \
                or line.startswith('search') \
                or line.strip() == '':
            continue
        else:
            result.add(line.strip('|.@/').strip('|'))

    return json.dumps(list(result))


def generate(proxy, rules, path):
    update_time = datetime.now().strftime('%Y %m-%d %H:%M')

    pac_content = '''/*
 * Last Update: %s
 * https://github.com/Taosky/simplepac
 */
var list = %s;

function isMatchProxy(url, pattern) {
    try {
        return new RegExp(pattern.replace('.', '\\.')).test(url);
    } catch (e) {
        return false;
    }
}
function FindProxyForURL(url, host) {
    var Proxy = '%s; DIRECT;';
    for(var i=0, l=list.length; i<l; i++) {
        if (isMatchProxy(url, list[i])) {
            return Proxy;
        }
    }
    return 'DIRECT';
}
    ''' % (update_time,rules, proxy)
    try:
        with open(path, 'w', encoding='utf-8') as pac:
            pac.write(pac_content)
    except BaseException as e:
        print(e)


def main(rule_url, proxy, pac_path, custom_rule):
    rule_data = get_url_rule(rule_url)
    if rule_data:
        rule_json = filter_rule(rule_data)
        generate(proxy, rule_json, pac_path)


def run():
    custom_rule_opt = ''
    parser = argparse.ArgumentParser(description='Generate a simple pac')
    parser.add_argument('-p', '--proxy', required=True, dest='proxy',
                        help='pac proxy like "PROXY 127.0.0.1:8888","SOCKS 127.0.0.1:1080"')
    parser.add_argument('-o', '--output', dest='output', required=True,
                        help='output pac file')
    parser.add_argument('--proxy-rule', dest='proxy_rule',
                        help='proxy rule, Base64 or text, default use gfwlist')
    parser.add_argument('--ad-rule', dest='ad_rule', help='ad rule to block ads')
    args = parser.parse_args()
    proxy_opt = args.proxy
    output_opt = args.output
    proxy_rule_opt = args.proxy_rule
    ad_rule_opt = args.ad_rule

    if not proxy_rule_opt:
        proxy_rule_opt = DEFAULT_PROXY_RULE

    main(proxy_rule_opt, proxy_opt, output_opt, custom_rule_opt)
