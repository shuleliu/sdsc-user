#!/usr/bin/env python
################################################################################
#  bundler.py - Pack multiple serial jobs into a single job script
#
#  September 2013              Glenn K. Lockwood, San Diego Supercomputer Center
################################################################################
import os
import sys
import socket

try:
    tasksfile = sys.argv[1]
    TF = open( os.path.abspath(tasksfile), 'r' )
except IOError:
    sys.stderr.write( "Unable to open tasks file %s\n" % tasksfile )

### Initialize MPI information
hostname = socket.gethostname()

if hostname.startswith( 'trestles' ):
    sys.path.append(r'/home/diag/opt/mpi4py/1.2.2/lib64/python2.4/site-packages')
elif hostname.startswith( 'gcn' ) or hostname.startswith( 'gordon' ):
    sys.path.append(r'/opt/amber/bin')

from mpi4py import MPI
comm = MPI.COMM_WORLD
myid = comm.Get_rank()
numprocs = comm.Get_size()

### Read in tasks to be executed
tasks = TF.readlines()
ntasks = len(tasks)
TF.close()

### Launch my assigned task(s)
for i in range(ntasks):
    if myid == (i % numprocs):
        task = tasks[i]
        task.rstrip()
        print "MPI process %d on %s running task [%s]" % (myid, hostname, task.strip())
        os.system(task)
