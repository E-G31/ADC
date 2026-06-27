     Python                 Hardware
| --------------------- | -------------------- |
| error = x-dac_out   | Summing amplifier    |
| integrator += error | RC Op-Amp Integrator |
| if integrator >=0   | Comparator           |
| dac_out = ±1        | 1-bit DAC            |
| Moving average      | Digital Filter       |

1. Analog input enters the summing junction
2. Feedback from DAC is subtracted
3. The integrator accumulates the error
4. The comparator converts the result into a one-bit stream
5. the DAC feeds back +- 1V
6. A digital filter reconstructs the analog signal
