"""
.. module:: generate_cim.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Generates CMIP6 CIM documents from simplified JSON output.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import json

import pyessv

from lib.models.utils import ModelTopicOutput
from lib.utils import vocabs



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Generates CMIP6 model comparator files.")
_ARGS.add_argument(
    "--destination",
    help="Folder to which CIM documents will be copied.",
    default=os.path.join(os.getenv('CMIP6_HOME'), 'repos/libs/esdoc-web-explorer/src/static/cmip6-comparator')
    dest="destination",
    type=str
    )


def _main(args):
    """Main entry point.

    """
    # Initialise nodes / edges.
    institutes = []
    models = []
    topics = []
    specializations = []
    values = []
    edges = []

    # Iterate documented models & extend nodes & edges. 
    for i, m, t, content in _yield_documentation():
        for sp in list(content):
            for v in content[sp]['values']:
                # Extend nodes.
                if i not in institutes:
                    institutes.append(i)
                if m not in models:
                    models.append(m)
                if t not in topics:
                    topics.append(t)
                if sp not in specializations:
                    specializations.append(sp)
                if v not in values:
                    values.append(v)
                
                # Extend edges.
                edges.append((
                    institutes.index(i),
                    models.index(m),
                    topics.index(t),
                    specializations.index(sp),
                    values.index(v),
                ))
    
    # Write to file system.
    _write(args, [
        institutes,
        models,
        topics,
        specializations,
        values,        
    ], edges)


def _yield_documentation():
    """Yields documentation for map/reduce job.
    
    """
    for i, m, t in vocabs.yield_topics(None):
        output = ModelTopicOutput.create(i, m, t)
        if output.content:
            yield i, m, t, output.content


def _write(args, nodes, edges):
    """Writes data to file system.
    
    """
    # Compact nodes.
    _nodes = []
    for idx, i in enumerate(nodes):  
        for jdx, j in enumerate(i):
            _nodes.append((idx, jdx, j.canonical_name if isinstance(j, pyessv.Term) else j))

    # Persist data.
    fpath = "{}/data.json".format(args.destination)

    with open(fpath, 'w') as fstream:
        fstream.write(json.dumps({
        "nodes": _nodes,
        "edges": edges
    }))


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
