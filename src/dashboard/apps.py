from django.apps import AppConfig

from .models import Article



import requests
from bs4 import BeautifulSoup
import datetime
class News:
    def __init__(self,post_id, post_title, post_url,here_posted_on,
                        posted_age, post_upvotes, post_comments ):
        self.post_id = post_id
        self.post_title = post_title
        self.post_url = post_url
        self.here_posted_on = here_posted_on
        self.posted_age = posted_age
        self.post_upvotes = post_upvotes
        self.post_comments = post_comments

class HnewsFetcher:
    def __init__(self, upto_page = 3):
        self.headers = []
        self.list_of_urls = list()
        self.all_articles = list()
        self.all_posts_raw = list()
        self.collectArticles(upto_page)

    def saveToDb(self):
        if len(self.all_articles) == 90:
            for item in self.all_articles:
                article = Article(id = item.post_id,
                        title = item.post_title,
                        hackernews_url = item.post_url,
                        url='',
                        posted_age = item.posted_age,
                        here_posted_on = item.here_posted_on,
                        upvotes = item.post_upvotes,
                        comments = item.post_comments
                        )
                article.save()

    def collectArticles(self,upto_page = 3):
        for pg_no in range(3):
            url = 'https://news.ycombinator.com/news?p={}'.format(pg_no+1)
            self.list_of_urls.append(url)

    def downloadData(self):
        for url in self.list_of_urls:
            response = requests.get( url)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find_all('table', attrs={'class':'itemlist'})
            posts = str(table[0]).split('<tr class="spacer" style="height:5px">')[:-1]
            for post in posts:
                    self.all_posts_raw.append(post)
                    post = post.split('\n')
                    #post_id
                    matcher = 'id="'
                    post_id = post[1][post[1].index(matcher)+ len(matcher)  :].replace('">','')

                    #post_url
                    matcher = 'storylink"'
                    temp_post = post[2][post[2].index(matcher)+len(matcher): ]
                    temp_for_title = temp_post
                    refined_post = temp_post[: temp_post.index('">')]
                    post_url = refined_post.replace('href="', '').strip()
                    #looking for hnews links here..
                    temp = 'item?id={}'.format(post_id)
                    if post_url == temp:
                        post_url = 'https://news.ycombinator.com/{}'.format(temp)
                    #looking for <rel="nofollow>
                    temp = '" rel="nofollow'
                    if temp in post_url:
                        post_url = post_url.replace( temp, '').strip()

                    #age
                    matcher = """age"><a href="item?id={}">""".format(post_id)
                    temp_for_comments = post[3][ post[3].index(matcher) + len(matcher): ].split('<')
                    temp = temp_for_comments[0].strip()
                    post_age = temp
                    post_age_numeric = int (post_age.split()[0] )
                    post_age_desc = post_age.split()[1]
                    here_posted_on = datetime.datetime.now()
                    if 'hours' in post_age_desc:
                        here_posted_on = datetime.datetime.now() - datetime.timedelta(hours=post_age_numeric)
                    elif 'minutes'  in post_age_desc:
                        here_posted_on = datetime.datetime.now() - datetime.timedelta(minutes=post_age_numeric)
                    elif 'seconds'  in post_age_desc:
                        here_posted_on = datetime.datetime.now() - datetime.timedelta(seconds=post_age_numeric)

                    try:
                        #upvotes
                        matcher = """score" id="score_{}">""".format(post_id)
                        temp = post[3][ post[3].index(matcher)+len(matcher):].split('<')[0].strip()
                        post_upvotes = temp.split()[0].strip()

                         #comments
                        temp = temp_for_comments[-4].split('>')[1].strip()
                        post_comments = temp.split()[0].strip()
                        if post_comments == 'discuss':
                            post_comments = 0

                    except Exception as e:
                        post_upvotes = 0
                        post_comments = 0

                    post_title = temp_for_title.split('>')[1].replace('</a', '').strip()
                    news = News(post_id, post_title, post_url,here_posted_on, post_age, post_upvotes, post_comments)
                    self.all_articles.append(news)
            print(len(self.all_articles))
class DashboardConfig(AppConfig):
    name = 'dashboard'
    news_fetcher_obj = HnewsFetcher()
