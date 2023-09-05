# FUSE_2023_Acoustics

This project aims to combine acoustic emission, a cost- effective, non-invasive rapid diagnostic technique whereby battery degradation phenomena can be detected, with machine learning (ML) techniques to determine state of health (SoH) and track key battery safety metrics. The repository contains additional experimental data, Python code that was developed for automated signal processing, and ML code.

- **Automated AE Waveform Processing.py**: Python code which automatically organises waveform data (from AEwin software) into an easily navigable directory structure and generates/stores unfiltered signal, filtered signal (digital Butterworth band-pass filter) and Fast Fourier Transform (FFT) of every waveform.
- **Full Cycling Data**: 1C and C/3 cycling data at all transducer positions for both aged (80% SoH) and pristine P42A cylindrical cells.
- **Supervised ML with AE in Cylindrical Cells.ipynb**: Juptyer notebook which contains supervised ML code, i.e. aged-pristine classifier, alongside explanations.
- **Unsupervised ML with AE in Cylindrical Cells.ipynb**: Juptyer notebook which contains unsupervised ML code, alongside explanations. PCA, k-means clustering, autoencoders code.

**IMPORTANT:** Jupyter notebook files are large, so GitHub can struggle to open them if the loading time exceeds 5 seconds. If this is the case, please download the files and view them using appropriate platforms or preview the files using the following links from [nbviewer.org](nbviewer.org):

- [Supervised ML code preview](https://nbviewer.org/github/seungbinjoo/FUSE_2023_Acoustics/blob/main/Supervised%20ML%20with%20AE%20in%20Cylindrical%20Cells.ipynb)
- [Unsupervised ML code preview](https://nbviewer.org/github/seungbinjoo/FUSE_2023_Acoustics/blob/main/Unsupervised%20ML%20with%20AE%20in%20Cylindrical%20Cells.ipynb)
