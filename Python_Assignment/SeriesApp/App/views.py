from django.shortcuts import render
import pandas as pd
import csv
import os.path
import series.arithmetic, series.arithmetico_geometric, series.catalan, series.fibonacci, series.geometric
import series.harmonic, series.hexagonal, series.lazy_caterer, series.triangular

# Create your views here.
def home(request):

	"""Returns the list containing the contents of CSV File"""

	# Reading the csv file and returning data to display
	data = pd.read_csv('../SeriesApp/csvfile/series.csv')
	data_list = []
	for index,rows in data.iterrows():
		data_dict = {'number': rows['Number'], 'name': rows['Series Name'], 'formula': rows['Formula'], 'params': rows['Seeding parameters']}
		data_list.append(data_dict)
	context = {'data':data_list}
	return render(request, 'index.html', context)

def create(request):

	"""Creates a user defined series"""
	if request.POST:

		# Getting the parameters from the form
		name = str(request.POST.get('name'))
		expr = request.POST.get('expr')
		expr = expr.lower()
		params = []

		# Finding the seeding parameters. If a character is in a-z and is not equal to x, then it is seeding parameter
		for letter in expr:
			if ord(letter) >= 97 and ord(letter) <= 122:
				if ord(letter) != 120:
					if letter not in params:
						params.append(letter)

		# Checking if filename entered by user exists or not
		if os.path.exists('series/'+name):
			return render(request, 'user_defined.html', {'error': 'Series already exists!'})
		else:
			# Writing the expression and parameters in the file as specified by user
			with open('series/'+name, 'w') as f:
				f.write(expr)
				f.write("\n")
				for param in params:
					f.write(param)
					f.write("\n")

			# Writing the csv file
			param_str = ""
			for i in range(0, len(params)-1):
				param_str += params[i] + ", "
			param_str += params[len(params) - 1]
			f = open('../SeriesApp/csvfile/count.txt', 'r')
			index = int(f.readline().strip('\n'))
			f.close()

			row = [str(index+1), name, '#', param_str]
			f = open('../SeriesApp/csvfile/count.txt', 'w')
			f.write(str(index+1))

			with open('../SeriesApp/csvfile/series.csv', 'a+') as f:
				csv_writer = csv.writer(f)
				csv_writer.writerow(row)

			# Finally display the whole csv file after new series is added
			data = pd.read_csv('../SeriesApp/csvfile/series.csv')
			data_list = []
			for index,rows in data.iterrows():
				data_dict = {'number': rows['Number'], 'name': rows['Series Name'], 'formula': rows['Formula'], 'params': rows['Seeding parameters']}
				data_list.append(data_dict)
			context = {'data':data_list}
			return render(request, 'index.html', context)

	return render(request, 'user_defined.html')

def calculate(request):

	"""Calculates the series value as entered by user"""

	if request.POST:
		name = request.POST.get('name')
		original_name = str(name)
		name = name.lower()
		params = request.POST.get('params').split(',')
		params = [int(i.strip(" ")) for i in params]
		x = int(request.POST.get('x'))

		# Checking if the name entered is standard or user defined
		values = {}
		if name == 'arithmetic progression':
			a = series.arithmetic.arithmetic_progression(params[0], params[1])
			n = a.nth_term(x)
			sum_n = a.sum_n_terms(x)
			l = a.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		elif name == 'arithmetico-geometric':
			n = series.arithmetico_geometric.nth_term(x)
			sum_n = series.arithmetico_geometric.sum_n_terms(x)
			l = series.arithmetico_geometric.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		elif name == 'catalan':
			n = series.catalan.nth_term(x)
			sum_n = series.catalan.sum_n_terms(x)
			l = series.catalan.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		elif name == 'fibonacci':
			n = series.fibonacci.nth_term(x)
			sum_n = series.fibonacci.sum_n_terms(x)
			l = series.fibonacci.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		elif name == 'geometric progression':
			a = series.geometric.geometric_progression(params[0], params[1])
			n = a.nth_term(x)
			sum_n = a.sum_n_terms(x)
			l = a.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		elif name == 'harmonic progression':
			a = series.harmonic.harmonic_progression(params[0], params[1])
			n = a.nth_term(x)
			sum_n = a.sum_n_terms(x)
			l = a.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		elif name == 'hexagonal':
			n = series.hexagonal.nth_term(x)
			sum_n = series.hexagonal.sum_n_terms(x)
			l = series.hexagonal.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		elif name == 'lazy caterer':
			n = series.lazy_caterer.nth_term(x)
			sum_n = series.lazy_caterer.sum_n_terms(x)
			l = series.lazy_caterer.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		elif name == 'triangular':
			n = series.triangular.nth_term(x)
			sum_n = series.triangular.sum_n_terms(x)
			l = series.triangular.get_series(x)
			values = {'nth_term': n, 'sum_n': sum_n, 'list_terms': l}

		else:
			# Logic for evaluating user defined series
			# seeding parameter are read and in their place we have placed the value entered by user
			# then using eval we can easily find out the series value
			if os.path.exists('series/'+original_name):
				f =  open('series/'+original_name, 'r')
				l = f.readlines()
				l = [i.strip('\n') for i in l]
				expr = l[0]
				var = l[1:]
				count = 0
				new_expr = ""
				for i in expr:
					if i in var:
						new_expr += str(params[count])
						count += 1
					else:
						new_expr += i
				result = eval(new_expr)
				values = {'nth_term': result}
			else:
				return render(request, 'calculate.html', {'error': 'Unknown Series!'})
		# Returning the values calculated by series
		data = {'values': values}
		return render(request, 'calculate.html', data)
	return render(request, 'calculate.html')