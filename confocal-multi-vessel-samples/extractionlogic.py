
# coding: utf-8

# In[ ]:


from vmtk import vmtkscripts
from extractionmethods import initialization_image, levelset_segmentation, marching_cubes, image_writer, surface_writer, image_reader
import numpy as np
import os
import json
from joblib import Parallel, delayed


# In[ ]:


datasetDir = os.path.join(os.getcwd(), 'multiphoton-sample-2')
datasetBaseDir = os.path.join(datasetDir, 'base')
datasetBaseImagePath = os.path.join(datasetBaseDir, 'sstack1_514um_2umstep_08xyspacing_.mha')

datasetDerivedDir = os.path.join(datasetDir, 'derived')
if not os.path.exists(datasetDerivedDir):
    os.makedirs(datasetDerivedDir)
    print(f'created derived dataset directory at: {datasetDerivedDir}')


# In[ ]:


def run_analysis(datasetDerivedDir, lowerThreshValue, iterationValue):
    parameterDir = os.path.join(datasetDerivedDir, f'thresh{lowerThreshValue}', f'iterations{iterationValue}')
    if not os.path.exists(parameterDir):
        os.makedirs(parameterDir)

    upperThreshValue = None
    curvature = 0
    propagation = 0
    advection = 1

    image = image_reader(datasetBaseImagePath)
    image_writer(image, os.path.join(parameterDir, 'input-image.vti'))

    init = initialization_image(image, lowerThreshValue, upperThreshValue)
    image_writer(init, os.path.join(parameterDir, 'initialization-image.vti'))

    ls = levelset_segmentation(image, init, curvature, propagation, advection, iterationValue)
    image_writer(ls, os.path.join(parameterDir, 'levelset-image.vti'))

    mc = marching_cubes(ls)
    surface_writer(mc, os.path.join(parameterDir, 'surface.vtp'))

    params = {'initialImagePath': datasetBaseImagePath,
              'parameterDir': parameterDir,
              'lowerThreshValue':lowerThreshValue,
              'upperThreshValue':upperThreshValue,
              'curvatureScaling':curvature,
              'propagation':propagation,
              'advection':advection,
              'iterationValue':iterationValue,
              'processSteps':['read_image', 'initialize_image', 'level_set_evolution', 'marching_cubes']}
    with open(os.path.join(parameterDir, 'parmas.json'), 'w+') as f:
        json.dump(params, f)

    return True
        


# In[ ]:


lowerThreshValues = [100, 125, 150, 175, 200, 225, 250]
iterationValues = [2, 10, 50, 100, 300, 600, 1000]

Parallel(n_jobs=12)(delayed(run_analysis)(datasetDerivedDir, lowThresh, iteration) for lowThresh in lowerThreshValues for iteration in iterationValues)

