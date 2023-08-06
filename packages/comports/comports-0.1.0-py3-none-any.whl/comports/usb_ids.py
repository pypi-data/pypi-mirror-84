import os
import re
import locale
import shutil
from datetime import datetime
from urllib import request


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'usb.ids')
DATE_PAT = re.compile(r'^# Date\: +(\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2}\:\d{2})$')
PAT = re.compile(r'^(?:(?P<vendor_id>[\da-f]{4})|\t(?P<product_id>[\da-f]{4}))  (?P<name>.+)$')
_cache = None


def get_ids_file_date(filename=DEFAULT_PATH):
    if not os.path.isfile(filename):
        return None
    with open(filename) as in_f:
        for line in in_f:
            m = DATE_PAT.findall(line)
            if m:
                return datetime.strptime(m[0], '%Y-%m-%d %H:%M:%S')


def auto_update_ids_file(filename=DEFAULT_PATH):
    file_date = get_ids_file_date(filename)
    req = request.urlopen('http://www.linux-usb.org/usb.ids')

    if file_date is not None:
        locale.setlocale(locale.LC_TIME, 'C')
        update_date = datetime.strptime(req.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')

        if file_date >= update_date:
            return False

    with open(filename, 'wb') as f:
        shutil.copyfileobj(req, f)

    return True


def _norm(value, do=True):
    value = value or 0
    if (not do) or isinstance(value, int):
        return value
    return int(value, 16)


def parse_ids_file(filename=DEFAULT_PATH, normalize=True, auto_update=True):
    if auto_update:
        try:
            auto_update_ids_file(filename)
        except Exception:
            pass

    ret = {}
    vendor_id = None
    with open(filename) as in_f:
        for line in in_f:
            match = PAT.match(line)
            if not match:
                continue
            d = match.groupdict()
            if d['vendor_id']:
                vendor_id = _norm(d['vendor_id'], normalize)
                ret[vendor_id] = (d['name'], {})
                continue
            ret[vendor_id][1][_norm(d['product_id'], normalize)] = d['name']
    return ret


def get(vendor_id, product_id=None, auto_update=True):
    global _cache
    if not _cache:
        _cache = parse_ids_file(auto_update=auto_update)
    vendor = _cache.get(_norm(vendor_id), ('', {}))
    if product_id is None:
        return vendor[0]
    return (vendor[0], vendor[1].get(_norm(product_id), ''))


def main():
    import json
    import sys
    args = [int(x, 0) for x in sys.argv[1:]]
    if len(args) >= 2:
        print(' : '.join(get(*args)))
    elif len(args) >= 1:
        print(get(*args))
    else:
        print(json.dumps(parse_ids_file(normalize=False),
                         separators=(',', ': '),
                         indent=2,
                         sort_keys=True))


if __name__ == '__main__':
    main()
