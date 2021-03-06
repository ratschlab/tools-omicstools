import sys
import numpy as np
import h5py
import os
import re

from ..utils import libsize
from ..utils import parsers

def parse_options(argv):

    """Parses options from the command line """

    from argparse import ArgumentParser

    parser = ArgumentParser(prog='compute_lib_size', description='This script takes an expression count file aggregated over multiple samples and computes the library size per sample.')
    parser.add_argument('-i', '--input', dest='infile', metavar='STR', help='expression counts in hdf5 or tsv format', default='-', required=True)
    parser.add_argument('-a', '--annotation', dest='annotation', metavar='STR', help='annotation file (needed for coding / autosome filtering) []', default='-')
    parser.add_argument('--coding', dest='coding', action='store_true', help='only use coding genes for normalization', default=False)
    parser.add_argument('--autosomes', dest='autosomes', metavar='LIST', nargs='+', help='list of autosomes to exclude from normalization []', default=[])
    
    return parser.parse_args(argv[1:])


def main():

    options = parse_options(sys.argv)

    ### get the data
    print('loading expression data from ' + options.infile)
    if options.infile.lower().endswith('hdf5'):
        IN = h5py.File(options.infile, 'r')
        expression = IN['counts'][:]
        genes = IN['gids'][:].view(np.chararray).decode('utf-8')
        strains = IN['sids'][:].view(np.chararray).decode('utf-8')
        IN.close()
    elif options.infile.lower().endswith('tsv'):
        expression = np.loadtxt(options.infile, dtype='str', delimiter='\t')
        strains = expression[0, 1:]
        expression = expression[1:, :]
        genes = expression[:, 0]
        expression = expression[:, 1:].astype('int')
        if len(expression.shape) < 2:
            expression = expression[:, np.newaxis]
    else:
        sys.stderr.write('ERROR: Unrecognized file ending. Able to accept *.hdf5 and *.tsv\n')
        return 1

    ### get list of protein coding genes
    coding = []
    if options.coding or len(options.autosomes) > 0:
        for line in open(options.annotation, 'r'):
            if line[0] in ['#']:
                continue
            sl = line.strip().split('\t')
            if sl[2].lower() != 'gene':
                continue
            if options.annotation.lower().endswith('.gtf'):
                tags = parsers.get_tags_gtf(sl[8])
                gene = tags['gene_id']
                is_coding = tags['gene_type'] == 'protein_coding'
            elif options.annotation.lower().endswith('.gff'):
                tags = parsers.get_tags_gff3(sl[8])
                try:
                    gene = tags['ID'] 
                    is_coding = tags['gene_type'] == 'protein_coding'
                except KeyError:
                    continue
            if not options.coding or is_coding:
                coding.append([sl[0], gene])
        coding = np.array(coding)        

        ### filter for autosomes
        if len(options.autosomes) > 0:
            k_idx = np.where(~np.in1d(coding[:, 0], options.autosomes))[0]
            coding = coding[k_idx, :]
        coding = coding[:, 1]

        ### filter expression
        k_idx = np.where(np.in1d(genes, coding))[0]
        genes = genes[k_idx]
        expression = expression[k_idx, :]

    ### compute normalizers
    libsize_uq = libsize.upper_quartile(expression)
    libsize_tc = libsize.total_count(expression)

    s_idx = np.argsort(libsize_uq)[::-1]

    out = open(re.sub('.hdf5$', '', options.infile) + '.libsize.tsv', 'w')
    print('sample\tlibsize_75percent\tlibsize_total_count', file=out)
    for i in s_idx:
        print('\t'.join([strains[i], str(libsize_uq[i]), str(libsize_tc[i])]), file=out)
    out.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
