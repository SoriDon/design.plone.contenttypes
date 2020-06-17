# -*- coding: utf-8 -*-
from plone.restapi.serializer.dxcontent import (
    SerializeFolderToJson as BaseSerializer,
)
from design.plone.contenttypes.interfaces.unita_organizzativa import (
    IUnitaOrganizzativa,
)

from plone import api
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class SerializeFolderToJson(BaseSerializer):
    def __call__(self, version=None, include_items=True):
        result = super(SerializeFolderToJson, self).__call__(
            version=None, include_items=True
        )
        catalog = api.portal.get_tool("portal_catalog")
        query = {
            self.index: result["UID"],
            "portal_type": ["Servizio"],
            "sort_on": "sortable_title",
            "sort_order": "ascending",
        }

        brains = catalog(**query)
        servizi = [
            {
                "title": x.Title or "",
                "description": x.Description or "",
                "@id": x.getURL() or "",
            }
            for x in brains
        ]
        result["servizi_offerti"] = servizi
        return result


@implementer(ISerializeToJson)
@adapter(IUnitaOrganizzativa, Interface)
class UOSerializer(SerializeFolderToJson):
    index = "ufficio_responsabile"