filepath = 'Results/19_346_10_2D_alpha_complex_collaps_NS.txt'
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       if(line[0] == 'b'):
           if(line[2:-2] != '{(<1 0 0> 1)}'):
               print(line[2:-2])
               print(cnt)
       line = fp.readline()
       cnt += 1
   print("DONE")