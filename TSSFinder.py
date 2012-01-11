import re
from collections import defaultdict
import pdb

def find_tss(fname):
    first_exons = {}
    fbgn_to_fbtr = defaultdict(list)
    fbtr_to_fbgn = {}
    transcript_starts = {}
    find_fbtr = re.compile('FBtr[0-9]+')
    find_fbgn = re.compile('FBgn[0-9]+')
    find_exon_number = re.compile('exon_number *"?([0-9]+)"?;')
    print 'Loading GTF...'
    for line in open(fname):
        if line.startswith("#"): continue
        data = line.split('\t')
        kind = data[2]
        strand = data[6]
        if kind == 'mRNA':
            fbtr = find_fbtr.findall(data[-1])[0]
            fbgn = find_fbgn.findall(data[-1])[0]
            fbtr_to_fbgn[fbtr] = fbgn
            fbgn_to_fbtr[fbgn].append(fbtr)
            transcript_starts[fbtr] = int(data[3 + (strand == '-')])

        #if find_fbgn.findall(line) == ['FBgn0003659']:
            #pdb.set_trace()
        elif kind == 'exon':
            fbtr = find_fbtr.findall(data[-1])[0]
            first_base = int(data[3 + (strand == '-')])
            exon_number = find_exon_number.findall(data[-1])
            if exon_number == ['1']:
                first_exons[fbtr] = data[0], int(data[3]), int(data[4])
                fbgn = find_fbgn.findall(data[-1])[0]
                print "loading ", fbtr, fbgn, data[3], data[4], line
                fbtr_to_fbgn[fbtr] = fbgn
                fbgn_to_fbtr[fbgn].append(fbtr)
            if ((fbtr not in transcript_starts) 
                or (first_base != transcript_starts[fbtr])):
                continue
            if fbtr in first_exons:
                print fbtr
                # This shouldn't happen, but maybe the data is malformed

            first_exons[fbtr] = data[0], int(data[3]), int(data[4])

    filtered_first_exons  = defaultdict(list)
    print "Filtering by gene..."

    for fbgn in fbgn_to_fbtr:
        for fbtr in fbgn_to_fbtr[fbgn]:
            for first_exon in filtered_first_exons[fbgn]:
                if (first_exons[fbtr][1] == first_exon[1]
                    or first_exons[fbtr][2] == first_exon[2]):
                    if (first_exons[fbtr][1] < first_exon[1] 
                        or first_exons[fbtr][2] > first_exon[2]):
                        filtered_first_exons[fbgn].remove(first_exon)
                        filtered_first_exons[fbgn].append(first_exons[fbtr])
                    break
            else:
                filtered_first_exons[fbgn].append(first_exons[fbtr])

    chroms = defaultdict(dict)
    print "Sorting by chromosome..."
    for gene in filtered_first_exons:
        if len(filtered_first_exons[gene]) == 1:
            # These are uninteresting for our purposes
            continue
        num = 0
        for num, (chrom, low, high) in enumerate(filtered_first_exons[gene]):
            chroms[chrom][low, high] = gene, num

    return chroms




    
if __name__ == "__main__":
    import sys
    from cPickle import dump
    tsss = find_tss(sys.argv[1])

    genes = defaultdict(list)
    for i, line in enumerate(sys.stdin):
        if i % 100000 == 0:
            print '.',
            sys.stdout.flush()
        data = line.split('\t',5)
        id = data[0]
        chrom = data[2]
        pos = int(data[3])
        for low, high in tsss[chrom]:
            if low <= pos <= high:
                gene, tss = tsss[chrom][low, high]
                while tss >= len(genes[gene]):
                    genes[gene].append(0)

                genes[gene][tss] += 1
                break

    outfh = open(sys.argv[2], 'w')
    dump(genes, outfh)
    outfh.close()

