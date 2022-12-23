# -*- coding: utf-8 -*-
from design.plone.contenttypes.interfaces.servizio import IServizio
from plone.restapi.deserializer import json_body
from plone.restapi.interfaces import IDeserializeFromJson
from zope.interface import implementer
from zope.component import adapter
from zope.interface import Interface
from plone.restapi.deserializer.dxcontent import DeserializeFromJson
from zExceptions import BadRequest
from plone.restapi.behaviors import IBlocks
from plone.restapi.indexers import SearchableText_blocks


TITLE_MAX_LEN = 160
DESCRIPTION_MAX_LEN = 160
EMPTY_BLOCK_MARKER = {'@type': 'text'}
MANDATORY_RICH_TEXT_FIELDS = [
    "motivo_stato_servizio",
    "a_chi_si_rivolge",
    "come_si_fa",
    "cosa_serve",
    "cosa_si_ottiene",
    "tempi_e_scadenze",
]


def new_error(message):
    return {
        "error": "ValidationError",
        "message": message
    }


def text_in_block(blocks):

    @implementer(IBlocks)
    class FakeObject(object):
        """
        We use a fake object to use SearchableText Indexer
        """
        def Subject(self):
            return ""

        def __init__(self, blocks, blocks_layout):
            self.blocks = blocks
            self.blocks_layout = blocks_layout
            self.id = ""
            self.title = ""
            self.description = ""

    if not blocks:
        return None

    fakeObj = FakeObject(
        blocks.get("blocks", ""),
        blocks.get("blocks_layout", "")
    )
    return SearchableText_blocks(fakeObj)()


@implementer(IDeserializeFromJson)
@adapter(IServizio, Interface)
class DeserializeServizioFromJson(DeserializeFromJson):
    def __call__(
        self, validate_all=False, data=None, create=False
    ):  # noqa: ignore=C901

        if data is None:
            data = json_body(self.request)

        method = self.request.get('method')
        is_post = method == 'POST'
        is_patch = method == 'PATCH'
        errors = []

        title = data.get('title')
        description = data.get('description')
        # stato_servizio = data.get('stato_servizio')
        # motivo_stato_servizio = data.get('motivo_stato_servizio')

        if is_post:
            # Title validation
            if not title:
                errors.append(
                    new_error(
                        "Il titolo del servizio è obbligatorio"
                    )
                )
            elif len(title) > TITLE_MAX_LEN:
                errors.append(
                    new_error(
                        "Il titolo può avere una lunghezza di massimo {} caratteri".format(TITLE_MAX_LEN)
                    )
                )

            # description validation
            if not description:
                errors.append(
                    new_error(
                        "La descrizione del servizio è obbligatorio"
                    )
                )
            elif len(description) > DESCRIPTION_MAX_LEN:
                errors.append(
                    new_error(
                        "La descrizione del servizio deve avere una lunghezza di massimo {} caratteri".format(DESCRIPTION_MAX_LEN)
                    )
                )

            for field in MANDATORY_RICH_TEXT_FIELDS:
                if field == 'motivo_stato_servizio':
                    if (data.get('stato_servizio') and not data.get("motivo_stato_servizio")) or\
                            (data.get('stato_servizio') and not text_in_block(data.get("motivo_stato_servizio"))):
                        errors.append(
                            new_error(
                                "Indicare il motivo per cui il servizio non è fruibile"
                            )
                        )
                elif field not in data:
                    errors.append(
                        new_error(
                            "Il campo {} è obbligatorio".format(field)
                        )
                    )
                elif field in data and not text_in_block(data.get(field)):
                    errors.append(
                        new_error(
                            "Il campo {} è obbligatorio".format(field)
                        )
                    )

        if is_patch:
            # Title validation
            if "title" in data and not title:
                errors.append(
                    new_error(
                        "Il titolo del servizio è obbligatorio"
                    )
                )
            if title and len(title) > TITLE_MAX_LEN:
                errors.append(
                    new_error(
                        "Il titolo può avere una lunghezza di massimo {} caratteri".format(TITLE_MAX_LEN)
                    )
                )
            # description validation
            if "description" in data and not description:
                errors.append(
                    new_error(
                        "La descrizione del servizio è obbligatorio"
                    )
                )
            if description and len(description) > DESCRIPTION_MAX_LEN:
                errors.append(
                    new_error(
                        "La descrizione del servizio deve avere una lunghezza di massimo {} caratteri".format(DESCRIPTION_MAX_LEN)
                    )
                )

            for field in MANDATORY_RICH_TEXT_FIELDS:
                if field == 'motivo_stato_servizio':
                    if 'stato_servizio' in data and\
                         data.get('stato_servizio') and not\
                            text_in_block(data.get(field)):
                        errors.append(
                            new_error(
                                "Indicare il motivo per cui il servizio non è fruibile"
                            )
                        )
                elif field in data and not text_in_block(data.get(field)):
                    errors.append(
                        new_error(
                             "Il campo {} è obbligatorio".format(field)
                        )
                    )

            # Per questo campo dobbiamo controllare anche il contesto: potrei aver
            # già scritto sull'oggetto che il servizio non è fruibile e modificare
            # solo lo stato
            if "stato_servizio" not in data and getattr(self.context, "stato_servizio") and\
                data.get('motivo_stato_servizio') and not\
                    text_in_block(data.get('motivo_stato_servizio')):
                errors.append(
                    new_error(
                        "Indicare il motivo per cui il servizio non è fruibile"
                    )
                )

        if errors:
            raise BadRequest(errors)
        return super(DeserializeServizioFromJson, self).__call__(
            validate_all=False, data=data, create=False
        )
