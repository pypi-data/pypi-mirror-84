
import os
import json

from glob import glob
from django import template

register = template.Library()

@register.filter
def hashed(filepath, static_path):
    """Webpack bundles are generated with a hash sufix to the filenane.
    This is done to avoid problems with caching.
    This template filter idetifies the hashed files that match the
    filename*.ext in the directory where and returns the correct url.
    """

    static_path = static_path if static_path.endswith('/') else '%s/' % static_path
    filepath_pattern, ext = filepath.split('.')
    filepath = glob('%s*.%s' % (os.path.join(static_path, filepath_pattern), ext))[0]

    return filepath.replace(static_path, '')
