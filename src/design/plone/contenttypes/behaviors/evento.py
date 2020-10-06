# -*- coding: utf-8 -*-
from design.plone.contenttypes import _
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import provider, implementer


@provider(IFormFieldProvider)
class IEvento(model.Schema):
    """Marker inteerface for content type Evento
    """

    sottotitolo = schema.TextLine(
        title=_(u"sottotitolo_label", default=u"Sottotitolo"),
        description=_(
            "sottotitolo_help",
            default="Indica un eventuale sottotitolo/titolo alternativo.",
        ),
        required=False,
    )

    descrizione_destinatari = RichText(
        title=_(
            u"descrizione_destinatari", default=u"Descrizione destinatari"
        ),
        required=False,
        description=_(
            "descrizione_destinatari_help",
            default="Descrizione dei principali interlocutori dell'evento.",
        ),
    )

    persone_amministrazione = RelationList(
        title=u"Persone dell'amministrazione che partecipano all'evento",
        default=[],
        value_type=RelationChoice(
            title=_(u"Persona dell'amministrazione"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "persone_amministrazione_help",
            default="Elenco delle persone dell'amministrazione che"
            " parteciperanno all'evento.",
        ),
        required=False,
    )
    form.widget(
        "persone_amministrazione",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona"],
        },
    )

    # model.fieldset(
    #     "correlati",
    #     label=_("correlati_label", default="Contenuti collegati"),
    #     fields=["luoghi_correlati"],
    # )

    # non vengono mostrati
    # indirizzo = schema.TextLine(
    #     title=_(u"indirizzo", default=u"Indirizzo"), required=True
    # )

    # quartiere = schema.TextLine(
    #     title=_(u"quartiere", default=u"Quartiere"), required=False
    # )

    # circoscrizione = schema.TextLine(
    #     title=_(u"circoscrizione", default=u"Circoscrizione"), required=False
    # )

    # cap = schema.TextLine(title=_(u"cap", default=u"CAP"), required=True)

    orari = RichText(
        title=_(u"orari", default=u"Informazioni sugli orari"),
        required=False,
        description=_(
            "orari_help",
            default="Informazioni sugli orari di svolgimento dell'evento.",
        ),
    )

    # TODO: come gestire il campo "Aggiungi al calendario"

    prezzo = RichText(
        title=_(u"prezzo", default=u"Prezzo"),
        required=False,
        description=_(
            "prezzo_help",
            default="Indicare il prezzo dell'evento, se presente, specificando"
            " se esistono formati diversi.",
        ),
    )

    organizzato_da_esterno = RichText(
        title=_(u"organizzato_da_esterno", default=u"Organizzato da"),
        required=False,
        description=_(
            "organizzato_da_esterno_help",
            default="Se l'evento non è organizzato direttamente dal comune,"
            " indicare l'organizzatore.",
        ),
    )

    contatto_reperibilita = schema.TextLine(
        title=_(
            u"contatto_reperibilita", default=u"Reperibilità organizzatore"
        ),
        required=False,
        description=_(
            "contatto_reperibilita_help",
            default="Indicare gli orari in cui l'organizzatore è"
            " telefonicamente reperibile.",
        ),
    )

    organizzato_da_interno = RelationList(
        title=_(
            u"Organizzato da_interno", default=u"Organizzato da (interno)"
        ),
        default=[],
        value_type=RelationChoice(
            title=_(u"Organizzatore"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        required=False,
        description=_(
            "organizzato_da_interno_help",
            default="Se l'evento è organizzato direttamente dal comune,"
            " indicare l'ufficio/ente organizzatore.",
        ),
    )
    form.widget(
        "organizzato_da_interno",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 10,
            "selectableTypes": ["Persona", "UnitaOrganizzativa", "Servizio"],
        },
    )

    # ref
    evento_supportato_da = RelationList(
        title=_(u"supportato_da", default=u"Evento supportato da"),
        required=False,
        default=[],
        value_type=RelationChoice(
            title=_(u"Evento supportato da"),
            vocabulary="plone.app.vocabularies.Catalog",
        ),
        description=_(
            "supportato_da_help",
            default="Se l'evento è organizzato direttamente dal comune,"
            " indicare l'ufficio/ente che supporta l'evento.",
        ),
    )

    # TODO: come fare il rating/recensione dell'evento

    patrocinato_da = schema.TextLine(
        title=_(u"patrocinato_da", default=u"Patrocinato da"),
        required=False,
        description=_(
            "patrocinato_da_help",
            default="Indicare l'ente che supporta l'evento, se presente.",
        ),
    )

    # custom widgets
    form.widget(
        "evento_supportato_da",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "maximumSelectionSize": 1,
            "selectableTypes": ["UnitaOrganizzativa"],
        },
    )

    # custom fieldsets
    # model.fieldset(
    #     "partecipanti",
    #     label=_("partecipanti_label", default=u"Partecipanti"),
    #     fields=["descrizione_destinatari", "persone_amministrazione"],
    # )
    # model.fieldset(
    #     "costi", label=_("costi_label", default=u"Costi"), fields=["prezzo"]
    # )
    # model.fieldset(
    #     "contatti",
    #     label=_("contatti_label", default=u"Contatti"),
    #     fields=[
    #         "organizzato_da_esterno",
    #         "organizzato_da_interno",
    #         "contatto_reperibilita",
    #         "evento_supportato_da",
    #     ],
    # )
    # model.fieldset(
    #     "informazioni",
    #     label=_("informazioni_label", default=u"Ulteriori informazioni"),
    #     fields=["patrocinato_da"],
    # )
    # model.fieldset(
    #     "date_evento",
    #     label=_("date_evento_label", default=u"Date dell'evento"),
    #     fields=["orari"],
    # )


@implementer(IEvento)
@adapter(IDexterityContent)
class Evento(object):
    """
    """

    def __init__(self, context):
        self.context = context
