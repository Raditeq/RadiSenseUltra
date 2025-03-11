# RadiSense Ultra Timed Measurement Demo

This repository contains demo code for the **RadiSense Ultra** product. The code demonstrates how to interface with and control the RadiSense Ultra device using Python.

## Repository Structure

- `install_requirements.py` – Installs all required Python packages.
- `main.py` – Main program that runs the demo.
- `driver.py` – Driver for controlling the RadiSense Ultra.

## Prerequisites

Ensure you have Python installed on your system (recommended version: Python 3.8 or higher).

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Raditeq/RadiSenseUltra.git
   cd RadiSenseUltra
   ```
2. Install required dependencies:
   ```bash
   python install_requirements.py
   ```

## Usage

1. Ensure the **RadiSense Ultra** device is connected and placed in **slot 1** of the **RadiCentre CTR2008A**.
2. Run the main demo script:
   ```bash
   python main.py
   ```

## Notes

- The demo assumes that the RadiSense Ultra is in **slot 1** of the RadiCentre CTR2008A.
- Modify `driver.py` if you need to configure a different slot or setup.

## License

This repository is provided for demonstration purposes only. Check the license file for more details.

---

For any issues or questions, feel free to open an issue on GitHub.

