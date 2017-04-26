import sys
import requests
import urllib.parse
import argparse

parser = argparse.ArgumentParser(description='Read chunks ids from stdin, read form IPFS, concat and print.')
parser.add_argument('--ipfs-api', type=str, default='http://localhost:5001/api/v0/', help='URL of IPFS API.')
parser.add_argument('--chunk-timeout', type=int, default=10, help='Chunk read timeout in seconds.')

if __name__ == '__main__':
    args = parser.parse_args()
    get_block_url = urllib.parse.urljoin(args.ipfs_api, 'block/get')

    while True:
        hash = sys.stdin.readline()
        if hash == '':
            sys.exit()
        hash = hash.strip()

        r = requests.get(
            get_block_url,
            params={'arg': hash},
            timeout=args.chunk_timeout
        )

        if r.status_code == requests.codes.ok:
            sys.stdout.buffer.write(r.content)
            sys.stdout.flush()
        else:
            print('read of chunk {} timed out'.format(hash), file=sys.stderr)
