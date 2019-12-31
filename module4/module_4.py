
import networkx as nx ;
import re ;

def final_sentences( text , edges ):
	
	output = [] ;
	sentence_list = [] ;
	
	for i in text:   	# iterate over every sentence in the given text .
		
		temp_list = [ 0 , [] , i ] ;
		
		for j in edges: 	# for each iterate over every edge .
			
			if( re.search( r'\b{}\b'.format( j[0] ) , i ) and re.search( r'\b{}\b'.format( j[1] ) , i ) ): # check whether the nodes/words forming an edge are present in the sentence .
				
				temp_list[0] += 1 ;
				temp_list[1].append( j ) ;
		
		sentence_list.append( list( temp_list ) ) ;  	# add temp_list in the sentence_list where the temp_list contains count and edges getting covered in that sentence .
	
	sentence_list.sort( key = lambda x : x[1] , reverse = True ) ; 	# sort sentence_list based on the count of edges being covered .
	hash_map = {} ;
	
	for i in sentence_list: 	# iterate over sentence_list
		
		flag = 0 ; 		# initialize flag to zero .
		
		for j in i[1]: 		# iterate over every edge covered by that sentence .
			
			if( j not in hash_map ): 		# check whether that edge is covered or not . If not indicates add it to hash_map and change flag to 1 .
				
				hash_map[ j ] = 1 ;
				flag = 1 ;
		
		if( flag ): 	# if flag is set to 1 which means that respective sentence covers atleast one edge which was not covered before ; add that sentence to the output .
			
			output.append( i[2] ) ;
	
	return output ;
	

def Create_Summary( graph , common_features , document_1 , document_2 ):
	
	graph.remove_nodes_from( common_features ) ;  # remove common nodes from the tree
	edges = list( graph.edges ) ;  # get all edges in the tree
	summary = [ "" , "" ] ; 
	text = document_1 ;
	ret = final_sentences( text , edges ) ;		# find sentences in the summary of document_1
	
	for i in ret:
		
		summary[0] += i ;		# create summary of document_1
	
	text = document_2 ;
	ret = final_sentences( text , edges ) ;		# find sentences in the summary of document_2
	
	for i in ret:
		
		summary[1] += i ;		# create summary of document_2
	
	return summary ;


