class MongoParser(object):
    def __init__(self):
        pass

    @classmethod
    def parse_songs_file(cls, file_path):
        elements = []
        with open(file_path, 'r') as readfile:
            header = readfile.next()

            for line in readfile:
                fields = line.replace('\n', '').replace('\r', '').split(';')
                song = {
                    'id': fields[0],
                    'title': fields[1].decode('utf-8'),
                    'author': fields[2],
                    'length': int(fields[3]),
                    'main_cat': fields[4],
                    'year': fields[5],
                    'hours_played': float(fields[6]),
                    'score': float(fields[7]),
                }
                elements.append(song)

        return elements

    @classmethod
    def parse_users_file(cls, file_path):
        elements = []
        with open(file_path, 'r') as readfile:
            header = readfile.next()

            for line in readfile:
                fields = line.replace('\n', '').replace('\r', '').split(';')
                user = {
                    'id': fields[0],
                    'name': fields[1],
                    'surname': fields[2],
                    'email': fields[3],
                    'age': int(fields[4]),
                    'gender': fields[5],
                    'playlists': [e for e in fields[6].replace('[', '').replace(']', '').split(',')]
                }
                elements.append(user)


        return elements

    @classmethod
    def parse_playlists_file(cls, file_path):
        elements = []
        with open(file_path, 'r') as readfile:
            header = readfile.next()

            for line in readfile:
                fields = line.replace('\n', '').replace('\r', '').split(';')
                playlist = {
                    'id': fields[0],
                    'name': fields[1],
                    'length': fields[2],
                    'creation_date': fields[3],
                    'main_cat': fields[4],
                    'songs': [e for e in fields[5].replace('[', '').replace(']', '').split(',')]
                }
                elements.append(playlist)
        return elements
