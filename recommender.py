from pymongo import MongoClient
import time
import argparse


class Recommender(object):
    def __init__(self):

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.everspoti

        self.songs_collection = self.db.songs
        self.users_collection = self.db.users
        self.playlists_collection = self.db.playlists

    def top_rated(self, limit=4):
        top_voted = self.songs_collection.find().sort([("score", -1)]).limit(limit)
        return top_voted

    def top_listened(self, limit=4):
        top_voted = self.songs_collection.find().sort([("hours_played", -1)]).limit(limit)
        return top_voted

    def user_based(self, user_id):
        user_playlists = self.users_collection.find({'id': user_id}, ['playlists'])
        return user_playlists

    def get_user_playlists(self, ids):
        elements = self.playlists_collection.find({"id": {'$in': ids}})
        return elements

    def get_top_songs_by_cat(self, main_cat, songs_to_filter=None):
        songs_to_filter = [] if not songs_to_filter else songs_to_filter
        top_songs_by_cat = self.songs_collection.find({'$and': [
            {'main_cat': main_cat.upper()}, {'id': {'$nin': songs_to_filter}}]}).sort([('hours_played', -1)])
        return top_songs_by_cat

    def get_playlists_with_song(self, song_id):
        # db.playlists.find({'songs': {'$in': ['13']}})
        songs = self.playlists_collection.find({'songs': {'$in': [song_id]}})
        return songs
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_id', help='ID of the user we have to recommend')

    options = parser.parse_args()
    user_id = options.user_id
    r = Recommender()

    """
    print 'Testing top rated songs: '
    print [e for e in r.top_rated()]

    print 'Testing top listened songs: '
    print [e for e in r.top_listened()]
    
    """
    print 'Getting playlists for user with ID %s ...' % user_id
    time.sleep(2)
    playlists = r.user_based(user_id)[0].get('playlists')
    print 'There are %s playlists ' % len(playlists)
    time.sleep(2)
    print 'Getting most heared category from those playlists ...'
    time.sleep(1)
    elements = r.get_user_playlists(playlists)
    returned_playlists = [e for e in elements]
    top_cat = max([e.get('main_cat') for e in [m for m in returned_playlists]])
    print 'The main category is %s' % top_cat
    time.sleep(1)
    user_songs = [e.get('songs') for e in returned_playlists]

    distinct_user_songs = set()
    for playlist_songs in user_songs:
        for song in playlist_songs:
            distinct_user_songs.add(song)
    print 'User has %s distinct songs added in his playlists' % len(distinct_user_songs)
    time.sleep(1)

    print 'Recommending new songs of main category ...'
    time.sleep(2)
    songs = r.get_top_songs_by_cat(top_cat, list(distinct_user_songs))

    print '*'*37
    print '*'*10 + ' RECOMMENDATIONS ' + '*'*10
    print '*'*37
    for e in songs:
        print 'SONG: %s' % e.get('title')
        print 'AUTHOR: %s\n\n' % e.get('author')
