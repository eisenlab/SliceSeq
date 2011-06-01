from __future__ import print_function, division

import collections as cs
from Bio.Blast import NCBIXML
import os

human_types = [('Homo', 'sapiens'), (u'Human', u'DNA'), 
               (u'Pan', u'troglodytes')]

fly_types = [(u'Drosophila', u'melanogaster'), (u'Synthetic', u'construct'),
             (u'Drosophila', u'simulans'), (u'Drosophila', u'sechellia'),
             (u'Drosophila', u'kikalaeleele'), (u'Drosophila', u'erecta'),
             (u'Drosophila', u'yakuba'), (u'Drosophila', u'sp.')]


os.chdir('blaststuff')
blast_recs5 = [r for r in NCBIXML.parse(open('5.blastout.xml'))]
blast_recs6 = [r for r in NCBIXML.parse(open('6.blastout.xml'))]
c5 = cs.Counter([tuple(r.alignments[0].hit_def.split()[:2]) for r in blast_recs5])
c6 = cs.Counter([tuple(r.alignments[0].hit_def.split()[:2]) for r in blast_recs6])


print(c5)
print(c6)

print("Percent Human in c5")
print(100.0 * sum(c5[sp] for sp in human_types)/(sum(c5[i] for i in c5)))


print("Percent Fly in c5")
print(100.0 * sum(c5[sp] for sp in fly_types)/(sum(c5[i] for i in c5)))

print("Percent Human in c6")
print(100.0 * sum(c6[sp] for sp in human_types)/(sum(c6[i] for i in c6)))


print("Percent Fly in c6")
print(100.0 * sum(c6[sp] for sp in fly_types)/(sum(c6[i] for i in c6)))
