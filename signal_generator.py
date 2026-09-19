import numpy as np
from scipy import signal

def verify_cycles(name, wave, expected_cycles):
    zero_crossings = np.where(np.diff(np.signbit(wave)))[0]
    actual_cycles = len(zero_crossings) / 2
    print(f"[{name}] Expected cycles: {expected_cycles:.2f}, Approximate actual cycles: {actual_cycles:.2f}")

def generate_sine_wave(sample_rate, duration, frequency, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    verify_cycles("Sine", wave, frequency * duration)
    return t, wave

def generate_square_wave(sample_rate, duration, frequency, amplitude, duty_cycle=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * signal.square(2 * np.pi * frequency * t, duty=duty_cycle)
    verify_cycles("Square", wave, frequency * duration)
    return t, wave

def generate_triangular_wave(sample_rate, duration, frequency, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * signal.sawtooth(2 * np.pi * frequency * t, width=0.5)
    verify_cycles("Triangular", wave, frequency * duration)
    return t, wave

def generate_chirp_wave(sample_rate, duration, f_start, f_end, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * signal.chirp(t, f0=f_start, f1=f_end, t1=duration, method='linear')
    
    # Phase calculation for linear chirp: phi(t) = 2*pi * (f0*t + (f1-f0)/(2*t1)*t^2)
    # Instantaneous frequency: f_inst(t) = f0 + (f1-f0)/t1 * t
    f_inst = f_start + (f_end - f_start) / duration * t
    
    if len(f_inst) > 0:
        mid_idx = len(f_inst) // 2
        print(f"[Chirp] Inst. freq at t=0: {f_inst[0]:.2f} Hz (expected {f_start} Hz)")
        print(f"[Chirp] Inst. freq at t={duration/2:.2f}: {f_inst[mid_idx]:.2f} Hz (expected {(f_start+f_end)/2:.2f} Hz)")
        print(f"[Chirp] Inst. freq at end: {f_inst[-1]:.2f} Hz (expected {f_end} Hz)")
        
    return t, wave

def generate_sinc_wave(sample_rate, duration, frequency, amplitude):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    t_centered = t - (duration / 2.0)
    wave = amplitude * np.sinc(2 * frequency * t_centered)
    
    zero_crossings = np.where(np.diff(np.signbit(wave)))[0]
    if len(zero_crossings) >= 2:
        center_idx = len(wave) // 2
        distances = np.abs(zero_crossings - center_idx)
        closest_indices = np.argsort(distances)[:2]
        closest_zc = zero_crossings[closest_indices]
        width_samples = np.abs(closest_zc[1] - closest_zc[0])
        width_time = width_samples / sample_rate
        expected_width = 1.0 / frequency
        print(f"[Sinc] Main lobe width: {width_time:.5f} s (expected {expected_width:.5f} s)")
        
    return t, wave
