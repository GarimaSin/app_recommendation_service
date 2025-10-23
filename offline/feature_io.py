import json
def save_features(path, features):
    with open(path,'w') as f:
        json.dump(features,f)
