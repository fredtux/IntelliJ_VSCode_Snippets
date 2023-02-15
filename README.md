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