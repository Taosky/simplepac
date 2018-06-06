/*
 * Last Update: __UPDATE__
 * https://github.com/Taosky/simplepac
 */

var proxy = '__PROXY__; DIRECT;';

// on iOS a working blackhole requires return code 200;
// e.g. use the adblock2privoxy nginx server as a blackhole
var blackhole = "__BLACKHOLE__";


var urlList = __DOMAINS__;

var cidrList = __CIDRS__;


__EASYLIST__


function isMatchProxy(url, pattern) {
    try {
        return new RegExp(pattern.replace('.', '\\.')).test(url);
    } catch (e) {
        return false;
    }
}
function FindProxyForURL(url, host) {
    if (isPlainHostName(host) ||
        shExpMatch(host, "10.*") ||
        shExpMatch(host, "172.16.*") ||
        shExpMatch(host, "192.168.*") ||
        shExpMatch(host, "127.*") ||
        dnsDomainIs(host, ".LOCAL") ||
        dnsDomainIs(host, ".local") ||
        (url.substring(0,4) == "ftp:")){
            return "DIRECT";
        }
    else if (EasyListFindProxyForURL(url, host)){
        return blackhole;
    }

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
