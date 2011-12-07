"""WSGI middleware to filter app output through XSLT.

This employs libxslt/libxml2 by way of lxml (http://codespeak.net/lxml/) to
optionally filter the output of a wrapped application through an XSLT
stylesheet.  

The stylesheet is specified via URL in a query string parameter
'xsl'.  If a value is given for the www_path parameter at creation,
relative file paths may be used for the value of the 'xsl' parameter and
will cause the XSL to be fetched from the local file system.

Share and Enjoy.
"""

__author__ = 'l.m.orchard <l.m.orchard@pobox.com>'

import os, os.path, cgi
from StringIO import StringIO
from lxml import etree

def xslfilter(www_path=None):
    '''Decorator for XSL Transform.'''
    def decorator(application):
        return XSLFilter(application, www_path)
    return decorator

class XSLFilter:
    """WCGI application class wrapper which provides XSLT filtering"""

    def __init__(self, app, www_path=None):
        """Wrap a given WSGI app, with optional path to local XSL files."""
        self.app         = app
        self.status      = '200 OK'
        self.headers_out = []
        self.exc_info    = None
        self.www_path    = www_path

    def start_response(self, status, headers_out, exc_info=None):
        """Intercept the response start from the filtered app."""
        self.status      = status
        self.headers_out = headers_out
        self.exc_info    = exc_info
        
    def __call__(self, env, start_response):
        """Facilitate WSGI API by providing a callable hook."""
        self.env        = env
        self.real_start = start_response
        return self.__iter__()
        
    def __iter__(self):
        """"""
        params       = cgi.parse_qs(self.env.get('QUERY_STRING',''))
        result       = self.app(self.env, self.start_response)
        result_iter  = result.__iter__()
        transform_ok = False
        headers_out  = []
       
        # Search for XML content header and XSL query parameter.
        for n,v in self.headers_out:
            if n.lower()=='content-type' and v=='text/xml':
                transform_ok = ('xsl' in params)
        
        if not transform_ok:
            # Don't transform, just pass headers & content through.
            headers_out += self.headers_out
            iter_out = result_iter
            
        else:
            # Get the XSL param, set some headers for troubleshooting.
            xslt_uri = params['xsl'][0]
            headers_out.append(('X-Filter', 'XSL'))
            headers_out.append(('X-Filter-XSL', xslt_uri))
            
            # Parse the output, grab & parse the XSL, transform the output.
            doc_file   = StringIO("".join(result_iter))
            doc        = etree.parse(doc_file)
            
            # HACK: Handle local XSL urls from filesystem in www path
            if self.www_path and xslt_uri.startswith('xsl/'):
                xslt_fn  = os.path.join(self.www_path, xslt_uri)
                xslt_doc = etree.parse(open(xslt_fn,'r'))
            else:
                xslt_doc = etree.parse(xslt_uri)
            style = etree.XSLT(xslt_doc)
            
            # Apply the XSL and get the results as a string.
            result     = style.apply(doc)
            result_str = style.tostring(result)
            
            # Munge content-type and -length headers.
            for n,v in self.headers_out:
                if n.lower() == 'content-type' and 'type' in params:
                    v = params['type'][0]
                elif n.lower() == 'content-length':
                    v = len(result_str)
                headers_out.append((n,v))

            # Produce the string list iterator out of the filtered output.
            iter_out = [result_str].__iter__()
        
        # Finish up with the output headers and iterator
        self.real_start(self.status, headers_out, self.exc_info)
        return iter_out
