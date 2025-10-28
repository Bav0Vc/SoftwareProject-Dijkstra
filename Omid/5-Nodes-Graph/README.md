# Codeblöcke

Bei jeder Aufgabe, wo ein Algorithmus genutzt wird, soll der jeweilige Algorithmus in Python Code dargestellt werden. Wir machen das indem wir jeweils an das Ende der Aufgabenbeschreibungen einen Knopf hinzufügen, welcher bei Klicken den Code zeigt oder wieder versteckt.

## Erstellung

Nutzt für die Erstellung bitte das beigeführte Python Skript `transform_py_to_html.py`.
`transform_py_to_html.py` ist ein Kommandozeilen Tool. Man gibt an, welche Datei als Eingabe genommen wird und in welcher Datei die Ausgabe gespeichert wird.

### Voraussetzungen

Ich habe Python Version 3.11.5 benutzt, es sollte aber mit den meisten gängigen Python Versionen funktionieren. Probiert es einfach mal. Ihr braucht PIP (Python Package Manager) um zusätzliche Bibliotheken zu installieren.
Die benötigten Bibliotheken sind in `requirements.txt` zu finden.
Ihr könnt direkt die benötigten Bibliotheken über die Kommandozeile installieren:
(Sofern der Ordner, wo auch diese Datei ist, euer Working Directory ist)

> pip install -r requirements.txt

Falls ihr beim Ausführen Fehler bekommt wie "Module ... not found", dann habe ich eventuell vergessen irgendeine Bibliothek in `requirements.txt` hinzuzufügen. Installiert sie bitte ggf. nach.

### Ausführung

Schreibt euren Python Code in die Datei `Python_Input.py`. Als Beispiel ist dort der Code für rekurisven Binärsuche.

Führt dann diesen Befehl aus:
(Sofern der Ordner, wo auch diese Datei ist, euer Working Directory ist)

> python transform_py_to_html.py -o HTML_Output.html Python_Input.py

Nun ist in `HTML_Output.html` der Code, welchen ihr in die Aufgabe einfügen müsst.

Falls etwas nicht funktioniert, könnt ihr

> python transform_py_to_html.py --help
> aufrufen. Ihr könnt aber die Argumente "-w/--wrap" und "-n/--nowrap" ignorieren.

### Hinweise bezüglich Eingabe

Eure Eingabe in `Python_Input.py` soll den Coding Standards entsprechen. Kurzgesagt, gelten gängige Python Konventionen wie z.B. Variablen/Funktionen in snake-case (z.B. binary_search) und Klassen in pascal-case (z.B. class BinarySearchTree). Wir nutzen einheitliche Formattierung mit einer Indentierung von 2 Spaces und jeweils zwei freie Zeilen zwischen Funktionen. Die Indentierung und die freien Zeilen sollten jedoch automatisch vom Skript korrigiert werden! Guckt also einfach bitte ob dies auch wirklich der Fall ist.

## Einfügung

Nachdem ihr den gesamten Code (startend und endend mit dem "details" Element), welcher in `HTML_Output.html` steht kopiert habt, könnt ihr das am Ende der Aufgabenbeschreibungen hinzufügen.
**WICHTIG**: Dafür müsst ihr den Code direkt als HTML einfügen. Das macht ihr indem ihr dem Editor der Aufgabenbeschreibung auf den Knopf "<>" (Source code) drückt.
Dann fügt ihr den Codeblock so ein (Beispiel):

```html
<div>
  You insert the following keys (in that order) into an initially empty
  red-black tree: 4, 6, 7, 5, 2, 1, 3
</div>
<div>Which statements are true?</div>
<div>&nbsp;</div>
<div>Please select one or multiple answers.</div>
<div>&nbsp;</div>
<details ...>Rest von dem Kopiertem...</details>
```

# Code Blocks (english version)

For every task that involves an algorithm, the respective algorithm must be represented as Python code.
We do this by adding a button at the end of the task description that shows or hides the code when clicked.

## Generation

To generate the code block, please use the provided Python script `transform_py_to_html.py`.
`transform_py_to_html.py` is a command-line tool. You specify which file should be used as input and in which file the output should be saved.

### Requirements

I used Python version 3.11.5, but it should work with most commonly used Python versions. Just give it a try.
You’ll need PIP (Python Package Installer) to install additional libraries.
The required libraries are listed in `requirements.txt`.
You can install the required libraries via command line:

```bash
pip install -r requirements.txt
```

If you encounter errors such as `Module ... not found` during execution, it’s possible that I forgot to include a library in `requirements.txt`.
In that case, please install the missing library manually.

### Execution

Write your Python code in the file `Python_Input.py`.
As an example, the code for recursive binary search is already included there.

Then run the following command:
(Assuming the folder where this file is located is your current working directory)

```bash
python transform_py_to_html.py -o HTML_Output.html Python_Input.py
```

Now the file `HTML_Output.html` contains the code that you need to insert into the task.

If something doesn’t work, you can try the following:

```python
python transform_py_to_html.py --help
```

aufrufen. Ihr könnt aber die Argumente "-w/--wrap" und "-n/--nowrap" ignorieren.

### Input Guidelines

Your input in `Python_Input.py` should follow coding standards.
In short, standard Python conventions apply, such as:

- Variables/functions in `snake_case` (e.g., `binary_search`)
- Classes in `PascalCase` (e.g., `class BinarySearchTree`)

We use a consistent formatting style with:

- 2-space indentation
- Two blank lines between functions

The script should automatically correct the indentation and spacing!
So just check to make sure that this is actually the case.

## Insertion

After copying the entire code block (starting and ending with the `<details>` element) from `HTML_Output.html`,
you can paste it at the end of the task description.

**IMPORTANT**: You must paste the code directly as HTML.
To do this, click the "`<>`" (source code) button in the task description editor.
Then insert the code block like this (example):

```html
<div>
  You insert the following keys (in that order) into an initially empty
  red-black tree: 4, 6, 7, 5, 2, 1, 3
</div>
<div>Which statements are true?</div>
<div>&nbsp;</div>
<div>Please select one or multiple answers.</div>
<div>&nbsp;</div>
<details ...>Rest of the copied block...</details>
```
