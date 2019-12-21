from GudhiExtension.alpha_complex_wrapper import alpha_complex_wrapper

if __name__ == "__main__":

    points = [[0.26769923355618297, 0.45240304147542876],
              [0.9598744928467646, 0.3782953015168027],
              [0.25428150106964686, 0.7139898543145881],
              [0.1660551512734323, 0.14300196258566045],
              [0.7420940369653124, 0.20982985342951765]]

    alpha_complex = alpha_complex_wrapper(points)
    print(alpha_complex.get_all_connected_filtration_steps())