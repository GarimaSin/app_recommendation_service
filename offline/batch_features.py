# batch feature computation placeholder
def aggregate_user_features(events):
    # events: list of dicts
    feats = {}
    for e in events:
        uid = e['user_id']
        feats.setdefault(uid, 0)
        feats[uid] += 1
    return feats
