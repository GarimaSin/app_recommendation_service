from catalog.catalog_loader import load_catalog
def get_app_meta(app_id):
    apps = load_catalog()
    for a in apps:
        if a['app_id']==app_id: return a
    return None
