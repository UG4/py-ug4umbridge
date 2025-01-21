import umbridge
import time
import os

from cookie_problem import CookieProblem

class CookieModel(umbridge.Model):

    def __init__(self):
        super().__init__("forward")

    def get_input_sizes(self, config):
        return [4] # 4 diffusion coeffs

    def get_output_sizes(self, config):
        return [2] # 2 fluxes

    def __call__(self, parameters, config):
        # Sleep for number of milliseconds defined in env var
        # time.sleep(int(os.getenv("TEST_DELAY", 0)) / 1000)

       
        print(parameters)
        print(config)
        
        # Create and solve problem.
        myProblem = CookieProblem("cookie4.ugx", 3, np.append([1.0], parameters))
        qoi=myProblem.ComputeQoI()
        
        return [[qoi]]

    def supports_evaluate(self):
        return True

    def gradient(self,out_wrt, in_wrt, parameters, sens, config):
        return [2*sens[0]]

    def supports_gradient(self):
        return False

cookie = CookieModel()
umbridge.serve_models([cookie], 4242)
