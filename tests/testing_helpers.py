from helpers.helper_functions import find_capacity_for_coding_region, \
    find_coding_region, embed_data, extract_data, dna_from_mat
# set sequence
seq = "aaaatgttattttaacatcacatgtatgcttagaat"
seq1 = "aaaatgttattattattattattttaacatcacatgtatgcttagaat"
ypt7 = dna_from_mat('ypt7.mat')

# find coding region start=[3,21] stop=[15, 33]
r = find_coding_region(dna_seq=ypt7, frame=1, gc=1)
print(r)

# find capacity = 8 bits
cap = find_capacity_for_coding_region(ypt7, region=r, frame=1, gc=1)
print(cap)

# watermark message
msg = 'ab'

# embed data
wm_seq = embed_data(dna_seq=ypt7, message=msg, frame=1, region=r, gc=1)
print(wm_seq)

# Expected vs observed
# expected = "aaaatgctcttctaacatcacatgtatgcatagaat"
# if expected == wm_seq:
#     print("shukar")
# else:
#     print(wm_seq)

# extract data
extracted = extract_data(wm_dna=wm_seq, frame=1, region=r, gc=1)
print(extracted)

if extracted == msg:
    print("shukar")
else:
    print("extracted:", extracted)

