# -*- coding: utf-8 -*-

import json
from five import grok
from plone.api.json.interfaces import IJSONAPI

class JSONAPI(grok.GlobalUtility):
    """A global utility that exposes plone.api using JSON.
    """
    grok.provides(IJSONAPI)

    def foobar(self):
        """foobar
        """
        return json.dumps('foobar')
