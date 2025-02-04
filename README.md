## Investigating the Performance and Safety of Li-Ion Cylindrical Cells Using Acoustic Emission and Machine Learning Analysis

This project aims to combine acoustic emission, a cost- effective, non-invasive rapid diagnostic technique whereby battery degradation phenomena can be detected, with machine learning (ML) techniques to determine state of health (SoH) and track key battery safety metrics. The repository contains additional experimental data, Python code that was developed for automated signal processing, and ML code. See our [paper](https://iopscience.iop.org/article/10.1149/1945-7111/ad59c9/meta).

- **Automated AE Waveform Processing.py**: Python code which automatically organises waveform data (from AEwin software) into an easily navigable directory structure and generates/stores unfiltered signal, filtered signal (digital Butterworth band-pass filter) and Fast Fourier Transform (FFT) of every waveform.
- **Supervised ML with AE in Cylindrical Cells.ipynb**: Juptyer notebook which contains supervised ML code, i.e. aged-pristine classifier, alongside explanations.
- **Unsupervised ML with AE in Cylindrical Cells.ipynb**: Juptyer notebook which contains unsupervised ML code, alongside explanations. PCA, k-means clustering, autoencoders code.
