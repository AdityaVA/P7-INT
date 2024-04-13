import regex as re
import os
def editP4(p4_code, u_port, tables_used, include_folder = "p4src/include/"): #put the file names as parameter

	#files used
	include_files = os.listdir(include_folder)  
	p4_original = p4_code # file name of original user p4 code
	rec_h = 0 # recirculation header
	parse = 0 # change parser
	egress = 0 # change egress port
	table_done = 0 # change tables
	include_files.append(p4_original) # add the user p4 code to the list

	user_port = u_port

	for file in include_files:
		# read the content from include file
		if file == p4_original:
			loc = p4_original
		else:
			loc = include_folder + file
		with open(loc, 'r') as includeFile:
			# read all the file content
			allContent = includeFile.read()
			# write the content in the new file
			if rec_h == 0:
								#--------------- C H A N G E  H E A D E R S ---------------
				
				# regex expression for match with header definitions
				patternHeaders = "\.*struct\s+headers\s*\{[\s\S]*?\ ethernet\s*;"

				#rec header
				rec_header = "header rec_h {\n\tbit<32> ts;\n\tbit<32> num;\n\tbit<32> jitter;\n\tbit<16> sw;\n\tbit<16> sw_id;\n\tbit<16> ether_type;\n\tbit<32> dest_ip;\n\tbit<1> signal;\n\tbit<31> pad;\n}\n\n"
				
				#match
				matchi = re.search(patternHeaders, allContent)

				# if pattern is found
				if matchi:
					# print("rec found in file: ", file)
					st = matchi.start()
					en = matchi.end()
					#add the recirculation header before
					allContent = allContent[:st] + rec_header + allContent[st:en] + "\n\trec_h\trec;" + allContent[en:]
					rec_h = 1

				#add the recirculation header before
			if parse == 0:
				#--------------- C H A N G E  P A R S E R ---------------
				
				# Regex expressions for parser
				patternEthernetFull = r'state\s+parse_ethernet\s*\{(?:[^{}]*{[^{}]*}[^{}]*|[^{}]+)*\}'
				patternEthernet = '\.*state\s+parse_ethernet\s*\{'
				patternTransitionStart = '\.*transition\s+select\([\w.]+\)\s*\{'
				add = "\n\t\t\t16w0x9966:   parse_rec;\n"

				transitionOptions = 0

				ethers = re.finditer(patternEthernet, allContent)
					

				
				for eth in ethers:
					# print("parse found in file: ", file)
					parse = 1
					ethStart = eth.start()
					ethFinal = eth.end()

					matchess = re.search(patternTransitionStart, allContent[ethFinal:])
					
					a = matchess.end()
					b = re.search("\}", allContent[ethFinal+a:]).start()

					transitionContent = allContent[ethFinal+a+1:ethFinal+a+b+1]

					allContent = allContent[:ethFinal+a+1] + add + allContent[ethFinal+a:]

					#new state to parser rec header
					newState = "\n\tstate parse_rec { \n\t\tpkt.extract(hdr.rec);\n\t\ttransition select(hdr.rec.ether_type){\n"+ transitionContent   +"\n\t}\n"
					x = ethStart
					aux = re.search(patternEthernetFull, allContent[x:])
					allContent = allContent[:x+aux.end()+1] + newState +allContent[x+aux.end()+1:]
			if table_done == 0:
				#--------------- C H A N G E  T A B L E S ---------------

				#regex expression for match and change all tables
				patternTable = r'table\s+[^{]+\s*\{(?:[^{}]*{[^{}]*}[^{}]*|[^{}]+)*\}' # exp to identify all tables
				keyMatch = "\.*key\s*=\s*{" #exp to identify the key section of a table

				#find the name of headers
				intrMD = "out\s+headers\s+"
				finalParent = "out\s+headers\s+\w+\\s*,"

				aux = re.search(intrMD, allContent)
				aux2 = re.search(finalParent, allContent)
				if aux and aux2:
					hdrName = allContent[aux.end():aux2.end()-1]

					#adapt the tables
					allTables = re.finditer(patternTable, allContent)

					for table in allTables:
						#print(table)
						a = table.start()
						b = table.end()
						newMat = re.finditer(keyMatch, allContent[a:b])
						table_name = re.search("table\s+\w+\s*\{", allContent[a:b]).group()
						table_name = table_name.split()
						table_name = table_name[1]
						if table_name in tables_used:
							print("table found in file: ", file)
						#if key is not found, add "key = { hdr.rec.sw_id : exact; }"
							empty = 1
							for n in newMat:
								empty = 0
								#print(n)
								c = n.end()
								
								# table name is the next word after table before the {
								# find the table name in the variable table
					
								
								# print("table name ", table_name)
								# print("table found in file: ", file)
								allContent = allContent[0:a+c] + "\n\t\t\t"+hdrName+".rec.sw_id   : exact;" + allContent[a+c:]
							if empty:
								print("table found in file: ", file)
								allContent = allContent[0:b-1] + "\n\t\tkey = { "+hdrName+".rec.sw_id : exact; }\n"+ "}" + allContent[b:] 
					
			if egress == 0:
				#--------------- C H A N G E  E G R E S S  P O R T  ---------------
	
				#regex expression for match and change apply block
				patternApply = r'apply\s*\{(?:[^{}]*\{(?:[^{}]*\{[^{}]*\}[^{}]*|[^{}]+)*\}[^{}]*|[^{}]+)*\}' # exp to identify apply block

				ingressProcess1 = "\.*Pipeline[\w\s(]+\)\s*,\s*"
				y = re.search(ingressProcess1, allContent)
				if y :
					# print("ingress found in file: ", file)
					ig2 = re.match("\w+", allContent[y.end():]).group()

					ig3 = re.search("\.*control\s+"+ig2+"\s*\(", allContent)

					matchi = re.search(patternApply, allContent[ig3.end():])
					st = matchi.start()
					en = matchi.end()

					allContent = allContent[:ig3.end()+en-1] + "\tig_tm_md.ucast_egress_port = " + str(user_port) + ";\n\t" + allContent[ig3.end()+en-1:]
			
			
			if file == p4_original:
				p4_name = p4_original.split(".")
				if p4_name[0].find('/') != -1:
					p4_copy = p4_name[0].split("/")
					p4_copy = "files/" + p4_copy[-1] + "_mod.p4"
				else:
					p4_copy = "files/" + p4_name[0] + "_mod.p4"
				with open(p4_copy, 'w') as new_file:
					# write the data
					new_file.write(allContent)
			else:
				# if include folder is not there
				if not os.path.exists("files/include"):
					# create the folder
					os.makedirs("files/include")
				with open("files/include/" + file, 'w') as new_file:
					# write the data
					new_file.write(allContent)
	


	
