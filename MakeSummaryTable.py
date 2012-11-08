import pandas
import os
from os import path
from glob import glob
from sys import argv


fnames = glob('analysis-multi/*/genes.fpkm_tracking')

conf = '-c' in argv

df = None
for fname in sorted(fnames):
    table = pandas.read_table(fname)
    alldir, fname = path.split(fname)
    basedir, dirname = path.split(alldir)
    table = table.drop_duplicates('gene_short_name').dropna(how='any')
    table.set_index('gene_short_name', inplace=True, verify_integrity=True)
    if df is None:
        df = pandas.DataFrame({dirname: table.FPKM})
        if conf:
            df.insert(len(df.columns),
                      dirname+"_conf_range", 
                      (table.FPKM_conf_hi - table.FPKM_conf_lo))
    else:
        df.insert(len(df.columns), dirname, table.FPKM)
        if conf:
            df.insert(len(df.columns), dirname + "_conf_range",
                      table.FPKM_conf_hi - table.FPKM_conf_lo)
    

df.to_csv('analysis-multi/summary.tsv', sep='\t')
