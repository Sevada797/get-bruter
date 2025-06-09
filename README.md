# get-bruter

**get-bruter** is a fast GET parameter brute-forcing tool designed for security researchers and penetration testers. It scans GET parameters for reflected values in the HTML response.

## Demo (GIF)
![Demo](https://github.com/Sevada797/get-bruter/blob/main/assets/Get-Bruter_demo.gif?raw=true)

## New modules!
I added new modules, which can help quite a bit, here how you can run them after full setup.

```gbr``` - basic mode

``` gbr d``` - dynamit mode

```gbr di``` - dynamit inject mode

```gbr dc``` - dynamit cookie injection

Please Note: before passing to any dynamit mode you should provide URLs and sure with parameters, <br>
so like you can `grep "?" urls | grep = >4d` then pass this "4d" file to gbr dynamit modules.

And just pass subs list (or single URL) to ```gbr``` basic mode since I designed it that way.. I may later fix to auto append https if it misses.

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

    ```
    python getbruter.py
    ```
or dynamit mode (just provide bunch of urls after 'grep ? urls | grep = >4d ')
run ```
    python3 getbruter.py --dynamit
    ```
additionally these are equivalent to running `gbr` & `gbr d` (4th step should be done for this)

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
