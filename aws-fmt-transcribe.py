#!/usr/bin/env python3

# Simple script to take the JSON output from AWS Transcribe and
# print it as a formatted text file
#
# Expects JSON to be fed on stdin

import collections
import json
import sys

def format_secs(secs):
    mins, secs = divmod(secs, 60)
    return "[%02d:%02d]" % (mins, secs)

data = json.load(sys.stdin)

speaker_starts = collections.defaultdict(lambda: "unknown")

for segment in data['results']['speaker_labels']['segments']:
    for item in segment['items']:
        speaker_starts[item['start_time']] = item['speaker_label']

last_speaker = None
start_time = -1
items = []
for item in data['results']['items']:
    if item['type'] == 'punctuation' and len(items) > 0:
        items[-1] += item['alternatives'][0]['content']
        continue

    speaker = speaker_starts[item['start_time']]
    if speaker != last_speaker:
        start_time = float(item['start_time'])
        if len(items):
            print("\n" + format_secs(start_time) + " "+speaker + ": " + " ".join(items))
        items = []
    items.append(item['alternatives'][0]['content'])
    last_speaker = speaker

if len(items):
    print("\n" + format_secs(start_time) + " "+speaker + ": " + " ".join(items))
