from bs4 import BeautifulSoup


class ffbookmarktools:
    FLAG_BS_PARSER = "html.parser"
    bookmark_file = ""
    bookmark_title = "Bookmarks"
    unsorted_bookmarks_title = "Unsorted Bookmarks"
    bookmark_file_title = ""
    is_bookmark_flag = False
    unsorted_bookmarks_line = -1
    array_index_links = []
    array_links = []
    duplicated_links = []
    duplicated_index_links = []
    bm_b = ""
    outputfile = "sampleOutputBookmark.html"

    def __init__(self, bm_file):
        self.FLAG_BS_PARSER = "html.parser"
        self.bookmark_file = ""
        self.bookmark_title = "Bookmarks"
        self.unsorted_bookmarks_title = "Unsorted Bookmarks"
        self.bookmark_file_title = ""
        self.is_bookmark_flag = False
        self.unsorted_bookmarks_line = -1
        self.array_index_links = []
        self.array_links = []
        self.outputfile = "sampleOutputBookmark.html"
        self.duplicated_links = []
        self.duplicated_index_links = []
        self.bookmark_file = bm_file

        self.bm_b = self.get_bookmarks_body(bm_file)
        self.get_unsort_position(self.bm_b)
        # print(self.unsorted_bookmarks_line)
        self.get_ubm_folders(self.bm_b)

    @staticmethod
    def get_file_text(bm_file):
        return open(bm_file, "r").read()

    def get_bookmarks_body(self, bm_file):
        html_text = self.get_file_text(bm_file)

        split_text = html_text.split("\n")
        array_body_text = ""

        init = 1
        for line in split_text:
            if init == 6:
                self.bookmark_file_title = BeautifulSoup(line, self.FLAG_BS_PARSER).text
                if self.bookmark_file_title == self.bookmark_title:
                    self.is_bookmark_flag = True

            # print(self.is_bookmark_flag)
            if self.is_bookmark_flag:
                if init > 8:
                    array_body_text += line + "\n"
            init += 1

        return array_body_text

    def get_unsort_position(self, bm_body):
        array_bm_body = bm_body.split("\n")
        # print(array_bm_body)

        init = 0
        for html_line in array_bm_body:
            # print(init)
            html_line_text = BeautifulSoup(html_line, self.FLAG_BS_PARSER).text
            if html_line_text.strip() == self.unsorted_bookmarks_title:
                self.unsorted_bookmarks_line = init
            init += 1

    def get_array_ubm(self, bm_html):
        array_body = bm_html.split("\n")
        index = 0
        array_ubm = []

        # =======================================
        # =======================================
        for ubm in array_body:
            if index >= self.unsorted_bookmarks_line:
                array_ubm += [ubm]
            index += 1

        return array_ubm

    def get_ubm_folders(self, bm_html):
        if self.unsorted_bookmarks_line != -1:
            array_ubm = self.get_array_ubm(bm_html)
            array_ubm_index_folder = []
            array_ubm_index_links = []

            # print(array_ubm)
            array_ubm_folders = []
            # print(array_ubm_folders)
            for folders in array_ubm:
                if "<H3" in folders:
                    array_ubm_folders += [folders]
            # print("@#@#@#" + str(array_ubm_folders))

            index2 = 0
            for ubm_line in array_ubm:
                for ubm_folder in array_ubm_folders:
                    if str(ubm_folder) == str(ubm_line):
                        # print(str(index2) + " " + str(ubm_folder))
                        array_ubm_index_folder += [index2]
                        # print colored("cyaaan@ " + ubm_folder + " " + str(index2), "cyan")
                        break
                index2 += 1
                self.get_line_href_and_index(ubm_line, index2)
            print(array_ubm_index_folder)
            print(self.array_index_links)

    def get_line_href_and_index(self, line, index):
        if "HREF" in line:
            href = BeautifulSoup(line, self.FLAG_BS_PARSER).find_all('a')
            href = href[0]['href']
            # print(href)
            # print colored(line + str(index), "magenta")
            self.array_links += [href]
            self.array_index_links += [index]

    def self_check_duplicated_links(self):
        original_links = self.array_links
        copy_links = self.array_links

        index = 0
        for o_link in original_links:
            c_index = 0
            for c_link in copy_links:
                if c_index > index:
                    if o_link == c_link:
                        self.duplicated_links += [o_link]
                        store_index = self.array_index_links[index] - 1
                        self.duplicated_index_links += [store_index]
                        # print colored("line: " + str(store_index) + " url: " + o_link, "green")
                        break
                c_index += 1
            index += 1
        return self.duplicated_links, self.duplicated_index_links

    def remove_duplicated_links(self):
        if len(self.duplicated_index_links) != 0:
            array_ubm = self.get_array_ubm(self.bm_b)
            array_removed = []
            TEMP_INDEX_IN = -1
            r_index = 0

            print(self.duplicated_index_links)
            for line in array_ubm:
                IS_INDEX_IN = False
                for i in self.duplicated_index_links:
                    # print(i)
                    if i == r_index:
                        IS_INDEX_IN = True
                        TEMP_INDEX_IN = i
                        break
                # break

                if IS_INDEX_IN is False:
                    if "<DD>" in line:
                        if TEMP_INDEX_IN != r_index - 1:
                            array_removed += [line]
                    else:
                        array_removed += [line]

                r_index += 1
                # if IS_INDEX_IN is True:
                #     print colored("Line removed: " + str(r_index) + " " + line, "yellow")
                # else:
                #     if "<DD>" in line:
                #         if TEMP_INDEX_IN == r_index - 1:
                #             print colored("Removing DD: " + line, "cyan")
                #         else:
                #             array_removed += [line]
                #     else:
                #         array_removed += [line]
                # r_index += 1

            print(len(self.duplicated_index_links))
            text_file = open(self.outputfile, "w")
            for line in array_removed:
                text_file.write(line + "\n")
                print(line)
            text_file.close()
            return array_removed

        else:
            print("No Links to Remove")

    def check_duplicated_links(self, array_links2, array_index_link2):
        array_duplicated_index = []
        if len(self.array_links) >= len(array_links2):
            high_links = self.array_links
            low_links = array_links2
        else:
            high_links = array_links2
            low_links = self.array_links

        print colored("cyan high" + str(high_links), "cyan")
        print colored("cyan low" + str(low_links), "cyan")
        index = 0
        for link in low_links:
            for cp_links in high_links:
                if link == cp_links:
                    print colored("red " + link, "red")
                    array_duplicated_index += [array_index_link2[index]]
            index += 1
        print(array_duplicated_index)

    def get_array_link(self):
        return self.array_links

    def set_output_file_name(self, file_name):
        if ".html" in file_name:
            self.outputfile = file_name
        else:
            self.outputfile = file_name + ".html"