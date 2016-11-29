from helpers.helper_functions import find_capacity_for_coding_region, find_coding_region, embed_data, extract_data

# set sequence
seq = "aaaatgttattttaacatcacatgtatgcttagaat"

# find coding region start=[3,21] stop=[15, 33]
r = find_coding_region(dna_seq=seq, frame=1, gc=1)
print(r)

# find capacity = 8 bits
cap = find_capacity_for_coding_region(seq, region=r, frame=1, gc=1)
print(cap)

# watermark message
msg = 'a'

# embed data
wm_seq = embed_data(dna_seq=seq, message=msg, frame=1, region=r, gc=1)
print(wm_seq)

# Expected vs observed
expected = "aaaatgctcttctaacatcacatgtatgcatagaat"
if expected == wm_seq:
    print("shukar")
else:
    print(wm_seq)

# extract data
extracted = extract_data(wm_dna=wm_seq, frame=1, region=r, gc=1)
print(extracted)

if extracted == msg:
    print("shukar")
else:
    print("extracted:", extracted)
