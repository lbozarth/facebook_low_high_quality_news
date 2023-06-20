import ast
import socket

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', -1)
hostname = socket.gethostname()

# sets cover problem
def set_cover(elements, subsets):
    """Find a family of subsets that covers the universal set"""
    # elements = set(e for s in subsets for e in s)
    # # Check the subsets cover the universe
    # if elements != universe:
    #     return None
    covered_key = []
    covered = set()

    iter = 10 #
    resss = []
    while(len(covered)/len(elements)<0.95):
    # for i in range(iter):
        max_key = None
        max_set = None
        max_diff = 0
        for key,val in subsets.items():
            diff = len(val - covered)
            if diff>max_diff:
                max_diff = diff
                max_set = val
                max_key = key
        print(max_key, max_diff)
        resss.append([max_key, max_diff])
        covered.update(max_set)
        covered_key.append(max_key)
    print(len(covered_key), covered_key, len(covered)/len(elements))
    df = pd.DataFrame(resss, columns=['category', 'ent_count'])
    return df

def set_cover_v2(subsets, limit=100):
    covered_key = []
    covered = set()

    resss = []
    while True:
        max_key = None
        max_set = None
        max_diff = 0
        for key,val in subsets.items():
            diff = len(val - covered)
            if diff>max_diff:
                max_diff = diff
                max_set = val
                max_key = key

        if max_diff<limit:
            return resss

        resss.append([max_key, max_diff])
        covered.update(max_set)
        covered_key.append(max_key)

cat_filters = ['use american english', 'use british english', 'engvarb from', 'commons category link', 'instances of infobox', 'ac with ', 'vague or ambiguous time', 'navigational boxes purge', 'biography with signature', 'establishments in', ' uncertain', ' descent', 'infobox person', 'disambiguation page',  'infobox', 'words and phrases', 'awards', 'events', 'occupations', 'surnames', 'languages with', 'populated places', 'location', 'date', 'names', 'languages', 'set indices']
month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_lst = ['from ' + x.lower() for x in month_lst]
exacts_list = ['long volume value', 'cs1 german-language sources (de)', 'julian–gregorian uncertainty', 'archived copy as title', 'missing periodical', 'use american english from april', 'rtt', 'all pages needing cleanup', 'all npov disputes', 'introductions', 'external links',
     'commons category link is locally defined', '"related ethnic groups" needing confirmation', 'use british english from august', 'all accuracy disputes', 'all pages needing factual verification', 'others', 'unfit url', 'pages including recorded pronunciations', 'usa-centric', 'surnames','extra punctuation', 'subscription required using via', 'in the united states', 'cite iucn maint', 'rttem', 'featured lists', 'all article disambiguation pages', 'free-content attribution', 'websites utilizing paywalls', 'pages linking to missing files', 'documents', 'dynamic lists', 'chapter ignored', 'dates', 'words coined in the', 'populated places', 'recurring events', 'authors list', 'date format', 'date and year']
def filter_wiki_cat(x):
    if x.startswith('cs1 '):
        return
    for cat_filter in cat_filters:
        if cat_filter in x:
            return
    for mon in month_lst:
        if mon in x:
            return

    for exact in exacts_list:
        if exact==x:
            return
    return x


def clean_cats_row(row):
    #remove useless categories like dates
    if pd.isna(row):
        return
    row = ast.literal_eval(row)
    row_clean = []
    for el in row:
        elparts = [x.strip() for x in el.split(" ") if not (x.startswith("19") or x.startswith('20') or x.startswith('17') or x.startswith('18') or x.startswith('21'))]
        el = " ".join(elparts).lower()
        if 'use dmy dates' in el or 'use mdy dates' in el or 'articles' in el or 'wikipedia' in el or 'pages using' in el \
                or 'wikidata' in el or 'ref=harv' in el or 'harv and sfn' in el or 'parameter' in el or 'template' in el\
                or "pages with" in el or "pages contain" in el or 'error' in el or 'unknown' in el:
            continue
        row_clean.append(el)
    return row_clean

def gen_cluster(wiki_cat):
    for x in ['histor', 'cultur', 'ethni']:
        if x in wiki_cat:
            return 'History&Culture'
    #GPE
    for x in ['cities', 'towns', 'counties', 'census-designated', 'territories', 'capitals of', 'capitals in', 'metropolitan area', 'prefectures', 'neighborhoods']:
        if x in wiki_cat:
            return 'GPE'

    for x in ['buildings', 'completed in', 'venues', 'airports', 'museums', 'hospitals', 'restaurants', 'zoos', 'amusement parks', 'hotels', 'railway stations', 'streets in', 'sculptures']:
        if x in wiki_cat:
            return 'FAC'

    for x in ['regions', 'lists of coordinates', 'protected areas', 'rivers']:
        if x in wiki_cat:
            return 'location'

    for x in ['universities', 'colleges', 'educational institution']:
        if x in wiki_cat:
            return 'University'

    for x in ['christ', 'islam', 'catholic', 'angelic visionaries', 'religio', 'biblical']:
        if x in wiki_cat:
            return 'Religion'

    for x in ['companies', 'brands', 'products']:
        if x in wiki_cat:
            return 'Business' #companies, products

    for x in ['album', 'music', 'songs', 'record labels']:
        if x in wiki_cat:
            return 'Music'

    for x in ['magazines', 'publications', 'newspapers', 'news websites', 'media', 'radio stations']:
        if x in wiki_cat:
            return 'News Media'

    for x in ['television', 'film']:
        if x in wiki_cat:
            return 'TV&Films'

    for x in ['league', 'teams', 'football', 'sport', 'hockey']:
        if x in wiki_cat:
            return 'Sports'

    for x in ['cuisine','culinary']:
        if x in wiki_cat:
            return 'Cuisine'

    for x in ['law', 'legal doctrine']:
        if x in wiki_cat:
            return 'Law'

    for x in ['military']:
        if x in wiki_cat:
            return 'Military'

    for x in ['medical', 'disorders', 'disease', 'chembox', 'physical exercise', 'nutrition', 'digestive']:
        if x in wiki_cat:
            return 'Medical&Chemical'

    for x in ['book', 'novel', 'comics', 'fiction']:
        if x in wiki_cat:
            return 'Books'

    for x in ['crime', 'violence']:
        if x in wiki_cat:
            return 'Crime'

    for x in ['organizations', 'institutes', 'think tanks', 'trade unions']:
        if x in wiki_cat:
            return 'NORG'

    for x in ['government agencies', 'agencies', 'states department', 'political parties', 'democratic party', 'republican party', 'state lower houses', 'state upper houses',  'legislature', 'supreme courts', 'district courts', 'ministries', 'executive office']:
        if x in wiki_cat:
            return 'GORG'

    for x in ['politi', 'conflict', 'movement']:
        if x in wiki_cat:
            return 'Political'
    return


def gen_broad_cluster(x):
    x = x.lower()
    if x in ['politicians', 'politician', 'political', 'gorg', 'crime', 'controversies', 'law&convention', 'law', 'norg', 'international figures']:
        return 'politics&government'
    if x in ['books', 'tv&films', 'music', 'sports', 'cuisine', 'comic&fiction', 'tv', 'film', 'cuisine*vegetation', 'entertainment', 'video games', 'history&culture', 'religion', 'philosopher,teacher&religious figures']:
        return 'art&culture'
    if x in ['business', 'business&products']:
        return 'business&finance'
    if x in ['news media']:
        return 'news&journalism'
    if x in ['medical&chemical', 'health&chemical', 'science&innovation']:
        return 'science,technology&medicine'
    if x in ['war&disaster', 'military', 'disaster']:
        return 'war&disaster'
    return 'other'


if __name__ == '__main__':
    # this scripts contains setcover code that clusters ners into categories
    # simple example of using setcover
    # elements = {'item1', 'item2', 'item3'}
    # subsets = [{'a':{'item2'}, 'b':{'item1', 'item3'}}]
    # set_cover(elements, subsets)
    pass