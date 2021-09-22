from .CartesianProductPolyDomain import CartesianProductPolyDomain 
from itertools import product
import numpy as np


class Zeta3Domain2(CartesianProductPolyDomain):
	"""
	This domain iters polynomials from this kind:
	a(n) = x0*n^3 + x0*(n+1)^3 + x1(2n+1)
	b(n) = -(x2**2)*n^6

	Note that all zeta3 results shown in the paper can be written using this
	scheme. 

	It is suggested to keep x1,x2<0, but this is not enforced by this class 
	"""

	def __init__(self, a_coefs_ranges=((0, 0),), b_coef_range=(0, 0), *args, **kwargs):
		# a_coef_range and b_coef_range are given blank values. they are initialized again afterwards
		super().__init__(a_deg=2, b_deg=1, a_coef_range=[0, 0], b_coef_range=[0, 0], *args, **kwargs)
		self.a_coef_range = a_coefs_ranges
		self.b_coef_range = [b_coef_range]

		self._setup_metadata()

	@staticmethod
	def get_calculation_method():
		def an_iterator(a_coefs, max_runs, start_n=1):
			for i in range(start_n, max_runs):
				yield a_coefs[0]*((i+1)**3 + i**3) + a_coefs[1]*(2*i+1)

		def bn_iterator(b_coefs, max_runs, start_n=1):
			for i in range(start_n, max_runs):
				yield -(b_coefs[0]**2)*(i**6)

		return an_iterator, bn_iterator

	@staticmethod
	def get_an_degree(an_coefs):
		return 3

	@staticmethod
	def get_bn_degree(bn_coefs):
		return 6

	@staticmethod
	def get_poly_an_lead_coef(an_coefs):
		return an_coefs[0]*2

	@staticmethod
	def get_poly_bn_lead_coef(bn_coefs):
		return -bn_coefs[0]**2
	
	def filter_gcfs(self, an_coefs, bn_coefs):
		# see Ramanujan paper for convergence condition on balanced an & bn degrees
		a_leading_coef = an_coefs[0] * 2
		if -1 * (bn_coefs[0]**2) * 4 < -1 * (a_leading_coef**2):
			return False

		if self.use_strict_convergence_cond and -1 * (bn_coefs[0]**2) * 4 == -1 * (a_leading_coef**2):
			return False

		# discarding expansions
		if np.gcd.reduce(an_coefs + bn_coefs) != 1:
			return False

		return True
