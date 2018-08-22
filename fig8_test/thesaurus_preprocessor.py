#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import csv
import xml.etree.ElementTree as ET


terms = {}
synonyms = {}
hierarchy = {}
relations = {}


def create_html_list(array):

    html = "<ul>"
    for item in array:
        html += "<li>{}</li>".format(item)

    html += "</ul>"
    return html

def main(skos_xml_file):
    #########################
    # Read skos definitions #
    #########################

    print("Reading SKOS file")

    # Set up XML parsing
    ns = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
          'skos': 'http://www.w3.org/2004/02/skos/core#',
          'cogitos': 'http://www.expertsystem.com/cogito-schema#'}

    tree = ET.parse(skos_xml_file)
    root = tree.getroot()

    x = 0

    # Process the XML
    for sage_term_el in root.findall('rdf:Description', ns):

        # Obtain the Term ID
        # Employs a workaround for python's poor XML namespace support for attributes
        term_attrib_key = "{" + ns['rdf'] + "}about"
        term_id = sage_term_el.get(term_attrib_key)

        # Use the first preferred label that is found
        pref_label = sage_term_el.find('skos:prefLabel', ns).text

        synonyms = []
        for alt_label_el in sage_term_el.findall('skos:altLabel', ns):
            synonyms.append( alt_label_el.text )

        classes = []
        for alt_label_el in sage_term_el.findall('cogitos:class', ns):
            rdf_resource_key = "{" + ns['rdf'] + "}resource"
            classes.append( alt_label_el.get(rdf_resource_key) )

        defs = []
        for def_el in sage_term_el.findall('skos:definition', ns):
            defs.append( def_el.text )


        # Store the term
        terms[term_id] = {
            'TermID': term_id,
            'PreferredTerm': pref_label,
            'Synonyms' : synonyms,
            'Classes': classes,
            'Definitions' : defs
        }

        x += 1
        if x > 100:
            break


    # Write the SRM terms to a node file
    with open("thesaurus.csv", 'w') as csvfile:

        print("Writing {}".format(csvfile.name))

        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        csvwriter.writerow(['TermID','PreferredTerm', 'Synonyms', 'Classes', 'Definitions'])
        for id in terms:
            term = terms[id]
            syn_field = '<br>'.join(term['Synonyms'])
            class_field = '<br>'.join(term['Classes'])
            def_field = create_html_list( term['Definitions'] )
            csvwriter.writerow([ term['TermID'], term['PreferredTerm'], syn_field, class_field, def_field])



if __name__ == "__main__":
    main(sys.argv[1])
