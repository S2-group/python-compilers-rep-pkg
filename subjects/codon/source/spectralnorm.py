from math import sqrt
import sys


def eval_A(i, j):
  return 1.0/((i+j)*(i+j+1)/2+i+1)

def eval_A_times_u(N, u, Au):
  for i in range(N):  
    Au[i] = 0
    for j in range(N):
        Au[i] += eval_A(i,j) * u[j]    

def eval_At_times_u(N, u, Au):
  for i in range(N):  
    Au[i] = 0.
    for j in range(N): Au[i]+=eval_A(j,i)*u[j]   

def eval_AtA_times_u(N, u, AtAu):
  v=[0.]*N; eval_A_times_u(N,u,v); eval_At_times_u(N,v,AtAu)

def main(n):
  u=[1.]*n
  v=[0.]*n

  for i in range(10):
    eval_AtA_times_u(n,u,v)
    eval_AtA_times_u(n,v,u)

  vBv=vv=0.

  for i in range(n):
    vBv+=u[i]*v[i]; vv+=v[i]*v[i]  

  result = float(int(sqrt(vBv / vv) * 10**9)) / 10**9

  # Print with full precision
  print(f"{result:.9f}")

if __name__ == '__main__':
    number = int(sys.argv[1])
    main(number)
