Streams over IPFS?
==================

Well, I think streams are impossible in content-adressed, immutable
filesystem... but we can use IPFS as a carrier of chunks.

Idea is as follows: you take stream, split it into chunks, you push each
chunk into IPFS and send the hashes to the receivers (using less fancy
media, like TCP). Receiver reads hashes, collects chunks from IPFS and
recreates the stream.

Utility
-------

 * `store.py` - splits stdin, saves to IPFS, outputs hashes to stdout
 * `restore.py` - reads hashes from stdin, reads data from IPFS, outputs
   original stream to stdout

Examples
--------

"Identity":

    python store.py | python restore.py

Webcam streaming (to a file...):

    ffmpeg -f v4l2 -framerate 25 -video_size 640x480 -i /dev/video0 -f mpeg - | python store.py > chunks

And a client for this stream:

    tail -f chunks | python restore.py | ffplay -f mpeg -
