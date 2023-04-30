# Hypertrophy Tool - Using Thermal Imagery as a Metric for Muscle Activation and Hypertrophy

## Mission Statement and Product Description

Gym interest, and the lengths people are willing to go to get great results, are both rising. However, improving muscle activation is often overlooked, leading the people who are able to stay consistent to sub-optimal results, and unbalanced physiques. We offer a solution to this problem, with our thermal-camera phone application named "TAct" - which stands for thermal activation. It is a non-invasive application that uses thermal imaging to estimate muscle activation, backed by science and as a data-driven solution.

It also provides a unified interface for tracking gym progress.


## High Level Project Planning

<figure style="margin-left: auto;
  margin-right: auto; width: 100%; display: block;">
    <img
    src="Experimental/Media/UML/overview.svg?raw=true"
    alt="Planning Page">
    <figcaption>Figure 1: Project data flow.</figcaption>
</figure><br>

### Read Images

First, the user must provide images taken before and after an exercise / set. The following data is required.

1. Camera image **directly** before exercise
2. Thermal image **directly** before exercise
3. Camera image **directly** after exercise
4. Thermal image **directly** after exercise
5. (Optional) User muscle group designation

*Using a phone-compatible FLIR devide will enable simultaneous capture of camera and thermal images*

See the top and bottom set of images in Figure 2. These are the 'Camera Images' and 'Thermal Images' before (left) and after (right) a quadriceps workout (leg extension). 

<figure style="margin-left: auto;
  margin-right: auto; width: 50%; display: block;">
    <img
    src="Experimental/Media/UML/loaded_images.png?raw=true"
    alt="Raw, Segmented, and Thermal Images." width="100%">
    <figcaption>Figure 2: Input images (raw and thermal) and segmented images (middle row).</figcaption>
</figure><br>

### Segment Image

The before and after images must be segmented in order to determine which region of the image is relevant, i.e. skin regions that match. This is a required step for the overall robustness of the model since the shape of body parts varies widely based on image angle, natural deformation, and joint angles.

A few methods were implemented:
1. GrabCut
2. RINDNet to extract edged directly
3. Mask_RCNN
4. Torchvision segmentation baseline implementation (deeplabv3_resnet50)

All implementations lacked perfect segmentation accuracy and contiguous region selection. For simplicity and a machine learning direction to the project, Torchvisions segmentation baseline was used.

An example of a result from this model is shown in the second row of Figure 2.

### Match Images

Using the computed segmentation maps, naive outlines were computed using an expanding polar coordinate search from an estimated center of mass.

<figure style="margin-left: auto;
  margin-right: auto; width: 50%; display: block;">
    <img
    src="Experimental/Media/UML/edgeandcentercomputation.png?raw=true"
    alt="Polar edge search theory (row 1), center computation in practice (row 2), and edge computation in practice (row 3).">
    <figcaption>Figure 3: Polar edge search theory (row 1), center computation in practice (row 2), and edge computation in practice (row 3).</figcaption>
</figure><br>

### Align and Transform Images

A mesh transformation algorithm is the current default. It generates a fantastic transformed thermal image shown in figure 4 below. The current approach uses a small sample of edge points (30 compared to thousands), so it computes much faster and more efficiently.

<figure style="margin-left: auto;
  margin-right: auto; width: 50%; display: block;">
    <img
    src="Experimental/Media/UML/thermal_deformed2.jpg?raw=true"
    alt="Naively transformed raw image.">
    <figcaption>Figure 4: Mesh transformed thermal image.</figcaption>
</figure><br>

The old approach was to use naive ray scaling via center and matching edge points. Unfortunately, this algorithm generates artifacts in the scaled images, as seen in the raw image (figure 5) and thermal images (figure 6).

<figure style="margin-left: auto;
  margin-right: auto; width: 50%; display: block;">
    <img
    src="Experimental/Media/UML/visual_deformed.jpeg?raw=true"
    alt="Naively transformed raw image.">
    <figcaption>Figure 5: Naively transformed raw image.</figcaption>
</figure><br>

<figure style="margin-left: auto;
  margin-right: auto; width: 50%; display: block;">
    <img
    src="Experimental/Media/UML/thermal_deformed.png?raw=true"
    alt="Naively transformed thermal image.">
    <figcaption>Figure 6: Naively transformed thermal image.</figcaption>
</figure><br>

### Compute Thermal Difference Image

Simply taking the pixel difference between the heatmap thermal images (post-scaling). Smoothing may alleviate the current artifacts, but the true culprit in need of fixing is the transformation algorithm.

<figure style="margin-left: auto;
  margin-right: auto; width: 50%; display: block;">
    <img
    src="Experimental/Media/UML/dif_img.png?raw=true"
    alt="Difference thermal image.">
    <figcaption>Figure 7: Difference thermal image.</figcaption>
</figure><br>

The improved results after updating the deformation algorithm and difference computation is shown in figure 8 below.

<figure style="margin-left: auto;
  margin-right: auto; width: 50%; display: block;">
    <img
    src="Experimental/Media/UML/dif_img2.png?raw=true"
    alt="Difference thermal image.">
    <figcaption>Figure 8: Improved difference thermal image.</figcaption>
</figure><br>

### Generate Insight

This step has not been approached yet, however we can interpret the low quality difference image generated using external information.

<figure style="margin-left: auto;
  margin-right: auto; width: 90%; display: block;">
    <img
    src="Experimental/Media/UML/insight.png?raw=true"
    alt="Insights.">
    <figcaption>Figure 9: Insights. Left image from the Cleveland Clinic: https://my.clevelandclinic.org/health/body/22816-quad-muscles.</figcaption>
</figure><br>

By rotating the image, and applying a blur to reduce visible artifacts, the image can be aligned with an anatomical model. This is shown in figure 7, where both the left and right images show the right quadricep. On the right, we see a thermal difference image. In general, red implies a large positive difference, i.e. increase in temperature, and blue implies a small positive difference, no difference, or negative difference in temperature. 

Using this model, we can see that there is a large temperature increase in the vastus intermedius (center muscle), a small peak of temperature in the vastus medialis, and low to no increase in temperature in the vastus lateralis. Futhermore, although not shown in the anatomical image, there is a temperature increase in the adductors (top right).

Using this information, we can infer that the exercise provided higher activation in the 'inner quads', i.e. the vastus medialis, and adductors, than the 'outer quads', i.e. the vastus lateralis.

In the scenario that this information is presented to you after a set of leg extensions with the intention of working the entire quadriceps, someone looking to build a balanced physique in the quadriceps may decide to angle their legs (point their toes) more inwards in order to more strongly target the vastus medialis.

<br><br>

*For reference, the exercise performed when these images were taken was a quad / leg extension, with external hip rotation, chosen to target the inner quads more. It ended up providing more information than expected, as it shows a surprising amount of activation in the hip adductor.*

<br><br>


## Putting it all together - Web Application

A web server was created via the Flask web framework. The application serves the public directory files to any endpoint user, and the python server handles requests, sending appropriately formatted images to the 'production' experimental scripts to compute the thermal difference image, and finally returning it to the user.

Images of the application interface are shown below:

<figure style="margin-left: auto;
  margin-right: auto; width: 90%; display: block;">
    <img
    src="Web_Application/media/s1.png?raw=true"
    alt="Application.">
    <figcaption>Figure 10: Application after images are set as input</figcaption>
</figure><br>

<figure style="margin-left: auto;
  margin-right: auto; width: 90%; display: block;">
    <img
    src="Web_Application/media/s2.png?raw=true"
    alt="Application 2.">
    <figcaption>Figure 11: Application after processing</figcaption>
</figure><br>

## References for Project Construction:

1. https://pyimagesearch.com/2020/07/27/opencv-grabcut-foreground-segmentation-and-extraction/ 
2. https://pyimagesearch.com/2020/09/28/image-segmentation-with-mask-r-cnn-grabcut-and-opencv/ 
3. https://davis.wpi.edu/~matt/courses/morph/2d.htm 
4. https://github.com/MengyangPu/RINDNet 
5. https://github.com/matterport/Mask_RCNN 

## Background References:

1. Saltin, B. J. A. J., Gagge, A. P., & Stolwijk, J. A. (1968). Muscle temperature during submaximal exercise in man. Journal of applied physiology, 25(6), 679-688.
 > The authors Bengt Saltin et al. performed research on the topic of muscle temperature during submaximal exercise at the John B. Pierce Laboratory which specializes in studying physiology and health in the modern environment. The researchers had subjects perform steady state cardio on a stationary cycling machine. While exercising, they measured core temperature, average skin temperature over the entire body using IR, and intramuscular temperature of the legs. The findings were that in submaximal steady state exercise, skin temperature behaved inverse to that of the muscle temperature measurements with the thermocouples. As ambient temperature increased however, the relationship did not hold, and the skin temperature was concave before plateauing above the initial skin temperature. Another interesting finding was that the difference between the temperature at differing depths of thermocouple-needle measurements diminished as workload increased. Note that the muscles were measured to vary three degrees celsius from baseline to the converged muscle temperature.

2. Priego Quesada, J. I., Carpes, F. P., Bini, R. R., Salvador Palmer, R., Pérez-Soriano, P., & Cibrián Ortiz de Anda, R. M. (2015). Relationship between skin temperature and muscle activation during incremental cycle exercise. Journal of Thermal Biology, 48, 28–35. https://doi.org/10.1016/j.jtherbio.2014.12.005
 > A group of researchers primarily based in Valencia, Spain studied the effects on skin temperature by cycling exercise, primarily muscles in the quadriceps. The study found that (1) the localized area of skin over an exercised muscle had a statistically significant increase in temperature, (2) overall activation of the vastus lateralis was inversely related with skin temperature, and (3) low frequency activation of the vastus lateralis had a strong positive correlation with skin temperature. An interesting conclusion was that “Participants with larger overall activation and reduced low frequency component for vastus lateralis activation presented a better adaptive response of their thermoregulatory system by showing fewer changes in skin temperature after incremental cycling test”.

3. Oliveira, U. F. de, Araújo, L. C. de, Andrade, P. R. de, Santos, H. H. dos, Moreira, D. G., Sillero-Quintana, M., & Almeida Ferreira, J. J. de. (2018). Skin temperature changes during muscular static stretching exercise. Journal of Exercise Rehabilitation, 14(3), 451–459. https://doi.org/10.12965/jer.1836056.028
 > Researchers at the Federal University of Paraíba measured the skin temperatures of subjects over 180 seconds of hamstring stretching using a thermographic camera. There was a statistically significant increase in temperature of about 0.3°C, with changes in temperature during this time being linear. An unrelated observation is that the stress or work done on a muscle may be correlated to the temperature-skin area, rather than any single point of maximal temperature.


4. Priego-Quesada, J. I., De la Fuente, C., Kunzler, M. R., Perez-Soriano, P., Hervás-Marín, D., & Carpes, F. P. (2020). Relationship between Skin Temperature, Electrical Manifestations of Muscle Fatigue, and Exercise-Induced Delayed Onset Muscle Soreness for Dynamic Contractions: A Preliminary Study. International Journal of Environmental Research and Public Health, 17(18), 6817. https://doi.org/10.3390/ijerph17186817 
 > With the knowledge that “during muscle contractions, most of the energy generated is heat (>70%) that is transferred to the skin by conduction between tissues or by convection through capillary blood flow”, researchers performed a correlation analysis between skin temperature during exercise - specifically single arm bicep curls to failure (the other arm acted as a control group) - and muscle fatigue post-workout - 24 hours later. The researchers used a FLIR camera with resolution 320 x 240 after calibration. Delayed Onset Muscle Fatigue (DOMS) was found not to be correlated with skin temperature, or any other quantity measured. The more sets that were performed, the less correlation between skin temperature and repetition existed. Furthermore, the temperature did not continue to rise. Increases were only measured in the first two sets in a declining manner. The third set actually had a decrease in skin temperature recorded. The researchers surmised that this trend may have been caused by sweating, and that the three minute rest period may have caused the trend to exacerbate. This study is relevant to my research project as they use similar equipment, and indicate that more data is required to determine DOMS. The researchers concluded that “Although we considered in our study that the presence of sweat was negligible, it may have affected the temperature responses of the skin during the exercise.”
Read the related works of this paper as it correlates highly with research topic.

5. da Silva, W., Machado, Á. S., Souza, M. A., Kunzler, M. R., Priego-Quesada, J. I., & Carpes, F. P. (2018). Can exercise-induced muscle damage be related to changes in skin temperature? Physiological Measurement, 39(10), 104007. https://doi.org/10.1088/1361-6579/aae6df
 > Researchers again used a FLIR camera system with resolution 320 x 240 pixels, and this time tested the hypothesis that there is a correlation between creatine kinase (CK) activity. CK activity “ is widely employed to estimate the magnitude of exercise-induced muscle damage in sports”. The researchers “found that CK and infrared thermography responses to exercise-induced muscle damage are different. At least for exercise of a specific muscle group in untrained participants, skin temperature did not correlate with the creatine kinase activity. Therefore, the use of infrared thermography to predict or monitor muscle damage deserves further attention”. Note that the exercise-induced muscle damage (EIMD) is not necessarily correlated with muscle hypertrophy. While highly cited on the matter, many believe it is possible to grow muscle without such painful indications.


Summary of background information

 - Steady state exercise is inversely related to muscle temperature.
 - Muscle temperature varied three degrees celsius over steady state exercise.
 - The localized skin over an exercised muscle had a significant increase in temperature
 - Low frequency activation of the muscle has a strong positive correlation with skin temperature. However, overall activation has an inverse trend.
 - Stretching has a minimal (0.3๐C) increase in muscle temperature.
 - Stress or work done on a muscle may be correlated to the temperature-skin area, rather than any single point of maximal temperature.
 - DOMS does not correlate with skin temperature.
 - Skin temperature may even decrease with work as sweat impacts readings.
 - Measuring muscle damage via CK has no measurable correlation with skin temperature.