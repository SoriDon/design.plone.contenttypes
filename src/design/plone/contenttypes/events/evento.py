# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.CMFPlone.utils import _createObjectByType
from plone import api


def eventoCreateHandler(evento, event):
    """
    Complete content type evento setup on added event, generating
    missing folders, fields, etc.

    @param evento: Content item

    @param event: Event that triggers the method (onAdded event)
    """

    galleria = _createObjectByType("Folder", evento, "multimedia")
    galleria.title = "Multimedia"
    galleria.reindexObject(idxs=["Title"])

    # galleria = api.content.create(
    #     container=event, type="Folder", title="Multimedia"
    # )
    constraintsGalleria = ISelectableConstrainTypes(galleria)
    constraintsGalleria.setConstrainTypesMode(1)
    # scegliere le restrizioni
    constraintsGalleria.setLocallyAllowedTypes(("Image", "Link"))

    documenti = _createObjectByType("Folder", evento, "documenti")
    documenti.title = "Documenti"
    documenti.reindexObject(idxs=["Title"])

    # documenti = api.content.create(
    #     container=event, type="Folder", title="Documenti"
    # )
    constraintsDocumenti = ISelectableConstrainTypes(documenti)
    constraintsDocumenti.setConstrainTypesMode(1)
    # scegliere le restrizioni
    constraintsDocumenti.setLocallyAllowedTypes(("File",))

    # add publish automation during creation
    api.content.transition(obj=galleria, transition="publish")
    api.content.transition(obj=documenti, transition="publish")
