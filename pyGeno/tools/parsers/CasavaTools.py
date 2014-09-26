import gzip
import pyGeno.tools.UsefulFunctions as uf

class SNPsTxtEntry(object) :

	def __init__(self, lineNumber, snpsTxtFile) :
		self.snpsTxtFile = snpsTxtFile
		self.lineNumber = lineNumber
		self.values = {}
		sl = snpsTxtFile.data[lineNumber].replace('\t\t', '\t').split('\t')
		
		self.values['chromosomeNumber'] = sl[0].upper().replace('CHR', '')
		#first column: chro, second first of range (identical to second column)
		self.values['start'] = int(sl[2])
		self.values['end'] = int(sl[2])+1
		self.values['bcalls_used'] = sl[3]
		self.values['bcalls_filt'] = sl[4]
		self.values['ref'] = sl[5]
		self.values['QSNP'] = int(sl[6])
		self.values['alleles'] = uf.encodePolymorphicNucleotide(sl[7]) #max_gt
		self.values['Qmax_gt'] = int(sl[8])
		self.values['max_gt_poly_site'] = sl[9]
		self.values['Qmax_gt_poly_site'] = int(sl[10])
		self.values['A_used'] = int(sl[11])
		self.values['C_used'] = int(sl[12])
		self.values['G_used'] = int(sl[13])
		self.values['T_used'] = int(sl[14])
	
	def __getitem__(self, i):
		return self.values[i]
	
	def __setitem__(self, i, v) :
		self.values[i] = v
		
	def __str__(self):
		return str(self.values)
	
class SNPsTxtFile(object) :
	
	def __init__(self, fil, gziped = False) :
		self.reset()
		if not gziped :
			f = open(fil)
		else :
			f = gzip.open(fil)
		
		for l in f :
			if l[0] != '#' :
				self.data.append(l)

		f.close()

	def reset(self) :
		self.data = []
		self.currentPos = 0
	
	def __iter__(self) :
		self.currentPos = 0
		return self
	
	def next(self) :
		if self.currentPos >= len(self) :
			raise StopIteration()
		v = self[self.currentPos]
		self.currentPos += 1
		return v

	def __getitem__(self, i) :
		if self.data[i].__class__ is not SNPsTxtEntry :
			self.data[i] = SNPsTxtEntry(i, self)
		return self.data[i]
	
	def __len__(self) :
		return len(self.data)