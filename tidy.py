import sys
import pandas as pd

df = pd.read_csv(sys.argv[1])
if df.empty:
    print()
    print('NO UPDATES')
    print()
else:
    for source in ['London Data', 'Government Statistical Research', 'ONS', 'Government Data']:
        print()
        print('~~~')
        print(source)
        print('~~~')
        print()
        for index, row in df[df['source'] == source].iterrows():
            print(row['datetime'])
            print(row['title'])
            print(row['url'])
            if source == ['Government Statistical Research']:
                print(row['description'])
            print()
            print('---')
            print()
        print()
        print()
        print()
