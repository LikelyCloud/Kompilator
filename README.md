# Kompilator

Kompilator napisany na zaliczenie kursu JFTT 2022/2023

## Instalacja potrzebnych pakietów

```bash
pip install foobar
sudo apt install python3
sudo apt install python3-pip
pip install sly
```

## Opis plików
compiler.py -> główny plik programu <br />
code_generator.py -> plik generujący kod na podstawie otrzymanego AST <br />
context.py -> plik definiujący struktury danych używane w programie <br />
lexer_parser.py -> plik zawierający parser i lekser <br />
exceptions.py -> plik definiujący wyjątki <br />

## Użycie

```bash
python3 compiler.py <input_file> <output_file>
```
