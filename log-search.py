#!/usr/bin/python
import sys, boto.logs, time
from datetime import datetime

log_group = 'LOG GROUP NAME'
timestamp = int(datetime.strptime(sys.argv[1], '%Y-%m-%dT%H:%M:%S').strftime('%s')) * 1000

logs = boto.logs.connect_to_region('eu-west-1')

if len(sys.argv) > 2:
    streams = sys.argv[2:]
else:
    def find_streams(token, timestamp):
        def valid_stream(stream):
            return stream['creationTime'] < timestamp and stream.get('lastIngestionTime') > timestamp

        data = logs.describe_log_streams(log_group_name=log_group, next_token=token)

        streams = filter(valid_stream, data['logStreams'])
        if len(streams) > 0 or 'nextToken' not in data:
            return streams

        time.sleep(0.5) # rate limiting
        print >> sys.stderr, data['logStreams'][-1]['logStreamName']
        return find_streams(data['nextToken'], timestamp)

    streams = [stream['logStreamName'] for stream in find_streams(None, timestamp)]

for stream in streams:
    print >> sys.stderr, '============== %s ==============' % stream

    def find_events(token, last_token, timestamp):
        def valid_event(event):
            return event['timestamp'] > timestamp and event['timestamp'] < timestamp + 60 * 60 * 1000

        data = logs.get_log_events(log_group_name=log_group, log_stream_name=stream, start_from_head=True, next_token=token)

        for event in filter(valid_event, data['events']):
            print event['message']

        if data['nextForwardToken'] != last_token:
            time.sleep(0.5) # rate limiting
            find_events(data['nextForwardToken'], token, timestamp)

    find_events(None, None, timestamp)
