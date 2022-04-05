import PyPDF2
import regex


def read_document(path):
	Document_1 = []

	fd = open(path,'rb');

	file_reader = PyPDF2.PdfFileReader(fd);

	for i in range(0,file_reader.numPages):
		page = file_reader.getPage(i);
		Document_1.append(page.extractText());

	index = Document_1[0].find('ABSTRACT');

	Document_1[0] = Document_1[0][index:]

	output = []

	for i in range(0,file_reader.numPages):
		Document_1[i] = regex.sub('(\(.*?\))|(\S*?[+*/%]+\S*)|([0-9]+[Ee.]+[0-9]+)|([0-9]+\S*)|(FIG.)','',Document_1[i]);
		output += Document_1[i].split('.')

	return output

def read_components(document):
		
	'''
	input : An list of sentences return by read_document
	output : List of List of strings , where first list is list of strings in abstract , second list is list of strings in description and third list is list of strings in
		claim section
	
	'''
	components = []
	i = 0
	length = len(document)
	temp = []

	while( i < length ):
		if( 'Claims' in document[i] ):
			break
		else:
			temp.append(document[i])
		
		i += 1
	
	components.append(list(temp))
	temp_1 = []
	temp_2 = []
	claim_words = ['claimed' , 'claims' , 'claim']
	
	while(i < length):
		
		if( any( j in document[i] for j in claim_words ) ):
			temp_2.append(document[i])
		else:
			temp_1.append(document[i])
		
		i += 1
	
	components.append(list(temp_1))
	components.append(list(temp_2))
	return components

def main():
	document = read_document('../../Document_1.pdf');

	print(document)

	print("*********************************")

	components = read_components(document)

	for i in components:
		print(i)

if __name__=="__main__":
	main()


