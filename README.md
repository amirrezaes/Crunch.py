# Pyrunch

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A high-performance password list generator written in pure Python, inspired by the original Crunch tool. Pyrunch offers flexible password generation with multiple customization options while maintaining efficiency.

## Features

- **Pure Python Implementation**: Built without relying on itertools.product for better control and customization
- **Multiple Output Formats**: Plain text, hashed outputs, and compressed files
- **Pattern-Based Generation**: Support for custom character masks and patterns
- **Memory Efficient**: Optional memory-friendly mode for handling large generations
- **Flexible Output**: Pipe output directly to other tools or save to files

## Installation

```bash
git clone https://github.com/amirrezaes/pyrunch.git
cd pyrunch
```

## Usage

### Basic Usage
```bash
python3 pyrunch.py <min> <max> <characters> <options>
```

### Mask-Based Generation
```bash
python3 pyrunch.py --mask <mask> <options>
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `-o` | Set output file name/directory (use `-o -` for piping) |
| `-m` | Enable memory-friendly mode (slower but RAM efficient) |
| `-s` | Add suffix to generated passwords |
| `-p` | Add prefix to generated passwords |
| `--hash` | Hash passwords with specified algorithm |
| `--combo` | Output both plain and hashed text |
| `--mask` | Use pattern-based generation |
| `--start` | Start from specific position |
| `--end` | Stop at specific word |
| `-b` | Specify output file size (supports kb, mb, gb) |
| `-z` | Compress output using LZMA |

### Supported Hash Algorithms
- MD5
- SHA1, SHA224, SHA256, SHA384, SHA512
- Blake2b, Blake2s
- SHA3_224, SHA3_256, SHA3_384, SHA3_512

### Mask Patterns
- `?l`: Lowercase letters
- `?u`: Uppercase letters
- `?s`: Special characters
- `?d`: Digits

## Example Usage

### Generate passwords of length 6-8 with specific characters
```bash
python3 pyrunch.py 6 8 abcdef123
```

### Use mask pattern with hashing
```bash
python3 pyrunch.py --mask ?l?d?d?d --hash md5
```

### Generate and pipe to another tool
```bash
python3 pyrunch.py 8 8 abcdefgh -o - | aircrack-ng test.cap
```

## Demo
![](gif.gif)

## Performance

While not as fast as the C-based original Crunch, Pyrunch offers competitive performance among Python-based password generators while providing additional features and flexibility.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original Crunch tool for inspiration
- All contributors and users who provided feedback
