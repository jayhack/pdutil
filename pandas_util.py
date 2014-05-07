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


@list_support
def apply_column_ops (df, ops):
	"""
		Function: apply_column_ops
		==========================
		Allows one to specify a list of operations to apply to 
		given columns, in sequence, if they are present. 
		Note: no guarantees on the order in which they apply. 
		Modifies the df in-place. 
		List support.

		params:
		-------
		df - pandas dataframe
		ops - dictionary mapping column names to a list of functions 
				to be applied to it for each passed df, in order.
	"""
	for col in present_cols (df, ops.keys()):
		for f in ops[col]:
			df[col] = f(df[col])


@list_support
def add_df_cols (df, ops):
	"""
		Function: add_df_cols
		=====================
		Allows one to specify a list of operations to apply to 
		an entire df, in sequence.
		Note: no guarantees on the order in which they apply. 
		Modifies the df in place.
		List support.

		params:
		-------
		df - pandas dataframe
		col_funs - dict mapping new column name to function for how 
					to create it
	"""
	for colname, f in ops.iteritems ():
		df[colname] = f(df)









if __name__ == "__main__":

	df = pd.DataFrame(np.random.randn(6,2), index=pd.date_range('2013-08-01', periods=6, freq='B'), columns=['A', 'B'])

	#####[ APPLY COLUMN OPS	]#####
	old_df = df.copy ()
	ops = 	{		
				'A': [lambda x: x + 1], 
				'B': [lambda x: x + 2], 
				'C': [lambda x: x - 1]
			}
	apply_column_ops (df, ops)
	assert (df.A - old_df.A).sum () == len(df)
	assert (df.B - old_df.B).sum () == 2*len(df)


	#####[ ADD DF COLS	]#####
	old_df = df.copy ()
	ops = 	{
				'sum': lambda df: df[['A', 'B']].sum (axis=1),
				'mean': lambda df: df[['A', 'B']].mean(axis=1)
			}
	add_df_cols (df, ops)
	assert df['sum'].mean () == old_df.sum(axis=1).mean ()
	assert df['mean'].sum () == old_df.mean(axis=1).sum ()	

