# -*- coding: utf-8 -*-

import json
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zExceptions import NotFound
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone import api

class JSONAPI(grok.View):
    """A view that exposes plone.api using JSON.
    """

    implements(IPublishTraverse)

    grok.context(INavigationRoot)
    grok.name('jsonapi')
    grok.require('cmf.ManagePortal')

    apimod = None
    apimet = None

    def publishTraverse(self, request, name):
        if self.apimod is None and name in ('portal', 'content', 'user', 'group'):
            self.apimod = name
            return self
        if self.apimod is not None and self.apimet is None:
            module = getattr(api, self.apimod)
            method = getattr(module, name, None)
            if method is not None:
                self.apimet = name
                return self
        raise NotFound()

    def render(self, method):
        """
        """
        request = self.request
        method = getattr(getattr(api, self.apimod), self.apimet)
        return json.dumps(method(**request.form))
