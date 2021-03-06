import os
import itertools
from qutip import *
from numpy import *
from matplotlib.pyplot import *


def integrate(N, h, J, Jx, Jy, Jz, defpos, epsi):

    #
    # Hamiltonian
    #
    # H = - 0.5 sum_n^N h_n sigma_z(n)
    #     - 0.5 sum_n^(N-1) [ Jx_n sigma_x(n) sigma_x(n+1) +
    #                         Jy_n sigma_y(n) sigma_y(n+1) +
    #                         Jz_n sigma_z(n) sigma_z(n+1)]
    #
    si = qeye(2)
    sx = sigmax()
    sy = sigmay()
    sz = sigmaz()

    sx_list = []
    sy_list = []
    sz_list = []
    for n in range(N):
        op_list = [si] * N
        op_list[n] = sx
        sx_list.append(tensor(op_list))
        op_list[n] = sy
        sy_list.append(tensor(op_list))
        op_list[n] = sz
        sz_list.append(tensor(op_list))

    # print("x",sx_list)
    # print("y",sy_list)
    # print("z",sz_list)

    # construct the hamiltonian
    H = 0

    # energy splitting terms
    for n in range(N):
        H += - 0.5 * h[n] * sz_list[n]

    # interaction terms
    for n in range(N - 1):
        H += - 0.5 * Jx[n] * sx_list[n] * sx_list[n + 1]
        H += - 0.5 * Jy[n] * sy_list[n] * sy_list[n + 1]
        H += - 0.5 * Jz[n] * sz_list[n] * sz_list[n + 1]

    H -= epsi*sz_list[defpos]

    # print(H)
    a = H.eigenstates()[1]
    b = H.eigenenergies()
    file = open('data_'+str(J)+'_'+str(epsi),'w+')
    for i in range(0,2**N):
    	# print(a[0].trans())
    	# print(a[i]*a[i].trans())
    	# print(entropy_conditional(a[i]*a[i].trans(),0,2))
    	# print(entropy_linear((a[i]*a[i].trans()).ptrace(0)))
    	# print entropy_vn((a[i]*a[i].trans()).ptrace(0))
    	file.write(str(b[i])+"\t"+str(entropy_vn((a[i]*a[i].trans()).ptrace(0),e))+"\n")
    file.close()


def run():
    os.system("tput reset")
    N = 8         # number of spins
    w = 1
    J = 10.0
    # array of spin energy splittings and coupling strengths. here we use
    # uniform parameters, but in general we don't have too
    # print(ones(N))
    h = 1.0 * 2 * w * ones(N)
    Jz = J * 2 * w * ones(N)
    Jx = J * 1 * w * ones(N)
    Jy = J * 1 * w * ones(N)

    integrate(N, h, J, Jx, Jy, Jz, N/2, 0.5)
    integrate(N, h, J, Jx, Jy, Jz, N/2, 0.5)
    integrate(N, h, J, Jx, Jy, Jz, N/2, 1.0)


if __name__ == "__main__":
    run()
