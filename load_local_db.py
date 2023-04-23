def load_local_database(treeview):
    music_database = []
    with open("./music/music_database.txt", "r") as file:
        for line in file:
            song_data = line.strip().split(',')
            treeview.insert('', 'end', values=song_data)
            music_database.append(tuple(song_data))
    print(music_database)
    return music_database

