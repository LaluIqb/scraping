import requests, sys, pprint
from bs4 import BeautifulSoup


pages = [num for num in range(1, int(sys.argv[1]))]


def get_data(list):
    link_list = []
    subtext_list = []

    for num in list:
        if num == 1:
            res = requests.get('https://news.ycombinator.com/news')
        else:
            res = requests.get(f'https://news.ycombinator.com/news?p={num}')

        soup = BeautifulSoup(res.text, 'html.parser')
        link = soup.select('.titlelink')
        subtext = soup.select('.subtext')

        link_list += link
        subtext_list += subtext

    return link_list, subtext_list


def sort_by_vote(hnlist):
    return sorted(hnlist, key= lambda k:k['vote'], reverse=True)


def create_custom(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            vote = int(vote[0].getText().replace(' points', ''))
            if vote >= 100:
                hn.append({'title': title, 'link': href, 'vote': vote})

    return sort_by_vote(hn)


links, subtexts = get_data(pages)
pprint.pprint(create_custom(links, subtexts))
