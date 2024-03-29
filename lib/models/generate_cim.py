"""
.. module:: generate_cim.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP6 CIM documents from simplified JSON output.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os

import pyesdoc

from pyesdoc.ontologies.cim import v2 as cim

from lib.models.utils import ModelTopicOutput
from lib.utils import io_mgr
from lib.utils import logger
from lib.utils import vocabs


# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model CIM files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str
    )

# Set of properties injected by machinery.
_INJECTED_PROPERTIES = {'Name', 'Overview', 'Keywords'}

# Name of file controlling publication.
_MODEL_PUBLICATION_FNAME = "model_publication.json"


def _main(args):
    """Main entry point.

    """
    # Write a CIM file per CMIP6 institute | source combination.
    institutes = vocabs.get_institutes(args.institution_id)
    for i in institutes:
        # Escape if settings file not found.
        try:
            all_settings = io_mgr.load_model_settings(i, _MODEL_PUBLICATION_FNAME)
        except IOError:
            warning = '{} model_publications.json not found'
            warning = warning.format(i.canonical_name)
            logger.log_warning(warning)
            continue

        for s in vocabs.get_institute_sources(i):
            # Escape if source settings undeclared.
            try:
                settings = all_settings[s.canonical_name]
            except KeyError:
                warning = '{} :: {} publication settings not found'
                warning = warning.format(i.canonical_name, s.canonical_name)
                logger.log_warning(warning)
                continue

            # Escape if no settings are switched 'on'.
            settings = {k:v for (k,v) in settings.items()
                        if settings[k]['publish'] == 'on'}
            if not settings:
                continue

            # Generate content.
            content = _get_content(i, s, settings)
            if content is None:
                warning = '{} :: {} CIM file not found'
                warning = warning.format(i.canonical_name, s.canonical_name)
                logger.log_warning(warning)
                continue

            # Write CIM file to fs.
            io_mgr.write_model_cim(i, s, content)


def _can_publish(i, s, settings):
    """Returns flag indicating whether a cim files is to be published or not.

    """
    return len([i for i in settings.values() if i['publish'] == 'on']) > 0


def _get_content(i, s, settings):
    """Generates a CIM document for a CMIP6 institute | source combination.

    """
    # Set JSON content accessors.
    accessors = _get_data_accessors(i, s, settings)

    # Map JSON -> CIM.
    doc = _map_model(i, s, accessors)
    if doc is None:
        return

    # Destructure injected properties.
    _destructure(doc)

    # Emit validation report.
    errors = pyesdoc.validate(doc)
    errors = [e for e in errors if
              e.endswith('values --> is an empty list') == False]
    if errors:
        print("INVALID CIM DOCUMENT: {}".format(s))
        for err in errors:
            print(err)

    # Return JSON string.
    return pyesdoc.encode(doc)


def _get_data_accessors(i, s, settings):
    """Returns a collection of model spreadsheet output accessors - one per spreadsheet.

    """
    topics = vocabs.get_model_topics(s)
    topics = [t for t in topics if t.canonical_name in settings]
    accessors = [ModelTopicOutput.create(i, s, t) for t in topics]

    return [a for a in accessors if a.content]


def _destructure_injected(container, doc, accessor):
    """Destructures properties injected by the machinery but which can be directly assigned to CIM type instances.

    """
    # Escape if the container was empty.
    if container is None:
        return

    # Set injected.
    injected = [i for i in container.properties if i.name in _INJECTED_PROPERTIES]

    # Assign to CIM type instance.
    for p in injected:
        if p.name == 'Name':
            doc.long_name = accessor.get_value(p.specialization_id)
        elif p.name == 'Overview':
            doc.description = accessor.get_value(p.specialization_id)
        elif p.name == 'Keywords':
            doc.keywords = accessor.get_comma_delimited_values(p.specialization_id)

    # Update container.
    container.properties = [i for i in container.properties if i not in injected]


def _destructure(model):
    """Destructures properties injected by the machinery but which can be directly assigned to CIM type instances.

    """
    if model.key_properties:
        for p in [i for i in model.key_properties.properties if i.values]:
            if p.name == 'Name':
                model.long_name = p.values[0]
            elif p.name == 'Overview':
                model.description = p.values[0]
            elif p.name == 'Keywords':
                model.keywords = [i.strip() for i in p.values[0].split(',')]


def _map_model(i, s, accessors):
    """Returns a mapped model CIM document.

    """
    m = pyesdoc.create(cim.Model, project='CMIP6', source='spreadsheet', version=1, institute=i.canonical_name)
    m.activity_properties = _map_model_activity_properties(accessors) or []
    m.canonical_id = s.canonical_name
    m.key_properties = _map_model_key_properties(accessors)
    m.model_type = _map_model_type(i, s)
    m.name = s.canonical_name.upper()
    m.realms = _map_realms(accessors)

    return m if (m.activity_properties or m.key_properties or m.realms) else None


def _map_model_type(i, s):
    """Returns a mapped model type.

    """
    # Workaround applied as a quick fix to rectify a specific inaccurate
    # model type reported by the CMCC liaison. For context, see:
    # https://github.com/ES-DOC/cmip6/issues/15
    if i.canonical_name == "cmcc":
        return "ESM"
    return "GCM"


def _map_model_activity_properties(accessors):
    """Maps a specialization to model activity properties.

    """
    for accessor in accessors:
        if accessor.specialization.id.endswith('toplevel'):
            return _map_topics(accessor.specialization['process'], accessor)


def _map_model_key_properties(accessors):
    """Maps a specialization to model key properties.

    """
    for accessor in accessors:
        if accessor.specialization.id.endswith('toplevel'):
            return _map_topic(accessor.specialization['keyprops'], accessor)


def _map_realms(accessors):
    """Maps specializations to realms.

    """
    accessors = [i for i in accessors if not i.specialization.id.endswith('toplevel')]
    result = [_map_realm(i.specialization, i) for i in accessors]

    return [i for i in result if i is not None]


def _map_realm(specialization, accessor):
    """Maps a specialization to a realm.

    """
    r = pyesdoc.create(cim.Realm, project='CMIP6', source='spreadsheet', version=1)
    r.description = specialization.description or specialization.name_camel_case_spaced
    r.name = specialization.name_camel_case_spaced
    r.specialization_id = specialization.id
    r.key_properties = _map_topic(specialization['keyprops'], accessor)
    r.grid = _map_topic(specialization['grid'], accessor)
    r.processes = _map_topics(specialization['process'], accessor)

    return r if (r.key_properties or r.grid or r.processes) else None


def _map_topic(specialization, accessor):
    """Maps a specialization to a topic.

    """
    if specialization is None:
        return
    t = _instantiate(specialization, cim.Topic, False)
    t.properties = _map_properties(specialization.properties, accessor)
    t.property_sets = _map_property_sets(specialization.property_sets, accessor)
    t.sub_topics = _map_topics(specialization.sub_topics, accessor)

    return t if (t.properties or t.property_sets or t.sub_topics) else None


def _map_topics(specializations, accessor):
    """Maps specializations to topics.

    """
    result = [_map_topic(i, accessor) for i in specializations]

    return [i for i in result if i is not None]


def _map_properties(specializations, accessor):
    """Maps specializations to properties.

    """
    result = [_map_property(i, accessor) for i in specializations]

    return [i for i in result if i is not None]


def _map_property(specialization, accessor):
    """Maps a specialization to a property.

    """
    tp = _instantiate(specialization, cim.TopicProperty, False)
    tp.values = accessor.get_values(specialization.id)
    tp.values = [i for i in tp.values if i is not None]
    tp.values = [i if isinstance(i, (str, unicode)) else unicode(i) for i in tp.values]

    return tp if tp.values else None


def _map_property_set(specialization, accessor):
    """Maps a specialization to a property set.

    """
    tps = _instantiate(specialization, cim.TopicPropertySet, False)
    tps.properties = [_map_property(i, accessor) for i in specialization.properties]
    tps.properties = [i for i in tps.properties if i is not None]

    return tps if tps.properties else None


def _map_property_sets(specializations, accessor):
    """Maps specializations to property sets.

    """
    result = [_map_property_set(i, accessor) for i in specializations]

    return [i for i in result if i is not None]


def _instantiate(specialization, cim_type, include_description):
    """Instantiates a CIM type instance.

    """
    instance = cim_type()
    if include_description:
        instance.description = specialization.description or specialization.name_camel_case_spaced
        instance.name = specialization.name_camel_case_spaced
    instance.specialization_id = specialization.id

    return instance


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
