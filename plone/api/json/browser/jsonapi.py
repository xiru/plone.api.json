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

    def _normalize_parameters(self, params):
        portal = api.portal.get()
        traverse = portal.restrictedTraverse
        d = {'datetime': DateTime,
             'properties': dict,
             'roles': list,
             'groups': list,
             'container': traverse,
             'source': traverse,
             'target': traverse,
             'obj': traverse}
        for k, v in d.items():
            if params.get(k, None) is not None:
                params[k] = v(params[k])
        return params

    def _serializable_output(self, result):
        if self.apimod == 'content' and self.apimet == 'create':
            return result.absolute_url()
        return result

    def render(self):
        """ Run the plone.api method
        """
        method = getattr(getattr(api, self.apimod), self.apimet)
        params = self._normalize_parameters(self.request.form)
        result = self._serializable_output(method(**params))
        try:
            return json.dumps(result)
        except TypeError:
            return json.dumps(None)

