import numpy as np
from scipy import signal

def analyze_signal(wave, sample_rate):
    """
    Analyzes a 1D numpy array representing a signal.
    Returns frequencies, magnitudes, RMS, peak amplitude, and dominant frequency.
    """
    n = len(wave)
    if n == 0:
        return np.array([]), np.array([]), 0.0, 0.0, 0.0
        
    # FFT computation
    freqs = np.fft.rfftfreq(n, d=1.0/sample_rate)
    fft_vals = np.fft.rfft(wave)
    
    # Normalize magnitudes
    magnitudes = np.abs(fft_vals) / n
    if len(magnitudes) > 2:
        magnitudes[1:-1] *= 2.0
        
    # Basic statistics
    rms = np.sqrt(np.mean(wave**2))
    peak_amplitude = np.max(np.abs(wave))
    
    # Dominant frequency (finding the peak in the magnitude spectrum)
    if len(magnitudes) > 0:
        dominant_idx = np.argmax(magnitudes)
        dominant_freq = freqs[dominant_idx]
    else:
        dominant_freq = 0.0
        
    return freqs, magnitudes, rms, peak_amplitude, dominant_freq

def compute_stft(wave, sample_rate, nperseg=1024):
    f, t, Zxx = signal.stft(wave, fs=sample_rate, nperseg=nperseg)
    mag = np.abs(Zxx)
    mag_db = 20 * np.log10(np.maximum(mag, 1e-10))
    return f, t, mag_db
