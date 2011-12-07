import sys
import os

from wsgiref.simple_server import make_server

filepath = os.path.abspath(__file__)
filepath = os.path.dirname(filepath)

#sys.path.append(filepath)

from selector import Selector
import service_api

def run(port=8000):

    s = Selector(mapfile=filepath+'/service.map')
    #s = Selector()
    #s.add('/xml/members/{username}/runs[/]', GET=service_api.get_user_runs)
    httpd = make_server('', port,s)
    httpd.serve_forever()    


if __name__ == '__main__':
    run()
