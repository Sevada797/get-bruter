# get-bruter

**get-bruter** is a fast GET parameter brute-forcing tool designed for security researchers and penetration testers. It scans GET parameters for reflected values in the HTML response.

## Demo (GIF)
<img src="https://i.imgur.com/XgNVaXC.gif" alt="Demo" width="600">

## Features

- **High-Speed Scanning**: Asynchronous HTTP requests for fast scanning.
- **Reflection Count Tracking**: Detects how many times a parameter is reflected.
- **Customizable Wordlists**: Includes **alpha1+2** and **commonparams** wordlists.
- **Flexible URL Input**: Supports direct URLs or subdomain lists.

## Installation

1. Clone the repo:

    ```bash
    git clone git@github.com:Sevada797/get-bruter.git
    cd get-bruter
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the tool:

    ```bash
    python getbruter.py
    ```
4. For setting up easy-to-use (recommended) run:

    ```
    bash setup.sh
    ```
    so that you can call the tool from any path.

## How It Works

- Input a **URL or file** of subdomains.
- Select a **query sign** (`?` or `&`).
- Choose a **wordlist** (alpha1+2, commonparams options or custom - you provide).
- **get-bruter** checks for parameter reflections and logs results in `getfound.txt`.

## Future Features

- **Session Cookie Support**: Let me know if you need this!

## Wordlist

Includes **AI-generated** and **GitHub** wordlists. You can add your own.

## Useful?

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-donate-orange?style=flat&logo=buy-me-a-coffee)](https://buymeacoffee.com/zatikyansed)
