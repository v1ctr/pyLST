# Lohnsteuerrechner für Python


Für die Berechnung werden die [Programmablaufpläne](https://www.bmf-steuerrechner.de/) mit [LstGen](https://github.com/jenner/LstGen) automatisch in Python Dateien übersetzt.
```
lstgen -p 2020 -l python --class-name Lohnsteuer2020 --outfile lst2012.py
```

## Testing
```
python -m unittest discover
```