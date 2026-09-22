# Waveform Toolbox — SP24 Signal Processing Project

**IIT Madras BS Electronic Systems — Signal Processing Project (SP24)**
**Team:** Vimalsibi S (24F3100199), Baradhwaj M (24F3100190)

A Streamlit web application for generating audio waveforms and analyzing their time-domain,
frequency-domain, and time-frequency characteristics.

## Features

### Generator
- Generate **Sine**, **Square**, **Triangular**, **Chirp**, and **Sinc** waveforms
- Configurable frequency, amplitude, and duration
- Configurable duty cycle for square waves
- Configurable start/end frequency for chirp sweeps
- Time-domain plot (static Matplotlib or interactive Plotly with zoom/pan range slider)
- In-browser audio playback of the generated signal

### Analyzer
- Upload a `.wav` file, or analyze the signal just generated in the Generator tab
- Computes RMS, peak amplitude, and dominant frequency
- Time-domain waveform plot (static Matplotlib or interactive Plotly)
- FFT magnitude spectrum plot
- Spectrogram (STFT) plot

## Project Structure

```
.
├── app.py                 # Streamlit app (UI, both Generator and Analyzer tabs)
├── signal_generator.py    # Waveform generation functions
├── signal_analyzer.py     # FFT / STFT / signal statistics functions
├── requirements.txt       # Python dependencies
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10 or later installed on your system

### macOS / Linux

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app.py
```

### Windows

```powershell
:: 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

:: 2. Create a virtual environment
python -m venv venv

:: 3. Activate the virtual environment
venv\Scripts\activate

:: 4. Install dependencies
pip install -r requirements.txt

:: 5. Run the app
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### Deactivating the environment

When you're done, deactivate the virtual environment with:
```bash
deactivate
```

## How to Use

1. **Generator tab:** Select a waveform type from the dropdown, set its parameters (frequency,
   amplitude, duration, and duty cycle for square waves), then click **Generate**. Choose between
   a static plot or an interactive (zoomable/pannable) plot to view the waveform, and use the
   built-in audio player to listen to it.

2. **Analyzer tab:** Either upload a `.wav` file, or leave the uploader empty to analyze the
   waveform you just generated. Click **Analyze** to view:
   - RMS, peak amplitude, and dominant frequency
   - Time-domain waveform (static or interactive)
   - FFT magnitude spectrum
   - Spectrogram (STFT)

## Notes on "Dominant Frequency"

The dominant frequency metric reports the single frequency bin with the highest magnitude in the
FFT. This is a meaningful, accurate value for tonal signals (sine, square, triangular). For
wideband signals such as **chirp** and **sinc**, energy is spread across a range of frequencies
rather than concentrated at one point, so the reported dominant frequency reflects only the
tallest bin in that spread spectrum (often near a band edge) rather than a single characteristic
frequency of the signal. This is expected DSP behavior, not a bug.

## Live Demo

A live deployed version of this app (via Streamlit Community Cloud) is available at:
`<add your streamlit.app link here after deployment>`

## Tech Stack

- **Language:** Python 3
- **Libraries:** NumPy, SciPy, Matplotlib, Plotly, Streamlit
- **Platform:** Web app (Streamlit)

## Team Contribution

- **Vimalsibi S (24F3100199):** Signal Generator module (`signal_generator.py`) — sine, square,
  triangular, chirp, and sinc waveform generation; Generator tab UI; project setup and
  integration.
- **Baradhwaj M (24F3100190):** Signal Analyzer module (`signal_analyzer.py`) — FFT magnitude
  spectrum, RMS/peak/dominant frequency statistics, STFT/spectrogram computation; Analyzer tab UI.
