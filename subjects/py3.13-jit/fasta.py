from sys import argv

IM = 139968
IA = 3877
IC = 29573

def fastaRand(max, seed):
   seed = (seed * IA + IC) % IM
   return seed, max * seed / IM

ALU = (
  "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGG" 
  "GAGGCCGAGGCGGGCGGATCACCTGAGGTCAGGAGTTCGAGA"
  "CCAGCCTGGCCAACATGGTGAAACCCCGTCTCTACTAAAAAT"
  "ACAAAAATTAGCCGGGCGTGGTGGCGCGCGCCTGTAATCCCA"
  "GCTACTCGGGAGGCTGAGGCAGGAGAATCGCTTGAACCCGGG"
  "AGGCGGAGGTTGCAGTGAGCCGAGATCGCGCCACTGCACTCC"
  "AGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAA" )

IUB = "acgtBDHKMNRSVWY"
HomoSapiens = "acgt"
LINELEN = 60

def repeatFasta(seq, n):
   length = len(seq)
   i = 0
   for i in range(0,n):
      print(seq[i % length])
      if (i % LINELEN == LINELEN - 1): print()      

   if (i % LINELEN != 0): print()  

def randomFasta(seq, probability, n, seed):
   length = len(seq)
   i, j = 0, 0
   for i in range(0,n):
      seed, v = fastaRand(1.0, seed)       
      for j in range(0,length):      
         v -= probability[j]
         if (v<0): break     

      print(seq[i % length])
      if (i % LINELEN == LINELEN - 1): print()      

   if ((i+1) % LINELEN != 0): print()

   return seed

def main(n):
   IUB_P = [
        0.27, 0.12, 0.12, 0.27, 
        0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02 
   ]
   HomoSapiens_P = [
        0.3029549426680,
        0.1979883004921,
        0.1975473066391,
        0.3015094502008
   ]  

   print(">ONE Homo sapiens alu")      
   repeatFasta(ALU, n*2)
   
   print(">TWO IUB ambiguity codes")     
   seed = randomFasta(IUB, IUB_P, n*3, 42)   
   
   print(">THREE Homo sapiens frequency")     
   randomFasta(HomoSapiens, HomoSapiens_P, n*5, seed)

if __name__ == '__main__':
  main(int(argv[1]) if len(argv) > 1 else 1000)