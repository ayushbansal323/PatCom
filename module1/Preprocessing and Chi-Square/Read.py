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

def read_claims(document):
	claims = []
	indicator = 0

	for i in document:
		if(i.find(' claimed ')!=-1):
			indicator = 1

		if(indicator):
			claims.append(i)

	return claims

def main():
	document = read_document('./Document_1.pdf');

	print(document)

	print("********************************")

	claims = read_claims(document)

	for i in claims:
		print(i)

	if __name__=="__main__":
		main()    
		

