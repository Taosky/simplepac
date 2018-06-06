# simplepac
Generate a simple pac for proxy and ad-block(use the code from [easylist-pac-privoxy](https://github.com/essandess/)).


    usage: simplepac [-h] -p PROXY -o OUTPUT [--proxy-rule PROXY_RULE]
                     [--user-rule USER_RULE] [--ad-block]
                     [--black-hole BLACK_HOLE]

    Generate a simple pac

    optional arguments:
      -h, --help            show this help message and exit
      -p PROXY, --proxy PROXY
                            pac proxy like "PROXY 127.0.0.1:8888","SOCKS
                            127.0.0.1:1080"
      -o OUTPUT, --output OUTPUT
                            output pac file
      --proxy-rule PROXY_RULE
                            [optional]proxy rule, Base64 or text, default use
                            gfwlist
      --user-rule USER_RULE
                            [optional]user rule like proxy rule, support cidr like
                            "IP-CIDR,91.108.4.0/22"
      --ad-block            [optional]enable ad block, use easylist.
      --black-hole BLACK_HOLE
                            [optional]ad proxy, usually use a unreachable proxy,
                            IOS may need to set nginx server,default:"PROXY
                            127.0.0.1:12306"


