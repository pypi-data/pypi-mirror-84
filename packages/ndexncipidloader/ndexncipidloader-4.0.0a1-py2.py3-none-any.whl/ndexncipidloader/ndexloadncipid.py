#! /usr/bin/env python


import os
import argparse
import sys
import time
import logging
from logging import config
import subprocess
import json
import pandas as pd
import requests
import gzip
import re
import xml.etree.ElementTree as ET
from requests.exceptions import HTTPError


from datetime import datetime

from ftpretty import ftpretty
from biothings_client import get_client
import ndexutil.tsv.tsv2nicecx2 as t2n

import networkx as nx
from ndex2.client import Ndex2
import ndex2
from ndexncipidloader.exceptions import NDExNciPidLoaderError
from ndexutil.config import NDExUtilConfig
from ndexutil.cytoscape import Py4CytoscapeWrapper
from ndexutil.cytoscape import DEFAULT_CYREST_API
from ndexutil.ndex import NDExExtraUtils
import ndexncipidloader

logger = logging.getLogger(__name__)

TSV2NICECXMODULE = 'ndexutil.tsv.tsv2nicecx2'

LOG_FORMAT = "%(asctime)-15s %(levelname)s %(relativeCreated)dms " \
             "%(filename)s::%(funcName)s():%(lineno)d %(message)s"

PARTICIPANT_TYPE_MAP = {
    'ProteinReference': 'protein',
    'ProteinReference;RnaReference': 'protein',
    'SmallMoleculeReference': 'smallmolecule'
}

DIRECTED_INTERACTIONS = ["controls-state-change-of",
                         "controls-transport-of",
                         "controls-phosphorylation-of",
                         "controls-expression-of",
                         "catalysis-precedes",
                         "controls-production-of",
                         "controls-transport-of-chemical",
                         "chemical-affects",
                         "used-to-produce"
                         ]

CONTROL_INTERACTIONS = ["controls-state-change-of",
                        "controls-transport-of",
                        "controls-phosphorylation-of",
                        "controls-expression-of"
                        ]

COMMON_CHEMICALS = ["GDP","GTP", "ATP", "ADP", "calcium(2+)"]

DEFAULT_FTP_HOST = 'ftp.ndexbio.org'
DEFAULT_FTP_DIR = 'NCI_PID_BIOPAX_2016-06-08-PC2v8-API'
DEFAULT_FTP_USER = 'anonymous'
DEFAULT_FTP_PASS = 'anonymous'
FTP_SUBDIR = 'ftp'
ICONURL_ATTRIB = '__iconurl'
ICON_URL = 'http://search.ndexbio.org/static/media/ndex-logo.04d7bf44.svg'

PARTICIPANT_NAME = 'PARTICIPANT_NAME'
"""
Participant name node attribute
"""

GENERATED_BY_ATTRIB = 'prov:wasGeneratedBy'
"""
Network attribute to denote what created this network
"""

DERIVED_FROM_ATTRIB = 'prov:wasDerivedFrom'
"""
Network attribute to denote source of network data
"""

NORMALIZATIONVERSION_ATTRIB = '__normalizationversion'

TYPE_ATTRIB = 'networkType'

LOAD_PLAN = 'loadplan.json'
"""
Name of file containing json load plan
stored within this package
"""

NET_ATTRIBS = 'networkattributes.tsv'
"""
Name of file containing network attributes
stored within this package
"""

STYLE = 'style.cx'
"""
Name of file containing CX with style
stored within this package
"""

GENE_SYMBOL_MAPPING = 'gene_symbol_mapping.json'
"""
Name of file containing json of gene to symbol mapping
stored within this package
"""

COMPLETE_INTERACTION_NAME = 'NCI PID - Complete Interactions'


def get_package_dir():
    """
    Gets directory where package is installed
    :return:
    """
    return os.path.dirname(ndexncipidloader.__file__)


def get_load_plan():
    """
    Gets the load plan stored with this package

    :return: path to file
    :rtype: string
    """
    return os.path.join(get_package_dir(), LOAD_PLAN)


def get_networkattributes():
    """
    Gets the network attributes stored with this package

    :return: path to file
    :rtype: string
    """
    return os.path.join(get_package_dir(), NET_ATTRIBS)


def get_style():
    """
    Gets the style stored with this package

    :return: path to file
    :rtype: string
    """
    return os.path.join(get_package_dir(), STYLE)


def get_gene_symbol_mapping():
    """
    Gets the gene symbol mapping with this package

    :return: path to file
    :rtype: string
    """
    return os.path.join(get_package_dir(), GENE_SYMBOL_MAPPING)


class Formatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass


def _parse_arguments(desc, args):
    """
    Parses command line arguments
    :param desc:
    :param args:
    :return:
    """
    help_fm = Formatter
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=help_fm)
    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' +
                                 ndexncipidloader.__version__))
    parser.add_argument('--profile', help='Profile in configuration '
                                          'file to use to load '
                                          'NDEx credentials which means'
                                          'configuration under [XXX] will be'
                                          'used',
                        default='ndexncipidloader')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'format consumable by fileConfig. See '
                             'https://docs.python.org/3/library/logging.html '
                             'for more information. '
                             'Setting this overrides -v|--verbose parameter '
                             'which uses default logger.')

    parser.add_argument('--conf', help='Configuration file to load '
                                       '(default ~/' +
                                       NDExUtilConfig.CONFIG_FILE + ')')
    parser.add_argument('--genesymbol',
                        help='Use alternate gene symbol mapping file',
                        default=get_gene_symbol_mapping())
    parser.add_argument('--loadplan', help='Use alternate load plan file',
                        default=get_load_plan())
    parser.add_argument('--iconurl',
                        help='Sets network attribute value __iconurl ',
                        default=ICON_URL)
    parser.add_argument('--networkattrib',
                        help='Use alternate Tab delimited file containing '
                             'PID Pathway Name, reviewed by, '
                             'curated by and revision data '
                             'for ncipid networks',
                        default=get_networkattributes())
    parser.add_argument('--visibility', default='PUBLIC',
                        choices=['PUBLIC', 'PRIVATE'],
                        help='Sets visibility of new '
                             'networks')
    parser.add_argument('--indexlevel', default='all',
                        choices=['none', 'meta', 'all'],
                        help='Sets how new networks are indexed')
    parser.add_argument('--disableshowcase', default=False, action='store_true',
                        help='If set, new networks are NOT showcased')
    parser.add_argument('--style',
                        help='Path to NDEx CX file to use for styling '
                             'networks',
                        default=get_style())
    rel_ver = datetime.now().strftime('%b-%Y').upper()
    parser.add_argument('--releaseversion',
                        help='Sets version network attribute',
                        default=rel_ver)
    parser.add_argument('--singlefile',
                        help='Only process file matching name in '
                             '<sifdir>', default=None)
    parser.add_argument('--paxtools', default='paxtools.jar',
                        help='Full path paxtools.jar file used to convert'
                             'owl file to sif file. Ignored if '
                             '--skipdownload flag is set. The default '
                             'assumes paxtools.jar '
                             'is in current working directory')
    parser.add_argument('--skipdownload', action='store_true',
                        help='If set, skips download of owl files '
                             'and conversion. The program assumes '
                             'the <sifdir> directory set as '
                             'the last argument on the command line '
                             'to this program contains sif files')
    parser.add_argument('--skipchecker', action='store_true',
                        help='If set, skips gene symbol checker that '
                             'examines all nodes of type protein '
                             'and verifies they are symbols')
    parser.add_argument('--getfamilies', action='store_true',
                        help='If set, code examines owl files and generates '
                             'mapping of protein families')
    parser.add_argument('--ftphost',
                        help='FTP host to download owl or sif files from. '
                             'Ignored if --skipdownload flag set ',
                        default=DEFAULT_FTP_HOST)
    parser.add_argument('--ftpdir',
                        help='FTP directory to download owl or sif files '
                             'from. Ignored if --skipdownload flag set ',
                        default=DEFAULT_FTP_DIR)
    parser.add_argument('sifdir',
                        help='Directory containing .sif files to parse. '
                             'Under this directory OWL files '
                             'will be downloaded and '
                             'converted to sif unless --skipdownload '
                             'flag is set, in which case this '
                             'script assumes the '
                             '*.sif files already exist')
    parser.add_argument('--layout', default='-',
                        help='Specifies layout '
                             'algorithm to run. If Cytoscape is running '
                             'and py4cytoscape is loaded any layout from '
                             'Cytoscape can be used. If "-" is passed in '
                             'force-directed-cl from Cytoscape will '
                             'be used. If no Cytoscape is available, '
                             '"spring" from networkx is supported')
    parser.add_argument('--cyresturl',
                        default=DEFAULT_CYREST_API,
                        help='URL of CyREST API. Default value '
                             'is default for locally running Cytoscape')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module and '
                             'in ' + TSV2NICECXMODULE + '. Messages are '
                                                        'output at these python logging levels '
                                                        '-v = ERROR, -vv = WARNING, -vvv = INFO, '
                                                        '-vvvv = DEBUG, -vvvvv = NOTSET (default is to '
                                                        'log CRITICAL)')
    return parser.parse_args(args)


def _setup_logging(args):
    """
    Sets up logging based on parsed command line arguments.
    If args.logconf is set use that configuration otherwise look
    at args.verbose and set logging for this module and the one
    in ndexutil specified by TSV2NICECXMODULE constant
    :param args: parsed command line arguments from argparse
    :raises AttributeError: If args is None or args.logconf is None
    :return: None
    """

    if args.logconf is None:
        level = (50 - (10 * args.verbose))
        logging.basicConfig(format=LOG_FORMAT,
                            level=level)
        logging.getLogger(TSV2NICECXMODULE).setLevel(level)
        logger.setLevel(level)
        return

    # logconf was set use that file
    logging.config.fileConfig(args.logconf,
                              disable_existing_loggers=False)


class GeneFamilyFromOwlExtractor(object):
    """
    Extracts genes for gene families from owl files
    """
    def __init__(self,
                 bclient=get_client('gene')):
        """
        Constructor
        """
        self._ns = { 'bp': 'http://www.biopax.org/release/biopax-level3.owl#',
                     'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                     'owl': 'http://www.w3.org/2002/07/owl#',
                     'base': 'http://pathwaycommons.org/pc2/'}
        self._bclient = bclient

    def _get_members_of_protein(self, proteinref):
        """
        Gets the memberPhysicalEntity elements from `proteinref` element
        passed in
        :param proteinref: element tree element of a protein family
        :return: list of ids of proteins as strings
        :rtype: list
        """
        res = []
        for memphys in proteinref.findall('bp:memberPhysicalEntity', self._ns):
            res.append(memphys.attrib['{' + self._ns['rdf'] + '}resource'].replace('#', '', 1))
        return res

    def _get_uniprot_url_for_protein(self, root, protein_id):
        """
        Gets uniprot url from entityReference element in a Protein element matching
        'protein_id' passed in
        :param root: root of xml document
        :type root: :py:class:`xml.etree.ElementTree.Element`
        :param protein_id: id of protein
        :type protein_id: string
        :return: list of protein ids
        :rtype: list
        """
        res = []
        for eref in root.findall(".//bp:Protein[@rdf:ID='" + protein_id + "']/bp:entityReference", self._ns):
            res.append(eref.attrib['{' + self._ns['rdf'] + '}resource'])
        return res

    def _replace_uniprot_with_gene_symbols(self, uniproturls):
        """

        :param uniproturls: list of uniprot urls
        :type uniproturls: list
        :return: list of gene symbols
        :rtype: string
        """
        newlist = []
        for entry in uniproturls:
            idonly = re.sub('^.*\/', '', entry)
            result = self._bclient.query(idonly, fields='symbol')
            if result is None:
                logger.error('result is None when querying: ' + idonly)
                continue
            newlist.append(result['hits'][0]['symbol'])
        newlist.sort()
        return newlist

    def extract_gene_family_mapping(self, xmlstream):
        """
        Reads 'xmlstream' and extracts all gene families by looking for
        proteins with ' family' in name.
        :param xmlstream: xml file
        :param xmlstream: filename or file object
        :return: dictionary where key is family name and value is list of gene symbols
        :rtype: dict
        """
        tree = ET.parse(xmlstream)
        root = tree.getroot()
        gene_map = {}
        for proteinref in root.findall('bp:Protein', self._ns):
            found_family = False
            for dispName in proteinref.findall('bp:displayName', self._ns):
                if ' family' in dispName.text:
                    found_family = True
            if found_family is True:
                if dispName.text in gene_map:
                    continue
                uniproturls = []
                for pid in self._get_members_of_protein(proteinref):
                    uniproturls.extend(self._get_uniprot_url_for_protein(root, pid))
                gene_map[dispName.text] = self._replace_uniprot_with_gene_symbols(uniproturls)
        return gene_map

    def get_gene_family_mapping_as_string(self, owldir):
        """
        Given a directory 'owldir' load every .owl file which is
        an xml document and extract genes in protein families
        (protein families have family in name)

        :param owldir: directory with .owl files
        :type owldir: string
        :return: string in format below for each protein family:
                 "<protein family": "<comma delimited list of genes",
        :rtype: string
        """
        finalstr = ''
        family_dict = {}
        for entry in os.listdir(owldir):
            if not entry.endswith('.owl'):
                continue
            fp = os.path.join(owldir, entry)
            res = self.extract_gene_family_mapping(fp)
            for dent in res.keys():
                if dent in family_dict:
                    if family_dict[dent] != res[dent]:
                        logger.error('Family gene lists differ: ' +
                                     str(family_dict[dent]) + ' != ' +
                                     str(res[dent]))
                    continue
                family_dict[dent] = res[dent]
        if len(family_dict) > 0:
            family_list = list(family_dict.keys())
            family_list.sort()
            for e in family_list:
                finalstr += '"' + e + '": "' + ','.join(family_dict[e]) +\
                            '",\n'
        return finalstr


class GeneSymbolSearcher(object):
    """
    Wrapper around :py:mod:`biothings_client` to query
    """

    def __init__(self,
                 bclient=get_client('gene')):
        """
        Constructor
        """
        self._cache = {}
        self._bclient = bclient

    def _query_mygene(self, val):
        """
        Queries biothings_client with 'val' to find
        hit

        :param val: id to send to :py:mod:`biothings_client`
        :type val: string
        :return: gene symbol or None
        :rtype: string
        """
        try:
            res = self._bclient.query(val)
            if res is None:
                logger.debug('Got None back from query for: ' + val)
                return ''
            logger.debug('Result from query for ' + val + ' ' + str(res))
            if res['total'] == 0:
                logger.debug('Got No hits back from query for: ' + val)
                return ''
            if len(res['hits']) > 0:
                logger.debug('Got a hit from query for: ' + val)
                sym_name = res['hits'][0].get('symbol')
                if sym_name is None:
                    logger.debug('Symbol name was None for ' + val)
                    return ''
                return sym_name.upper()
        except HTTPError as he:
            logger.error('Caught exception running query for: ' + val)

        return None

    def _query_uniprot(self, val):
        """

        :param val:
        :return:
        """
        res = requests.get('https://www.uniprot.org/uniprot/' +
                           val.upper() + '.txt')
        for entry in res.text.split('\n'):
            if entry.startswith('GN'):
                if 'Name' in entry:
                    return re.sub(';.*', '',
                                  re.sub(' .*', '',
                                         re.sub('^GN.*Name=',
                                                '', entry)))
        return None

    def get_symbol(self, val):
        """
        Queries biothings_client with 'val' to find
        hit

        :param val: id to send to :py:mod:`biothings_client`
        :type val: string
        :return: gene symbol or None
        :rtype: string
        """
        if val is None:
            logger.error('None passed in')
            return None

        cache_symbol = self._cache.get(val)
        if cache_symbol is not None:
            if cache_symbol == '':
                return None
            return cache_symbol

        sym_name = self._query_mygene(val)
        if sym_name is None or sym_name == '':
            res = self._query_uniprot(val)
            if res is not None:
                self._cache[val] = res
                return res
            sym_name = ''
        self._cache[val] = sym_name
        return sym_name


class NetworkAttributesFromTSVFactory(object):
    """
    Factory to create NetworkAttributes object
    from TSV file using Pandas
    """

    def __init__(self, tsvfile, delim='\t',
                 pid_key='PID',
                 name_key='Pathway Name',
                 cname_key='Corrected Pathway Name',
                 reviewed_key='Reviewed By',
                 curated_key='Curated By'):
        self._tsvfile = tsvfile
        self._delim = delim
        self._pid_key = pid_key
        self._reviewed_key = reviewed_key
        self._curated_key = curated_key
        self._name_key = name_key
        self._cname_key = cname_key

    def get_network_attributes_obj(self):
        if self._tsvfile is None:
            logger.error('TSV file is None')
            return None

        df = pd.read_csv(self._tsvfile, sep=self._delim)
        net_attr = NetworkAttributes()
        for id, row in enumerate(df[self._name_key]):
            net_attr.add_author_entry(str(row),
                                      str(df[self._curated_key][id]))
            net_attr.add_reviewers_entry(str(row),
                                         str(df[self._reviewed_key][id]))
            net_attr.add_labels_entry(str(row),
                                      str(df[self._pid_key][id]))

            # some network names only match in the corrected pathway column
            if df[self._cname_key][id] is not None:
                cnameval = str(df[self._cname_key][id])
                if cnameval != '' and cnameval != 'nan':
                    net_attr.add_author_entry(cnameval,
                                              str(df[self._curated_key][id]))
                    net_attr.add_reviewers_entry(cnameval,
                                                 str(df[self._reviewed_key][id]))
                    net_attr.add_labels_entry(cnameval,
                                              str(df[self._pid_key][id]))

        return net_attr


class NetworkAttributes(object):
    """
    Contains database of additional network attributes
    for NCI-PID networks
    """
    LABELS = 'labels'
    AUTHOR = 'author'
    REVIEWERS = 'reviewers'

    def __init__(self):
        """
        Constructor
        """
        self._db = {}

    def add_labels_entry(self, name, val):
        """
        Add label 'val' to network 'name'
        :param name:
        :param val:
        :return:
        """
        if name not in self._db:
            self._db[name] = {}
        self._db[name][NetworkAttributes.LABELS] = val

    def add_author_entry(self, name, val):
        """
        Add author 'val' to network 'name'
        :param name:
        :param val:
        :return:
        """
        if name not in self._db:
            self._db[name] = {}
        self._db[name][NetworkAttributes.AUTHOR] = val

    def add_reviewers_entry(self, name, val):
        """
        Add reviewer 'val' to network 'name'
        :param name:
        :param val:
        :return:
        """
        if name not in self._db:
            self._db[name] = {}
        self._db[name][NetworkAttributes.REVIEWERS] = val

    def get_labels(self, name):
        """
        Get labels with network name
        :param name:
        :return:
        """
        if name not in self._db:
            return None
        return self._db[name].get(NetworkAttributes.LABELS)

    def get_author(self, name):
        """
        Gets author with network name
        :param name:
        :return:
        """
        if name not in self._db:
            return None
        return self._db[name].get(NetworkAttributes.AUTHOR)

    def get_reviewers(self, name):
        """
        Gets reviewers with network name
        :param name:
        :return:
        """
        if name not in self._db:
            return None
        return self._db[name].get(NetworkAttributes.REVIEWERS)


class NetworkIssueReport(object):
    """
    Holds summary information about issues found during network
    creation
    """
    def __init__(self, network_name):
        """
        Constructor
        """
        self._networkname = network_name
        self._issuemap = {}
        self._nodetype = set()

    def add_nodetype(self, nodetype):
        """
        Adds `nodetype` to set of node types
        :param nodetype: value of type node attribute
        :type nodetype: string
        :return:
        """
        if nodetype is None:
            return
        self._nodetype.add(nodetype)

    def get_nodetypes(self):
        """
        Gets node types
        :return: set of node types
        :rtype: set
        """
        return self._nodetype

    def addissues(self, description, issue_list):
        """

        :param description: description of issue
        :type description: string
        :param issue_list:
        :type issue_list: list
        :return: None
        """
        if issue_list is None:
            return
        if len(issue_list) is 0:
            return
        if description is None:
            return
        self._issuemap[description] = issue_list

    def get_fullreport_as_string(self):
        """
        Gets report as string

        :return:
        """
        res = ''
        for key in self._issuemap.keys():
            num_issues = len(self._issuemap[key])
            if num_issues == 1:
                issue_word = 'issue'
            else:
                issue_word = 'issues'
            res += '\t' + str(num_issues) + ' ' + issue_word + ' -- ' +\
                   key + '\n'
            for entry in self._issuemap[key]:
                res += '\t\t' + entry + '\n'
        if len(res) is 0:
            return ''

        return str(self._networkname) + '\n' + res


class NetworkUpdator(object):
    """
    Base class for classes that update
    a network
    """
    def __init__(self):
        """
        Constructor
        """
        pass

    def get_description(self):
        """
        Subclasses should implement
        :return:
        """
        raise NotImplementedError('subclasses should implement')

    def update(self, network):
        """
        subclasses should implement
        :param network:
        :return:
        """
        raise NotImplementedError('subclasses should implement')


class UniProtToGeneSymbolUpdater(NetworkUpdator):
    """
    Replaces node names with gene symbols.
    For more information see :py:func:`~update`
    """

    def __init__(self,
                 searcher=GeneSymbolSearcher()):
        """
        Constructor

        :param searcher: gene symbol searcher object used by
                         :py:func:`~update` method.
        :type searcher: :py:class:`GeneSymbolSearcher`
        """
        self._searcher = searcher

    def get_description(self):
        """

        :return:
        """
        return 'Replacement of uniprot value in node name with gene symbol'

    def update(self, network):
        """
        Given a network with nodes, instances of this
        class query the node name and see if that
        name is in the represents field of that
        node with a uniprot: prefix. If it is, this
        object then queries `searcher` passed in via constructor for a
        gene symbol. This gene symbol is then set as the node name.
        If no symbol is found then original name is left.

        :param network: network to examine
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of node names for which no replacement was found
        :rtype: list
        """
        if network is None:
            return None

        counter = 0
        issues = []
        for nodeid, node in network.get_nodes():
            name = node.get('n')
            represents = node.get('r')
            logger.debug('represents is: ' + str(represents))
            if represents is None:
                issues.append('For node with id (' + str(nodeid) +
                              ') and name (' +
                              name + ') no represents value found')
                continue
            if 'uniprot:' + name.lower() in represents.lower():
                # uniprot id is the node name
                # use the lookup tool to try to
                # find a gene symbol that can be used
                symbol = self._searcher.get_symbol(name)
                if symbol is not None and symbol != '':
                    logger.info('On network: ' + str(network.get_name()) +
                                 ' Replacing: ' + node['n'] +
                                 ' with ' + symbol)
                    node['n'] = symbol
                    counter = counter + 1
                else:
                    issues.append('For node with id (' + str(nodeid) +
                                  ') No symbol found to replace node name (' +
                                  name + ') and represents (' +
                                  represents + ')')
                    logger.info('On network: ' + str(network.get_name()) +
                                   ' No replacement found for ' + name)
        if counter > 0:
            logger.debug('On network: ' + str(network.get_name()) +
                         ' updated ' + str(counter) +
                         ' node names with symbol')

        return issues


class DirectedEdgeSetter(NetworkUpdator):
    """
    Iterates through edges setting an edge
    type :py:const:`DirectedEdgeSetter.DIRECTED_ATTRIB` to
    True or False as described
    below in :py:func:`update_edge_direction`
    """
    DIRECTED_ATTRIB = 'directed'

    def __init__(self):
        """
        Constructor
        """
        super(DirectedEdgeSetter, self).__init__()

    def get_description(self):
        """
        Sets :py:const:`DirectedEdgeSetter.DIRECTED_ATTRIB` edge attribute

        :return:
        """
        return 'Sets ' + DirectedEdgeSetter.DIRECTED_ATTRIB +\
               ' edge attribute'

    def update(self, network):
        """
        Examine all edges in network and updates
        :py:const:`DirectedEdgeSetter.DIRECTED_ATTRIB`
        to True if existing value is 't' otherwise False

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of strings with any issues found
        :rtype: list
        """
        if network is None:
            return ['Network is None']

        for k, v in network.get_edges():
            if v['i'] in DIRECTED_INTERACTIONS:
                network.set_edge_attribute(k,
                                           DirectedEdgeSetter.DIRECTED_ATTRIB,
                                           True, type='boolean')
            else:
                network.set_edge_attribute(k,
                                           DirectedEdgeSetter.DIRECTED_ATTRIB,
                                           False, type='boolean')
        return []


class EmptyCitationAttributeUpdator(NetworkUpdator):
    """
    Iterates through all edges removing the citation
    edge attribute removing any citations that are
    just pubmed:
    """

    CITATION = 'citation'

    def __init__(self):
        """
        Constructor
        """
        super(EmptyCitationAttributeUpdator, self).__init__()

    def get_description(self):
        """
        Gets description
        :return: description as string
        :rtype: string
        """
        return 'Removes empty and pubmed: only entries in citation ' \
               ' edge types'

    def update(self, network):
        """
        Iterates through all edges in network and examines
        'citation' edge attribute. Any entries with
        with only 'pubmed:' are removed

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCxNetwork`
        :return: list of issues as strings found
        :rtype: list
        """
        if network is None:
            return ['Network is None']
        citation = EmptyCitationAttributeUpdator.CITATION
        for k, v in network.get_edges():
            edge_attr = network.get_edge_attribute(k,
                                                   citation)
            if edge_attr == (None, None):
                network.set_edge_attribute(k, citation, values=[],
                                           type='list_of_string')
                continue

            new_list = []
            for entry in edge_attr['v']:
                if entry == '' or entry.strip() == 'pubmed:':
                    continue
                new_list.append(entry)

            network.remove_edge_attribute(k, citation)
            network.set_edge_attribute(k, citation, values=new_list,
                                       type='list_of_string')
        return []


class RedundantEdgeAdjudicator(NetworkUpdator):
    """
    Examines network and removes redundant edges as
    described in :py:func:`~RedundantEdgeAdjudicator.update`
    """
    CITATION = 'citation'
    _edge_map = {}

    def __init__(self):
        """
        Constructor

        """
        super(RedundantEdgeAdjudicator, self).__init__()

    def get_description(self):
        """

        :return:
        """
        return 'Removes redundant edges'

    def _remove_edge(self, network, edgeid):
        """
        Removes edge and its attributes

        :param network: network with edge
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :param edgeid:
        :type edgeid: int
        :return: None
        """
        network.remove_edge(edgeid)

        # remove edge attributes for deleted edge
        net_attrs = network.get_edge_attributes(edgeid)
        if net_attrs is None:
            return
        for net_attr in net_attrs:
            network.remove_edge_attribute(edgeid, net_attr['n'])

    def _remove_node(self, network, nodeid):
        """
        Removes node and its attributes.
        This implementation currently digs into
        internals of :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        which is bad if that ever ends up
        changing.

        :param network: network with nodes
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :param nodeid:
        :type nodeid: int
        :return: None
        """
        network.remove_node(nodeid)
        network.nodeAttributes.pop(nodeid)

    def _remove_node_edges(self, network, node_id):
        edges_to_remove = set()

        for edge_id, edge in network.get_edges():
            source_nodeid = edge["s"]
            if source_nodeid == node_id:
                edges_to_remove.add(edge_id)
                break
            target_node_id = edge["t"]
            if target_node_id == node_id:
                edges_to_remove.add(edge_id)

        for edge_id in edges_to_remove:
            self._remove_edge(network, edge_id)

    def _make_key(self, node_id1, node_id2):
        """
        Concatenates 'node_id1' and 'node_id2' strings
        together putting a _ between.

        :param node_id1:
        :param node_id2:
        :return: <node_id1>_<node_id2>
        :rtype: str
        """
        return ("%s_%s" % (node_id1, node_id2))

    def _make_new_edge_map(self, network):
        """
        Iterates through all edges in 'network' and
        builds up a dict of following structure:

        {'edgesourceid_edgetargetid': <edge object ie CX dict {}>}

        This method then replaces the internal object
        self._edge_map with this dict.

        :param network: Network to get edges from
        :type: network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: None
        """
        edge_map={}
        for edge_id, edge_object in network.get_edges():
            source_nodeid = edge_object['s']
            target_nodeid = edge_object['t']
            edge_map_key = self._make_key(source_nodeid, target_nodeid)
            if not edge_map_key in edge_map:
                edge_map[edge_map_key] = [edge_object]
            else:
                list_of_edges = edge_map[edge_map_key]
                list_of_edges.append(edge_object)
        self._edge_map = edge_map

    def _get_edges_between_two_nodes(self, node_id1, node_id2):
        return self._edge_map.get(self._make_key(node_id1, node_id2))

    def _subsumes(self, edge1, edge2, higher_priority_edges=CONTROL_INTERACTIONS):
        """
        If 'edge1' is in 'higher_priority_edges' list and 'edge2' interaction type
        defined by edge2['i'] is 'controls-state-change-of this method
        returns True otherwise False
        :param edge1: edge dict in CX format {'@id': #, 'i': 'neigh', 's': #, 't': #}
        :type edge1: dict
        :param edge2: edge dict in CX format {'@id': #, 'i': 'neigh', 's': #, 't': #}
        :type edge2: dict
        :param higher_priority_edges: list of edge interactions as string
        :type higher_priority_edges: list
        :return: True if edge1 can "subsume" edge2 otherwise False
        :type bool
        """
        if edge1['i'] in higher_priority_edges and edge2['i'] == "controls-state-change-of":
            return True
        return False

    def _remove_redundant_from_pair(self, network, edges):
        for current_edge in edges:
            current_edge_id = current_edge['@id']
            for comparison_edge in edges:
                comparison_edge_id = comparison_edge['@id']
                if comparison_edge_id != current_edge_id:
                    if self._subsumes(current_edge, comparison_edge):
                        self._remove_edge(network, comparison_edge_id)

    def _remove_if_redundant(self, network):
        self._make_new_edge_map(network)
        edge_count = len(network.edges)
        for node_pair_edges in self._edge_map.values():
            self._remove_redundant_from_pair(network, node_pair_edges)
        number_removed = edge_count - len(network.edges)
        logger.debug('removed ' + str(number_removed) +
                     ' subsumed edges out of ' + str(edge_count))

    def _remove_all_neighbor_of(self, network):
        """
        Iterates through 'neighbor_of_map' and
        deletes the attributes and edges permanently

        :param network: Network to update
        :type network: :py:class:`ndex2.nice_cx_network.NiceCXNetwork`
        :return:
        """
        edge_count = len(network.edges)
        edges_to_remove = set()

        for edge_id, edge in network.get_edges():
            if edge['i'] == 'neighbor-of':
                edges_to_remove.add(edge_id)

        for edge_id in edges_to_remove:
            self._remove_edge(network, edge_id)
        number_removed = edge_count - len(network.edges)
        logger.debug('removed ' + str(number_removed) + ' neighbor-of edges out of ' +
                     str(edge_count))

    def _remove_orphan_nodes(self, network):
        """
        Iterates through every node and deletes the attributes and the nodes PERMANENTLY
        param network
        """
        node_ids_to_remove = set()
        node_ids_with_edges = set()

        for k, v in network.get_edges():
            s = v['s']
            t = v['t']
            node_ids_with_edges.add(s)
            node_ids_with_edges.add(t)

        pre_node_count = len(network.nodes)
        pre_node_attribute_count = len(network.nodeAttributes)
        for node_id, node in network.get_nodes():
            if node_id not in node_ids_with_edges:
                node_ids_to_remove.add(node_id)

        for node_id in node_ids_to_remove:
            self._remove_node(network, node_id)

        post_node_count = len(network.nodes)
        post_node_attribute_count = len(network.nodeAttributes)
        logger.debug('removed ' + str(len(node_ids_to_remove)) +
                     ' orphaned nodes: ' + str(pre_node_count) +
                     '  -> ' + str(post_node_count) + ', attributes ' +
                     str(pre_node_attribute_count) + ' -> ' +
                     str(post_node_attribute_count))

    def update(self, network):
        """

        :param network:
        :return:
        """
        issues = []
        if network is None:
            return ['Network passed in is None']

        self._remove_all_neighbor_of(network)
        self._remove_if_redundant(network)
        self._remove_orphan_nodes(network)
        return issues


class CHEBINodeNameReplacer(NetworkUpdator):
    """
    If node name starts with CHEBI (then replace that name
    with value in :py:const:`PARTICIPANT_NAME` node attribute
    """
    def __init__(self):
        """
        Constructor
        """
        super(CHEBINodeNameReplacer, self).__init__()

    def get_description(self):
        """
        Gets description
        :return:
        """
        return 'Replaces node names that start with CHEBI with value in ' + PARTICIPANT_NAME

    def update(self, network):
        """
        If node name starts with CHEBI (anthen replace that name
        with value in :py:const:`PARTICIPANT_NAME` node attribute

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of issues as strings encountered
        :rtype: list
        """
        issues = []
        for nodeid, node in network.get_nodes():
            if not node['n'].startswith('CHEBI'):
                continue
            node_attr = network.get_node_attribute(nodeid, PARTICIPANT_NAME)
            if node_attr is None or node_attr == (None, None):
                issues.append('Node: ' + str(node) +
                              ' starts with CHEBI but ' + PARTICIPANT_NAME +
                              ' node attribute does not exist')
                continue
            node['n'] = node_attr['v']
        return issues


class CHEBINodeRepresentsPrefixRemover(NetworkUpdator):
    """
    If node represents starts with chebi:CHEBI then remove
    the chebi:
    """
    def __init__(self):
        """
        Constructor
        """
        super(CHEBINodeRepresentsPrefixRemover, self).__init__()

    def get_description(self):
        """
        Gets description
        :return:
        """
        return 'Removes chebi: from node represents fields that ' \
               'start with chebi:CHEBI'

    def update(self, network):
        """
        If node name starts with CHEBI (anthen replace that name
        with value in :py:const:`PARTICIPANT_NAME` node attribute

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of issues as strings encountered
        :rtype: list
        """
        issues = []
        for nodeid, node in network.get_nodes():
            if not node['r'].startswith('chebi:CHEBI'):
                continue
            node['r'] = node['r'].replace('chebi:', '', 1)
        return issues


class GeneSymbolNodeNameUpdator(NetworkUpdator):
    """
    For protein nodes updates gene symbol from data
    in gene symbol lookup dictionary
    """
    def __init__(self, genesymbol):
        """
        Constructor
        """
        super(GeneSymbolNodeNameUpdator, self).__init__()
        self._gene_symbol_map = None
        self._load_gene_symbol_map(genesymbol)

    def _load_gene_symbol_map(self, genesymbol):
        """
        Loads gene symbol map from command line flag --genesymbol
        :return:
        """
        if not os.path.isfile(genesymbol):
            raise NDExNciPidLoaderError('Gene symbol mapping file ' +
                                        str(genesymbol) +
                                        ' does not exist')

        with open(genesymbol, 'r') as f:
            self._gene_symbol_map = json.load(f)

    def get_description(self):
        """
        Gets description
        :return:
        """
        return 'Replaces gene symbol with another symbol from lookup table'

    def update(self, network):
        """
        Iterates through all nodes in network that are
        proteins and updates node names with gene symbol
        in mapping table.

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of issues as strings encountered
        :rtype: list
        """
        issues = []
        for nodeid, node in network.get_nodes():
            node_attr = network.get_node_attribute(nodeid, PARTICIPANT_NAME)
            if node_attr is None or node_attr == (None, None):
                continue
            p_name = node_attr['v']

            if p_name is not None and '_HUMAN' not in p_name:
                continue
            gene_symbol_mapped_name = self._gene_symbol_map.get(p_name)
            if gene_symbol_mapped_name is None:
                continue
            clean_symbol = self._gene_symbol_map.get(p_name)
            if len(clean_symbol) == 0 or clean_symbol == '-':
                issues.append('Mapping came back with "-"  Going with '
                              'old name => ' + node['n'])
            else:
                if node['n'] != clean_symbol:
                    logger.debug('Updating node from name: ' +
                                 node['n'] + ' to ' + clean_symbol)
                    node['n'] = clean_symbol
        return issues


class GeneSymbolChecker(NetworkUpdator):
    """
    For protein nodes updates gene symbol from data
    in gene symbol lookup dictionary
    """
    def __init__(self, searcher=GeneSymbolSearcher()):
        """
        Constructor
        """
        super(GeneSymbolChecker, self).__init__()
        self._searcher = searcher

    def get_description(self):
        """
        Gets description
        :return:
        """
        return 'Checks all gene symbols to make sure they are really symbols'

    def update(self, network):
        """
        Iterates through all nodes in network that are
        proteins and updates node names with gene symbol
        in mapping table.

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of issues as strings encountered
        :rtype: list
        """
        issues = []
        for nodeid, node in network.get_nodes():
            node_attr = network.get_node_attribute(nodeid, 'type')
            if node_attr is None or node_attr == (None, None):
                issues.append('No type attribute found for node: ' + str(node))
                continue
            if node_attr['v'] != 'protein':
                continue

            res = self._searcher.get_symbol(node['n'])
            if res is None or res == '':
                issues.append(str(node['n']) + ' does not come back as gene symbol')
            elif res != node['n']:
                issues.append(str(node['n']) + ' differs from symbol ' + res)
        return issues


class NodeTypeUpdator(NetworkUpdator):
    """
    Update node types using values in this map
    :py:const:`PARTICIPANT_TYPE_MAP`

    """
    def __init__(self):
        """
        Constructor
        """
        super(NodeTypeUpdator, self).__init__()

    def get_description(self):
        """
        Gets description
        :return:
        """
        return 'Updates node names via lookup table'

    def update(self, network):
        """
        Iterates through all nodes in network and updates
        'type' node attribute value by replacing existing
        type with values found in :py:const:`PARTICIPANT_TYPE_MAP`

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of issues as strings encountered
        :rtype: list
        """
        issues = []
        for nodeid, node in network.get_nodes():
            node_type = network.get_node_attribute(nodeid, 'type')
            typeval = PARTICIPANT_TYPE_MAP.get(node_type['v'])
            if typeval is None:
                issues.append('For node (' + str(node['@id']) +
                              ') with name (' + node['n'] +
                              ') and represents (' +
                              node['r'] +
                              ') no valid mapping for type (' +
                              node_type['v'] +
                              ') found')
            else:
                network.set_node_attribute(nodeid, 'type', typeval,
                                           overwrite=True)
        return issues


class NodeAliasUpdator(NetworkUpdator):
    """
    Update node alias attribute
    """
    def __init__(self):
        """
        Constructor
        """
        super(NodeAliasUpdator, self).__init__()

    def get_description(self):
        """
        Gets description
        :return:
        """
        return 'Updates node alias attribute'

    def update(self, network):
        """
        Iterates through all nodes in network and sets the
        represents field in node to the first element in
        'alias' node attribute. That element is then removed
        from the 'alias' attribute. If the 'alias' attribute
        is empty it is removed. If there isn't an 'alias' attribute
        or its empty then the node represents is set to the node name

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of issues as strings encountered
        :rtype: list
        """
        issues = []
        for k, v in network.get_nodes():
            # =============================
            # SET REPRESENTS
            # =============================
            aliases = network.get_node_attribute(v, 'alias')
            if aliases is not None and len(aliases['v']) > 0:
                logger.debug('Aliases is: ' + str(aliases))
                v['r'] = (aliases['v'][0])
                if len(aliases['v']) > 1:
                    network.set_node_attribute(k, 'alias', aliases['v'][1:], type=aliases['d'],
                                               overwrite=True)
                else:
                    network.remove_node_attribute(k, 'alias')
            else:
                v['r'] = v['n']
        return issues


class GeneFamilyExpander(NetworkUpdator):
    """
    Expands gene families by updating
    type to proteinfamily and setting gene symbols
    in member node attribute
    """
    def __init__(self, genesymbol):
        """
        Constructor
        """
        super(GeneFamilyExpander, self).__init__()
        self._gene_symbol_map = None
        self._load_gene_symbol_map(genesymbol)

    def _load_gene_symbol_map(self, genesymbol):
        """
        Loads gene symbol map from command line flag --genesymbol
        :return:
        """
        if not os.path.isfile(genesymbol):
            raise NDExNciPidLoaderError('Gene symbol mapping file ' +
                                        str(genesymbol) +
                                        ' does not exist')

        with open(genesymbol, 'r') as f:
            self._gene_symbol_map = json.load(f)

    def get_description(self):
        """
        Gets description
        :return:
        """
        return 'Expands any nodes of type protein with family in name' \
               ' to their proper gene families'

    def update(self, network):
        """
        Iterates through all nodes in network that are
        proteins and updates node names with gene symbol
        in mapping table.

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of issues as strings encountered
        :rtype: list
        """
        issues = []
        for nodeid, node in network.get_nodes():
            if 'family' not in node['n']:
                continue
            genelist = self._gene_symbol_map.get(node['n'])
            if genelist is None:
                issues.append('No gene list for family ' + str(node['n']))
                continue
            memberlist = []
            if len(genelist) is 0:
                issues.append('Gene list for family is empty ' + str(node['n']))
                continue
            for entry in genelist.split(','):
                memberlist.append('hgnc.symbol:' + entry)
            network.set_node_attribute(nodeid, 'member', memberlist, type='list_of_string',
                                       overwrite=True)
            network.set_node_attribute(nodeid, 'type', 'proteinfamily', type='string',
                                       overwrite=True)
        return issues


class NodeAttributeRemover(NetworkUpdator):
    """
    Update node alias attribute
    """
    def __init__(self, attribute_name):
        """
        Constructor
        """
        super(NodeAttributeRemover, self).__init__()
        self._attr_name = attribute_name

    def get_description(self):
        """
        Gets description
        :return:
        """
        return 'Removes node attribute named ' + str(self._attr_name)

    def update(self, network):
        """
        Iterates through all nodes in network that are
        proteins and updates node names with gene symbol
        in mapping table.

        :param network: network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: list of issues as strings encountered
        :rtype: list
        """
        if self._attr_name is None:
            return ['Attribute name is None']

        issues = []
        for k, v in network.get_nodes():
            aliases = network.remove_node_attribute(k, self._attr_name)
        return issues


class NDExNciPidLoader(object):
    """
    Loads content from NCI-PID sif files to NDEx
    """
    STYLE = 'style'

    def __init__(self, args,
                 netattribfac=None,
                 networkupdators=None,
                 py4cyto=Py4CytoscapeWrapper(),
                 ndexextra=NDExExtraUtils()):
        """
        Constructor

        :param args: list of arguments passed in via the command line
        :type args: list
        :param netattribfac: network attributes factory object
        :type netattribfac: :py:class:`NetworkAttributesFromTSVFactory`
        :param networkupdators: list of :py:class:`NetworkUpdators`
        :type networkupdators: list(:py:class:`NetworkUpdators`)
        """
        self._args = args
        self._user = None
        self._pass = None
        self._server = None
        self._template = None
        self._gene_symbol_map = {}
        self._net_summaries = None
        self._ndex = None
        self._loadplan = None
        self._netattrib = None
        self._netattribfac = netattribfac
        self._networkupdators = networkupdators
        self._py4 = py4cyto
        self._ndexextra = ndexextra
        try:
            self._visibility = args.visibility
        except AttributeError:
            self._visibility = 'PUBLIC'
        try:
            self._indexlevel = args.indexlevel
        except AttributeError:
            logger.error('showcase was not found in args. Setting value to ALL')
            self._indexlevel = 'ALL'

        try:
            self._showcase = not args.disableshowcase
        except AttributeError:
            logger.error('showcase was not found in args. Setting value to True')
            self._showcase = True

        self._networksystemproperty_retry = 3
        self._networksystemproperty_wait = 1

    def _parse_config(self):
        """
        Parses config extracting the following fields:

        :py:const:`~ndexutil.config.NDExUtilConfig.USER`
        :py:const:`~ndexutil.config.NDExUtilConfig.PASSWORD`
        :py:const:`~ndexutil.config.NDExUtilConfig.SERVER`

        :return: None
        """
        ncon = NDExUtilConfig(conf_file=self._args.conf)
        con = ncon.get_config()
        self._user = con.get(self._args.profile, NDExUtilConfig.USER)
        self._pass = con.get(self._args.profile, NDExUtilConfig.PASSWORD)
        self._server = con.get(self._args.profile, NDExUtilConfig.SERVER)

    def _parse_load_plan(self):
        """

        :return:
        """
        with open(self._args.loadplan, 'r') as f:
            self._loadplan = json.load(f)

    def _load_network_attributes(self):
        """
        Uses netattribfac passed in constructor to create
        a network attributes object
        :return:
        """
        self._netattrib = self._netattribfac.get_network_attributes_obj()

    def _load_style_template(self):
        """
        Loads the CX network specified by self._args.style into self._template
        :return:
        """
        self._template = ndex2.create_nice_cx_from_file(os.path.abspath(self._args.style))

    def _load_network_summaries_for_user(self):
        """
        Gets a dictionary of all networks for user account
        <network name upper cased> => <NDEx UUID>
        :return: dict
        """
        net_summaries = self._ndex.get_network_summaries_for_user(self._user)
        self._net_summaries = {}
        for nk in net_summaries:
            if nk.get('name') is not None:
                self._net_summaries[nk.get('name').upper()] = nk.get('externalId')

    def _get_network_properties(self, network_id):
        """
        Uh
        :param network_id:
        :return:
        """
        logger.debug('Getting network aspect for network: ' + network_id)
        nps = self._ndex.get_network_aspect_as_cx_stream(network_id, 'networkAttributes')

        network_properties = nps.json()
        return_properties = {}
        for net_prop in network_properties:
            return_properties[net_prop.get('n')] = net_prop.get('v')

        return return_properties

    def _merge_node_attributes(self, network, source_attribute1,
                               source_attribute2, target_attribute):
        """
        Iterate through every node in 'network' and put the attributes in
        'source_attribute1' or 'source_attribute2' into a new 'target_attribute'
        'source_attribute1' and 'source_attribute2' are removed. This implementation
        is a bit weird cause if both 'source_attribute1' and 'source_attribute2' have
        data then 'source_attribute1' is taken
        :param network:
        :param source_attribute1:
        :param source_attribute2:
        :param target_attribute:
        :return: list of issues as string
        :rtype: list
        """
        issues = []
        for node_id, node in network.get_nodes():
            value1 = network.get_node_attribute(node, source_attribute1)
            value2 = network.get_node_attribute(node, source_attribute2)
            if value1 and value2:
                if value1['v'] != value2['v']:
                    issues.append('both attributes have values' +
                                  source_attribute1 + ' => ' + str(value1['v']) + ' and ' +
                                  source_attribute2 + ' => ' + str(value2['v']))
            merged_value = value1 or value2
            if merged_value:
                network.set_node_attribute(node['@id'], target_attribute, merged_value['v'],
                                           type=merged_value['d'],
                                           overwrite=True)
                network.remove_node_attribute(node, source_attribute1)
                network.remove_node_attribute(node, source_attribute2)
        return issues

    def _get_pandas_dataframe(self, file_name):
        """
        Gets pandas data frame from file
        :param file_name:
        :return: tuple (dataframe, node lines list, node fields list)
        """
        path_to_sif = os.path.join(os.path.abspath(self._args.sifdir),
                                   file_name)
        if os.path.getsize(path_to_sif) is 0:
            logger.error('File is empty: ' + path_to_sif)
            return None

        with open(path_to_sif, 'r') as f:
            lines = f.readlines()

        mode = "edge"
        edge_lines = []
        edge_rows_tuples = []
        node_rows_tuples = []
        edge_fields = []
        node_fields = []
        for index in range(len(lines)):
            line = self._normalize_context_prefixes(lines[index])
            if index is 0:
                edge_fields = [h.strip() for h in line.split('\t')]
            elif line == '\n':
                mode = "node_header"
            elif mode is "node_header":
                node_fields = [h.strip() for h in line.split('\t')]
                mode = "node"
            elif mode is "node":
                node_tuple = tuple(line.split('\t'))
                node_rows_tuples.append(node_tuple)
            elif mode is "edge":
                edge_tuple = tuple(line.split('\t'))
                edge_rows_tuples.append(edge_tuple)
                edge_lines.append(line)

        df = pd.DataFrame.from_records(edge_rows_tuples, columns=edge_fields)

        df_nodes = pd.DataFrame.from_records(node_rows_tuples, columns=node_fields)

        df_with_a = df.join(df_nodes.set_index('PARTICIPANT'), on='PARTICIPANT_A')

        df_with_a_b = df_with_a.join(df_nodes.set_index('PARTICIPANT'), on='PARTICIPANT_B', lsuffix='_A',
                                     rsuffix='_B')
        df_with_a_b = df_with_a_b.replace('\n', '', regex=True)
        df_with_a_b['PARTICIPANT_A'] = df_with_a_b['PARTICIPANT_A'].map(lambda x: x.lstrip('[').rstrip(']'))
        df_with_a_b['PARTICIPANT_B'] = df_with_a_b['PARTICIPANT_B'].map(lambda x: x.lstrip('[').rstrip(']'))
        return df_with_a_b

    def _normalize_context_prefixes(self, theline):
        """this function replaces any references of uniprot knowledgebase: with uniprot: and
        kegg compound: with kegg.compound: to adhere to new normalization conventions
        """
        if theline is None:
            logger.warning('Unexpected None passed in')
            return None
        return theline.replace('uniprot knowledgebase:',
                               'uniprot:').replace('kegg compound:',
                                                   'kegg.compound:').replace('UniProt:', 'uniprot:')

    def _cartesian(self, G):
        """
        Converts node coordinates from a :py:class:`networkx.Graph` object
        to a list of dicts with following format:

        [{'node': <node id>,
          'x': <x position>,
          'y': <y position>}]

        :param G:
        :return: coordinates
        :rtype: list
        """
        return [{'node': n,
                 'x': float(G.pos[n][0]),
                 'y': float(G.pos[n][1])} for n in G.pos]

    def _apply_simple_spring_layout(self, network, iterations=50):
        """
        Applies simple spring network by using
        :py:func:`networkx.drawing.spring_layout` and putting the
        coordinates into 'cartesianLayout' aspect on the 'network' passed
        in

        :param network: Network to update
        :type network: :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :param iterations: Number of iterations to use for networkx spring layout call
                           default is 50
        :type iterations: int
        :return: None
        """
        num_nodes = len(network.get_nodes())
        my_networkx = network.to_networkx(mode='default')
        if num_nodes < 10:
            nodescale = num_nodes*20
        elif num_nodes < 20:
            nodescale = num_nodes*15
        elif num_nodes < 100:
            nodescale = num_nodes*10
        else:
            nodescale = num_nodes*5

        my_networkx.pos = nx.drawing.spring_layout(my_networkx,
                                                   scale=nodescale,
                                                   k=1.8,
                                                   iterations=iterations)
        cartesian_aspect = self._cartesian(my_networkx)
        network.set_opaque_aspect("cartesianLayout", cartesian_aspect)

    def _apply_cytoscape_layout(self, network):
        """
        Applies Cytoscape layout on network
        :param network:
        :return:
        """

        try:
            self._py4.cytoscape_ping()
        except Exception as e:
            raise NDExNciPidLoaderError('Cytoscape needs to be running to run '
                                        'layout: ' + str(self._args.layout))

        tmp_cx_file = os.path.join(self._args.sifdir, 'tmp.cx')

        with open(tmp_cx_file, 'w') as f:
            json.dump(network.to_cx(), f)

        annotated_cx_file = os.path.join(self._args.sifdir, 'annotated.tmp.cx')

        self._ndexextra.add_node_id_as_node_attribute(cxfile=tmp_cx_file,
                                                      outcxfile=annotated_cx_file)
        file_size = os.path.getsize(annotated_cx_file)

        logger.info('Importing network from file: ' + annotated_cx_file +
                    ' (' + str(file_size) + ' bytes) into Cytoscape')
        net_dict = self._py4.import_network_from_file(annotated_cx_file,
                                                      base_url=self._args.cyresturl)
        if 'networks' not in net_dict:
            raise NDExNciPidLoaderError('Error network view could not '
                                        'be created, this could be cause '
                                        'this network is larger then '
                                        '100,000 edges. Try increasing '
                                        'viewThreshold property in '
                                        'Cytoscape preferences')

        os.unlink(annotated_cx_file)
        net_suid = net_dict['networks'][0]

        logger.info('Applying layout ' + self._args.layout +
                    ' on network with suid: ' +
                    str(net_suid) + ' in Cytoscape')
        res = self._py4.layout_network(layout_name=self._args.layout,
                                       network=net_suid,
                                       base_url=self._args.cyresturl)
        logger.debug(res)

        os.unlink(tmp_cx_file)

        logger.info('Writing cx to: ' + tmp_cx_file)
        res = self._py4.export_network(filename=tmp_cx_file, type='CX',
                                       network=net_suid,
                                       base_url=self._args.cyresturl)
        self._py4.delete_network(network=net_suid,
                                 base_url=self._args.cyresturl)
        logger.debug(res)

        layout_aspect = self._ndexextra.extract_layout_aspect_from_cx(input_cx_file=tmp_cx_file)
        network.set_opaque_aspect('cartesianLayout', layout_aspect)

    def _process_sif(self, file_name):
        """
        Processes sif file
        :param file_name:
        :return: Report on issues found with processing
        :rtype: :py:class:`NetworkIssueReport`
        """
        node_table = []

        df = self._get_pandas_dataframe(file_name)
        if df is None:
            return None

        network = t2n.convert_pandas_to_nice_cx_with_load_plan(df, self._loadplan)

        siflessname = file_name.replace('.sif', '')

        # Renaming PathwayCommons.8.NCI_PID.BIOPAX to
        # NCI PID - Complete Interactions
        if siflessname == 'PathwayCommons.8.NCI_PID.BIOPAX':
            siflessname = COMPLETE_INTERACTION_NAME

        network.set_name(siflessname)

        report = NetworkIssueReport(network.get_name())

        # merge node attributes, logic was removed ndex2 python client so call a local implementation
        issues = self._merge_node_attributes(network, 'alias_a', 'alias_b', 'alias')
        report.addissues('Merge of alias_a and alias_b node attributes to alias node attribute', issues)

        # more node attribute merging
        issues = self._merge_node_attributes(network, 'PARTICIPANT_TYPE_A',
                                             'PARTICIPANT_TYPE_B', 'type')
        report.addissues('Merge of PARTICIPANT_TYPE_A and PARTICIPANT_TYPE_B '
                         'node attributes to type node attribute', issues)

        # more node attribute merging
        issues = self._merge_node_attributes(network, 'PARTICIPANT_NAME_A',
                                             'PARTICIPANT_NAME_B',
                                             'PARTICIPANT_NAME')
        report.addissues('Merge of PARTICIPANT_NAME_A and PARTICIPANT_NAME_B '
                         'node attributes to PARTICIPANT_NAME node attribute',
                         issues)

        if self._networkupdators is not None:
            for updator in self._networkupdators:
                issues = updator.update(network)
                report.addissues(updator.get_description(), issues)

        if len(network.get_nodes()) is 0:
            report.addissues('Other',
                             ['Network has 0 nodes remaining.'
                              'Skipping Save to NDEx'])
            return report

        # apply style to network
        network.apply_style_from_network(self._template)

        if self._args.layout is not None:
            if self._args.layout == 'spring':
                self._apply_simple_spring_layout(network)
            else:
                if self._args.layout == '-':
                    self._args.layout = 'force-directed-cl'
                self._apply_cytoscape_layout(network)

        network_update_key = self._net_summaries.get(network.get_name().upper())

        # set the version in the network
        self._set_version_in_network_attributes(network)

        # set provenance for network
        self._set_generatedby_in_network_attributes(network)

        # set normalization version for network
        self._set_normalization_version(network)

        # set was derived from
        self._set_wasderivedfrom(network)

        # set type network attribute
        self._set_type(network)

        # set iconurl
        self._set_iconurl(network)

        # set common attributes from style network
        issues = self._set_network_attributes_from_style_network(network)
        report.addissues('Setting description and organism network attributes', issues)

        # set labels, author, and reviewer network attributes
        issues = self._set_labels_author_and_reviewer_attributes(network)
        report.addissues('Setting labels, author and reviewer network attributes', issues)

        self._add_node_types_in_network_to_report(network, report)

        if network_update_key is not None:
            logger.debug('Updating existing network: ' + network.get_name())
            network.update_to(network_update_key, self._server, self._user, self._pass,
                              user_agent=self._get_user_agent())
        else:
            logger.debug('Saving new network: ' + network.get_name())
            neturl = self._ndex.save_new_network(network.to_cx(),
                                                 visibility=self._visibility)
            updateprops = self._update_network_system_properties(neturl)
            if updateprops is not None:
                report.addissues('Updating network system properties', [updateprops])
        return report

    def _update_network_system_properties(self, neturl):
        """
        Updates network index_level and showcase values for
        network specified by 'neturl'
        :param neturl: Full URL to network just saved
        :return: None upon success or string with error message
        :rtype: str
        """
        net_uuid = re.sub('^.*\/', '', neturl)
        prop_dict = {'index_level': self._indexlevel.upper(),
                     'showcase': self._showcase}

        retry_count = 0
        while retry_count < self._networksystemproperty_retry:
            logger.debug('Attempting to update network (' +
                         net_uuid + ') system properties: ' +
                         str(prop_dict))
            try:
                res = self._ndex.set_network_system_properties(net_uuid,
                                                               prop_dict)
                if res == '':
                    return None
            except Exception as e:
                res = 'Error updating network ( ' + \
                       net_uuid + ' ) system properties' + str(e)

            retry_count += 1
            logger.debug('Retry # ' + str(retry_count) + ' got error ' +
                         res + ' attempting to update network system' +
                         'properties for network ' + net_uuid +
                         '. Sleeping and retrying')
            time.sleep(self._networksystemproperty_wait)

        return 'After ' + str(retry_count) + ' retries receiving ' +\
               str(res) +\
               ' when trying to update network with id: ' + net_uuid

    def _add_node_types_in_network_to_report(self, network, report):
        """
        Adds node types to report
        :param network:
        :param report:
        :return: None
        """
        for i, node in network.get_nodes():
            val = network.get_node_attribute_value(i, 'type')
            report.add_nodetype(val)

    def _set_labels_author_and_reviewer_attributes(self, network):
        """

        :param network:
        :return: list of strings describing issues getting author, reviewer and label attributes
        :rtype: list
        """
        issues = []
        name = network.get_name()
        author = self._netattrib.get_author(name)
        if author is not None:
            network.set_network_attribute(NetworkAttributes.AUTHOR,
                                          author)
        else:
            issues.append('no author found in network attributes tsv')

        reviewers = self._netattrib.get_reviewers(name)
        if reviewers is not None:
            network.set_network_attribute(NetworkAttributes.REVIEWERS,
                                          reviewers)
        else:
            issues.append('no reviewers found in network attributes tsv')

        labels = self._netattrib.get_labels(name)
        if labels is not None:
            network.set_network_attribute(NetworkAttributes.LABELS,
                                          labels)
        else:
            issues.append('no labels found in network attributes tsv')
        return issues

    def _set_network_attributes_from_style_network(self, network):
        """
        Copies organism and description network from style aka template
        network and adds it to the network passed in.
        :param network:
        :return: list of strings denoting issues setting description and or organism
        :rtype: list
        """
        issues = []

        # for complete interaction network use this description
        if network.get_name() == COMPLETE_INTERACTION_NAME:
            description = 'This network includes all interactions of the ' \
                          'individual NCI-PID pathways.<br/>'
        else:
            tempdesc = self._template.get_network_attribute('description')
            if tempdesc is None:
                issues.append('description network attribute not set cause its '
                              'missing from template network')
                description = ''
            else:
                description = tempdesc['v']

        network.set_network_attribute('description', description)

        organism = self._template.get_network_attribute('organism')
        if organism is not None:
            network.set_network_attribute('organism', organism['v'])
        else:
            issues.append('organism network attribute not set cause its '
                          'missing from template network')
        return issues

    def _set_version_in_network_attributes(self, network):
        """
        :param network_update_key:
        :param network:
        :return:
        """
        network.set_network_attribute('version', self._args.releaseversion)

    def _set_generatedby_in_network_attributes(self, network):
        """
        Sets the network attribute :py:const:`GENERATED_BY_ATTRIB`
        with ndexncipidloader <VERSION>
        :param network: network to add attribute
        :type :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: None
        """
        network.set_network_attribute(GENERATED_BY_ATTRIB,
                                      '<a href="https://github.com/'
                                      'ndexcontent/ndexncipidloader"'
                                      '>ndexncipidloader ' +
                                      str(ndexncipidloader.__version__) +
                                      '</a>')

    def _set_normalization_version(self, network):
        """
        Sets the network attribute :py:const:`NORMALIZATIONVERSION`
        with 0.1
        :param network: network to add attribute
        :type :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: None
        """
        network.set_network_attribute(NORMALIZATIONVERSION_ATTRIB, '0.1')

    def _set_type(self, network):
        """
        Sets the network attribute :py:const:`TYPE_ATTRIB`
        with ['pathway']
        :param network: network to add attribute
        :type :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: None
        """
        typeval = ['pathway']
        if network.get_name() == COMPLETE_INTERACTION_NAME:
            typeval = ['pathway', 'interactome']

        network.set_network_attribute(TYPE_ATTRIB, typeval,
                                      type='list_of_string')

    def _set_iconurl(self, network):
        """
        Sets the network attribute :py:const:`ICONURL_ATTRIB` with
        value from self._args.iconurl passed in constructor
        :param network: network to add attribute
        :type :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return:
        """
        network.set_network_attribute(ICONURL_ATTRIB,
                                      self._args.iconurl)

    def _set_wasderivedfrom(self, network):
        """
        Sets the 'prov:wasDerivedBy' network attribute to the
        ftp location containing the OWL file for this network.
        The ftp information is pulled from :py:const:`DEFAULT_FTP_HOST` and
         :py:const:`DEFAULT_FTP_DIR` and the owl file name is the
         name of the network with .owl.gz appended

        :param network: network to add attribute
        :type :py:class:`~ndex2.nice_cx_network.NiceCXNetwork`
        :return: None
        """
        network.set_network_attribute(DERIVED_FROM_ATTRIB,
                                      '<a href="'
                                      'ftp://' + DEFAULT_FTP_HOST +
                                      '/' + DEFAULT_FTP_DIR + '/' +
                                      network.get_name() + '.owl.gz">' +
                                      network.get_name() + '.owl.gz</a>')

    def _get_user_agent(self):
        """
        Builds user agent string
        :return: user agent string in form of ncipid/<version of this tool>
        :rtype: string
        """
        return 'ncipid/' + self._args.version

    def _create_ndex_connection(self):
        """
        creates connection to ndex
        :return:
        """
        if self._ndex is None:
            self._ndex = Ndex2(host=self._server, username=self._user,
                               password=self._pass, user_agent=self._get_user_agent())

    def run(self):
        """
        Runs content loader
        :return:
        """
        self._parse_config()
        self._create_ndex_connection()
        logger.debug('Parsed config: ' + self._user)
        self._load_network_summaries_for_user()
        self._parse_load_plan()
        self._load_network_attributes()
        self._load_style_template()
        report_list = []
        file_reverse = sorted(os.listdir(self._args.sifdir),
                              key=lambda s: s.lower(), reverse=True)

        for file in file_reverse:
            if self._args.singlefile is not None:
                if self._args.singlefile != os.path.basename(file):
                    continue

            if file.endswith(".sif"):
                logger.debug('Processing ' + file)
                report_list.append(self._process_sif(file))

        node_type = set()
        for entry in report_list:
            for nt in entry.get_nodetypes():
                node_type.add(nt)
            sys.stdout.write(entry.get_fullreport_as_string())

        sys.stdout.write('Node Types Found in all networks:\n')
        for entry in node_type:
            sys.stdout.write('\t' + entry + '\n')

        return 0


class PaxtoolsRunner(object):
    """
    Runs paxtools.jar to convert .owl files to .sif
    """

    def __init__(self, ftpdir, outdir, paxtools,
                 java='java'):
        """
        Constructor

        :param ftpdir: directory containing owl files
        :type ftpdir: string
        :param outdir: Directory to write .sif files
        :type outdir: string
        :param paxtools: Path to paxtools.jar jar file
        :type paxtools: string
        :param java: Path to Java binary
        :type java: string
        """
        self._ftpdir = ftpdir
        self._outdir = outdir
        self._paxtools = paxtools
        self._java = java

    def run_paxtools(self):
        """Runs paxtools on .owl files in ftp directory set in
        constructor. The output SIF files are written to
        the 'outdir' also set in the constructor.
        """
        counter = 0
        logger.info('Running ' + self._paxtools + ' on .owl files in ' + self._ftpdir)
        for entry in os.listdir(self._ftpdir):
            if not entry.endswith('.owl'):
                continue
            owlfile = os.path.join(self._ftpdir, entry)
            siffile = os.path.join(self._outdir, re.sub('\.owl', '.sif', entry))
            if os.path.isfile(siffile):
                continue
            self._run_paxtool(owlfile, siffile)
            counter += 1
        logger.info('Ran ' + self._paxtools + ' on ' + str(counter) + ' files')

    def _run_paxtool(self, owlfile, siffile):
        """
        Runs paxtools to convert the owl file to SIF using these arguments:

        java -jar toSIF <owlfile> <sif file>
        seqDb=hgnc,uniprot,refseq,ncbi,entrez,ensembl
        chemDb=chebi,pubchem
        -useNameIfNoId -extended

        :param owlfile: Input owl file
        :type owlfile: string
        :param siffile: Output sif file
        :type siffile: string
        :return: None
        """
        cmd = [self._java, '-jar',
               self._paxtools, 'toSIF', owlfile, siffile,
               'seqDb=hgnc,uniprot,refseq,ncbi,entrez,ensembl', 'chemDb=chebi,pubchem',
               '-useNameIfNoId', '-extended']
        logger.debug('Running ' + ' '.join(cmd))
        status = subprocess.call(cmd)
        if status is not 0:
            logger.error('Got non zero exit from command')


class FtpDataDownloader(object):
    """
    Downloads OWL files (.gz files are automatically uncompressed) from
    FTP site.
    """

    def __init__(self, outdir, ftphost=DEFAULT_FTP_HOST,
                 ftpdir=DEFAULT_FTP_DIR,
                 ftpuser=DEFAULT_FTP_USER,
                 ftppass=DEFAULT_FTP_PASS,
                 timeout=10):
        """
        Constructor that sets parameters needed to download OWL
        files

        :param outdir: Directory to store downloaded data files
        :type outdir: string
        :param ftphost: FTP host containing OWL files
        :type ftphost: string
        :param ftpdir: Directory on FTP host where OWL files reside
        :type ftpdir: string
        :param ftpuser: FTP user
        :type ftpuser: string
        :param ftppass: FTP password
        :type ftppass: string
        :param timeout: timeout in seconds for FTP connection
        :type timeout: int
        """
        self._ftphost = ftphost
        self._ftpdir = ftpdir
        self._ftpuser = ftpuser
        self._ftppass = ftppass
        self._outdir = outdir
        self._timeout = timeout
        self._altftp = None
        self._ftp = None

    def set_alternate_ftp(self, altftp):
        """
        Sets alternate ftp connection
        """
        self._altftp = altftp

    def connect_to_ftp(self):
        """
        Connects to ftp server
        """
        if self._altftp is not None:
            self._ftp = self._altftp
            return
        self._ftp = ftpretty(self._ftphost, self._ftpuser, self._ftppass,
                             timeout=self._timeout)
        return

    def disconnect(self):
        """
        Disconnects from FTP
        :return:
        """
        if self._ftp is not None:
            self._ftp.close()

    def download_data(self):
        """
        Creates output directory set in constructor and then proceeds
        to download all files in ftp directory also set in constructor.

        If the downloaded file ends with *.gz* extension it is gunzipped
        first and the suffix is removed.

        .. note::

        If a file already exists on the file system (regardless of size)
        this code does NOT download that file again.

        :return: None
        """
        if not os.path.isdir(self._outdir):
            os.makedirs(self._outdir, mode=0o755)
        filelist = self._ftp.list(self._ftpdir)
        if filelist is None:
            logger.error('No files found in ftp directory')
            return
        logger.info('Found ' + str(len(filelist)) +
                    ' files in ftp directory. Starting download')
        counter = 0
        for entry in filelist:
            destfile = re.sub('\\.gz', '',
                              os.path.join(self._outdir,
                                           os.path.basename(entry)))
            if os.path.isfile(destfile) and os.path.getsize(destfile) > 0:
                logger.debug(entry +
                             ' appears to have been downloaded. Skipping...')
                continue
            logger.debug('Downloading ' + entry + ' to ' + destfile)
            if entry.endswith('.gz'):
                data = self._ftp.get(entry)
                with open(destfile, 'wb') as f:
                    f.write(gzip.decompress(data))
            else:
                with open(destfile, 'wb') as f:
                    self._ftp.get(entry, f)
            counter += 1
        logger.info('Downloaded ' + str(counter) + ' files')


def main(args):
    """
    Main entry point for program

    :param args: command line arguments usually :py:const:`sys.argv`
    :return: 0 for success otherwise failure
    :rtype: int
    """
    desc = """
    Version {version}

    Loads NDEx NCI-PID content data into NDEx (http://ndexbio.org)
    using SIF files as input. This tool downloads
    OWL files from an FTP site (default {ftphost} under
    {ftpdir} directory) and converts them to SIF files using the 
    paxtools.jar whose location is set via --paxtools flag.      
    
    In order for this tool to upload data to NDEx, a configuration file 
    must either reside here ~/{confname} or be set via --conf parameter. 
         
    The configuration file should be formatted as follows:
         
    [<value of --profile flag (default ndexncipidloader)>]
         
    {user} = <NDEx username>
    {password} = <NDEx password>
    {server} = <NDEx server(omit http) ie public.ndexbio.org>

    Example configuration file:
         
     [ndexncipidloader]
     
     {user} = joe123
     {password} = somepassword123
     {server} = dev.ndexbio.org
    
    Example usage:
    
    ndexloadncipid.py tmpdatadir/
    
    The above example uses the default ftp server and assumes
    paxtools.jar is in the current working directory.

    For more information about the transformations being performed
    visit: https://github.com/ndexcontent/ndexncipidloader
    """.format(confname=NDExUtilConfig.CONFIG_FILE,
               user=NDExUtilConfig.USER,
               password=NDExUtilConfig.PASSWORD,
               server=NDExUtilConfig.SERVER,
               version=ndexncipidloader.__version__,
               ftphost=DEFAULT_FTP_HOST,
               ftpdir=DEFAULT_FTP_DIR)
    theargs = _parse_arguments(desc, args[1:])
    theargs.program = args[0]
    theargs.version = ndexncipidloader.__version__

    try:
        outdir = os.path.abspath(theargs.sifdir)
        ftpdir = os.path.join(outdir, FTP_SUBDIR)

        _setup_logging(theargs)
        if theargs.skipdownload is True:
            logger.info('--skipdownload set. Skipping download')
        else:
            logger.info('Downloading data from ftp')
            paxtools = os.path.abspath(theargs.paxtools)
            dloader = FtpDataDownloader(ftpdir)
            dloader.connect_to_ftp()
            dloader.download_data()
            dloader.disconnect()
            logger.info('Converting owl files to sif, if needed')
            paxy = PaxtoolsRunner(ftpdir, outdir, paxtools)
            paxy.run_paxtools()

        if theargs.getfamilies is True:
            extractor = GeneFamilyFromOwlExtractor()
            res = extractor.get_gene_family_mapping_as_string(ftpdir)
            sys.stdout.write(res)
            return 0

        nafac = NetworkAttributesFromTSVFactory(theargs.networkattrib)
        searcher = GeneSymbolSearcher()
        updators = [NodeTypeUpdator(),
                    NodeAliasUpdator(),
                    EmptyCitationAttributeUpdator(),
                    RedundantEdgeAdjudicator(),
                    DirectedEdgeSetter(),
                    UniProtToGeneSymbolUpdater(searcher=searcher),
                    CHEBINodeNameReplacer(),
                    CHEBINodeRepresentsPrefixRemover(),
                    GeneSymbolNodeNameUpdator(theargs.genesymbol),
                    NodeAttributeRemover('PARTICIPANT_NAME'),
                    GeneFamilyExpander(theargs.genesymbol)]

        if theargs.skipchecker is False:
            updators.append(GeneSymbolChecker(searcher=searcher))

        loader = NDExNciPidLoader(theargs,
                                  netattribfac=nafac,
                                  networkupdators=updators)
        logger.info('Running network generation')
        return loader.run()
    except Exception as e:
        logger.exception('Caught exception')
        return 2
    finally:
        logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
