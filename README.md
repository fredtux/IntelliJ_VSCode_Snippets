# IntelliJ <---> VSCode snippets
Provides snippet conversion from IntelliJ XML to VSCode JSON and from VSCode JSON to IntelliJ XML

## IntelliJ to VSCode snippet conversion
```bash
./convert_jc.py -i MyPHPSnippets.xml -o MyPHPSnippets.json
```
OR
```bash
python3 convert_jc.py -i MyPHPSnippets.xml -o MyPHPSnippets.json
```

## VSCode to IntelliJ snippet conversion
```bash
./convert_jc.py -i MyPHPSnippets.json -o MyPHPSnippets.xml -c PHP
```
OR
```bash
python3 convert_jc.py -i MyPHPSnippets.json -o MyPHPSnippets.xml -c PHP
```

## Help
```bash
./convert_jc.py -h
```
OR
```bash
python3 convert_jc.py -h
```
___
```bash
usage: convert_jc [-h] -i INFILE -o OUTFILE [-c CONTEXT]

IntelliJ XML <-> VSCode JSON converter

options:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        In file
  -o OUTFILE, --outfile OUTFILE
                        Out file
  -c CONTEXT, --context CONTEXT
                        Context (i.e.: PHP, Java etc.)
```