import httplib
import base64

server_base = 'lca.ucsd.edu'

def post(username, password, post_loc, xml=None):

    usernamepass = username + ':' + password
    usernamepass = base64.encodestring(usernamepass).strip()
    authorization = 'Basic ' + usernamepass

    con = httplib.HTTP(server_base)
    con.putrequest('POST', post_loc)
    con.putheader('Authorization', authorization)

    if xml:
        clen = len(xml)
        con.putheader('Content-Type', 'text/xml')
        con.putheader('Content-Length', `clen`)
    con.endheaders()

    if xml:
        con.send(xml)

    respcode, respmsg, headers = con.getreply()

    # 201 == created
    # 200 == OK

    if respcode not in [200, 201]:
        print 'Response code %d' % respcode
        print 'An error occurred: %s' % respmsg
        print '======== Headers ========'
        print headers
        return (respcode, '')
    else:
        fin = con.getfile()
        new_id = fin.read()
        fin.close()
        return (0, new_id)

def delete(username, password, del_loc):

    usernamepass = username + ':' + password
    usernamepass = base64.encodestring(usernamepass).strip()
    authorization = 'Basic ' + usernamepass

    con = httplib.HTTP(server_base)
    con.putrequest('DELETE', del_loc)
    con.putheader('Authorization', authorization)

    con.endheaders()

    respcode, respmsg, headers = con.getreply()

    # 201 == created
    # 200 == OK

    if respcode != 200:
        print 'Response code %d' % respcode
        print 'An error occurred: %s' % respmsg
        print '======== Headers ========'
        print headers
        return respcode
    else:
        return 0
