# Test Data Planning

To explore the removal of noise using various algorithms and tools, a variety of test data will be generated and downloaded. The focus is on data that is representative of Infrared remote sensing data.

## Generating truth data

Synthetic noise-free images containing test patterns and geometric shapes will be used as truth models. To these truth models, we will add well-characterized noise and then test different algorithms for removal of that noise. The de-noised data can be compared to the truth data to evaluate the performance of the algorithms.
 
### Tasks

- Describe common IR remotes sensing data formats (bit depth and size).
- Search web for noise-free synthetic test images that can be fit into these formats.
- [ ] Discuss python tools/libraries for generating geometric test shapes or test patterns to save as noise-free test images

## Downloaded data

Additional free data sets representing real remote sensing Infrared band data should be located and instructions for downloading the data provided. 

## Plan for applying noise sources to the test data

Raw test data will have deterministic noise - representing fixed-source errors such as from sensor characteristics - as well as stochastic and other common noise patterns applied to it. 

### Tasks

- Classify common types of noise in remote sensing IR imagery
- Discuss 1-3 statistical noise models that could be applied to the test data. 
- Classify the tunable parameters for such models.
- Write a plan for what Python packages or tools to use to apply the models to the test data.

## Organization
Plan how to structure directories to support both generated and downloaded data sets, preserving the raw/original data, while having a directory structure naming convention or documentation method for the noise-added data that makes it clear what model was applied and with which parameters.