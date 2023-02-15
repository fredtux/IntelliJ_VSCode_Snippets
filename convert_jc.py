#!/usr/bin/python3

import argparse
from xml.dom.minidom import parse, Document
import json
import re
from sys import stderr, exit


class IntelliJXML:
    """ A class to handle IntelliJ XML documents"""
    fpath = ""
    document = ""

    def __init__(self, path):
        self.fpath = path

    def parse(self):
        self.document = parse(self.fpath)

    def getBody(self, template):
        body = template.getAttribute("value")

        # Get rid of double dollar signs and make them single dollar signs
        body = re.sub(r"\$([0-9]*)\$", r"$\1", body)

        result = body.split("\n")
        return result

    def create(self):
        group = self.fpath[:-4]
        group = re.sub(r"(/.*/)", r"", group)
        group = re.sub(r"(\\.*\\)", r"", group)
        group = re.sub(r"(.*/)", r"", group)
        group = re.sub(r"(.*\\)", r"", group)

        self.document = Document()

        templateSet = self.document.createElement('templateSet')
        templateSet.setAttribute("group", group)

        self.document.appendChild(templateSet)

    def add(self, context, name, value):
        # Add template
        template = self.document.createElement("template")
        template.setAttribute("name", value["prefix"])
        template.setAttribute("description", name)
        template.setAttribute("toReformat", "false")
        template.setAttribute("toShortenFQNames", "true")

        body = "\n".join(value["body"])

        # Find all variables
        vars = set()
        for var in [x.group() for x in re.finditer(r"(\$[0-9]+)", body)]:
            vars.add(var)

        # Replace single dollar sign with encolsing dollar signs
        body = re.sub(r"(\$[0-9]+)", r"\1$", body)

        # Escape \n
        body = body.replace("\n", "&#10;")

        template.setAttribute("value", body)

        # Add all the variables in template
        for i in range(0, len(vars)):
            variable = self.document.createElement("variable")
            variable.setAttribute("name", str(i+1))
            variable.setAttribute("expression", "")
            variable.setAttribute("defaultValue", "")
            variable.setAttribute("alwaysStopAt", "true")

            template.appendChild(variable)

        # Add context and option
        ctx = self.document.createElement("context")
        option = self.document.createElement("option")

        option.setAttribute("name", context)
        option.setAttribute("value", "true")
        ctx.appendChild(option)

        template.appendChild(ctx)

        templateSet = self.document.getElementsByTagName("templateSet")[0]
        templateSet.appendChild(template)

    def write(self):
        xmlString = self.document.toprettyxml().split(
            "\n", 1)[1].replace("&amp;#10;", "&#10;")

        xmlFile = open(self.fpath, 'w')
        xmlFile.write(xmlString)
        xmlFile.close()


class VSCodeJSON:
    """ A class to handle VSCode JSON documents"""
    fpath = ""
    document = {}

    def __init__(self, path):
        self.fpath = path

    def create(self):
        pass

    def add(self, name, body):
        # self.document.append({name: {"prefix": name, "body": body}})
        self.document[name] = {"prefix": name, "body": body}

    def write(self):
        # Dump into formatted JSON
        jsonString = json.dumps(self.document, indent=4)
        # Replace begining and and [] with {}
        jsonString = '{' + jsonString[1:-1] + '}'

        jsonFile = open(self.fpath, "w")
        jsonFile.write(jsonString)
        jsonFile.close()

    def parse(self):
        datafile = open(self.fpath, 'r')
        self.document = json.load(datafile)
        datafile.close()


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        stderr.write('error: %s\n_____\n' % message)
        self.print_help()
        exit(-2)

    def getValuesFromArgs(self):
        self.__init__(prog='convert_jc',
                      description='IntelliJ XML <-> VSCode JSON converter')
        self.add_argument("-i", "--infile", help="In file", required=True)
        self.add_argument("-o", "--outfile", help="Out file", required=True)
        self.add_argument(
            "-c", "--context", help="Context (i.e.: PHP, Java etc.)")

        args = self.parse_args()

        xml = args.infile if args.infile[-3:] == "xml" else args.outfile
        json = args.infile if args.infile[-4:] == "json" else args.outfile
        direction = 1 if args.infile[-3:] == "xml" else -1

        return [xml, json, args.context, direction]


if __name__ == "__main__":
    (xmldoc, jsondoc, context, direction) = ArgParser().getValuesFromArgs()
    intellij = IntelliJXML(xmldoc)
    vscode = VSCodeJSON(jsondoc)

    if direction == 1:  # IntelliJ -> VSCode
        intellij.parse()
        vscode.create()

        for template in intellij.document.getElementsByTagName("template"):
            name = template.getAttribute("name")
            body = intellij.getBody(template)

            vscode.add(name, body)

        vscode.write()
    else:  # VScode -> IntelliJ
        if context is None:
            print("Please provide context (i.e.: PHP, JAVA_SCRIPT etc.)")
            exit(-1)

        vscode.parse()
        intellij.create()

        for k, v in vscode.document.items():
            intellij.add(context, k, v)

        intellij.write()
