from vmtk import vmtkscripts

def image_reader(fileName):
    reader = vmtkscripts.vmtkImageReader()
    reader.InputFileName = fileName
    reader.Execute()
    return reader.Image

def image_writer(image, fileName):
    writer = vmtkscripts.vmtkImageWriter()
    writer.Image = image
    writer.OutputFileName = fileName
    writer.Execute()
    print(f'image wrote to location {fileName}')
    return

def surface_reader(fileName):
    reader = vmtkscripts.vmtkSurfaceReader()
    reader.InputFileName = fileName
    reader.Execute()
    return reader.Surface

def surface_writer(surface, fileName):
    writer = vmtkscripts.vmtkSurfaceWriter()
    writer.Surface = surface
    writer.OutputFileName = fileName
    writer.Execute()
    print(f'surface wrote to loaction {fileName}')
    return


def vessel_enhancer(image, method, iterations, diffusionIterations):
    enhance = vmtkscripts.vmtkImageVesselEnhancement()
    enhance.Image = image
    enhance.Method = method
    enhance.NumberOfIterations = iterations
    enhance.NumberOfDiffusionSubIterations = diffusionIterations
    enhance.Execute()
    return enhance.Image

def image_cast(image):
    caster = vmtkscripts.vmtkImageCast()
    caster.Image = image
    caster.OutputType = "float"
    caster.Execute()
    return caster.Image

def initialization_image(image, lowerThresh, upperThresh):
    initialization = vmtkscripts.vmtkImageInitialization()
    initialization.Image = image
    initialization.Interactive = 0
    initialization.Method = 'threshold'
    initialization.LowerThreshold = lowerThresh
    initialization.UpperThreshold = upperThresh
    initialization.Execute()
    print(f'image intialized with lower threshold: {lowerThresh} upper threshold: {upperThresh}')
    return initialization.InitialLevelSets

def levelset_segmentation(image, initialLevelSets, featureImage, propagation, curvature, advection, iterations):
    levelset = vmtkscripts.vmtkLevelSetSegmentation()
    levelset.Image = image
    levelset.InitialLevelSets = initialLevelSets
    levelset.FeatureImage = featureImage
    levelset.PropagationScaling = propagation
    levelset.CurvatureScaling = curvature
    levelset.AdvectionScaling = advection
    levelset.NumberOfIterations = iterations
    levelset.Execute()
    print(f'level set evolation occured with: \n',
          f'    propagtion scaling: {propagation} \n',
          f'    curvature scaling: {curvature} \n',
          f'    advection scaling: {advection} \n',
          f'    number of iterations: {iterations}')
    return levelset.LevelSets

def marching_cubes(levelSets, level=0.0):
    marching = vmtkscripts.vmtkMarchingCubes()
    marching.Image = levelSets
    marching.Level = level
    marching.Execute()
    print(f'marching cubes occured with extration level: {level}')
    return marching.Surface
