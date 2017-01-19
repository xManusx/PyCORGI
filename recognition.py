import numpy as np


def similarity(vec1, vec2):
    return np.inner(vec1, vec2)/(np.linalg.norm(vec1) *  np.linalg.norm(vec2))


def recognition(templates, features):
    ret = np.zeros((features.shape[0], templates.shape[0]))
    for i in range(features.shape[0]):
        for j in range(templates.shape[0]):
            test = similarity(features[i], templates[j])
            ret[i][j]  = test
            #print(similarity(features[i], templates[j]))

    return ret
