# Vessel Modeling

# Viewing the Data
## A 2D View of the Data

I used a volume data view in order to take a look at the data sets in 3D, rather than using the standard planar views. While I was actually exploring the data in 3D, the screenshot below is taken from the top of the Z (depth) axis, and might be thought of as similar to a maximum intensity projection from the XY plane. While this looks fine, we see a limitation of the modality when viewed from the side. There is significant blurring along the z direction. 

![Raw dataset viewed from the XY plane](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187206471_Top-Down-View.png)
![Raw Dataset Viewed from the XZ plane](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187206524_Side-View.png)



## A 3D View of the Data
https://www.dropbox.com/s/e6c15qfdl0qhv1j/3DVolume.mp4?dl=0

# Isolating Structures from the Dataset
## Thresholding

In this first pass, I used a simple thresholding scheme to extract the desired regions of the 3D volume. The image volume has intensity bounds in the range of 0-255. After a quick look, i could see that most of the vessel intensities lied above 100, so I set that as a starting lower bound. 

**The problem with thresholding:**

- setting a low value can include all of the desired structure, but it also tends to include noise and random variations
- setting a high threshold reduces noise, but it can fail to include some of the desired structures

This is observed in the following screenshots

![The 3D volume displaying the raw data to be thresholded. We need to determine which “shades of red” we actually care about](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187206707_ThresholdCallout.png)
![A 2D slice of a thresholded volume which highlights that by choosing a low threshold, random noise can be generated](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187193357_InitializationPlane.png)


**How significant an impact does the lower bound value have?**

In order to figure out how bad this problem is, I analyzed each data set 7 times, varying the lower bound threshold in each run. These variations set the lower bound at: 100, 125, 150, 175, 200, 225, and 250.

Unfortunately, there is quite a significant impact. I haven’t done a formal analysis yet, but for an “at a glance” overview, the following image shows the extracted masks overlaid on each-other. The yellow structures are what appear when a lower bound of 125 is set, the red structures are what is extracted when a lower bound of 250 is set. 


![Demonstration that the masks received from setting various thresholds significantly impact the result of the generated mask.](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187205727_Threshold-Differences.png)


***Technical Note:*** the image shown above is not the final segmented surface, it is simply a 3D rendering of the voxel masks generated by thresholding. 


## Level Set Evolution

A common scheme I employ is to take my initial pass at a segmentation (via thresholding in this case) and feed the binary mask as an input to a gradient based geodesic active contours level set evolution algorithm. The goal is to ensure that the segmented mask fits the image boundaries as closely as possible. 

Essentially, this method:

1. Takes the segmentation mask and converts it to an implicit surface in 4D.
2. Takes the gradient of the initial (base) image which the mask was generated from.
3. Defines a time dimension
4. Evolves the zero-level isosurface across time, modifying the zero-level contour each timestep in relation to it’s position relative to the gradient image. 
5. Returns a new 3D image volume with floating point values between -1 and 1, where the zero level refers to where the algorithm evolved the boundaries of the mask to. 

This is demonstrated in the figure below (for a 2d example). The image was taken from http://profs.etsmtl.ca/hlombaert/levelset/, which is a great explanation of the method.


![](https://www.dropbox.com/s/o4bz4puolguhnec/LevelSetDemo.png?raw=1)


For our project the following screenshots demonstrate the effect that this method has on the cleanliness of the output mask: 


![A 2D slice of a thresholded volume which highlights that by choosing a low threshold, random noise can be generated](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187193357_InitializationPlane.png)
![A 2D slice showing how desired regions are more uniformly generated after the level set segmentation](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187193430_LevelSetsCalloutImage.png)


There are a number of important parameters (along with variations) of the level sets algorithm. For the geodesic active contours variation these are: 

- Curvature scaling
- Advection scaling
- Propagation scaling
- Number of timesteps

By far the most important parameter is the number of timesteps, as setting this too low will not allow the algorithm to converge on a solution. Unfortunately, due to the nature of the images provided here (I won’t go into the details here, just take my experience for what it’s worth), the computational time is large for each iteration (roughly 10 seconds per timestep). 

If I have simpler images, I would just set the number of timesteps to something like 10,000 and call it a day, but that’s not really going to work for this. To determine how long it took us to reach convergence, I ran 6 variations of the algorithm for each dataset and each threshold bound. These were set to run at: 2, 10, 50, 100, and 300 timesteps.

The value set at 300 seemed to perform the best, so I’ll have to run more tests and a formal analysis in the future in order to figure out where the computational cost vs accuracy boundary is. 

This is what the level set algorithm produces (a floating point valued array with values between -1 and 1):

![](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187193810_Initialization-Volume.png)



## Surface Generation

I used a standard marching cubes algorithm to generate surface representations from the output level sets.  performing this operaiton highlighted the blurring issue that I mentioned at the start. When viewing images from the XY plane, things look absolutly great!

![](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187204222_SurfaceTopDown.png)


However, when we look at a side view, we see significant blurring along the Z direction. 

![](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187204468_SideViewBlurringCallout.png)

## Cleaning the surface. 

The data processing up to this point was really quick, dirty (let alone uninformed by your expertise). The output surface is extremly noisy, and will not lend itself well to further analysis via centerline extraction or region classification. I manually cleaned up one of the surfaces to show the difference between what we got on a first pass, and what we’ll want in an ideal scenario. These are displayed in the images below. 

![](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187204512_SurfaceSideView.png)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187193655_CleanedSurfaceComparison.png)

![](https://d2mxuefqeaa7sj.cloudfront.net/s_26936E64AD039002896E90F8B2B8C76B73EFF048D7FA27BA4F09840048736DDE_1519187204564_SurfaceCleaned.png)



# Next Steps
## Questions:
1. what are the structures we actually want to isolate from this volumes? 
2. what methods were used to aquire the data? what proteins are the fluorescent markers attaching to? what is their relationship to the disease?
3. what types of parameters should we plan to calculate? (this will affect the structure of the file data arrays)


## Methods:
1. preprocess images appropriatly
2. build auto view and comparison utilities

