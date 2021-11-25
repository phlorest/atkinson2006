import pathlib

import phlorest

class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "atkinson2006"
    __ete3_newick_format__ = 1  # We have internal nodes!

    def cmd_makecldf(self, args):
        self.init(args)
        args.writer.add_summary(
            self.raw_dir.read_tree('MayanSwd100_3_12_05bn30chrono.t'),
            self.metadata,
            args.log)
