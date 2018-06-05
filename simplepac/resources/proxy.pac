/*
 * Last Update: __UPDATE__
 * https://github.com/Taosky/simplepac
 */

var urlList = __DOMAINS__;

var cidrList = __CIDRS__;

var proxy = '__PROXY__; DIRECT;'; // 'PROXY' or 'SOCKS5' or 'HTTPS'

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
            return proxy;
        }
    }

    for(var j=0, m=urlList.length; j<m; j++) {
        if (isMatchProxy(url, urlList[j])) {
            return proxy;
        }
    }
    return 'DIRECT';
}