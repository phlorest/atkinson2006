import shutil
import pathlib

import attr
import nexus
from cldfbench import Dataset as BaseDataset, Metadata


@attr.s
class PhlorestMetadata(Metadata):
    name = attr.ib(default=None)
    author = attr.ib(default=None)
    year = attr.ib(default=None)
    scaling = attr.ib(default=None)
    analysis = attr.ib(default=None)
    family = attr.ib(default=None)
    missing = attr.ib(default=attr.Factory(dict))


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "atkinson2006"
    metadata_cls = PhlorestMetadata

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return super().cldf_specs()

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        #shutil.copy(self.raw_dir / 'MayanSwd100_3_12_05bn30chrono.t', self.cldf_dir / 'summary.trees')
        shutil.copy(self.raw_dir / 'source.bib', self.cldf_dir / 'sources.bib')
        args.writer.cldf.add_component('LanguageTable')
        args.writer.cldf.add_table(
            'trees.csv',
            {
                'name': 'ID',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#id',
            },
            {
                'name': 'Name',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#name',
            },
            {
                'name': 'rooted',  # bool or None
                'datatype': 'boolean',
                'dc:description': "Whether the tree is rooted (true) or unrooted (false) (or no "
                                  "info is available (null))"
            },
            {
                'name': 'type',  # summary or sample
                'datatype': {'base': 'string', 'format': 'summary|sample'},
                'dc:description': "Whether the tree is a summary (or consensus) tree, i.e. can be "
                                  "analysed in isolation, or whether it is a sample, resulting "
                                  "from a method that creates multiple trees",
            },
            {
                'name': 'method',
                'dc:description': 'Specifies the method that was used to create the tree'
            },
            {
                'name': 'newick',
                'dc:format': 'text/plain+newick',
                'dc:description': 'Newick representation of the tree, labeled with identifiers '
                                  'as described in the LanguageTable',
            },
            {
                'name': 'Source',
                'separator': ';',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#source',
            },
        )
        lids = set()
        glangs = {lg.id: lg for lg in args.glottolog.api.languoids()}
        for row in self.etc_dir.read_csv('taxa.csv', dicts=True):
            #
            # FIXME: add metadata from Glottolog, put in dplace-tree-specific Dataset base class.
            #
            lids.add(row['taxon'])
            glang = glangs[row['glottocode']]
            args.writer.objects['LanguageTable'].append(dict(
                ID=row['taxon'],
                Name=row['taxon'],
                Glottocode=row['glottocode'],
                Latitude=glang.latitude,
                Longitude=glang.longitude,
            ))

        summary = nexus.NexusReader(self.raw_dir / 'MayanSwd100_3_12_05bn30chrono.t')
        assert len(summary.trees.trees) == 1
        summary = summary.trees.trees[0]
        for node in summary.newick_tree.walk():
            if node.name == 'root':
                continue
            if node.is_leaf:
                assert node.name
            if node.name:
                try:
                    lids.remove(node.name)
                except KeyError:
                    if node.is_leaf:
                        args.log.error('Summary tree references undefined leaf {}'.format(node.name))
                    else:
                        args.log.warning('Summary tree references undefined inner node {}'.format(node.name))

        if lids:
            args.log.error('extra taxa specified in LanguageTable: {}'.format(lids))

        args.writer.objects['trees.csv'].append(dict(
            ID='summary',
            Name=summary.name,
            rooted=summary.rooted,
            type='summary',
            method='Consensus tree from a bayesian analysis',
            newick=summary.newick_string,
            Source=['atkinson2006'],
        ))
