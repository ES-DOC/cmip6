"""
.. module:: init_settings.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initializes CMIP6 model settings files.

.. moduleauthor:: Mark A. Conway-Greenslade


"""
import argparse
import collections
import json
import os

import pyessv
from cmip6.utils import vocabs
from cmip6.utils import io_mgr



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model setting files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )

# File name: model publication.
_MODEL_PUBLICATION_FNAME = "model_publication.json"

# File name: model initialization (from_CMIP5).
_MODEL_INITIALIZATION_FNAME = "initialization_from_CMIP5.json"


class ModelSettings(object):
    def __init__(self, institution, fname):
        """Ctor.

        """
        self.directory = io_mgr.get_models_folder(institution)
        self.fname = fname
        self.institution = institution
        self.new = collections.OrderedDict()
        self.previous = None


    def execute(self):
        """Executes settings initialisor.

        """
        self._set_previous()
        self._set_new()
        self._write()


    def _set_previous(self):
        """Assigns previous settings.

        """
        fpath = os.path.join(self.directory, self.fname)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fstream:
                self.previous = json.loads(fstream.read())


    def _set_new(self):
        """Assigns new settings.

        """
        for source in vocabs.get_institute_sources(self.institution):
            settings = collections.OrderedDict()
            for topic in vocabs.get_source_topics(source):
                settings[topic.canonical_name] = self._get_new_setting(source, topic)
            self.new[source.canonical_name] = settings


    def _write(self):
        """Writes settings to file system.

        """
        fpath = os.path.join(self.directory, self.fname)
        with open(fpath, 'w') as fstream:
            fstream.write(json.dumps(self.new, indent=4))


class InitialisationFromCmip5ModelSettings(ModelSettings):
    """Encpasulates initialisation settings drawn from CMIP5.

    """
    def __init__(self, institution):
        """Ctor.

        """
        super(InitialisationFromCmip5ModelSettings, self).__init__(institution, _MODEL_INITIALIZATION_FNAME)


    def _get_new_setting(self, source, realm):
        """Returns a new setting to be written to fs.

        """
        def get_initialized_from():
            try:
                return self.previous[source.canonical_name][realm.canonical_name]['initializedFrom']
            except (TypeError, KeyError) as err:
                return ""

        return {
            "initializedFrom": get_initialized_from()
        }


class ModelPublicationSettings(ModelSettings):
    """Encpasulates model publication settings.

    """
    def __init__(self, institution):
        """Ctor.

        """
        super(ModelPublicationSettings, self).__init__(institution, _MODEL_PUBLICATION_FNAME)


    def _get_new_setting(self, source, realm):
        """Returns a new setting to be written to fs.

        """
        def get_publish_state():
            try:
                return self.previous[source.canonical_name][realm.canonical_name]['publish']
            except (TypeError, KeyError) as err:
                return "off"

        return {
            "publish": get_publish_state()
        }


# Settings writers to be executed.
_WRITERS = [
    InitialisationFromCmip5ModelSettings,
    ModelPublicationSettings
]


def _main(args):
    """Main entry point.

    """
    institutes = vocabs.get_institutes(args.institution_id)
    for institute in institutes:
        for writer in [i(institute) for i in _WRITERS]:
            writer.execute()


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
