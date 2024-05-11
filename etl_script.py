import sys
import logging
import json

from typing import Dict, List
from elasticsearch import Elasticsearch

from elasticloader import ElasticLoader


logging.basicConfig(
    filename='etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s. %(message)s - %(filename)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


def movie_loader(file: json, index: str) -> None:
    with open(file, encoding='utf8') as f:
        content = f.read()
        result = json.loads(content)
        for doc in result['hits']['hits']:
            data = doc['_source']
            es.add_movie(index, data)
    f.close()


def person_loader(file: json, index: str) -> None:
    with open(file, encoding='utf8') as f:
        content = f.read()
        result = json.loads(content)
        for doc in result['hits']['hits']:
            data = doc['_source']
            es.add_person(index, data)
    f.close()


def genre_loader(file: json, index: str) -> None:
    with open(file, encoding='utf8') as f:
        content = f.read()
        result = json.loads(content)
        for doc in result['hits']['hits']:
            data = doc['_source']
            es.add_genre(index, data)
    f.close()


def main(indices: List[tuple]) -> None:
    """The main method of loading data to Elasticsearch."""

    movies_index = indices[0][0]
    persons_index = indices[1][0]
    genres_index = indices[2][0]

    movie_loader('data/_search_movies.json', movies_index)
    logging.info("Movies Done")

    person_loader('data/_search_persons.json', persons_index)
    logging.info("Persons Done")

    genre_loader('data/_search_genres.json', genres_index)
    logging.info("Genres Done")

    logging.info("Done. All data was sent to Elasticsearch")


if __name__ == '__main__':

    client = Elasticsearch('http://127.0.0.1:9200')
    es = ElasticLoader(client)

    indices = [
        ('movies', 'indices/movieIndex.json'),
        ('persons', 'indices/personIndex.json'),
        ('genres', 'indices/genreIndex.json')
    ]

    for idx in indices:
        create_index = es.create_index(*idx)

        if not create_index:
            logging.warning(f'The index {idx[0]} was not created.')
            sys.exit(1)

    main(indices)
