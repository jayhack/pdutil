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

class Op:
	"""
		Ideal Operation:
			Op (operations) (dataframes)
			o1 = Op (operations)
			o2 = Op (other operations)
			o3 = o1 + o2
			o4 = o2 - o1
			o5 = o1 * 5
			o1[1:-1] (dataframes)
			o2["process_text":"run_inference"] (dataframes)
			o2["step a":"step b"] + o2["step c":"step d"] (dataframes)
			for command in o2:
				...
	"""

	def __init__ (self, script, pass_val=False):
		if type(script) == list:
			self.ops_df = pd.DataFrame (script, columns=['stepname', 'in_cols', 'out_col', 'funcs'])
		elif type(script) == pd.core.frame.DataFrame:
			self.ops_df = script
		else:
			raise Exception ('Argument "script" not recognized')
		self.ops_df.index = self.ops_df.stepname


	def __call__ (self, df, verbose=False):
		"""
			MAGIC: __call__
			===============
			applies the operations contained in this Op to the specified 
			dataframe 

			params:
			-------
			df: pandas dataframe to apply operations to 
			inplace: when True (default), return values of operations are disregarded;
						when false, the output of a given step is the operand of 
						the subsequent step and the return value is the final output.
			verbose: when True, prints out the step names

			returns:
			--------
			when inplace=False, returns the final output value.
		"""
		for stepname, row in self.ops_df.iterrows ():
			for f in row.funcs:
				out = f(df[list(row.in_cols)])
				if row.out_col:
					df[row.out_col] = out


	def __add__ (self, other):
		"""
			returns concatenation of the two operations
			o3 = o1 + o2
		"""
		if type(other) != type(self):
				raise TypeError ('Error: must pass in another Op object')
		return Op (pd.concat ([self.ops_df, other.ops_df]))


	def __mul__ (self, scalar):
		"""
			returns the concatenation of this op 
			n times 
		"""
		if type(scalar) != int:
			raise TypeError ('Error: * operator only accepts integers')
		return Op(pd.concat ([self.ops_df]*scalar))


	def __str__ (self):
		return self.ops_df.__str__ ()




if __name__ == "__main__":

	df = pd.DataFrame (np.random.randn(5, 2), columns=['A', 'B'])
	op = Op ([	
			('Add 1 to A', 		('A',), 'A+1', 		[lambda A: A + 1]),
			('Square B', 		('B',), 'B*2',		[lambda B: B * 2]),
			('Add A/B',			('A', 'B'), 'sum',	[lambda df: df.sum (axis=1)]),
			('Average A/B', 	('A', 'B'), 'mean', [lambda df: df.mean (axis=1)])
		])
	op(df)
	assert int(df['A+1'].sum ()) == int(df['A'].sum () + float(len(df)))
	assert int(df['B*2'].sum ()) == int(df['B'].sum () * 2.)
	assert int(df['sum'].mean ()) == int(df[['A', 'B']].sum (axis=1).mean ())
	assert int(df['mean'].sum ()) == int(df[['A', 'B']].mean (axis=1).sum ())	








