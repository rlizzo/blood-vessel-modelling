import numpy as np

def _get_vector_indices(image, return_label=False):
    
        if return_label == False:
            
        
            binary_image = np.copy(image)
            binary_image[binary_image >= 1] = 1

            tuple_vector_indices = np.where(binary_image == 1)
            vector_indices = np.zeros(shape=(tuple_vector_indices[0].shape[0], len(tuple_vector_indices)))
            vector_indices[:, 0] = tuple_vector_indices[0]
            vector_indices[:, 1] = tuple_vector_indices[1]
            vector_indices[:, 2] = tuple_vector_indices[2]

            return vector_indices
        
        elif return_label == True:
            
            unique_labels = np.unique(image[np.nonzero(image)])
            
            vi = []
            lb = []
            for labelId in unique_labels:
                indices = np.stack(np.where(image == labelId)).T
                lab = np.zeros(shape=indices.shape[0])
                vi.append(indices)
                lb.append(labelId)
            
            return vi, lb