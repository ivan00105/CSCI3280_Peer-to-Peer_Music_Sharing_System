from load_local_db import load_local_database

def search_music_local(event, search_entry, treeview, music_database):
    search_query = search_entry.get().strip().lower()

    # Clear the treeview
    treeview.delete(*treeview.get_children())

    if not search_query:
        load_local_database(treeview)
        return  # Ignore empty search query

    # Filter the music database and display relevant results
    for music in music_database:
        if any(search_query in data.lower() for data in music):
            treeview.insert('', 'end', values=music)


def search_music_global():
    pass