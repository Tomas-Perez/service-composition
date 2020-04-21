import luigi
import sys

from service_composition.composer.task import Task
from service_composition.composer import service

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise RuntimeError("Please specify username and password (in that order, only the values ex: \"user\" \"password\") for cime server")

    username = sys.argv[1]
    password = sys.argv[2]

    crawler = Task(
        service=service.PythonService("service_composition.twitter_example.get_tweets"), 
        path='output_files/twitter_results/tweets', 
        name='crawler',
    )
    geolocate = Task(
        service=service.HTTPService(
            "http://131.175.120.108:20007/e2mc/CIME/v1.0/tweet/twitter_json",
            service.HTTPMethod.POST,
            auth=(username, password), 
            timeout=200,
            headers={'Content-Type': 'application/json'},
        ), 
        path='output_files/twitter_results/geolocate', 
        dependencies=[crawler], 
        threads=4,
        name='geolocate',
    )
    print_crawled = Task(
        service=service.PythonService("service_composition.twitter_example.print_it"), 
        name='print_crawled',
        path='output_files/twitter_results/done', 
        dependencies=[geolocate],
    )


    luigi.build([print_crawled])