# Viterbi Decoder Simulator

A Python implementation of convolutional encoding and Viterbi decoding developed as part of the **Information Theory & Coding** course at BITS Pilani. The project explores the complete decoding workflow, trellis-based decoding, performance evaluation for different message lengths, and comparison of hard and soft decision decoding techniques.

The repository demonstrates practical implementation of channel coding algorithms together with visualization and performance analysis.

---

## Features

- Convolutional encoder implementation
- Viterbi decoding algorithm
- Trellis visualization
- Survivor path reconstruction
- Performance analysis across different message lengths
- BER analysis under varying channel error probabilities
- Hard vs. Soft decision decoding comparison
- Visualization of decoding performance

---

## Repository Structure

```
viterbi-decoder-simulator/

├── src/
│   ├── Program.py
│   ├── Program1.py
│   ├── Program2.py
│   └── Program3.py
│
├── results/
│   ├── ber/
│   ├── hard_soft/
│   └── trellis.png
│
├── docs/
│   └── report.pdf
│
├── README.md
├── LICENSE
└── .gitignore
```

---

## Source Files

| File | Description |
|------|-------------|
| Program.py | Convolutional encoding and Viterbi decoding implementation with trellis visualization |
| Program1.py | Trellis generation and visualization |
| Program2.py | Decoder performance analysis for different message lengths and channel conditions |
| Program3.py | Comparison of hard and soft decision decoding techniques |

---

## Results

The repository includes:

- Trellis visualization
- BER plots for different channel error probabilities
- Hard vs. Soft decision decoding comparison plots
- Decoder performance analysis across varying message lengths

---

## Concepts Implemented

- Convolutional Codes
- Trellis Representation
- Viterbi Decoding
- Hard Decision Decoding
- Soft Decision Decoding
- Binary Symmetric Channel
- Additive White Gaussian Noise (AWGN) Channel
- Bit Error Rate (BER)

---

## Tools Used

- Python
- NumPy
- Matplotlib
- Graphviz

---

## Future Improvements

Possible extensions include:

- Support for higher constraint length convolutional codes
- Configurable code rates
- Soft-output Viterbi decoding
- Comparison with Turbo and LDPC codes
- FPGA implementation of the decoder

---

## License

This project is released under the MIT License.
