from pymongo import MongoClient
import mongo_parser
import os

def ingest():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.everspoti

    songs = db.songs
    playlists = db.playlists
    users = db.users

    ETC_PATH = './etc'

    songs_file = os.path.join(ETC_PATH, 'Songs.csv')
    users_file = os.path.join(ETC_PATH, 'UsersCollectionData.csv')
    playlists_file = os.path.join(ETC_PATH, 'PlaylistsCollectionData.csv')

    data_ingestion = (
        [songs, songs_file, 'Songs', mongo_parser.MongoParser.parse_songs_file],
        [users, users_file, 'Users', mongo_parser.MongoParser.parse_users_file],
        [playlists, playlists_file, 'Playlists', mongo_parser.MongoParser.parse_playlists_file],
    )

    for element in data_ingestion:
        collection, file_path, alias, function_name = element

        print 'Reading file in path %s to ingest in collection %s ... ' % (file_path, alias)

        if not os.path.exists(file_path):
            print '\n\n*****%s file does not exist !*****\n\n' % file_path
            continue

        elements = function_name(file_path)
        collection.drop()
        collection.insert_many(elements)
    print 'Data loaded into Mongo !'

if __name__ == '__main__':
    ingest()
