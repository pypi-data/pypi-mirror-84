#!/usr/bin/python

# @author CicakGoreng
# @description A blueprint to download n magazine

# import required files
# non-standard modules
try:
    from bs4 import BeautifulSoup as bs
except:
    # raise error to inform module not found
    raise Exception(
        'Cannot import BeautifulSoup from bs4 module. Make sure to install bs4 to use this program')

try:
    import requests
except:
    # raise error to inform module not found
    raise Exception(
        'Cannot import requests module. Make sure to install requests to use this program')

# standard modules
import os
import re
import datetime

# define class


class Ndownloader:
    # class properties
    sort_options = ['', 'popular-today', 'popular-week', 'popular']
    path = os.path.dirname(os.path.abspath(__file__))

    url = 'https://nhentai.net'
    code = 0
    pages = 0

    # class methods
    # constructor
    def __init__(self, path='', sort=0):
        # set to default if none inserted
        self.path = path if path != '' else self.path
        self.sort_by(sort)

        # test if user can access the page
        try:
            test = requests.get(self.url)
            bs(test.text, 'html.parser')
        except:
            raise Exception(
                'Cannot access the page. Try use vpn or something.')

    # sort_by
    # use to change or add propert sort
    def sort_by(self, sort):
        try:
            # assign sort property sort for later use
            self.sort = self.sort_options[sort]
            # print("Sort set to:", self.sort)

        except:
            # raise error if sort is invalid
            raise Exception('Invalid sort!')

    # download
    # use to download magazine using code or the code user insert
    def download(self, code=0):
        assert str(type(code)) == "<class 'int'>", "Invalid code!"

        # assign code to property code if it != 0
        self.code = code if code != 0 else self.code

        # request the page
        request_url = self.url + '/g/' + str(self.code)
        print('Looking for code...')

        html = requests.get(request_url)
        soup = bs(html.text, 'html.parser')

        # test if the page is found
        # ph1t: abbr = page h1 tag
        ph1t = soup.find('h1')
        if ph1t.text == '404 – Not Found':
            # page not found
            # print aborting messsage
            print(f'{ph1t.text}. Aborting...')
            return None

        # page is not set, find it
        if self.pages == 0:
            # get all tag container
            containers = soup.find_all(
                'div', attrs={'class': 'tag-container field-name'})
            # try to get total pages
            for tag in containers:
                page_pattern = r'Pages'
                match = re.search(page_pattern, tag.text)

                if match:
                    # found the container contains total page number
                    # assign the total page to property page
                    self.pages = int(
                        tag.find('span', attrs={'class': 'name'}).text)
                    break

        # try to open path directory
        if not(os.path.isdir(self.path)):
            raise Exception(
                f'Directory [{self.path}] is not exist. Aborting...')

        ####download all pages####
        # try to open directory with the name as property code
        ndir = os.path.join(self.path, str(self.code))
        overwrite = False
        dir_exist = False
        # if dir is exists and overwrite = false, prompt user with some input
        while os.path.isdir(ndir) and overwrite == False:
            dir_exist = True
            cond = ''
            action_options = ['r', 'e', 'c']
            folder_name = ndir.split('/')[-1]
            while cond not in action_options:
                cond = str(input(
                    f'Folder named "{folder_name}" exists in {self.path}, do you want to \noverwrite it[e]\nchange dirname[r]\n or cancel[c]\n>>> ')).lower()
                if cond == 'r':
                    rename = input('Enter new folder name: ')
                    ndir = os.path.join(self.path, str(rename))
                    pass
                elif cond == 'e':
                    overwrite = True
                    break
                else:
                    exit()

        if not(dir_exist):
            # create new dir if dir is not exists
            try:
                os.mkdir(ndir)
            except:
                raise Exception('Cannot create directory!')

        print('Download started')
        # get every single image
        for page in range(1, self.pages+1):
            page_url = request_url + '/' + str(page)
            filename = os.path.join(ndir, str(page) + '.jpg')

            # page
            phtml = requests.get(page_url)
            psoup = bs(phtml.text, 'html.parser')

            # image source
            image_source = psoup.find(
                'section', attrs={'id': 'image-container'}).find('img').get('src')

            # write the file
            with open(filename, 'wb') as file:
                print(f'Downloading page {page}...')
                file.write(requests.get(image_source).content)

    def search(self, keyword, sort=0, page=1):

        #match_result
        ##use to find result number in  result's string
        def match_result(result):
                    #print('Matching results... Please wait')
                    stage = 0
                    r = result
                    resnum = ''
                    tir = ''
                    for i in range(len(result)):
                        try:
                            tir = int(r[i])
                            resnum += r[i]
                        except:
                            if stage != 0:
                                break
                            continue
                    return int(resnum)


        self.sort_by(sort)
        search_type = 0  # search by code
        # try convert into int if keyword is string
        try:
            keyword = int(keyword)
        except:
            search_type = 1

        # 2 desicion
        if search_type == 0:  # keyword is code number
            # prompt user if they want to open detail about keyword number
            confirm = str(
                input(f'Do you want to see details about {keyword}[y/n]:')).lower()
            if confirm == 'y':
                # self.detail(keyword)
                pass
            self.code = int(keyword)
            return self.code

        elif search_type == 1:
            print(f'Searching for {keyword}')

            # set request url
            request_url = f'{self.url}/search/?q={keyword}&sort={self.sort}&page={page}'

            # get result content
            html = requests.get(request_url)
            soup = bs(html.text, 'html.parser')

            # if page not found
            # ph1t: abbr = page h1 tag
            ph1t = soup.find('h1')
            if(ph1t.text == '404 – Not Found'):
                print(f'{ph1t.text}')
                return None
            else:
                total_result = match_result(ph1t.text)
                adds = f' sorted by' + self.sort if self.sort != '' else ''
                print(f'Search result for "{keyword}"{adds}: ({ph1t.text})')

                try:
                    current_page = soup.find(
                        'a', attrs={'class': 'page current'}).text
                except:
                    current_page = '1'
                print(f'Page {current_page}:')

                # show all result
                page_result = soup.find_all('div', attrs={'class': 'gallery'})
                counter = 0
                for result in page_result:
                    counter += 1
                    #result captio
                    caption = result.find('div', attrs={'class': 'caption'}).text

                    print(f'{counter}. {caption}')

                #get results lastpage
                lastpage = None
                try:
                    lastpage = int(soup.find('a', attrs={'class': 'last'}))
                    if lastpage == None:
                        raise Exception('Last page not found')
                except:
                    try:
                        lastpage = soup.find_all('a', attrs={'class': 'page'})[-1]
                        if lastpage == None:
                            raise Exception('Last page not found 2')
                    except:
                        #set custom a tag to get and set lastpage
                        lastpage = bs('<a href="iwjwpage=1">1</>', 'html.parser').find('a')
                
                lastpage_num = int(lastpage.get('href').split('page=')[-1])
                #user actions
                print(type(current_page))
                print('\nActions:')
                print('b: previous' if int(current_page) - 1 > 0 else '\b\b')
                print('n: next' if int(current_page) + 1  <= lastpage_num else '\b\b')
                print(f'[p1 - p{str(lastpage_num)}]{ph1t.text}: select page' ) #if ph1t.text != ' 0 results' else '\b\b'
                print(f'[1-{len(page_result)}]: select magazine' if len(page_result) != 0 else '\b\b')
                print(f'c: cancel')

                action = ''
                while action == '':
                    action = input('Enter something: ')
                    if action == '':
                        continue
                    try:
                        action = int(action)
                        print('yeet')
                        if(action < 1 or action > len(page_result)):
                            action = ''
                            continue
                        self.code = int(page_result[action - 1].find('a', attrs={'class': 'cover'}).get('href').split('/')[2])
                        return self.code
                    except:
                        if action == '':
                            continue
                    action = str(action).lower()
                    if action == 'b':
                        if page - 1 > 0:
                            self.search(keyword, sort, page - 1)
                    elif action == 'n':
                        if (page - 1) * 25 + len(page_result) + 1 < total_result or total_result > 25:
                            self.search(keyword, sort, page + 1)
                    elif action[0] == 'p':
                        page_num = int(action.split('p')[1])
                        if page_num > 0 or page_num <= lastpage_num:
                            self.search(keyword, sort, page_num)
                    elif action == 'c':
                        exit()
                    action = ''
                        


                


# for testing purpose
if __name__ == '__main__':
    downloader = Ndownloader()
    keyword = input('Search: ')
    downloader.download(downloader.search(keyword))
