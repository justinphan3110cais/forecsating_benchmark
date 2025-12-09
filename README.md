# Forecasting Benchmark

A comprehensive benchmarking framework for evaluating AI forecasting models on real-world prediction tasks.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/justinphan3110cais/forecsating_benchmark.git
cd forecsating_benchmark
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Then edit `.env` and add your API keys.

## Required API Keys

Add the following to your `.env` file:

- `OPENAI_API_KEY` - Your OpenAI API key
- `SERPER_API_KEY` - Get from [Serper.dev](https://serper.dev/)
- `GROK_API_KEY` - Your Grok API key

## Usage

```bash
cd benchmarks
python run_new.py
```



### Scrape new metaculus data
```
bash
cd scrape_data
python metaculus.py
```

then run the [process_metaculus.ipynb](scrape_data/process_metaculus.ipynb) notebook