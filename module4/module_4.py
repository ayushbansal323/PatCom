
import networkx as nx ;
import re ;

def final_sentences( text , edges ):
	
	'''
	param text : It is the list of strings .
	param edges : It is the list of egdes .
	return : list of strings , where each string is an sentence which is to be present in summary of particular document .
	
	'''
	
	output = [] ;
	sentence_list = [] ;
	
	for i in text:   
		
		temp_list = [ 0 , [] , i ] ;
		
		for j in edges: 
			
			if( re.search( r'\b{}\b'.format( j[0] ) , i ) and re.search( r'\b{}\b'.format( j[1] ) , i ) ): 
				
				temp_list[0] += 1 ;
				temp_list[1].append( j ) ;
		
		sentence_list.append( list( temp_list ) ) ;  
	
	sentence_list.sort( key = lambda x : x[1] , reverse = True ) ; 	
	hash_map = {} ;
	
	for i in sentence_list: 
		
		flag = 0 ; 
		
		for j in i[1]: 	
			
			if( j not in hash_map ): 
				
				hash_map[ j ] = 1 ;
				flag = 1 ;
		
		if( flag ): 
			
			output.append( i[2] ) ;
	
	return output ;
	

def Create_Summary( graph , common_features , document_1 , document_2 ):
	
	'''
	param graph : An steiner tree generated in module 3 
	param common_features : List of common features present in both the document
	param document_1 : List of strings , where each string is an each sentence in document_1
	param document_2 : list of strings , where each string is an each sentence in document_2
	return : list of strings , where first string is an summary of document_1 and second string is an summary of document_2 .
	
	'''
	graph.remove_nodes_from( common_features ) ;
	edges = list( graph.edges ) ;  
	
	summary = [ "" , "" ] ; 
	text = document_1 ;
	ret = final_sentences( text , edges ) ;	
	
	for i in ret:
		
		summary[0] += i ;
	
	text = document_2 ;
	ret = final_sentences( text , edges ) ;	
	
	for i in ret:
		
		summary[1] += i ;
	
	return summary ;


