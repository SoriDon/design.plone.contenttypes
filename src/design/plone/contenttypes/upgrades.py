# -*- coding: utf-8 -*-
from plone import api

import logging

logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"


def update_profile(context, profile):
    context.runImportStepFromProfile(DEFAULT_PROFILE, profile)


def update_types(context):
    update_profile(context, "typeinfo")


def update_rolemap(context):
    update_profile(context, "rolemap")


def update_registry(context):
    update_profile(context, "plone.app.registry")


def update_controlpanel(context):
    update_profile(context, "controlpanel")


def to_1001(context):

    update_types(context)
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
    mapping = {
        "descrizione_destinatari": "a_chi_si_rivolge",
        "canale_fisico": "dove_rivolgersi_extra",
        "canale_fisico_prenotazione": "prenota_appuntamento",
        "fasi_scadenze": "tempi_e_scadenze",
        "sedi_e_luoghi": "dove_rivolgersi",
        "box_aiuto": "ulteriori_informazioni",
    }
    tot = len(brains)
    logger.info("Trovati {} elementi da sistemare.".format(tot))
    # remap fields
    for brain in brains:
        item = brain.getObject()
        for old, new in mapping.items():
            value = getattr(item, old, None)
            if value:
                setattr(item, new, value)
                setattr(item, old, None)
                logger.info(
                    "- {url}: {old} -> {new}".format(
                        url=brain.getURL(), old=old, new=new
                    )
                )
