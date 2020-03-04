#whatever needed to get the data to a table version
import pandas as pd 
import numpy as np
from mlxtend.frequent_patterns import apriori
mat = {}

symptoms = pd.read_csv('diagnosis_analysis/sym_t.csv')
symptoms = symptoms.set_index('syd')
diagnosis = pd.read_csv('diagnosis_analysis/dia_t.csv')
diagnosis = diagnosis.set_index('did')
match = pd.read_csv('diagnosis_analysis/diffsydiw.csv')
match = match.set_index('did')
match = match.drop('wei', axis = 1)

column = []
count = 0
for i, row in match.iterrows(): 
    if not np.isnan(row['syd']):
        count += 1
        column.append(symptoms.at[int(row['syd']),'symptom'])
    else: 
        column.append('')
match['syd_t'] = column


for i, row in match.iterrows(): 
    if row['syd_t'] == 'NaN': 
        continue
    if i in mat: 
        mat[i].append(row['syd_t'])
    else: 
        mat[i] = [row['syd_t']]
        
print(type(mat))
diag_symp = {}
for key in mat:
    if not np.isnan(key):
        diag_symp[diagnosis.at[int(key),'diagnose']] = mat[key]


#clean up nan values in the symptoms
for diag in diag_symp:
    indextoremove = []
    for i,sym in enumerate(diag_symp[diag]):
        #if diag == "Lung abscess\x0bcollection of pus":
        #    print(diag_symp[diag])
        #    print("Symptom:",sym)
        #    print("type:",type(sym))
        #    print(pd.isna(sym))
        #    print(sym == "nan")
        if pd.isna(sym) or sym == "nan":
            indextoremove.append(i)
            #del diag_symp[i]
            # if diag == "Lung abscess\x0bcollection of pus":
            #     print("Before",diag_symp[diag])
            # #diag_symp[diag].remove(sym)
            # if diag == "Lung abscess\x0bcollection of pus":
            #     print("after",diag_symp[diag])
        #print("i:",i)
        #print("length:",len(diag_symp[diag]))
        if i == len(diag_symp[diag])-1:
            #end of loop, remove
            #print("INDEXES TO REMOVE",indextoremove)
            for index in reversed(indextoremove):
                del diag_symp[diag][index]

#Generate symptom to diagnosis table
diccy = {}

for diag in diag_symp:
    veccy = []
    for x in symptoms['symptom']:
        if x in diag_symp[diag]:
            veccy.append(True)
        else:
            veccy.append(False)
    diccy[diag] = veccy
  
    
testtttdf = pd.DataFrame(diccy)
testtttdf["Allsymptoms"] = [x for x in symptoms['symptom']]
testtttdf = testtttdf.set_index("Allsymptoms")
testtttdf = testtttdf.T



#print("YO THE SHAPE:",testtttdf.shape)

#And this is the apriori part. I'm thinking of immediately eliminating all rows whose values is false
#And keep apriori-ing it
def apriit(conf_symptoms):
	#print("YO THE SHAPE PER APRIT CALL:",testtttdf.shape)
	suggestions = {}
	print("IS SUGGESTIONS CONTAMINATED", suggestions)
	tablecopy = testtttdf.copy()
	#we filter our DF according to the symptoms that we have atm
	for s in conf_symptoms:
		tablecopy.drop(tablecopy[tablecopy[s] == False].index,inplace=True)
	print("table",tablecopy.shape)
	aprioriedtable = apriori(tablecopy, min_support=0.6, use_colnames=True)
	#print("Aprioried shape",aprioriedtable.shape)
	for i,frozensets in enumerate(aprioriedtable["itemsets"]):
		print("LE SET",frozensets)
		print("FROZENSET LENGTH",len(frozensets))
		print("MA CONFIRMED LENGTH",len(conf_symptoms))
		if len(frozensets) >= len(conf_symptoms):
			#print("HANDLE THIS")
			for frozenitem in frozensets:
				#print("so the frozenitem in that set is",frozenitem)
				if frozenitem not in conf_symptoms:
					#print("ADD NEW SUGGESTIONS WHEEE")
					suggestions[str(frozenitem)] = aprioriedtable["support"][i]
	print("WAT AM I RETURNING", suggestions)
	return suggestions

def getdiagnosed(conf_symptoms):
	tablecopy = testtttdf.copy()
	#we filter our DF according to the symptoms that we have atm
	for s in conf_symptoms:
		tablecopy.drop(tablecopy[tablecopy[s] == False].index,inplace=True)
	diagnosisstat = {}
	possiblediags = tablecopy.T.columns.values
	for diag in possiblediags:
		symps = diag_symp[diag]
		totalmatch = 0.0
		total = len(symps)
		for x in conf_symptoms:
			if x in symps:
				totalmatch += 1
		diagnosisstat[diag] = "{0:.0%}".format(totalmatch/total)
	return diagnosisstat



