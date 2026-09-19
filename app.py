import streamlit as st
import numpy as np
import io
import matplotlib.pyplot as plt
from scipy.io import wavfile
import plotly.graph_objects as go
import signal_generator
import signal_analyzer

st.title("Waveform Toolbox")

with st.expander("ℹ️ How to use this app"):
    st.markdown("""
    **Generator tab:** Select a waveform type, set its parameters 
    (frequency, amplitude, duration, duty cycle for square waves), 
    then click Generate to see the time-domain plot and hear the audio.
    
    **Analyzer tab:** Upload a .wav file, or use the waveform you just 
    generated. Click Analyze to see RMS, peak amplitude, dominant 
    frequency, the time-domain waveform, FFT magnitude spectrum, and 
    spectrogram (STFT). Use the plot type dropdown to switch between 
    a static view and an interactive zoomable/pannable view.
    """)

tab_gen, tab_ana = st.tabs(["Generator", "Analyzer"])

with tab_gen:
    waveform_type = st.selectbox("Select Waveform", ["Sine", "Square", "Triangular", "Chirp", "Sinc"])

    col1, col2 = st.columns(2)
    with col1:
        if waveform_type == "Chirp":
            f_start = st.number_input("Start Frequency (Hz)", min_value=0.001, value=20.0)
            f_end = st.number_input("End Frequency (Hz)", min_value=0.001, value=100.0)
            frequency = 440.0  # default to avoid undefined errors elsewhere
        else:
            frequency = st.number_input("Frequency (Hz)", min_value=0.001, value=440.0)
        amplitude = st.number_input("Amplitude", min_value=0.001, value=0.5)
    with col2:
        duration = st.number_input("Duration (sec)", min_value=0.001, value=1.0)
        duty_cycle = 0.5
        if waveform_type == "Square":
            duty_cycle = st.number_input("Duty Cycle", min_value=0.1, max_value=0.9, value=0.5)

    if st.button("Generate"):
        sample_rate = 44100
        
        if waveform_type == "Sine":
            t, wave = signal_generator.generate_sine_wave(sample_rate, duration, frequency, amplitude)
        elif waveform_type == "Square":
            t, wave = signal_generator.generate_square_wave(sample_rate, duration, frequency, amplitude, duty_cycle)
        elif waveform_type == "Triangular":
            t, wave = signal_generator.generate_triangular_wave(sample_rate, duration, frequency, amplitude)
        elif waveform_type == "Chirp":
            t, wave = signal_generator.generate_chirp_wave(sample_rate, duration, f_start, f_end, amplitude)
        elif waveform_type == "Sinc":
            t, wave = signal_generator.generate_sinc_wave(sample_rate, duration, frequency, amplitude)
            
        st.session_state['generate_triggered'] = True
        st.session_state['generated_wave'] = wave
        st.session_state['generated_sr'] = sample_rate
        st.session_state['generated_t'] = t
        st.session_state['generated_type'] = waveform_type
        if waveform_type == "Chirp":
            st.session_state['generated_f_start'] = f_start
            st.session_state['generated_f_end'] = f_end
        else:
            st.session_state['generated_frequency'] = frequency
            
    if st.session_state.get('generate_triggered', False):
        t = st.session_state['generated_t']
        wave = st.session_state['generated_wave']
        sample_rate = st.session_state['generated_sr']
        gw_type = st.session_state['generated_type']
        
        plot_mode_gen = st.selectbox("Generator Plot Type", ["Matplotlib (Static)", "Plotly (Interactive)"])
        
        if plot_mode_gen == "Matplotlib (Static)":
            fig, ax = plt.subplots(figsize=(10, 4))
            
            if gw_type == "Chirp":
                ax.plot(t, wave)
                ax.set_title(f"Chirp Wave (starts sweeping {st.session_state['generated_f_start']} Hz to {st.session_state['generated_f_end']} Hz)")
            elif gw_type == "Sinc":
                freq = st.session_state['generated_frequency']
                window_size = 10.0 / freq
                center_idx = len(wave) // 2
                half_win = int((window_size / 2) * sample_rate)
                start_idx = max(0, center_idx - half_win)
                end_idx = min(len(wave), center_idx + half_win)
                ax.plot(t[start_idx:end_idx], wave[start_idx:end_idx])
                ax.set_title(f"Sinc Wave ({freq} Hz)")
            else:
                freq = st.session_state['generated_frequency']
                num_cycles = 5
                num_samples_to_plot = int((num_cycles / freq) * sample_rate)
                ax.plot(t[:num_samples_to_plot], wave[:num_samples_to_plot])
                ax.set_title(f"{gw_type} Wave ({freq} Hz)")
                
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.grid(True)
            st.pyplot(fig)
            
        elif plot_mode_gen == "Plotly (Interactive)":
            fig_plotly = go.Figure()
            fig_plotly.add_trace(go.Scatter(x=t, y=wave, mode='lines', name='Signal'))
            
            if gw_type == "Chirp":
                title_str = f"Chirp Wave (starts sweeping {st.session_state['generated_f_start']} Hz to {st.session_state['generated_f_end']} Hz)"
            else:
                title_str = f"{gw_type} Wave ({st.session_state['generated_frequency']} Hz)"
                
            fig_plotly.update_layout(
                title=title_str,
                xaxis_title="Time (s)",
                yaxis_title="Amplitude",
                xaxis=dict(rangeslider=dict(visible=True), type="linear")
            )
            st.plotly_chart(fig_plotly, use_container_width=True)
            
        # Audio playback
        wave_int16 = np.int16(wave * 32767)
        buf = io.BytesIO()
        wavfile.write(buf, sample_rate, wave_int16)
        st.audio(buf, format="audio/wav")

with tab_ana:
    st.header("Signal Analyzer")
    upload_file = st.file_uploader("Upload a .wav file (optional)", type=["wav"])
    
    if st.button("Analyze"):
        st.session_state['analyze_triggered'] = True
        
    if st.session_state.get('analyze_triggered', False):
        wave_to_analyze = None
        sample_rate_to_analyze = 44100
        
        if upload_file is not None:
            sr, data = wavfile.read(upload_file)
            sample_rate_to_analyze = sr
            # Convert to float
            if data.dtype == np.int16:
                wave_to_analyze = data.astype(np.float32) / 32767.0
            else:
                wave_to_analyze = data
                
            # If stereo, take one channel
            if len(wave_to_analyze.shape) > 1:
                wave_to_analyze = wave_to_analyze[:, 0]
        else:
            if 'generated_wave' in st.session_state:
                wave_to_analyze = st.session_state['generated_wave']
                sample_rate_to_analyze = st.session_state.get('generated_sr', 44100)
            else:
                st.warning("No signal generated yet or uploaded. Go to the Generator tab and click 'Generate' first.")
        
        if wave_to_analyze is not None:
            freqs, magnitudes, rms, peak, dom_freq = signal_analyzer.analyze_signal(wave_to_analyze, sample_rate_to_analyze)
            
            # Display metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("RMS", f"{rms:.4f}")
            c2.metric("Peak Amplitude", f"{peak:.4f}")
            c3.metric("Dominant Freq", f"{dom_freq:.1f} Hz")
            
            plot_mode = st.selectbox("Time Domain Plot Type", ["Matplotlib (Static)", "Plotly (Interactive)"])
            st.subheader("Time Domain Waveform")
            
            t_plot = np.arange(len(wave_to_analyze)) / sample_rate_to_analyze
            
            if plot_mode == "Matplotlib (Static)":
                fig_time, ax_time = plt.subplots(figsize=(10, 3))
                ax_time.plot(t_plot, wave_to_analyze)
                ax_time.set_xlabel("Time (s)")
                ax_time.set_ylabel("Amplitude")
                ax_time.set_title("Full Signal")
                ax_time.grid(True)
                st.pyplot(fig_time)
                
                # Show the zoomed-in "first few cycles" as well
                fig_time_zoom, ax_time_zoom = plt.subplots(figsize=(10, 3))
                plot_len = min(2000, len(wave_to_analyze))
                ax_time_zoom.plot(t_plot[:plot_len], wave_to_analyze[:plot_len])
                ax_time_zoom.set_xlabel("Time (s)")
                ax_time_zoom.set_ylabel("Amplitude")
                ax_time_zoom.set_title("First 2000 Samples (Zoomed)")
                ax_time_zoom.grid(True)
                st.pyplot(fig_time_zoom)
                
            elif plot_mode == "Plotly (Interactive)":
                fig_time_plotly = go.Figure()
                fig_time_plotly.add_trace(go.Scatter(x=t_plot, y=wave_to_analyze, mode='lines', name='Signal'))
                
                title_str = "Time Domain Waveform"
                if dom_freq > 0:
                    title_str += f" (Dominant Freq ~{dom_freq:.1f} Hz)"
                    
                fig_time_plotly.update_layout(
                    title=title_str,
                    xaxis_title="Time (s)",
                    yaxis_title="Amplitude",
                    xaxis=dict(rangeslider=dict(visible=True), type="linear")
                )
                st.plotly_chart(fig_time_plotly, use_container_width=True)
            
            st.subheader("Magnitude Spectrum (FFT)")
            fig_fft, ax_fft = plt.subplots(figsize=(10, 3))
            ax_fft.plot(freqs, magnitudes)
            ax_fft.set_xlabel("Frequency (Hz)")
            ax_fft.set_ylabel("Magnitude")
            ax_fft.grid(True)
            # Limit x-axis to a reasonable range if dominant freq is low
            if dom_freq > 0:
                ax_fft.set_xlim(0, max(2000, dom_freq * 3))
            st.pyplot(fig_fft)

            st.subheader("Spectrogram (STFT)")
            fig_stft, ax_stft = plt.subplots(figsize=(10, 4))
            f_stft, t_stft, mag_db = signal_analyzer.compute_stft(wave_to_analyze, sample_rate_to_analyze)
            c = ax_stft.pcolormesh(t_stft, f_stft, mag_db, shading='gouraud', cmap='viridis')
            ax_stft.set_xlabel("Time (s)")
            ax_stft.set_ylabel("Frequency (Hz)")
            if dom_freq > 0:
                ax_stft.set_ylim(0, max(2000, dom_freq * 3))
            fig_stft.colorbar(c, ax=ax_stft, label="Magnitude (dB)")
            st.pyplot(fig_stft)
