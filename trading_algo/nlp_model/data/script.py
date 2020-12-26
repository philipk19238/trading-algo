import json 

with open('daily_data.json', 'r') as f: 
    all_comments = json.loads(f.readline())
    with open('temp.json', 'w') as fs:
        for comment in all_comments:
            json.dump(comment, fs)
            fs.write('\n')