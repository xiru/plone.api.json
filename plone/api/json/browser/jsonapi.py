# -*- coding: utf-8 -*-

import json
from DateTime import DateTime
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

    def render(self):
        """ Run the plone.api method
        """
        r = self.request
        method = getattr(getattr(api, self.apimod), self.apimet)
        params = r.form
        params['request'] = r
        # api.portal.localized_time
        if params.get('datetime', None) is not None:
            params['datetime'] = DateTime(params['datetime'])
        # api.content.create
        if params.get('container', None) is not None:
            params['container'] = api.portal.get().restrictedTraverse(params['container'])
        result = method(**params)
        # api.content.create
        if self.apimod == 'content' and self.apimet == 'create':
            result = result.absolute_url()
        return json.dumps(result)
