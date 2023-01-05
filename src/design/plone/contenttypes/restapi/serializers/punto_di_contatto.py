# -*- coding: utf-8 -*-
from .related_news_serializer import SerializeFolderToJson
from Acquisition import aq_inner
from design.plone.contenttypes.interfaces.punto_di_contatto import IPuntoDiContatto
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission


@implementer(ISerializeToJson)
@adapter(IPuntoDiContatto, Interface)
class PuntoDiContattoSerializer(SerializeFolderToJson):
    index = ""

    def related_contents(self, field, portal_type):
        """ """
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        items = []
        relations = catalog.findRelations(
            dict(
                to_id=intids.getId(aq_inner(self.context)),
                from_attribute=field,
            )
        )

        for rel in relations:
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission("zope2.View", obj) and getattr(obj, 'portal_type', None) == portal_type:
                summary = getMultiAdapter(
                    (obj, getRequest()), ISerializeToJsonSummary
                )()
                items.append(summary)
        return sorted(items, key=lambda k: k["title"])

    def __call__(self, version=None, include_items=True):
        result = super(PuntoDiContattoSerializer, self).__call__(
            version=version, include_items=include_items
        )
        strutture_correlate = self.related_contents(field="contact_info", portal_type="UnitaOrganizzativa")
        servizi_correlati = self.related_contents(field="contact_info", portal_type="Servizio")
        luoghi_correlati = self.related_contents(field="contact_info", portal_type="Venue")
        persone_correlate = self.related_contents(field="contact_info", portal_type="Persona")

        if strutture_correlate:
            result["strutture_correlate"] = strutture_correlate
        if servizi_correlati:
            result["servizi_correlati"] = servizi_correlati
        if luoghi_correlati:
            result["luoghi_correlati"] = luoghi_correlati
        if persone_correlate:
            result["persone_correlate"] = persone_correlate

        return result
