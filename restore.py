import sys
import requests
import urllib.parse
import argparse
import threading
import time

parser = argparse.ArgumentParser(description='Read chunks ids from stdin, read form IPFS, concat and print.')
parser.add_argument('--ipfs-api', type=str, default='http://localhost:5001/api/v0/', help='URL of IPFS API.')
parser.add_argument('--max-lag', type=float, default=10, help='How big lag behind a source is acceptable, in seconds. (Will drop chunks to catch-up.)')

def retrive_block(get_block_url, hash, deadline, callback):
    try:
        r = requests.get(
            get_block_url,
            params={'arg': hash},
            timeout=deadline - time.monotonic()
        )

        if r.status_code == requests.codes.ok:
            callback(r.content)
        else:
            print('{} read failed'.format(hash), file=sys.stderr)
            callback(None)

    except requests.exceptions.ReadTimeout:
        print('{} read timed out'.format(hash), file=sys.stderr)
        callback(None)

def retrive_block_in_order(previous_done, this_done, callback, **kwargs):
    def cb(data):
        previous_done.wait()
        callback(data)
        this_done.set()
    retrive_block(
        callback=cb,
        **kwargs
    )

def print_binary(data):
    if data is not None:
        sys.stdout.buffer.write(data)
        sys.stdout.flush()

if __name__ == '__main__':
    args = parser.parse_args()
    get_block_url = urllib.parse.urljoin(args.ipfs_api, 'block/get')

    previous_done = threading.Event()
    previous_done.set()
    while True:
        hash = sys.stdin.readline()
        if hash == '':
            previous_done.wait()
            sys.exit()
        hash = hash.strip()

        this_done = threading.Event()
        threading.Thread(
            target=retrive_block_in_order,
            kwargs=dict(
                previous_done=previous_done,
                this_done=this_done,
                callback=print_binary,
                get_block_url=get_block_url,
                hash=hash,
                deadline=time.monotonic() + args.max_lag
            )
        ).start()
        previous_done = this_done
