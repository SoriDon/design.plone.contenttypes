# Design Plone Content-types

Pacchetto per la gestione dei content-type per un sito Agid con Plone.

# Features

Installando questo pacchetto, si rendono disponibili diversi content-type per la
gestione di un sito Agid con Plone e Volto.

# Tipi di contenuto

## Elenco tipi implementati

- [ ] **Dataset**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Documento**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Documento Personale**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Evento**

  - [x] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Collegamento**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata
  - [ ] Selezione link interno

- [ ] **Messaggio**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [x] **Notizia**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

- [ ] **Luogo**

  - [x] Definizione campi
  - [ ] Abilitare behavior collective.address.address
  - [ ] Ordine campi
  - [x] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Pagina Argomento**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Persona**

  - [x] Definizione campi
  - [ ] Ordine campi
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

- [ ] **Pratica**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Ricevuta Pagamento**

  - [ ] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [ ] Vista su Volto completata

- [ ] **Servizio**

  - [x] Definizione campi
  - [ ] Ordine campi
  - [ ] Indicizzazione testo
  - [x] Vista su Volto completata

- [x] **Unità Organizzativa**

  - [x] Definizione campi
  - [x] Ordine campi
  - [x] Indicizzazione testo
  - [x] Vista su Volto completata

## Pagina

- Può essere usata anche come pagina di disambiguazione. C'è una behavior attivata (_design.plone.contenttypes.behavior.info_testata_)
  per impostare informazioni aggiuntive per la testata delle pagine di disambiguazione.

## Notizie e comunicati stampa

- Tipo base "Notizia" di Plone con alcuni campi aggiuntivi.
- Folderish (grazie a redturtle.volto)
- Può contenere Immagini, Collegamenti, File, Documenti (utile per strutturare i contenuti al suo interno)
- Alla creazione di una Notizia, vengono create automaticamente al suo interno due cartelle
  "Multimedia" e "Documenti allegati" per poter organizzare meglio i contenuti

## Luogo

Esiste un deserializer per plone.restapi per il campo di tipo "GeolocationField" che si occupa di trasformare
le coordinate in input, in un oggetto corretto per quel campo.

Accetta un valore del tipo::

    {
      "latitude": 10.0000,
      "longitude": 20.0000,
    }

Alcuni campi della geolocalizzazione hanno dei valori predefiniti quando viene richiesto lo schema mediante plone.restapi:

- city
- street
- geolocation
- country

Sono pre-popolati con la sede di AGID a Roma.

# Gestione vocabolari

Per diversi tipi di contenuto servono dei vocabolari con una lista di valori predefiniti.

Questi sono configurabili dal pannello di controllo "_Vocabolari Design Plone_".

I vocabolari personalizzabili sono i seguenti:

- Tipologie notizia
- Tipologie unità organizzativa

# Installazione

Questo prodotto non è stato pensato per funzionare da solo, ma fa parte della suite "design.plone".

Per utilizzare questo prodotto, fare riferimento a design.plone.policy\_.

.. \_design.plone.policy: https://github.com/RedTurtle/design.plone.policy

# Traduzioni

Per aggiornare le traduzioni, basta usare lo script `update_locales` dentro alla cartella bin::

> bin/update_locales

**N.B.: lo script va chiamato due volte perché al primo giro non aggiorna i file.**

# Contribuisci

- Issue Tracker: https://github.com/redturtle/design.plone.contenttypes/issues
- Codice sorgente: https://github.com/redturtle/design.plone.contenttypes

# Licenza

Questo progetto è rilasciato con licenza GPLv2.

# Autori

Questo progetto è stato sviluppato da **RedTurtle Technology**.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
:alt: RedTurtle Technology Site
:target: http://www.redturtle.it/
