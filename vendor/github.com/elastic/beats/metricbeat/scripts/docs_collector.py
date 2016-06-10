import os
import yaml

# Collects docs for all modules and metricset


def collect():

    base_dir = "module"
    path = os.path.abspath("module")

    generated_note = """////
This file is generated! See scripts/docs_collector.py
////

"""

    # Iterate over all modules
    for module in os.listdir(base_dir):

        module_doc = path + "/" + module + "/_beat/docs.asciidoc"

        # Only check folders where fields.yml exists
        if os.path.isfile(module_doc) == False:
            continue

        # Create directory for each module
        os.mkdir(os.path.abspath("docs") + "/modules/" + module)

        module_file = generated_note
        module_file += "[[metricbeat-module-" + module + "]]\n"

        with file(module_doc) as f:
            module_file += f.read()

        beat_path = path + "/" + module + "/_beat"

         # Load title from fields.yml
        with open(beat_path + "/fields.yml") as f:
            fields = yaml.load(f.read())
            title = fields[0]["title"]

        config_file = beat_path + "/config.yml"

        # Add example config file
        if os.path.isfile(config_file) == True:

            module_file += """

[float]
=== Example Configuration

The """ + title + """ module supports the standard configuration options which can be found
here <<configuration-metricbeat,here>>. Below is an example of a configuration option:

[source,yaml]
----
metricbeat.modules:
"""

            # Load metricset yaml
            with file(config_file) as f:
                # Add 2 spaces for indentation in front of each line
                for line in f:
                    module_file += line

            module_file += "----\n\n"

        # Add metricsets title as below each metricset adds its link
        module_file += "[float]\n"
        module_file += "=== MetricSets\n\n"
        module_file += "The following MetricSets are available:\n\n"


        module_links = ""
        module_includes = ""

        # Iterate over all metricsets
        for metricset in os.listdir(base_dir + "/" + module):

            metricset_docs = path + "/" + module + "/" + metricset + "/_beat/docs.asciidoc"

            # Only check folders where fields.yml exists
            if os.path.isfile(metricset_docs) == False:
                continue

            link_name = "metricbeat-metricset-" + module + "-" + metricset
            link = "<<" + link_name + "," + metricset + ">>"
            reference = "[[" + link_name + "]]"

            module_links += "* " + link + "\n\n"

            module_includes += "include::" + module + "/" + metricset + ".asciidoc[]\n\n"

            metricset_file = generated_note

            # Add reference to metricset file and include file
            metricset_file += reference + "\n"
            metricset_file += 'include::../../../module/' + module + '/' + metricset + '/_beat/docs.asciidoc[]' + "\n"

            # TODO: This should point directly to the exported fields of the metricset, not the whole module
            metricset_file += """

==== Fields

A description of each field in the MetricSet can be found in the
<<exported-fields-""" + module + """,exported fields>> section

"""

            data_file = path + "/" + module + "/" + metricset + "/_beat/data.json"

            # Add data.json example json document
            if os.path.isfile(data_file) == True:
                metricset_file += "Below is an example document generated by this metricset."
                metricset_file += "\n\n"

                metricset_file += "[source,json]\n"
                metricset_file += "----\n"
                metricset_file += "include::../../../module/" + module + "/" + metricset + "/_beat/data.json[]\n"
                metricset_file += "----\n"

            # Write metricset docs
            with open(os.path.abspath("docs") + "/modules/" + module + "/" + metricset + ".asciidoc", 'w') as f:
                f.write(metricset_file)

        module_file += module_links
        module_file += module_includes

        # Write module docs
        with open(os.path.abspath("docs") + "/modules/" + module + ".asciidoc", 'w') as f:
            f.write(module_file)

if __name__ == "__main__":
    collect()



