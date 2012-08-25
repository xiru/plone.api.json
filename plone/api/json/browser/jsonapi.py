# -*- coding: utf-8 -*-

import json
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot

class JSONAPI(grok.View):
    """A view that exposes plone.api using JSON.
    """

    grok.name('jsonapi')
    grok.context(INavigationRoot)
    grok.require('cmf.ManagePortal')
    
    def render(self):
        """foobar
        """
        return json.dumps('foobar')
