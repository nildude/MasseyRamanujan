import os
import sys
import argparse
import pickle
from functools import partial
import sympy
from enumerate_over_gcf import multi_core_enumeration_wrapper
import series_generators
import constants    # declares constants as sympy Singeltons, "not" used is intended

g_const_dict = {
    'zeta': sympy.zeta,
    'e': sympy.E,
    'pi': sympy.pi,
    'catalan': sympy.Catalan,
    'golden_ratio': sympy.GoldenRatio,
    'khinchin': sympy.S.Khinchin,
    'euler-mascheroni': sympy.gamma
}


def get_custom_generator(generator_name, args):
    """
    Hackish custom generators. create a new one and add it here to include in API.
    :param generator_name: name of custom generator
    :param args: program args
    :return: generator function , number of free coefficients
    """
    if generator_name is None:
        return None, None
    elif generator_name == 'zeta_bn':
        return partial(series_generators.create_zeta_bn_series, args.function_value * 2), 2
    elif generator_name == 'zeta3_an':
        return series_generators.zeta3_an_generator, 2
    elif generator_name == 'zeta5_an':
        return series_generators.zeta5_an_generator, 3


def get_constant(const_name, args):
    """
    for function constants
    """
    if const_name == 'zeta':
        return g_const_dict['zeta'](args.function_value)
    else:
        return g_const_dict[const_name]


# Initialize the argument parser that accepts inputs from the end user
def init_parser():
    parser = argparse.ArgumentParser(
        description='TODO',
        usage='''main.py <enumeration_type> [<args>]
        
Currently the optional enumeration types are:
    enumerate_over_gcf    enumerates over different RHS permutation by using 2 series generators for {an} and {bn}

        ''')

    subparsers = parser.add_subparsers(help='enumeration type to run')

    gcf_parser = subparsers.add_parser('enumerate_over_gcf')
    gcf_parser.add_argument('-LHS_constant', choices=g_const_dict.keys(), default='zeta',
                            help='constants to search for - initializing the LHS hash table')
    gcf_parser.add_argument('-function_value', type=int,
                            help='Which value of the function are we assessing \
                                 (assuming LHS constant takes an arguments)',
                            default=3)
    gcf_parser.add_argument('-lhs_search_limit', type=int,
                            help='The limit for the LHS coefficients', default=20)
    gcf_parser.add_argument('-num_of_cores', type=int,
                            help='The number of cores to run on', default=4)
    gcf_parser.add_argument('-poly_a_order', type=int,
                            help='the number of free coefficients for {a_n} series', default=3)
    gcf_parser.add_argument('-poly_a_coefficient_max', type=int,
                            help='The maximum value for the coefficients of the {a_n} polynomial', default=20)
    gcf_parser.add_argument('-poly_b_order', type=int,
                            help='the number of free coefficients for {b_n} series', default=3)
    gcf_parser.add_argument('-poly_b_coefficient_max', type=int,
                            help='The maximum value for the coefficients of the {b_n} polynomial', default=20)
    gcf_parser.add_argument('--custom_generator_an', type=str, default='zeta3_an',
                            help='(optional) custom generator for {a_n} series. if defined, poly_a_order is ignored')
    gcf_parser.add_argument('--custom_generator_bn', type=str, default='zeta_bn',
                            help='(optional) custom generator for {a_n} series. if defined, poly_b_order is ignored')
    return parser


def main():
    # Initializes the argument parser to receive inputs from the user
    parser = init_parser()
    if len(sys.argv) == 1:  # run from editor
        args = parser.parse_args(['enumerate_over_gcf'])
    else:
        args = parser.parse_args()

    an_generator, poly_a_order = get_custom_generator(args.custom_generator_an, args)
    if an_generator is None:
        poly_a_order = args.poly_a_order

    bn_generator, poly_b_order = get_custom_generator(args.custom_generator_bn, args)
    if bn_generator is None:
        poly_b_order = args.poly_a_order

    sympy_const = get_constant(args.LHS_constant, args)

    # Runs the enumeration wrapper
    final_results = multi_core_enumeration_wrapper(
        sym_constant=sympy_const,  # constant to run on
        lhs_search_limit=args.lhs_search_limit,
        poly_a=[[i for i in range(args.poly_a_coefficient_max)]] * poly_a_order,  # a_n polynomial coefficients
        poly_b=[[i for i in range(args.poly_b_coefficient_max)]] * poly_b_order,  # b_n polynomial coefficients
        num_cores=args.num_of_cores,  # number of cores to run on
        manual_splits_size=None,  # use naive tiling
        saved_hash=os.path.join('hash_tables', f'{str(sympy_const)}_{args.lhs_search_limit}_hash.p'),  # if existing
        create_an_series=an_generator,  # use default
        create_bn_series=bn_generator
    )

    with open('tmp_results', 'wb') as file:
        pickle.dump(final_results, file)


if __name__ == '__main__':
    main()