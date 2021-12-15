# -*- coding: utf-8 -*-
''' siblings module '''

from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer, providedBy
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class ObjectProvides(object):
    ''' Object provides '''
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        if expand:
            result = {
                'object_provides': [
                    '{}.{}'.format(interface.__module__, interface.__name__)
                    for interface in providedBy(self.context)
                ]
            }
        else:
            result = {
                "object_provides": {
                    "@id": "{}/@object_provides".format(
                        self.context.absolute_url())
                }
            }
        return result


class ObjectProvidesGet(Service):
    ''' Object provides - get '''
    def reply(self):
        ''' reply '''
        object_provides = ObjectProvides(self.context, self.request)

        return object_provides(expand='object_provides')["object_provides"]
