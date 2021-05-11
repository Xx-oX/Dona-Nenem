# Dona-Nenem

## Description
* Compile AUTOSAR(*arxml) configure code to OIL code.
* Only suitable for specific type of arxml schema.

## Usage
```
python3 ./dona_nenem/main.py INPUT_FILE_NAME
```

## Methods
* **parse**
  * Use xml.etree.ElementTree to parse the input sorce file.
  * Return a element list.
* **gen**
  * Generating the output target file.

## Install
* Still under development :P
```
python3 setup.py install
```

## TODO
+ syntax & sementric examination
+ automatically generates internal modules(e.g. CallbackAlarm)
+ add unsupported modules
