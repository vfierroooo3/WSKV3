def access_collection(client,collection_name):
    '''Enter Collection Name to Access From Database'''
    db = client.WSKV3
    return db[collection_name]
