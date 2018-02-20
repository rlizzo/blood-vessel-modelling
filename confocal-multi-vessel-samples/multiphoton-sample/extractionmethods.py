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

def surface_writer(surface, fileName):
    writer = vmtkscripts.vmtkSurfaceWriter()
    writer.Surface = surface
    writer.OutputFileName = fileName
    writer.Execute()
    print(f'surface wrote to loaction {fileName}')
    return

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

def levelset_segmentation(image, initialLevelSets, propagation, curvature, advection, iterations):
    levelset = vmtkscripts.vmtkLevelSetSegmentation()
    levelset.Image = image
    levelset.InitialLevelSets = initialLevelSets
    levelset.PropagationScaling = propagation
    levelset.CurvatureScaling = curvature
    levelset.AdvectionScaling = advection
    levelset.NumberOfIterations = iterations
    levelset.Execute()
    print(f'level set evolation occured with: \n',
          '    propagtion scaling: {propagation} \n',
          '    curvature scaling: {curvatue} \n',
          '    advection scaling: {advection} \n',
          '    number of iterations: {iterations}')
    return levelset.LevelSets

def marching_cubes(levelSets, level=0.0):
    marching = vmtkscripts.vmtkMarchingCubes()
    marching.Image = levelSets
    marching.Level = level
    marching.Execute()
    print(f'marching cubes occured with extration level: {level}')
    return marching.Surface
