
## Noise Characterization and Application

Apply well-characterized noise of several statistical types to the downloaded thermal imagery. This allows controlled testing of denoising algorithms.

### Tasks

- [x] Create parameter logging system to track noise configurations:
  - Noise type
  - Parameters (σ, λ, density, etc.)
  - Random seed
  - Timestamp

**Implementation**: Created `src/noise_logger.py` module with functions:
- `log_noise_parameters()`: Save noise config to JSON per output directory
- `append_to_noise_log()`: Append entry to central log file
- `format_output_folder_name()`: Standardized folder naming
- `create_noise_parameter_summary()`: Human-readable summary generation

Updated `scripts/add_noise.py` to use the logging system. Each noise application creates:
- Per-directory metadata: `{output_dir}/noise_metadata.json`
- Central log: `~/data/noise/metadata/noise_params.json`

Logs include: timestamp, noise_type, parameters, random_seed, python_version, source files
- [x] Create a JSON parameter input file that specifies current parameters to use for each noise type that will persist between runs of the script

**Implementation**: Created `config/active_noise_params.json` with:
- Global settings: random_seed, data_paths (source, destination_base)
- Per-type parameters: gaussian (sigma), saltpepper (density), speckle (variance), poisson
- Enable/disable flag for each noise type
- User-editable configuration that persists between runs

Added functions to `src/noise_logger.py`:
- `load_active_noise_params()`: Load config file
- `get_enabled_noise_types()`: Get list of enabled noise types with params

Test with: `python3 scripts/test_active_params.py`
Documentation: `docs/ACTIVE_PARAMS_USAGE.md`
- [ ] Implement a Python noise application script that takes an input image argument and applies either a specified noise model or the full suite if none is specified, using the parameter input file
- [ ] Generate noisy versions of dataset with multiple noise types/levels/parameters as enumerated in NOISE_STUDY.md


## Metrics Measurement on Noisy Data

Measure the same quality metrics on noise-corrupted images to quantify degradation.

### Tasks

- [ ] Apply metric measurement to all noise-corrupted image variants
- [ ] Log metrics alongside noise parameters in structured format (JSON/CSV)
- [ ] Create visualization/comparison of metric degradation vs noise level:
  - PSNR vs noise level plots
  - SSIM vs noise level plots
  - Per noise-type comparison charts
- [ ] Document observations on how different noise types affect metrics
- [ ] Identify which metrics are most sensitive to which noise types


