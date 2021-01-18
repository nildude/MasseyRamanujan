from ramanujan.enumerators.EfficientGCFEnumerator import EfficientGCFEnumerator
from ramanujan.poly_domains.CartesianProductPolyDomain import CartesianProductPolyDomain
from ramanujan.LHSHashTable import LHSHashTable
from ramanujan.constants import g_const_dict

# create a LHS table for pi
saved_hash = 'pi.lhs.dept20.db'
lhs_search_limit = 20
lhs = LHSHashTable(
    saved_hash,
    lhs_search_limit,
    [g_const_dict['pi']]) 

# define a poly domain to iter through, of the following form:
# an = x0 * n + x1
# bn = x0 * n^2 + x1 * n + x3
# an coefs can range between -13 and 13, bn coefs can range from -11 to 11.
# all coefs are independent and all combinations will be generated.
poly_search_domain = CartesianProductPolyDomain(
    1, [-13, 13],
    2, [-11, 11])

# create an enumerator to iter thought the poly domain and compare it to the
# lhs table
enumerator = EfficientGCFEnumerator(
    lhs,
    poly_search_domain,
    [g_const_dict['pi']])

results = enumerator.full_execution()
