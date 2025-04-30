USAGE:

    url_metadata_query.py file-name

    This is actually useful ;-), but it's also a quick exploration of some of the
    functionality provided in the public API for querying YouTube.  The same API
    can download videos, gather metadata and statistics, etc.  There are (naturally!)
    some good YouTube videos on leveraging it.

    In this case, it reads in a file of data lines looking for "https://" and writes
    out just the site/host name for non-YouTube links.  For YouTube links of various
    forms, it uses the API to query out the "channel" name to go along with the basic
    web site/host name.
