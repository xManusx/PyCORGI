import numpy as np


def similarity(vec1, vec2):
    return np.inner(vec1, vec2)/(np.linalg.norm(vec1), np.linalg.norm(vec2))


def recognition(templates, features):
    ret = np.array((features.size[0], templates.size[0]))
    for i in range(features.size[0]):
        for j in range(templates.size[0]):
            ret[i][j] = similarity(features[i], templates[j])

    return ret
