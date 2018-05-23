import argparse
import ingesta
import mongo_parser
import recommender
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ingest', action='store_true', help='Begin the process to load data into Mongo')
    parser.add_argument('--top_rated_songs', type=int, help='Show n top songs ordered by rating')
    parser.add_argument('--top_played_songs', type=int, help='Show n top songs ordered by minutes played')
    parser.add_argument('--get_added_songs', action='store_true', help='Show N songs in playlists for user X. <user_id> is mandatory')
    parser.add_argument('--recommend_songs', action='store_true', help='Recommend songs for user X. <user_id> is mandatory')
    parser.add_argument('--user_id', help='ID of the user we have to recommend')

    options = parser.parse_args()
    do_ingest = options.ingest
    user_id = options.user_id
    top_rated_songs = options.top_rated_songs
    top_played_songs = options.top_played_songs
    get_added_songs = options.get_added_songs
    recommend_songs = options.recommend_songs

    if do_ingest:
        print '\n' * 2 + '*' * 10 + ' DATA INGESTION ' + '*' * 10
        ingesta.ingest()

    if top_rated_songs:
        print '\n'*2 + '*'*10 + ' TOP RATED SONGS ' + '*'*10
        r = recommender.Recommender()
        results = r.top_rated(top_rated_songs)
        for result in results:
            print result

    if top_played_songs:
        print '\n' * 2 + '*' * 10 + ' TOP PLAYED SONGS ' + '*' * 10
        r = recommender.Recommender()
        results = r.top_listened(top_played_songs)
        for result in results:
            print result

    if get_added_songs and user_id:
        print '\n' * 2 + '*' * 10 + ' SONGS ADDED BY USER ' + '*' * 10
        r = recommender.Recommender()
        playlists = r.user_based(user_id)[0].get('playlists')
        elements = r.get_user_playlists(playlists)
        returned_playlists = [e for e in elements]
        user_songs = [e.get('songs') for e in returned_playlists]
        for song in user_songs:
            print song

    if recommend_songs and user_id:
        print '\n' * 2 + '*' * 10 + ' RECOMMENDATIONS FOR USER ' + '*' * 10
        r = recommender.Recommender()
        print 'Getting playlists for user with ID %s ...' % user_id

        playlists = r.user_based(user_id)[0].get('playlists')
        print 'There are %s playlists ' % len(playlists)

        print 'Getting most heared category from those playlists ...'

        elements = r.get_user_playlists(playlists)
        returned_playlists = [e for e in elements]
        top_cat = max([e.get('main_cat') for e in [m for m in returned_playlists]])
        print 'The main category is %s' % top_cat

        user_songs = [e.get('songs') for e in returned_playlists]

        distinct_user_songs = set()
        for playlist_songs in user_songs:
            for song in playlist_songs:
                distinct_user_songs.add(song)
        print 'User has %s distinct songs added in his playlists' % len(distinct_user_songs)


        print 'Recommending new songs of main category ...'

        songs = r.get_top_songs_by_cat(top_cat, list(distinct_user_songs))

        print '*' * 37
        print '*' * 10 + ' RECOMMENDATIONS ' + '*' * 10
        print '*' * 37
        for e in songs:
            print 'SONG: %s' % e.get('title')
            print 'AUTHOR: %s\n\n' % e.get('author')







