import numpy as np


class lens():
    def __init__(self, R:float, n_lenses:float, n_air:float = 1) -> None:
        self.R = R
        self.n_lenses = n_lenses
        self.n_air = n_air

    ################## get lens matrices #################
    def amit_get_mat(self, amit_from:str = 'in'):
        D = -(self.n_lenses-self.n_air)/self.R
        D = D if amit_from == 'in' else -D # out
        mat = np.array([[1, D],
                        [0, 1]])
        return mat
    
    ################## get output vecs #################
    def amit(self, vec, amit_from:str = 'in'):
        input_vec = np.array(vec)
        mat = self.amit_get_mat(amit_from)
        # return vec(a_out, x_out)
        return mat @ input_vec

    
class thin_lenses():
    def __init__(self, R_left: float, R_right: float, n_lenses: float, n_air: float = 1) -> None:
        """
        Constructor method for thin_lenses.

        Parameters:
        - R_left (float): Radius of the left surface of the lens.
        - R_right (float): Radius of the right surface of the lens.
        - n_lenses (float): Refractive index of the lenses material.
        - n_air (float): Refractive index of air (default is 1).
        """
        self.n_lenses, self.n_air = n_lenses, n_air
        self.left_lens = lens(R_left, n_lenses, n_air)
        self.right_lens = lens(R_right, n_lenses, n_air)

    def focal_length(self):
        n_lens, n_air, R_left, R_right = self.n_lenses, self.n_air, self.left_lens.R, self.right_lens.R
        try:
            f = 1 / ((n_lens - n_air) * (1/R_left - 1/R_right))
            return f
        except ZeroDivisionError:
            print("Error: Division by zero. Check the values of R and R_prime.")
            return None
    
    def amit(self, vec, amit_from:str = 'left'):
        """
        Simulates the propagation of light through the thin lenses.

        Parameters:
        - vec: vec(a, x), can be list of np.

        Returns:
        - Output vector representing the propagated light.
        """
        input_vec = np.array(vec)
        if amit_from == 'left':
            mat_in = self.left_lens.amit_get_mat('in')
            mat_out = self.right_lens.amit_get_mat('out')
        else:          # right
            mat_in = self.right_lens.amit_get_mat('in')
            mat_out = self.left_lens.amit_get_mat('out')
        return mat_out @ mat_in @ input_vec


if __name__ == "__main__":
    print('part 1')
    lens1 = thin_lenses(200, -100, 1.5)
    f1 = -lens1.amit((0, 1), 'left')[0]**-1
    print(f'f1 = {f1}')

    lens2 = thin_lenses(100, -200, 1.5)
    f2 = -lens2.amit((0, 1), 'left')[0]**-1
    print(f'f2 = {f2}')

    lens3_1 = thin_lenses(200, -100, 1.5)
    lens3_2 = thin_lenses(-100, np.infty, 1.5)
    out_3_1 = lens3_1.amit((0, 1), 'left')
    out_3_2 = lens3_2.amit(out_3_1, 'left')
    f3 = -out_3_2[0]**-1
    print(f'f3 = {f3}')

    lens4_1 = thin_lenses(-100, np.infty, 1.5)
    lens4_2 = thin_lenses(200, -100, 1.5)
    out_4_1 = lens4_1.amit((0, 1), 'left')
    out_4_2 = lens4_2.amit(out_4_1, 'left')
    f4 = -out_4_2[0]**-1
    print(f'f4 = {f4}')

    print('part 2')
    s0 = 500
    calculate_s_tag = lambda f, s0: ((f**-1) - (s0**-1)) ** -1
    print(f's_1 = {calculate_s_tag(f1, s0)}mm')
    print(f's_2 = {calculate_s_tag(f2, s0)}mm')
    print(f's_3 = {calculate_s_tag(f3, s0)}mm')
    print(f's_4 = {calculate_s_tag(f4, s0)}mm')



