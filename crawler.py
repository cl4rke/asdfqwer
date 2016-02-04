import re
from datetime import datetime
from bs4 import BeautifulSoup


def main():
    dcs_html = open("ccmit-dcs.html")
    soup = BeautifulSoup(dcs_html.read(), "html.parser")
    dcs_html.close()

    posts_html = soup.select('div._4-u2.mbm._5jmm._5pat._5v3q._4-u8._x72._50nb')

    posts = []

    for post_html in posts_html:
        post = {}

        post_author_html = post_html.select('span.fwb')
        post_content_html = post_html.select('div.userContent')
        post_created_at_html = post_html.select('abbr')
        post_comments_html = post_html.select('div._4oep')
        post_likes_html = post_html.select('span._1g5v')

        if len(post_author_html):
            post['author'] = post_author_html[0].text

        if len(post_content_html):
            post['content'] = post_content_html[0].text

        if len(post_created_at_html):
            post['created_at'] = datetime.fromtimestamp(
                int(post_created_at_html[0].attrs['data-utime'])
            )

        if len(post_likes_html):
            post['likes'] = int(post_likes_html[0].text)
        else:
            post['likes'] = 0

        post['comments'] = []
        for post_comment_html in post_comments_html:
            post_comment_author_html = post_comment_html.select('a.UFICommentActorName')
            post_comment_content_html = post_comment_html.select('span.UFICommentBody')
            post_comment_created_at_html = post_comment_html.select('abbr')
            post_comment_likes_html = post_comment_html.select('a.UFICommentLikeButton')

            post_comment = {}

            if len(post_comment_author_html):
                post_comment['author'] = post_comment_author_html[0].text

            if len(post_comment_content_html):
                post_comment['content'] = post_comment_content_html[0].text

            if len(post_comment_created_at_html):
                post_comment['created_at'] = datetime.fromtimestamp(
                    int(post_comment_created_at_html[0].attrs['data-utime'])
                )

            if len(post_comment_likes_html):
                post_comment['likes'] = int(post_comment_likes_html[0].text)
            elif len(post_comment.keys()):
                post_comment['likes'] = 0

            if len(post_comment.keys()):
                post['comments'].append(post_comment)
        
        posts.append(post)

    post_data = [post['content'] for post in posts]

    comment_data = [comment['content']
            for post in posts
            for comment in post['comments']]

    words = reduce(merge_dicts, map(get_words, post_data + comment_data))

    print '\n'.join(["%s (%d)" % (word_tuple[0], word_tuple[1])
        for word_tuple in sorted([(word[0], word[1])
            for word in words.iteritems()], key=lambda w:w[1])])


def convert_to_dict(key):
    if type(key) is tuple:
        return {key[0]: key[1]}
    return {key: 1}


def get_words(content):
    tokenizer = re.compile(r'([:\?\!\.\/\\\(\)\#\@\'\"\|\-_])|(\w+)|(\$[\d\.]+)|(\S+)')

    words = {}
    for match in [''.join(match).lower() for match in tokenizer.findall(content)]:
        if match not in words:
            words[match] = 0
        words[match] += 1

    return words


def get_word_likes(content_and_likes):
    content = content_and_likes[0]
    likes = content_and_likes[1]

    tokenizer = re.compile(r'([:\?\!\.\/\\\(\)\#\@\'\"\|\-_])|(\w+)|(\$[\d\.]+)|(\S+)')

    words = {}
    for match in [''.join(match).lower() for match in tokenizer.findall(content)]:
        if match not in words:
            words[match] = 0
        words[match] = likes

    return words


def get_words(content):
    tokenizer = re.compile(r'([:\?\!\.\/\\\(\)\#\@\'\"\|\-_])|(\w+)|(\$[\d\.]+)|(\S+)')

    words = {}
    for match in [''.join(match).lower() for match in tokenizer.findall(content)]:
        if match not in words:
            words[match] = 0
        words[match] += 1

    return words


def merge_dicts(d1, d2):
    d3 = {}

    for key, value in d1.iteritems():
        if key not in d3:
            d3[key] = 0

        d3[key] += value

    for key, value in d2.iteritems():
        if key not in d3:
            d3[key] = 0

        d3[key] += value

    return d3

main()
