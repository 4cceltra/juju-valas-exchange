# JUJU — Premium Exchange Rate

## 1. Install Python
Pastikan Python sudah terpasang.

## 2. Buka folder ini di VS Code

## 3. Install library
Buka Terminal VS Code lalu jalankan:

pip install flask yfinance

## 4. Jalankan website

python app.py

## 5. Buka browser
http://127.0.0.1:5000

Kurs diambil dari Yahoo Finance melalui yfinance.
Harga beli = mid-market - 0.45%
Harga jual = mid-market + 0.45%
Total spread = sekitar 0.90%.

Catatan: Yahoo Finance adalah sumber market reference, bukan necessarily kurs retail money changer.
