import unittest
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import riccati_jn, riccati_yn, spherical_jn

from platon import _mie_multi_x

class TestMie(unittest.TestCase):
    def get_num_iters(self, m, x):
        y = np.sqrt(np.real(m * np.conj(m))) * x
        num = 1.25 * y + 15.5

        if y < 1: num = 7.5*y + 9.0
        if y > 100 and y < 50000: num = 1.0625*y + 28.5
        if y > 50000: num = 1.005*y + 50.5

        return 2*int(num)

    def simple_Qext(self, m, x):
        max_n = self.get_num_iters(m, x)
        all_psi, all_psi_derivs = riccati_jn(max_n, x)

        jn = spherical_jn(range(max_n + 1), m*x)
        all_mx_vals = m * x * jn
        all_mx_derivs = jn + m * x * spherical_jn(range(max_n + 1), m * x, derivative=True)
        all_D = all_mx_derivs/all_mx_vals

        all_xi = all_psi - 1j * riccati_yn(max_n, x)[0]

        all_n = np.arange(1, max_n+1)

        all_a = ((all_D[1:]/m + all_n/x)*all_psi[1:] - all_psi[0:-1])/((all_D[1:]/m + all_n/x)*all_xi[1:] - all_xi[0:-1])
        all_b = ((m*all_D[1:] + all_n/x)*all_psi[1:] - all_psi[0:-1])/((m*all_D[1:] + all_n/x)*all_xi[1:] - all_xi[0:-1])

        all_terms = 2.0/x**2 * (2*all_n + 1) * (all_a + all_b).real
        Qext = np.sum(all_terms[~np.isnan(all_terms)])
        return Qext

    def test_real_refractive_index(self):
        radius = 1e-6
        m = 2.1
        wavelengths = np.load("platon/data/wavelengths.npy")
        xs = 2*np.pi*radius/wavelengths
        Qext = _mie_multi_x.get_Qext(m, xs)
        simple_Qext = np.array([self.simple_Qext(m, x) for x in xs])

        #Make sure fiducial Qext calculation agrees with simple version
        #plt.plot(xs, Qext)
        #plt.plot(xs, simple_Qext)
        #plt.show()
        self.assertTrue(np.allclose(Qext, simple_Qext))


    def test_complex_refractive_index(self):
        radius = 1e-6
        m = 1.33 - 0.1j
        wavelengths = np.load("platon/data/wavelengths.npy")
        xs = 2*np.pi*radius/wavelengths
        Qext = _mie_multi_x.get_Qext(m, xs)
        simple_Qext = np.array([self.simple_Qext(m, x) for x in xs])

        lx_mie_Qext = np.loadtxt("tests/testing_data/lx_mie_output.dat", unpack=True)[4]

        #Make sure our simple calculation agrees with LX-MIE
        self.assertTrue(np.allclose(simple_Qext, lx_mie_Qext))

        #Make sure fiducial Qext calculation agrees with simple version
        self.assertTrue(np.allclose(Qext, simple_Qext))
        #plt.plot(xs, Qext)
        #plt.plot(xs, lx_mie_Qext)
        #plt.plot(xs, simple_Qext)
        #plt.show()

    def test_lx_mie_values(self):
        # Check values reported in Kitzmann & Heng 2017
        Qexts = _mie_multi_x.get_Qext(10 - 10j, [0.001, 0.1, 1, 100, 1000, 2e4, 1e6])
        expected = [6.0020755e-5, 3.2039088e-2, 2.53299308, 2.07112433, 2.02426046, 2.00361474, 2.00021914]
        self.assertTrue(np.allclose(Qexts, expected))

        Qexts = _mie_multi_x.get_Qext(1.5 - 1j, [1e2, 1e4])
        expected = [2.09750176, 2.00436771]
        self.assertTrue(np.allclose(Qexts, expected))

        Qexts = _mie_multi_x.get_Qext(1.33 - 1e-5j, [1e2, 1e4])
        expected = [2.10132071, 2.00408893]
        self.assertTrue(np.allclose(Qexts, expected))

        Qexts = _mie_multi_x.get_Qext(0.75, [10, 1e3, 1e4])
        expected = [2.23226484, 1.99790818, 2.00125518]
        self.assertTrue(np.allclose(Qexts, expected))
        

if __name__ == '__main__':
    unittest.main()
