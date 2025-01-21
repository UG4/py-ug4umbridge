#!/usr/bin/env python

import sys
sys.path.append(".")

import modsimtools as util
import ug4py.pyugcore as ug4
import ug4py.pyconvectiondiffusion as cd

# import ug4py.pylimex as limex

# ## Assemble linear system:
def SolveProblem(domainDisc, approxSpace):
    A = ug4.AssembledLinearOperatorCPU1(domainDisc)
    x = ug4.GridFunction2dCPU1(approxSpace)
    b = ug4.GridFunction2dCPU1(approxSpace)

    # x.clear(0.0)
    domainDisc.assemble_linear(A, b)
    domainDisc.adjust_solution(x)


    # ## Solve linear system

    solver=ug4.LUCPU1()
    solver.init(A, x)
    solver.apply(x, b)
    
    # For debug.
    # solFileName = "fem01_solution_u"
    # ug4.WriteGridFunctionToVTK(x, solFileName)
    
    return x


# ## Problem definition

class CookieProblem:
    def __init__(self):
        self.myGridName= "cookie4.ugx" # grids/unit_square_tri.ugx",
        self.myNumRefs= 3
        self.mySubsets = {"Inner", "Cookie1", "Cookie2", "Cookie3", "Cookie4"}
        self.diffusionCoeffs = [1.0, 0.1, 1.0, 1.0, 0.1]
    
    def __init__(self, gridName, numRefs, diffusionCoeffs):
        self.myGridName=gridName
        self.myNumRefs= numRefs
        self.mySubsets = {"Inner", "Cookie1", "Cookie2", "Cookie3", "Cookie4"}
        self.diffusionCoeffs = diffusionCoeffs

# Boundary conditions are defined using callback:
#def myDirichletBndCallback(x, y, t) :
#    if (y==1) :
#        return True, 0.0
#    elif (y==0) :
#        return True, math.sin(math.pi*1*x)
#    else :
#        return False, 0.0
    
    def CreateApproxSpace(self):

    # ## Computational domain
        dom = util.CreateDomain(self.myGridName, self.myNumRefs, self.mySubsets)

        # ## Create ansatz space
        approxSpaceDesc = dict(fct = "u", type = "Lagrange", order = 1)
        approxSpace = util.CreateApproximationSpace(dom, approxSpaceDesc)
        return approxSpace




    # ## Discretization
    def CreateDomainDisc(self, approxSpace):
        elemDisc0 = cd.ConvectionDiffusionFE2d("u", "Inner")
        elemDisc0.set_diffusion(self.diffusionCoeffs[0])
        elemDisc0.set_source(0.0)
    
        elemDisc1 = cd.ConvectionDiffusionFE2d("u", "Cookie1")
        elemDisc1.set_diffusion(self.diffusionCoeffs[1])
        elemDisc1.set_source(0.0)


        elemDisc2 = cd.ConvectionDiffusionFE2d("u", "Cookie2")
        elemDisc2.set_diffusion(self.diffusionCoeffs[2])
        elemDisc2.set_source(0.0)

        elemDisc3 = cd.ConvectionDiffusionFE2d("u", "Cookie3")
        elemDisc3.set_diffusion(self.diffusionCoeffs[3])
        elemDisc3.set_source(0.0)


        elemDisc4 = cd.ConvectionDiffusionFE2d("u", "Cookie4")
        elemDisc4.set_diffusion(self.diffusionCoeffs[4])
        elemDisc4.set_source(0.0)


        #Create object for **boundary condiditions**:
        dirichletBND = ug4.DirichletBoundary2dCPU1()
        dirichletBND.add(1.0, "u", "North")
        dirichletBND.add(0.0, "u", "South")

        # Both objects contribute to the **domain discretization**, which serves as a container for the full problem:
        domainDisc = ug4.DomainDiscretization2dCPU1(approxSpace)
        domainDisc.add(elemDisc0)
        domainDisc.add(elemDisc1)
        domainDisc.add(elemDisc2)
        domainDisc.add(elemDisc3)
        domainDisc.add(elemDisc4)

        domainDisc.add(dirichletBND)
        return domainDisc


# ## Output of results
    def ComputeQoI(self):
    
        approxSpace=myProblem.CreateApproxSpace()
        domainDisc=myProblem.CreateDomainDisc(approxSpace)

        x=SolveProblem(domainDisc, approxSpace)
    
        fluxN=ug4.IntegrateNormalGradientOnManifold(x, "u", "North", "Inner")
        fluxS=ug4.IntegrateNormalGradientOnManifold(x, "u", "South", "Inner")

        print(fluxN)
        print(fluxS)
        return [fluxN, fluxS]



# Example call
myProblem = CookieProblem("cookie4.ugx", 3, [1.0, 0.1, 1.0, 1.0, 0.1])
qoi=myProblem.ComputeQoI()


#ug4.SaveVectorForConnectionViewer(x, solFileName + ".vec")


# In[16]:
#result = pyvista.read(solFileName + ".vtu")
#result.plot(scalars="u", show_edges=True, cmap='jet')


# b) Right hand side $b$ and matrix $A$

#solFileName = "tmp/fem01_rhs_b"
#ug4.WriteGridFunctionToVTK(b, solFileName)
#ug4.SaveVectorForConnectionViewer(b, solFileName + ".vec")
#ug4.SaveMatrixForConnectionViewer(x, A, "tmp/fem01_matrix_A.mat")


# In[18]:


#result = pyvista.read(solFileName + ".vtu")
#result.plot(scalars="u", show_edges=True, cmap='jet')

