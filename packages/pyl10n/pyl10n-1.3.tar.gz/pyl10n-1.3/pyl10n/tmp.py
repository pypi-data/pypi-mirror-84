import json
import sys
import pickle
for f in sys.argv[1:]:
    print(f)
    with open(f, 'rb') as fp:
        d = pickle.load(fp)
    with open(f, 'w') as fp:
        json.dump(obj=d, fp=fp, sort_keys=True, separators=(',', ':'))
