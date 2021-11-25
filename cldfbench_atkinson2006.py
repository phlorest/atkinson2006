import pathlib

import phlorest

class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "atkinson2006"
    __ete3_newick_format__ = 1  # We have internal nodes!

    def cmd_makecldf(self, args):
        self.init(args)
        stree = self.raw_dir / 'MayanSwd100_3_12_05bn30chrono.t'
        with self.nexus_summary() as nex:
            self.add_tree(args, self.read_tree(stree), nex, 'summary')
