import GudhiExtension.filtration_manipulation as fm
import GudhiExtension.column_algo.column_algo_outs as cao
import GudhiExtension.column_algo.column_algorithm as ca

filtration = [[0], [1], [2], [4], [3], [7], [6], [5],
                                [0, 1], [0, 2], [0, 4]]


mat = ca.build_boundary_matrix_from_filtration(filtration)
_, red = ca.column_algorithm_with_reduced_return(mat)

max_len = max([len(i) for i in filtration])

xticklabels = [-1] + [elem for elem in filtration if len(elem) > 1]
yticklabels = [-1] + [elem for elem in filtration if len(elem) < max_len]

cao.mat_visualization(mat,xticklabels,yticklabels)
