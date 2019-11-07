"""
.. module:: pyessv.utils.logger.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package logging utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyessv

# Returns set of institutional model configurations.
get_institute_sources = pyessv.WCRP.cmip6.get_institute_sources
get_model_configurations = pyessv.WCRP.cmip6.get_institute_sources

# Returns set of topics associated with a model.
get_model_topics = pyessv.ESDOC.cmip6.getmodel_topics

# Returns set of experiments.
get_experiments = pyessv.WCRP.cmip6.experiment_id


def get_institutes(institution_id=None):
    """Returns set of institutes to be processed.

    """
    return pyessv.WCRP.cmip6.institution_id if institution_id in (None, '', 'all') else \
           [pyessv.WCRP.cmip6.institution_id[institution_id]]


def get_source_topics(source_id):
    """Returns set of institutes to be processed.

    """
    return [pyessv.ESDOC.cmip6.model_topic.toplevel] + pyessv.WCRP.cmip6.get_source_realms(source_id)


def yield_sources(institution_id):
    """Yields set of model sources.

    """
    for i in get_institutes(institution_id):
        for s in get_institute_sources(i):
            yield i, s


def yield_topics(institution_id):
    """Yields set of model sourcce topics.

    """
    for i, s in yield_sources(institution_id):
        for t in get_model_topics(s):
            yield i, s, t
