from ffbookmarktools import ffbookmarktools

if __name__ == '__main__':
    my_bookmark = ffbookmarktools("sampleBookmark.html")
    my_bookmark.self_check_duplicated_links()
    my_bookmark.remove_duplicated_links()
