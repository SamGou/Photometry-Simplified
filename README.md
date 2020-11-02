# Photometry Simplified
 PS is a tool which simplifies (as the name suggests) the differential photometry process but also the production of colour-magnitude diagrams for cluster ageing**. It was created to be used with a few other pieces of software:
- AstroImageJ (AIJ)
- TOPCAT
- Excel*

*_The aim of PS is to be a better alternative to current amateur photometry approaches and as such it is important that it and all of the supporting software are free. AstroImageJ and TOPCAT are both free, however Excel isn't. Hence, in the future it will not be required._

**_Note: While PS is used for cluster ageing in this example, it can be used for any photometric measurements_

## What does PS do exactly?
 PS was made to simplify and speed the differential aperture photometry process and the production of colour-magnitude diagrams. This is achieved by automation of the most time consuming steps of photometry.

Currently, the most prevalent method of star selection is to randomly choose stars in your image one by one, adjusting the aperture size for each one. This is a long and tedious process and it also involves substantial human error as fainter stars can be easily missed. The calculations afterwards have to also be done in Excel, which slows the whole photometry process down even more. Furthermore, applying the complicated conversion functions in Excel and performing differential photometry is also error-prone. 

PS solves those issues by providing automated cluster star selection as well as automatic photometric filter conversions and magnitude calculations. The automation directly translates into better results, since we are not limited by how many data points we can have. **PS works with Johnson-Cousins photometric filters ONLY! Currently the two supported Johnson's filters are (B & V) and (B & R)**

## Usage
  After having imaged your cluster of choice, we can begin the photometric process. For accurate calculations, we need to use a calibrated image. In this example, we will be using a calibrated frame of the Messier 34 (M34) cluster. Calibration instructions can be found [here](http://slittlefair.staff.shef.ac.uk/teaching/phy217/lectures/instruments/L13/).

<img src="https://github.com/SamGou/Photometry-Simplified/blob/master/Images/M34_after_calib.jpg" width="50%">

_The images were taken at Queen Mary's University in London (specifications of the telescope can be found [here](https://github.com/SamGou/Photometry-Simplified/blob/master/Images/Files/STXL_6303-39815.pdf))_

Next step we need to do is to locate our image on the night sky and add that information to the image's metadata. This is known as plate solving. [Astrometry.net](http://nova.astrometry.net/) has a great tool for exactly this purpose. Upload your image and download the plate solved .fits file. This is the end of the image alterations.

 We now need to seperate our cluster members from the background stars. This is done solely with [TOPCAT](http://www.star.bris.ac.uk/~mbt/topcat/). I will not go into too much detail here, but the generally we will need to:
  - Perform a TOPCAT Cone Search of the chosen cluster (in this case M34).
  - Use the subset and sky vector features to extract the cluster memebers based on density in PMRA-PMDEC space.
  - Export the subset as a CSV. We will call this file **topcatcluster.csv**.
  
Information on how to do this whole process can be found [here](https://github.com/SamGou/Photometry-Simplified/blob/master/Images/Files/tutorial-topcat-stilts_2018Nov.pdf) (courtesy of M.Taylor of University of Bristol)

Here is an example of the subset that was created for M34.
<img src="https://github.com/SamGou/Photometry-Simplified/blob/master/Images/M34_skyplot.jpeg" width="80%">

_The red arrows represent the cluster and the gray ones reperesent the background stars._

Now we need to run `TkinterWindow.py`. The window that opens should look like this:
<img src="https://github.com/SamGou/Photometry-Simplified/blob/master/Images/GUI.jpg" width="80%">

Click the "Create Aperture file" button and browse to the location of your **topcatcluster.csv** file. In your repository folder there should now be a file called GAIA Data and inside it another folder called RADEC. Inside it will be the _RADEC_Py.radec_ file which is ready for use. You may run into a problem with the `PyAstronomy` package if using anaconda. If that does happen, just follow the steps in this [thread](https://stackoverflow.com/questions/39299726/cant-find-package-on-anaconda-navigator-what-to-do-next). **Make sure you rename or just move the file into a seperate folder as the RADEC_Py.radec will be re-written everytime you run the script!**

Next we need to open our image in AstroImageJ and import the radec file **(File -> Import apertures from RA/Dec list...)** and select the .radec file we just created. This will place all the apertures on the image:
<img src="https://github.com/SamGou/Photometry-Simplified/blob/master/Images/apertures.jpg" width="80%">

_Some apertures are outside of the image. This is okay, as it will be automatically accounted for in PS_

To complete the measurement tables just follow the [instructions](https://github.com/SamGou/Photometry-Simplified/blob/master/Images/Files/AIJ%20tutorial.pdf) starting from **step 5.** to the end. We will call the measurement tables **TableB.xls** and **TableV.xls***.

*_Note, we are choosing **B** and **V** since these are the filters M34 was imaged in._

We need to convert the _.xls_ files to _.xlsx_. Due to the outputed files from AIJ being in the wrong format, we have to do this manually. Open the files in Excel and export them as a workbook **(File -> Export -> Change File Type -> Workbook (*.xlsx))***

Now we have everything we need. Last step is to open PS again. Before you do anything else, choose from the two filter sets in the bottom left (**"Filters: B and R" or "Filters: B and V"**). Then, in no particular order, import the **topcatcluster.csv, TableB.xlsx, TableV.xlsx** by clicking on the "Import Topcat data", "Import V Table", "Import B Table" buttons respectively. When all 3 files are imported, an "OK" button will appear. You are also given the option to add extinction coefficients or the distance to the cluster in the bottom right corner (leaving the default values will apply no corrections). Lastly, click the "OK" button to generate the final _.csv_ file. It will be in the _GAIA DATA_ folder under the name of _"PhotometryTable_..." where "..." will be replaced by the optional parameters you had put. 

## Conclusion
This is it! A quick and easy process with no limit on how many stars one can perform differential photometry on. The automation both speeds up the process and improves the results by allowing for more data points. The main limitation now comes from your telescope and camera - the FOV, as well as the light sensitivity and resolution. 

Here are the results that PS can produce:
### Comparison of the Colour Magntiude diagrams for M34 as imaged by us and as given by the GAIA DR2 Database in the GAIA photometric filter set.
<img src="https://github.com/SamGou/Photometry-Simplified/blob/master/Images/M34_GAIA_comp.jpeg" width="90%">


### Colour Magnitude diagram with a fitted isochrone. Gives an age and metallicity estimation of the cluster.
<img src="https://github.com/SamGou/Photometry-Simplified/blob/master/Images/M34_Best_fit.jpeg" width="90%">

_From this image we estimate that M34 is ~ 150 Myrs old. For comparison, M34 was calculated to be 180 Myrs in 1993 by [G. Meynet's Geneva Team.](http://www.messier.seds.org/m-ref.html#meynet) A great result in no time!_
