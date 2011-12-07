from wsgiauth import basic
from xslfilter import xslfilter

from run_store import RunStore
from tag_store import TagStore
from member_store import MemberStore

from tag import Tag
import run
import member

rootdir = '/Users/rpwagner/Projects/lcagrid/cadac/code/cadac'

# these are the actual functions that get called by selector

# POST, DELETE are decorated with authentication

# GET is decorated with XSL transforms


def check_role(environ, username, password):
    if username in ['rpwagner', 'dcollins'] and (password=='amrrox'):
        return True
    return False

@xslfilter(rootdir)
def get_user_runs(environ, start_response):

    username = environ['selector.vars']['username']

    rs = RunStore()
    resp = ''
    try:
        resp = str(rs.get_user_run_list(username))
        start_response("200 OK", [('Content-type', 'text/xml')])
    except:
        resp = '404 Not Found\n\nThe server has not found anything matching the Request-URI.'
        start_response("404 NOT FOUND", [('Content-type', 'text/plain')])
    return [resp]


@xslfilter(rootdir)
def get_run(environ, start_response):

    run_id = environ['selector.vars']['uuid']
    start_response("200 OK", [('Content-type', 'text/xml')])
    rs = RunStore()

    return [ str(rs.get_run(run_id)) ]

@basic.basic('cadac',check_role)
def add_run(environ, start_response):

    clen = int(environ['CONTENT_LENGTH'])
    body = environ['wsgi.input'].read(clen)
    new_run = run.readXML(body)
    rs = RunStore()

    new_id = rs.add_run(new_run)
    start_response("201 OK", [('Content-type', 'text/xml')])
    return [ str(new_id) ]

@basic.basic('cadac',check_role)
def update_run(environ, start_response):

    uuid = environ['selector.vars']['uuid']
    clen = int(environ['CONTENT_LENGTH'])
    body = environ['wsgi.input'].read(clen)
    new_run = run.readXML(body)

    rs = RunStore()
    rs.update_run(new_run, uuid)

    start_response("200 OK", [])
    return [ ]

@xslfilter(rootdir)
def get_run_tags(environ, start_response):

    run_id = environ['selector.vars']['uuid']
    start_response("200 OK", [('Content-type', 'text/xml')])
    ts = TagStore()

    return [ str(ts.get_object_tags(run_id)) ]

@xslfilter(rootdir)
def get_user_tags(environ, start_response):

    username = environ['selector.vars']['username']
    start_response("200 OK", [('Content-type', 'text/xml')])
    ts = TagStore()

    return [ str(ts.get_user_tags(username)) ]

@xslfilter(rootdir)
def get_object_tags_by_tag(environ, start_response):

    uuid = environ['selector.vars']['uuid']
    tagname = environ['selector.vars']['tag']
    start_response("200 OK", [('Content-type', 'text/xml')])
    ts = TagStore()
    return [ str(ts.get_object_tags_by_tag(uuid, tagname)) ]

@xslfilter(rootdir)
def get_tagged_runs(environ, start_response):

    tag = environ['selector.vars']['tag']
    username = environ['selector.vars']['username']
    start_response("200 OK", [('Content-type', 'text/xml')])
    rs = RunStore()
    tag_obj = Tag(tag, username)
    return [ str(rs.get_user_tagged_run_list(tag_obj, username)) ]

@basic.basic('cadac',check_role)
def delete_object_tag(environ, start_response):
    tag = environ['selector.vars']['tag']
    uuid = environ['selector.vars']['uuid']
    username = environ['selector.vars']['username']
    ts = TagStore()
    tag_obj = Tag(tag, username)
    ts.delete_object_tag(tag_obj, uuid)
    start_response("200 OK", [])
    return []

@basic.basic('cadac',check_role)
def add_object_tag(environ, start_response):
    tag = environ['selector.vars']['tag']
    uuid = environ['selector.vars']['uuid']
    username = environ['selector.vars']['username']
    ts = TagStore()
    tag_obj = Tag(tag, username)
    ts.update(tag_obj, uuid)
    start_response("201 OK", [])
    return []

@basic.basic('cadac',check_role)
def delete_object_tags(environ, start_response):
    uuid = environ['selector.vars']['uuid']
    ts = TagStore()
    ts.delete_object_tags(uuid)
    start_response("200 OK", [])
    return []

@basic.basic('cadac',check_role)
def delete_run(environ, start_response):
    run_id = environ['selector.vars']['uuid']
    rs = RunStore()
    rs.delete(run_id)
    start_response("200 OK", [])
    return []

@xslfilter(rootdir)
def get_members(environ, start_response):

    ms = MemberStore()
    resp = str(ms.get_members())
    start_response("200 OK", [('Content-type', 'text/xml')])
    return [resp]

@xslfilter(rootdir)
def get_member(environ, start_response):

    username = environ['selector.vars']['username']
    ms = MemberStore()
    mem = ms.get_member(username)

    ts = TagStore()
    tl = ts.get_user_tags(username)
    
    mem.childnodes.append(tl)
    resp = str(mem)
    start_response("200 OK", [('Content-type', 'text/xml')])
    return [resp]

@basic.basic('cadac',check_role)
def delete_member(environ, start_response):

    username = environ['selector.vars']['username']
    ms = MemberStore()
    resp = str(ms.delete_member(username))
    start_response("200 OK", [('Content-type', 'text/xml')])
    return [resp]

@basic.basic('cadac',check_role)
def update_member(environ, start_response):

    clen = int(environ['CONTENT_LENGTH'])
    body = environ['wsgi.input'].read(clen)

    member_data = member.readXML(body)

    ms = MemberStore()
    ms.update(member_data)

    start_response("200 OK", [])
    return [ ]
