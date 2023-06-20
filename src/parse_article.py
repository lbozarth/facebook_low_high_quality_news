from newspaper.article import ArticleException
import trafilatura
from newspaper import Article


def parse_using_newspaper3k(content, url=None):
    if not content:
        return

    if url:
        print('downloading')
        article = Article(url=url)
        article.download()
    else:
        article = Article(url='')
        article.set_html(content)

    try:
        article.parse()
    except ArticleException as e:
        # this is caused by html not proper
        return

    clean_text = article.text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    if clean_text and clean_text.strip() != "":
        return clean_text


def parse_using_trafila(content, url=None):
    if not content:
        return

    result = trafilatura.extract(content, xml_output=False, include_comments=False, include_tables=False,
                                 target_language='en')
    if result:
        result = str(result).replace("\\n", "").replace("\\t", "").replace("\\r", "").replace("\n", " ").replace("\t", " ").replace("\r", " ")
        return result

s
if __name__ == '__main__':
    # this script get the actual article text from html webpages
    content = None  # webpage HTML
    parse_using_trafila(content)
    parse_using_newspaper3k(content)
