# -*- coding: utf-8 -*-
from collective.volto.blocksfield.field import BlocksField
from design.plone.contenttypes.controlpanels.vocabularies import (
    IVocabulariesControlPanel,
)
from plone import api
from copy import deepcopy
from design.plone.contenttypes.upgrades.draftjs_converter import to_draftjs
from plone.app.textfield.value import RichTextValue
from plone.app.upgrade.utils import installOrReinstallProduct
from plone.dexterity.utils import iterSchemata
from zope.schema import getFields


import logging
import json
import six

logger = logging.getLogger(__name__)

DEFAULT_PROFILE = "profile-design.plone.contenttypes:default"

# standard upgrades #


def update_profile(context, profile, run_dependencies=True):
    context.runImportStepFromProfile(
        DEFAULT_PROFILE, profile, run_dependencies
    )


def update_types(context):
    update_profile(context, "typeinfo")


def update_rolemap(context):
    update_profile(context, "rolemap")


def update_registry(context):
    update_profile(context, "plone.app.registry", run_dependencies=False)


def update_catalog(context):
    update_profile(context, "catalog")


def update_controlpanel(context):
    update_profile(context, "controlpanel")


def remap_fields(mapping):
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
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
                delattr(item, old)


# custom ones #


def to_1001(context):

    update_types(context)

    # cleanup event behaviors
    portal_types = api.portal.get_tool(name="portal_types")
    behaviors = portal_types["Event"].behaviors
    to_remove = [
        "design.plone.contenttypes.behavior.luoghi_correlati",
        "design.plone.contenttypes.behavior.argomenti_evento",
        "design.plone.contenttypes.behavior.additional_help_infos_evento",
    ]
    portal_types["Event"].behaviors = tuple(
        [x for x in behaviors if x not in to_remove]
    )

    mapping = {
        # "descrizione_destinatari": "a_chi_si_rivolge",
        "canale_fisico": "dove_rivolgersi_extra",
        "canale_fisico_prenotazione": "prenota_appuntamento",
        "fasi_scadenze": "tempi_e_scadenze",
        "sedi_e_luoghi": "dove_rivolgersi",
        "box_aiuto": "ulteriori_informazioni",
        "riferimento_telefonico_luogo": "telefono",
        "riferimento_mail_luogo": "email",
    }
    remap_fields(mapping=mapping)


def to_1003(context):

    update_types(context)

    mapping = {
        "unita_amministrativa_responsabile": "unita_amministrative_responsabili",  # noqa
        "sedi": "sede",
        "contatto_reperibilita": "reperibilita",
        "evento_supportato_da": "supportato_da",
    }
    remap_fields(mapping=mapping)


def to_1005(context):
    def fix_index(blocks):
        for block in blocks.values():
            if block.get("@type", "") == "listing":
                for query in block.get("query", []):
                    if (
                        query["i"] == "argomenti_correlati"
                        or query["i"] == "tassonomia_argomenti"
                    ):  # noqa
                        query["i"] = "argomenti"
                        logger.info(" - {}".format(brain.getURL()))

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_index(portal_blocks)
    portal.blocks = json.dumps(portal_blocks)

    logger.info("Fixing listing blocks.")
    for brain in api.content.find(
        object_provides="plone.restapi.behaviors.IBlocks"
    ):
        item = brain.getObject()
        blocks = deepcopy(getattr(item, "blocks", {}))
        if blocks:
            fix_index(blocks)
            item.blocks = blocks
    logger.info("** Reindexing items that refers to an argument **")
    for brain in api.portal.get_tool("portal_catalog")():
        item = brain.getObject()
        if getattr(item.aq_base, "tassonomia_argomenti", []):
            logger.info(" - {}".format(brain.getURL()))
            item.reindexObject(idxs=["argomenti"])


def to_1006(context):
    def fix_index(blocks):
        for block in blocks.values():
            if block.get("@type", "") == "listing":
                for query in block.get("query", []):
                    if (
                        query["i"] == "argomenti_correlati"
                        or query["i"] == "tassonomia_argomenti"
                        or query["i"] == "argomenti"
                    ):  # noqa
                        query["i"] = "argomenti"
                        query["v"] = [
                            x.Title for x in api.content.find(UID=query["v"])
                        ]
                        logger.info(" - {}".format(brain.getURL()))

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_index(portal_blocks)
    portal.blocks = json.dumps(portal_blocks)

    logger.info("Fixing listing blocks.")
    for brain in api.content.find(
        object_provides="plone.restapi.behaviors.IBlocks"
    ):
        item = brain.getObject()
        blocks = deepcopy(getattr(item, "blocks", {}))
        if blocks:
            fix_index(blocks)
            item.blocks = blocks


def to_1007(context):
    for brain in api.content.find(portal_type="Persona"):
        item = brain.getObject()
        if item.email:
            item.email = [item.email]
        if item.telefono:
            item.telefono = [item.telefono]


def to_1008(context):
    installOrReinstallProduct(api.portal.get(), "redturtle.bandi")


def to_1009(context):
    def fix_index(blocks):
        """
        revert to tassonomia_argomenti
        """
        for block in blocks.values():
            if block.get("@type", "") == "listing":
                for query in block.get("query", []):
                    if query["i"] == "argomenti":
                        query["i"] = "tassonomia_argomenti"
                        logger.info(" - {}".format(brain.getURL()))

    # fix root
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    fix_index(portal_blocks)
    portal.blocks = json.dumps(portal_blocks)

    logger.info("Fixing listing blocks.")
    for brain in api.content.find(
        object_provides="plone.restapi.behaviors.IBlocks"
    ):
        item = brain.getObject()
        blocks = deepcopy(getattr(item, "blocks", {}))
        if blocks:
            fix_index(blocks)
            item.blocks = blocks
    logger.info("** Reindexing items that refers to an argument **")
    for brain in api.portal.get_tool("portal_catalog")():
        item = brain.getObject()
        if getattr(item.aq_base, "tassonomia_argomenti", []):
            logger.info(" - {}".format(brain.getURL()))
            item.reindexObject(idxs=["tassonomia_argomenti"])


def to_1010(context):
    pc = api.portal.get_tool(name="portal_catalog")
    pc.manage_reindexIndex(ids=["event_location"])


def to_1013(context):
    def fix_template_name(blocks):
        """
        revert to tassonomia_argomenti
        """
        found = False
        for block in blocks.values():
            if (
                block.get("@type", "") == "listing"
                and block.get("template", "") == "imageGallery"
            ):
                block["template"] = "photogallery"
                found = True
        return found

    # fix root
    logger.info(
        'Changing listing block template from "imageGallery" to "photogallery'
    )
    portal = api.portal.get()
    portal_blocks = json.loads(portal.blocks)
    to_update = fix_template_name(portal_blocks)
    fixed_items = []
    if to_update:
        portal.blocks = json.dumps(portal_blocks)
        fixed_items.append("Root")
    i = 0
    brains = api.content.find(
        object_provides="plone.restapi.behaviors.IBlocks"
    )
    tot = len(brains)
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        item = brain.getObject()
        blocks = deepcopy(getattr(item, "blocks", {}))
        if blocks:
            to_update = fix_template_name(blocks)
            if to_update:
                item.blocks = blocks
                fixed_items.append(brain.getPath())

    logger.info("Finish")
    if fixed_items:
        logger.info("Updated items:")
        for fixed in fixed_items:
            logger.info("- {}".format(fixed))
    else:
        logger.info("No items affected.")


def to_1014(context):
    update_types(context)
    portal_types = api.portal.get_tool(name="portal_types")
    portal_types["Bando"].behaviors = tuple(
        [
            x
            for x in portal_types["Bando"].behaviors
            if x != "design.plone.contenttypes.behavior.argomenti"
        ]
    )


def to_1015(context):
    update_types(context)

    # cleanup trasparenza behavior from CTs
    portal_types = api.portal.get_tool(name="portal_types")
    service_behaviors = portal_types["Servizio"].behaviors
    to_remove = [
        "design.plone.contenttypes.behavior.trasparenza",
    ]
    portal_types["Servizio"].behaviors = tuple(
        [x for x in service_behaviors if x not in to_remove]
    )


def to_1016(context):
    section_ids = ["amministrazione", "servizi", "novita", "documenti-e-dati"]
    sections = []
    portal = api.portal.get()
    for id in section_ids:
        item = portal.get(id, None)
        if item:
            sections.append({"title": item.title, "linkUrl": [item.UID()]})
    settings = [{"rootPath": "/", "items": sections}]
    api.portal.set_registry_record(
        "search_sections",
        json.dumps(settings),
        interface=IVocabulariesControlPanel,
    )


def to_2000(context):
    # remove volto.blocks behavior from news and events and add new one
    update_types(context)
    portal_types = api.portal.get_tool(name="portal_types")
    for ptype in ["News Item", "Event"]:
        portal_types[ptype].behaviors = tuple(
            [x for x in portal_types[ptype].behaviors if x != "volto.blocks"]
        )
    portal_types["Pagina Argomento"].behaviors = tuple(
        [
            x
            for x in portal_types["Pagina Argomento"].behaviors
            if x != "design.plone.contenttypes.behavior.additional_help_infos"
        ]
    )
    # now copy values in new fields
    pc = api.portal.get_tool(name="portal_catalog")
    brains = pc()
    tot = len(brains)
    i = 0
    logger.info("### START CONVERSION FIELDS RICHTEXT -> DRAFTJS ###")
    for brain in brains:
        i += 1
        if i % 1000 == 0:
            logger.info("Progress: {}/{}".format(i, tot))
        item = brain.getObject()
        if brain.portal_type in ["Event", "News Item"]:
            blocks = getattr(item, "blocks", {})
            blocks_layout = getattr(item, "blocks_layout", {"items": []})[
                "items"
            ]
            if not blocks:
                continue
            title_uid = ""
            new_blocks = {}
            for uid, block in blocks.items():
                if block.get("@type", "") == "title":
                    title_uid = uid
                else:
                    new_blocks[uid] = block
            item.descrizione_estesa = {
                "blocks": new_blocks,
                "blocks_layout": {
                    "items": [x for x in blocks_layout if x != title_uid]
                },
            }
            item.blocks = None
            item.blocks_layout = None
        for schema in iterSchemata(item):
            for name, field in getFields(schema).items():
                if not isinstance(field, BlocksField):
                    continue
                value = field.get(item)
                if not value:
                    continue
                if isinstance(value, six.string_types):
                    value = "<p>{}</p>".format(value)
                elif isinstance(value, RichTextValue):
                    value = value.raw
                else:
                    continue
                if value == "<p><br></p>":
                    value = ""
                try:
                    new_value = to_draftjs(value)
                except Exception as e:
                    logger.error(
                        "[NOT MIGRATED] - {}: {}".format(brain.getPath(), name)
                    )
                    raise e
                setattr(item, name, new_value)