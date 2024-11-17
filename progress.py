
from time import time
from tests import assert_eq

def interleave(its):
    its = list(map(iter, its))
    r = []
    while True:
        sz = len(r)
        for l in list(its):
            try:
                r.append(next(l))
            except StopIteration:
                its.remove(l)
        if len(r) == sz:
            return r

# see the assert below to understand what this does
# @splitvs has to be sorted in ascending order
def split_less_than(l, splitvs, key):
    r = [ [] for e in splitvs ] + [[]]
    def add(v):
        for i, sv in enumerate(splitvs):
            if key(v) < sv:
                r[i].append(v)
                return
        r[-1].append(v)
    #
    for v in l:
        add(v)
    #
    return r
############################
assert_eq(
    split_less_than(
        [(5,4),(3,0),(1,1),(0,1)],
        [3,4],
        lambda v: v[0] + v[1]
    ),
    [[(1,1),(0,1)], [(3,0)], [(5,4)]]
)

def pretty_float(v, p=2):
    return f'{v:.{p}f}'.rstrip('0').rstrip('.')

def pretty_size(v):
    v = int(v)
    if v < 1024:
        return f'{v} B'
    v /= 1024
    if v < 1024:
        return pretty_float(v, 1) + ' KB'
    v /= 1024
    if v < 1024:
        return pretty_float(v, 1) + ' MB'
    v /= 1024
    return pretty_float(v, 1) + ' GB'

assert_eq(pretty_size(1023), '1023 B')
assert_eq(pretty_size(1024 + 32), '1 KB')
assert_eq(pretty_size(1024 + 490), '1.5 KB')
assert_eq(pretty_size(round(1024 * 1024 * 1.88)), '1.9 MB')
assert_eq(pretty_size(round(1024 * 1024 * 1024 * 1.88)), '1.9 GB')

def pretty_duration(v):
    if v < 0.001:
        return pretty_float(v * 1000, 2) + ' ms'
    if v < 1:
        return f'{round(v * 1000)} ms'
    if v < 60:
        return f'{round(v)} sec'
    if v < 3600:
        m = int(v / 60)
        s = round(v - m * 60)
        return f'{m} min {s} sec'
    h = int(v / 3600)
    m = int((v - h * 3600) / 60)
    s = round(v - h * 3600 - m * 60)
    return f'{h} h {m} min {s} sec'

assert_eq(pretty_duration(0.0005908), '0.59 ms')
assert_eq(pretty_duration(0.5908), '591 ms')
assert_eq(pretty_duration(59.1), '59 sec')
assert_eq(pretty_duration(3564.8), '59 min 25 sec')
assert_eq(pretty_duration(3782.8), '1 h 3 min 3 sec')

def print_row(vs, aligns, lengths):
    s = ' | '.join(f'{vs[i]:{aligns[i]}{lengths[i]}}' for i in range(len(vs)))
    print(s)
    return len(s)

def print_table(titles, rows, vs_aligns, title_aligns=None):
    if not title_aligns:
        title_aligns = ['^'] * len(titles)
    #
    lengths = [0] * len(titles)
    for i,t in enumerate(titles):
        lengths[i] = max(len(t), lengths[i])
    for vs in rows:
        for i,l in enumerate(lengths):
            lengths[i] = max(l, len(vs[i]))
    #
    rowLen = print_row(titles, title_aligns, lengths)
    print( '-' * rowLen)
    for vs in rows:
        print_row(vs, vs_aligns, lengths)

def print_item_progress(processedSz, sz):
    print('                         \r', end='')
    print(f'\rcurrent ({pretty_size(sz)}) {processedSz / sz * 100:.2f} %\r', end='')

MB = 1024 * 1024
def progress(items, sz_f, f):
    if not items:
        return
    # to avoid division by zero
    # and have a meaningful and accurate progress for empty files
    sz_f_nonzero = lambda v: sz_f(v) or 1
    #
    # sort in ascending order
    # for ETA to be ready quicker
    # and give the worst possible time
    items.sort()
    splitValues = [10*1024, 1*MB, 10*MB, 100*MB, 1*MB*1024]
    #--------------------------------------------------------------------
    splitItems = split_less_than(items, splitValues, sz_f)
    splitSums = [ sum(map(sz_f_nonzero, vs)) for vs in splitItems ]
    splitProcessed = [0] * len(splitItems)
    splitDuration = [0] * len(splitItems)
    items = interleave(splitItems)
    def getSplitIdx(sz):
        for i, v in enumerate(splitValues):
            if sz < v:
                return i
        return len(splitValues)
    def getEta():
        r = 0
        for i in range(len(splitItems)):
            dur = splitDuration[i]
            if not splitItems[i]:
                continue
            if not dur:
                return None
            processed = splitProcessed[i]
            remain = splitSums[i] - processed
            bps = processed / dur
            r += remain / bps
        return r
    def updateSplitStats(sz, d):
        si = getSplitIdx(sz)
        splitProcessed[si] += sz
        splitDuration[si] += d
        return getEta()
    def printSplitStats():
        realSums = [ sum(map(sz_f, vs)) for vs in splitItems ]
        rows = []
        for i in range(len(splitItems)):
            items = splitItems[i]
            if not items:
                continue
            if i < len(splitValues):
                pr = pretty_size(splitValues[i-1]) if i else '0'
                cur = pretty_size(splitValues[i])
                sV = f'{pr} - {cur}'
            else:
                sV = f'larger than {pretty_size(splitValues[-1])}'
            dur = splitDuration[i]
            bps = realSums[i] / dur
            sCnt = f'{len(items)}'
            sSum = pretty_size(realSums[i])
            sDur = pretty_duration(dur)
            sSpeed = f'{pretty_size(bps)}/s'
            vs = (sV, sCnt, sSum, sDur, sSpeed)
            rows.append(vs)
        titles = ['range', 'files', 'size', 'time', 'speed']
        aligns = ['>'] * len(titles)
        aligns[0] = '<'
        print_table(titles, rows, aligns)
    #--------------------------------------------------------------------

    itemsSize = sum(map(sz_f_nonzero, items))
    processedSz = 0
    start = time()
    for item in items:
        s = time()
        f(item)
        d = time() - s
        #
        sz = sz_f_nonzero(item)
        realSz = sz_f(item)
        processedSz += sz
        perc = (processedSz / itemsSize) * 100
        eta = updateSplitStats(sz, d)
        etastr = 'not ready' if eta is None else pretty_duration(eta)
        d_s = pretty_duration(d) if d < 1 else f'{d:.1f} sec'
        print(
            f'{perc:>5.2f} % | '
            f'{pretty_size(realSz):>9} | '
            f'{d_s:>8} | '
            f'{pretty_size(realSz / d):>8}/s | '
            f'ETA {etastr}'
        )

    total_dur = time() - start
    print()
    printSplitStats()
    print()
    realTotalSz = sum(map(sz_f, items))
    print('total size:', pretty_size(realTotalSz))
    print('total duration:', pretty_duration(total_dur))
