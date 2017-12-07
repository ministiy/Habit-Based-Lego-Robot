import csv


class WriteCSV:
    def writeHeader(self):
        header = ['left sensor', 'right sensor', 'left ultraviolet sensor', 'right ultraviolet sensor', 'left motor',
                  'right motor']
        with open('output.csv', 'w', newline="") as output_file:
            wr = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_ALL)
            wr.writerow(header)

"""   def writeData(self):
		# writing to a csv file called output.csv to store sensory-motor data where
			#   lsv = left colour sensor value
			#   rsv = right colour sensor value
			#   luv = left ultraviolet sensor value
			#   ruv = right ultraviolet sensor value
			#   lmv = left motor value
			#   rmv = right motor value
		with open('output.csv', 'a', newline="") as output_file:
			wr = csv.writer(output_file, delimiter = ',' , quoting=csv.QUOTE_ALL)
			wr.writerow([lsv, rsv, luv, ruv, lmv, rmv])"""