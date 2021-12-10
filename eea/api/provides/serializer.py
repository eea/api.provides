""" Overrides for the default Plone serialization
"""

from eea.api.provides.interfaces import IEeaApiProvidesLayer
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer import dxcontent
from zope.component import adapter
from zope.interface import implementer, providedBy


@implementer(ISerializeToJson)
@adapter(IDexterityContent, IEeaApiProvidesLayer)
class SerializeToJson(dxcontent.SerializeToJson):
    ''' serialize to json '''
    def __call__(self, version=None, include_items=True):
        res = super(SerializeToJson, self).__call__(version, include_items)

        if self.request.form.get('expand') == 'provides':
            res['@provides'] = [
                '{}.{}'.format(interface.__module__, interface.__name__)
                for interface in providedBy(self.context)]

        return res


@implementer(ISerializeToJson)
@adapter(IDexterityContainer, IEeaApiProvidesLayer)
class SerializeFolderToJson(dxcontent.SerializeFolderToJson):
    ''' serialize folder to json '''
    def __call__(self, version=None, include_items=True):
        res = super(SerializeFolderToJson, self).__call__(
            version, include_items)

        if self.request.form.get('expand') == 'provides':
            res['@provides'] = [
                '{}.{}'.format(interface.__module__, interface.__name__)
                for interface in providedBy(self.context)]

        return res
