# Test Data Planning - Thermal Imagery Focus

To explore the removal of noise using various algorithms and tools, we will use downloaded thermal imagery datasets and apply controlled noise patterns. The focus is on real-world thermal/infrared imagery representative of remote sensing data.

# Test Data Set

The dataset chosen is from https://adas-dataset-v2.flirconservator.com/#fulldownloadsection


### Assumptions
SRC_FOLDER is ~/data/FLIR_ADAS_v2/images_thermal_train/data
PRJ_FOLDER is this project's folder
DST_FOLDER is ~/data/noise/thermal/original
### Tasks
- [ ] Create a python script to copy some data
  - Ask user num_files to copy
  - Seed a random number generator
  - Read the filenames from SRC_FOLDER into a src_file_list
  - Using the seeded random sequence, create an index list with num_files random indexes between 0 and len(src_file_list-1)
  - Create ${DST_FOLER}src_file_list.txt
  - for idx in index_list: 
    - write src_file_list[idx] into the src_file_list.txt file
    - create a dst_file_name using just the *fname_000nnn* portion of the source file name, and append .jpg 
    - print f"copying {src_file_list[idx]} to ./data/{dst_file_name}"

