import sys
import requests
import urllib.parse
import argparse

parser = argparse.ArgumentParser(description='Read data from stdin, store chunks in IPFS, print chunk hashes.')
parser.add_argument('--chunk-size', type=int, default=4096, help='Chunk size in bytes.')
parser.add_argument('--ipfs-api', type=str, default='http://localhost:5001/api/v0/', help='URL of IPFS API.')

if __name__ == '__main__':
    args = parser.parse_args()

    buff = bytearray([0 for i in range(args.chunk_size)])
    put_block_url = urllib.parse.urljoin(args.ipfs_api, 'block/put')

    while True:
        n = sys.stdin.buffer.readinto(buff)
        if n == 0:
            sys.exit()

        r = requests.post(put_block_url, files={'file': ('buff', buff[:n], 'application/octet-stream')})
        r.raise_for_status()
        sys.stdout.write('{}\n'.format(r.json()['Key']))
        sys.stdout.flush()
