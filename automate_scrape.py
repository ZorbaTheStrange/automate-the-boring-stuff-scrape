#! /usr/bin/python3

'''
automate_scrape.py - runs throught the online verision of the text book, 'Automate the boring stuff with python' and pulls out all of the projects and stores them in a file.
'''

import requests, os, bs4, sys


def page_download(web_page, chapter_num, no_project_count, no_chapter_projects):
    '''
    Downloads the web page. Keeps the varibales, chapter_num, no_project_count, no_chapter_projects to be then used in chapter_loop_and_write. 
    '''

    print('Downloading page {0}'.format(web_page))
    res = requests.get(web_page)
    res.raise_for_status()
              
    soup = bs4.BeautifulSoup(res.text)

    chapter_loop_and_write(soup, chapter_num, no_project_count, no_chapter_projects)


def chapter_loop_and_write(downloaded_page, chapter_num, no_project_count, no_chapter_projects):
    '''
    Takes a downloaded web page and pulls out the practice projects and writes them to a file. It then moves to the next chapter, gets that url. Counts the number of chapters where practice projects could not be found and stores those chapters in a list.
    '''
    
    soup = downloaded_page
    projects = soup.find_all('div', {'class': "book", 'title' : 'Practice Projects'})

    if projects == []:
        print('Could not find Projects.')
        no_project_count += 1
        no_chapter_projects.append('Chapter' + str(chapter_num))

    else:
        with open('automateProjects.txt', 'a') as f:
            for el in projects:
                f.write(el.get_text())
                print('Writing text to file')
        f.close()

    chapter_num += 1

    if chapter_num == 19:
        print('\n{0} chapters where Practice Projects could not be found'.format(no_project_count))
        print('Here is the list of those chapters:\n{0}'.format(no_chapter_projects))
        print('='*20 + 'Done' + '='*20 +'\n')
        return

    next_link = soup.find('a', href='/chapter' + str(chapter_num))
    web_page = 'http://automatetheboringstuff.com' + next_link.get('href') +'/'

    page_download(web_page, chapter_num, no_project_count, no_chapter_projects)


def main():
    '''
    main
    '''

    web_page = 'https://automatetheboringstuff.com/chapter1/'
    
    page_download(web_page, 1, 0, [])


if __name__ == '__main__':
    sys.exit(main())
