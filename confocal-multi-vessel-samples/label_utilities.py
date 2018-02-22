import numpy as np
from scipy.sparse import csr_matrix

def get_indices_sparse(data):
    '''find indices of array corresponding to labels in a dense matrix
    
    designed to recieve a 3D dense array with multiple repeate values in the form
    of "labels" for a mask data. 
    
    returns an ordered list of length equal to the number of labels in the input array
    list indexes correspond to the label number. ie accessing out[15] gives the indices
    where label 15 is found. 
    '''
    M = _compute_sparse_matrix(data)
    return [np.unravel_index(row.data, data.shape) for row in M]

def _compute_sparse_matrix(data):
    '''private function to construct the sparse csr matrix from a 3d data set
    '''
    cols = np.arange(data.size)
    return csr_matrix((cols, (data.ravel(), cols)),
                      shape=(data.max() + 1, data.size), dtype=np.int32)