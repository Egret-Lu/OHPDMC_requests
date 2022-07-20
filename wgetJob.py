import os
seedPath='./seedFile'
cwd=os.getcwd()
print(cwd)
if not os.path.exists(seedPath):
    os.makedirs(seedPath)
f= open('seedlist.txt','r')
seed=f.readline()
m=0 #job enumber
n=0 #seed number in job
while (seed):
    if n==0:
        jobFile=open(seedPath+f'/job{m}','w')
        jobFile.write('#!/bin/bash\n')
        jobFile.write(f'#SBATCH -o {cwd}/seedFile/stdout.txt \
        -e {cwd}/seedFile/stderr.txt \
            -j job{m} -t 16:00:00 \
                --mem-per-cpu=1024 \
                    --cpus-per-task 1\n')
        jobFile.write('#SBATCH -A tolugboj_lab -p urseismo\n')
#SBATCH -o /scratch/tolugboj_lab/Prj7_RadonT/3_src/l_src/parDatDwnld/obspy_batch/AK/AK-A19K/stdout.txt                           -e /scratch/tolugboj_lab/Prj7_RadonT/3_src/l_src/parDatDwnld/obspy_batch/AK/AK-A19K/stderr.txt                           -J AK-A19K                          -t 16:00:00                           --mem-per-cpu=1024                           --cpus-per-task 1
#SBATCH -A tolugboj_lab -p urseismo
    jobFile.write('wget '+ seed + '\n')
    seed=f.readline()
    n+=1
    if n>20:
        n=0
        m+=1
        jobFile.close()


        