# FUSE_2023_Acoustics

This project aims to combine acoustic emission, a cost- effective, non-invasive rapid diagnostic technique whereby battery degradation phenomena can be detected, with machine learning (ML) techniques to determine state of health (SoH) and track key battery safety metrics. The following repository contains additional experimental data, Python code that was developed for automated signal processing, and ML code.

- **Automated AE Waveform Processing.py**: Python code which automatically organises waveform data (from AEwin software) into an easily navigable directory structure and generates/stores unfiltered signal, filtered signal (digital Butterworth band-pass filter) and Fast Fourier Transform (FFT) of every waveform.
- **Full Cycling Data**: 1C and C/3 cycling data at all transducer positions for both aged (80% SoH) and pristine P42A cylindrical cells.
- **Machine Learning for Acoustic Emission with Cylindrical Cells.ipynb**: Juptyer notebook which contains unsupervised and supervised ML code developed, alongside explanations.
