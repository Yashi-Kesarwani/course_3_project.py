import requests_with_caching
import json


def get_movies_from_tastedive(title):
    endpoint = 'https://tastedive.com/api/similar'
    param = {}
    param['q'] = title
    param['limit'] = 5
    param['type'] = 'movies'

    this_page_cache = requests_with_caching.get(endpoint, params=param)
    return json.loads(this_page_cache.text)


def extract_movie_titles(dic):
    return ([i['Name'] for i in dic['Similar']['Results']])
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_related_titles(["Black Panther", "Captain Marvel"])
# get_related_titles([])
def get_related_titles(movie_list):
    li = []
    for movie in movie_list:
        li.extend(extract_movie_titles(get_movies_from_tastedive(movie)))
    return list(set(li))
def get_movie_data(title):
    url = 'http://www.omdbapi.com/'
    param = {}
    param['t'] = title
    param['r'] = 'json'
    this_page_cache = requests_with_caching.get(url, params=param)
    return json.loads(this_page_cache.text)
print(get_movie_data("Black Panther")['Ratings'][1])
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
def get_movie_rating(dic):
    ranking = dic['Ratings']
    for dic_item in ranking:
        if dic_item['Source'] == 'Rotten Tomatoes':
            return int(dic_item['Value'][:-1])
    return 0
get_movie_rating(get_movie_data("Deadpool 2"))
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

def get_sorted_recommendations(lst):
    new_list = get_related_titles(lst)
    new_dict = {}
    for i in new_list:
        rating = get_movie_rating(get_movie_data(i))
        new_dict[i] = rating
    print(new_dict)
   
    return [i[0] for i in sorted(new_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)]
