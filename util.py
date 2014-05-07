import pandas as pd
import numpy as np

################################################################################
####################[ PREDICATES ABOUT COLUMNS ]################################
################################################################################

def present_cols (df, cols):
	""""
		returns: intersection of cols and df.columns
	"""
	return list(set(df.columns).intersection(set(cols)))


def present_col_lists (df, col_lists):
	"""
		returns: set of col_tuples where all elements are present 
					in df.columns
	"""
	return [c for c in col_lists if len(present_cols(list(df, col_lists))) == len(col_lists)]


def absent_cols (df, cols):
	"""
		returns: set difference of df.columns and columns
	"""
	return list(set(df.columns).difference (set(cols)))




################################################################################
####################[ DECORATORS ]##############################################
################################################################################

def list_support (f):
	"""
		Decorator: list_support
		=======================
		converts a function that takes a single dataframe as first arg
		to supporting a list of dataframes as first arg. (applies function
		to all in list, then returns the modified list.)
	"""
	def support (df, x):
		if type(df) == list:
			for i in range(len(df)):
				df[i] = f(df[i], x)
			return df
		else:
			return f(df, x)
	return support



################################################################################
####################[ SERIALIZED OPERATIONS ]###################################
################################################################################

class OpList:

	def __init__ (self, ops_dict, pass_val=False):
		self.df = pd.DataFrame (ops_dict)

	def apply (self, ops_df):

	
	def __add__ (self, ops_df):
		"""
			adds the two ops lists
		"""
		raise NotImplementedError

	
	def __sub__ (self, ops_df):
		"""
			removes the specified procedures, in order
			if possible
		"""
		



class ApplyOps:

	def __init__ (self):
		pass

	def ops_seq (self):
		pass

	def apply (self, df, ops_df, pass_val=False):
		"""
			PUBLIC: apply
			=============
			applies operations contained in 
		"""
		for name, coltup, oplist in ops_df.iterrows ():
			for f in oplist:
				out = f(df[list(coltup)])
				if pass_val:
					df = out











@list_support
def retain_cols (df, retain_cols):
	"""
		Function: retain_cols
		=====================
		Allows one to specify a set of columns to retain in df, if they
		are present. also supports lists of dataframes. 
		given columns if they are present. List support.

		params
		------
		df - pandas dataframe
		cols - list of column names to retain if present.
	"""
	df.drop (absent_cols(df, retain_cols), axis=1, inplace=True)











