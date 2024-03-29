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

# Synonmy for above.
get_model_configurations = get_institute_sources

# Returns set of topics associated with a model.
get_model_topics = pyessv.ESDOC.cmip6.getmodel_topics

# Returns set of experiments.
get_experiments = pyessv.WCRP.cmip6.experiment_id


def get_institute(institution_id):
    """Returns institute to be processed.

    """
    if isinstance(institution_id, pyessv.Term):
        return institution_id
    return pyessv.WCRP.cmip6.institution_id[institution_id]


def get_institutes(institution_id=None):
    """Returns set of institutes to be processed.

    """
    if institution_id in (None, '', 'all'):
        return pyessv.WCRP.cmip6.institution_id
    if isinstance(institution_id, pyessv.Term):
        return [institution_id]    
    return [pyessv.WCRP.cmip6.institution_id[institution_id]]


def get_source(institution_id, source_id):
    """Returns source to be processed.

    """
    for _, s in yield_sources(institution_id):
        if s.canonical_name == source_id:
            return s


def get_source_topics(source_id):
    """Returns set of institutes to be processed.

    """
    return [pyessv.ESDOC.cmip6.model_topic.toplevel] + pyessv.WCRP.cmip6.get_source_realms(source_id)


def get_source_topic(source_id, topic_id):
    """Returns set of institutes to be processed.

    """
    for t in get_source_topics(source_id):
        if t.canonical_name == topic_id:
            return t


def get_applicable_mips_with_experiments(institution):
    """Return MIPs applicable to the given institute mapped to experiments."""
    # First find all of the applicable MIPs for the institute
    all_applicable_mips = list()
    for source in get_institute_sources(institution):
        for mip in source.activity_participation:
            all_applicable_mips.append(mip.encode())

    # Some experiments apply to multiple MIPs, so handle the mapping:
    exps_to_mips = dict()
    for exp in get_experiments:
        mips = [mip.encode() for mip in exp.data["activity_id"]]
        exps_to_mips.update({exp.canonical_name.encode(): mips})

    # Now change the mapping from current exp -> MIP to the required MIP -> exp
    mips_to_exps = {}
    for exp, mips in exps_to_mips.items():
        for mip in mips:
            if mip in all_applicable_mips:  # filter out non-applicable
                mips_to_exps.setdefault(mip.encode(), []).append(exp)

    return mips_to_exps


# Shorthand.
get_model_topics = get_source_topics


def yield_sources(institution_id):
    """Yields set of model sources (optionally filtered by institution).

    """
    for i in get_institutes(institution_id):
        for s in get_institute_sources(i):
            yield i, s


def yield_topics(institution_id):
    """Yields set of model source topics (optionally filtered by institution).

    """
    for i, s in yield_sources(institution_id):
        for t in get_model_topics(s):
            yield i, s, t
