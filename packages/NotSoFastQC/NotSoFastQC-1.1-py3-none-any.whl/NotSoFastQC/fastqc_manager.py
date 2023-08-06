import sys
import re
import os
import csv
import shutil
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import scipy.stats as stats
from tabulate import tabulate
from NotSoFastQC.modules import module_dict as md
from NotSoFastQC.utils import TerminalLog as Log


ENTRY = ">>"
END_MODULE = ">>END_MODULE"

FILTER_TEXT = 0
HEADER = 1
ROWS = 2


# Class that represents an object processing the FastQC file input and generating all data needed.
# Graph generation functions can most probably be optimised as there is some repeated code.
# Each graph is slightly different however and would need a bit of re-shuffling to work. Something to work on maybe.
class FastQCManager:
    """FastQCManager takes the user input validated args and creates reports for all selected modules.
    Table of Basic Statistics gets displayed in console
    """

    def __init__(self, validated_args, overwrite):

        self.file = validated_args[0]
        self.directory = validated_args[1]
        self.modules = validated_args[2]
        self.encoding = None

        Log.notify("STARTING MODULE REPORTS...")
        # Creates directory and reports for each module in succession.
        # Could be optimised so that file doesn't need to be opened and parsed for each module given
        for module in self.modules:
            self.module_name = md.get(module)
            self.working_path = os.path.join(self.directory, self.module_name.replace(' ', '_'))
            self.build_directory(overwrite)

            self.data = self.pull_data(self.module_name)
            self.write_reports()

            # For some reason graph generation doesn't work in terminal but does in PyCharm... can't figure this out.
            # I know it is exclusively to do with sns.lineplot() (based on console output), but works fine in my IDE?
            # With longer deadline, I think this could be fixed by altering code, but will probably take time.
            try:
                self.switch_graph(module)
            except IndexError:
                Log.warning("Graph cannot be made, this problem is recognised.")

        self.show_basic_statistics()

    def mod_1_graph(self):
        """Creates graph for Per base sequence quality"""

        data = []
        bases = []
        means = {}

        # Puts data into format that can be used for creating graphs
        for row in self.data[ROWS]:
            bases.append(row[0])
            means[int(row[0])-1] = float(row[1])
            data.append([row[5], row[3], row[2], row[4], row[6]])

        # Sets window size for graph
        fig, ax = plt.subplots(figsize=(12, 10))

        sns.boxplot(data=data, whis=[0, 100], color="yellow", zorder=1)
        sns.lineplot(data=means, ax=ax, zorder=10)

        # Axis configuration
        ax.set(xticklabels=bases, title="Quality scores across all bases (" + self.encoding + " encoding)")
        ax.set(ylim=0)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(base=2))

        plt.xlabel('Position in read (bp)')

        # Formats colour for background of graph
        for line in ax.get_lines()[4::6]:
            line.set_color('red')

        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(10)

        for i in range(0, len(bases)):
            if i % 2 == 0:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0.08, zorder=-100)
            else:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0, zorder=-100)

        for i in range(0, int(ax.get_ylim()[1]) + 2):
            if i <= 20:
                plt.axhspan(i - 1, i, facecolor='red', alpha=0.3, zorder=-100)
            elif 20 < i <= 28:
                plt.axhspan(i - 1, i, facecolor='yellow', alpha=0.3, zorder=-100)
            else:
                plt.axhspan(i - 1, i, facecolor='green', alpha=0.3, zorder=-100)

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_2_graph(self):
        """Creates graph for Per tile sequence quality"""

        # Puts data in format for creating graph
        df = pd.DataFrame(self.data[ROWS], columns=["Tile", "Position in read (bp)", "value"])
        df["value"] = pd.to_numeric(df["value"], downcast="float")
        df["Position in read (bp)"] = pd.to_numeric(df["Position in read (bp)"], downcast="integer")

        table = df.pivot(index="Tile", columns="Position in read (bp)", values="value")

        # axis configuration
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.set(title="Quality per tile")

        sns.heatmap(data=table, cmap="rainbow_r", linewidths=0.3, ax=ax, vmin=-1, vmax=1, cbar=False)

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_3_graph(self):
        """Creates graph for Per sequence quality scores"""

        data = {}

        # Puts data in format for graph
        for row in self.data[ROWS]:
            data[int(row[0])] = float(row[1])

        fig, ax = plt.subplots(figsize=(12, 10))

        # Axis configuration
        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))

        keys = []

        for key in data.keys():
            keys.append(key)

        ax.set(title="Quality score distribution over all sequences", xlim=(keys[0] - 0.5, keys[-1] + 1))
        plt.ticklabel_format(style='plain', axis='y')

        # Formats colour for background of graph
        for i in range(keys[0], keys[-1] + 1):
            if i % 2 == 0:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0.08, zorder=-100)
            else:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0, zorder=-100)

        sns.lineplot(data=data, ax=ax, color='red')
        plt.legend(labels=['Average quality per read'])

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_4_graph(self):
        """Creates graph for Per base sequence content"""

        g = {}
        a = {}
        t = {}
        c = {}

        # Puts data in format for creating graph
        for row in self.data[ROWS]:
            g[int(row[0])] = float(row[1])
            a[int(row[0])] = float(row[2])
            t[int(row[0])] = float(row[3])
            c[int(row[0])] = float(row[4])

        fig, ax = plt.subplots(figsize=(12, 10))

        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))

        keys = []

        for key in g.keys():
            keys.append(key)

        # axis configuration
        ax.set(title="Sequence content across all bases", xlim=(keys[0] - 0.5, keys[-1] + 0.5), ylim=(0, 100))
        plt.ticklabel_format(style='plain', axis='y')

        # Formats colour for background of graph
        for i in range(keys[0], keys[-1] + 1):
            if i % 2 == 0:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0.08, zorder=-100)
            else:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0, zorder=-100)

        sns.lineplot(data=g, ax=ax, color='red')
        sns.lineplot(data=a, ax=ax, color='blue')
        sns.lineplot(data=t, ax=ax, color='green')
        sns.lineplot(data=c, ax=ax, color='black')

        plt.legend(labels=['%G', '%A', '%T', '%C'])

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_5_graph(self):
        """Creates graph for Per sequence GC content"""

        data = {}

        # Puts data in format for creating graph
        for row in self.data[ROWS]:
            data[int(row[0])] = float(row[1])

        keys = []
        values = []
        maximum = 0
        mode = 0

        for key in data.keys():
            keys.append(key)
            val = data.get(key)
            values.append(val)
            if val > maximum:
                maximum = val
                mode = key

        # axis configuration
        fig, ax = plt.subplots(figsize=(12, 10))

        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=5))
        ax.set(title="Quality score distribution over all sequences", xlim=(keys[0] - 0.5, keys[-1] + 1))

        plt.ticklabel_format(style='plain', axis='y')

        # Formats colour for background of graph
        for i in range(keys[0], keys[-1] + 1):
            if i % 2 == 0:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0.08, zorder=-100)
            else:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0, zorder=-100)

        sns.lineplot(data=data, ax=ax, color='red')

        x = np.linspace(0, 100, 1000)
        plt.plot(x, sum(values) * stats.norm.pdf(x, mode, 10))

        plt.xlabel('Mean GC content (%)')
        plt.ylim(0, maximum + (maximum/10))
        plt.legend(labels=['GC count per read', 'Theoretical distribution'])

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_6_graph(self):
        """Creates graph for Per base N content"""

        data = {}

        # Puts data in format for creating graph
        for row in self.data[ROWS]:
            data[int(row[0])] = float(row[1])

        fig, ax = plt.subplots(figsize=(12, 10))

        # axis configuration
        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))

        keys = []

        for key in data.keys():
            keys.append(key)

        ax.set(title="Quality score distribution over all sequences", xlim=(keys[0] - 0.5, keys[-1] + 1))
        plt.ticklabel_format(style='plain', axis='y')

        # Formats colour for background of graph
        for i in range(keys[0], keys[-1] + 1):
            if i % 2 == 0:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0.08, zorder=-100)
            else:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0, zorder=-100)

        sns.lineplot(data=data, ax=ax, color='red')

        plt.ylim(0, 100)
        plt.legend(labels=['%N'])

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_7_graph(self):
        """Creates graph for Sequence Length Distribution"""

        data = {}

        # Puts data in format for creating graph
        for row in self.data[ROWS]:
            if row[1].find('E') >= 0:
                temp = row[1].split('E')
                data[int(row[0])] = float(temp[0]) * math.pow(10, int(temp[1]))
            else:
                data[int(row[0])] = int(row[1])

        fig, ax = plt.subplots(figsize=(12, 10))

        keys = []

        # Warning for this part of the code, I think it's because data{} can be empty. Isn't a problem when running.
        for key in data.keys():
            keys.append(key)

        # axis configuration
        if len(data) == 1:
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
            data[keys[0] - 1] = 0
            data[keys[0] + 1] = 0
        else:
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))

        keys = []

        for key in data.keys():
            keys.append(key)
        keys.sort()

        ax.set(title="Distribution of sequence lengths over all sequences", xlim=(keys[0] - 0.5, keys[-1] + 0.5))
        plt.ticklabel_format(style='plain', axis='y')

        # Formats colour for background of graph
        for i in range(keys[0], keys[-1] + 1):
            if i % 2 == 0:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0.08, zorder=-100)
            else:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0, zorder=-100)

        sns.lineplot(data=data, ax=ax, color='red')

        plt.ylim(0)
        plt.xlabel("Sequence length (bp)")
        plt.legend(labels=['Sequence length'])

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_8_graph(self):
        """Creates graph for Sequence Duplication Levels"""

        deduplicated_percent = float(self.data[HEADER][0][1])

        deduplicated = {}
        total = {}
        count = 1
        labels = []

        # Puts data in format for creating graph
        for row in self.data[ROWS]:
            deduplicated[count] = float(row[1])
            total[count] = float(row[2])
            labels.append(row[0])
            count += 1

        fig, ax = plt.subplots(figsize=(12, 10))

        # axis configuration
        ax.yaxis.set_major_locator(ticker.MultipleLocator(base=10))

        keys = []

        for key in deduplicated.keys():
            keys.append(key)

        ax.set(title="Percent of seqs remaining if deduplicated " + "{:.2f}".format(deduplicated_percent) + "%",
               xlim=(keys[0] - 0.5, keys[-1] + 1))
        plt.ticklabel_format(style='plain', axis='y')

        # Formats colour for background of graph
        for i in range(keys[0], keys[-1] + 1):
            if i % 2 == 0:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0.08, zorder=-100)
            else:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0, zorder=-100)

        sns.lineplot(data=deduplicated, ax=ax, color='red')
        sns.lineplot(data=total, ax=ax, color='blue')

        plt.ylim(0, 100)
        plt.xticks(ticks=keys, labels=labels)
        plt.xlabel("Sequence duplication level")
        plt.legend(labels=['% Deduplicated sequences', '% Total sequences'])

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_10_graph(self):
        """Creates graph for Adapter Content"""

        iua = {}
        isra = {}
        nts = {}
        ssra = {}

        # Puts data in format for creating graph
        for row in self.data[ROWS]:
            iua[int(row[0])] = float(row[1])
            isra[int(row[0])] = float(row[2])
            nts[int(row[0])] = float(row[3])
            ssra[int(row[0])] = float(row[4])

        fig, ax = plt.subplots(figsize=(12, 10))

        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=2))

        keys = []

        for key in iua.keys():
            keys.append(key)

        # axis configuration
        ax.set(title="% Adapter", xlim=(keys[0] - 0.5, keys[-1] + 0.5), ylim=(0, 100))
        plt.ticklabel_format(style='plain', axis='y')

        # Formats colour for background of graph
        for i in range(keys[0], keys[-1] + 1):
            if i % 2 == 0:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0.08, zorder=-100)
            else:
                plt.axvspan(i - 0.5, i + 0.5, facecolor='black', alpha=0, zorder=-100)

        sns.lineplot(data=iua, ax=ax, color='red')
        sns.lineplot(data=isra, ax=ax, color='blue')
        sns.lineplot(data=nts, ax=ax, color='green')
        sns.lineplot(data=ssra, ax=ax, color='black')

        plt.xlabel("Position in read (bp)")
        plt.legend(labels=['Illumina Universal Adapter', 'Illumina Small RNA Adapter',
                           'Nextera Transposase Sequence', 'SOLID Small RNA Adapter'])

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def mod_11_graph(self):
        """Creates graph for Kmer Content"""

        kmers = []
        counts = []

        # Puts data in format for creating graph
        for row in self.data[ROWS]:
            kmers.append(row[0])
            counts.append(int(row[1]))

        fig, ax = plt.subplots(figsize=(12, 10))

        # working out values for x axis tick labels
        max_count = max(counts)
        max_count = max_count + 1000 - max_count % 1000

        # axis configuration
        ax.xaxis.set_major_locator(ticker.MultipleLocator(base=(max_count / 10)))

        ax.set(title="K-mer counts")
        plt.xlabel("Counts")
        plt.ylabel("K-mers")

        sns.barplot(x=counts, y=kmers, ax=ax, color='gray')

        plt.savefig(os.path.join(self.working_path, "graph.png"))

    def switch_graph(self, module):
        """Switch-like method to call graph creation for a given module"""

        Log.notify("Creating graph for module [" + self.module_name + "]")

        # Could be optimised for speed if using a dictionary possibly, but isn't too great a deal with so few choices
        if module == 1:
            self.mod_1_graph()
        elif module == 2:
            self.mod_2_graph()
        elif module == 3:
            self.mod_3_graph()
        elif module == 4:
            self.mod_4_graph()
        elif module == 5:
            self.mod_5_graph()
        elif module == 6:
            self.mod_6_graph()
        elif module == 7:
            self.mod_7_graph()
        elif module == 8:
            self.mod_8_graph()
        elif module == 10:
            self.mod_10_graph()
        elif module == 11:
            self.mod_11_graph()
        else:
            Log.confirm("\tNo graph needed for module [" + self.module_name + "]")
            return

        Log.confirm("\tGraph created for module [" + self.module_name + "]")

    def write_reports(self):
        """Writes filter_text.txt and QC_report.txt files for a given module"""

        # Write filter_text file
        with open(os.path.join(self.working_path, "filter.txt"), 'w') as file:
            file.write(self.data[FILTER_TEXT])

        # Write QC_report file
        with open(os.path.join(self.working_path, "QC_report.txt"), 'w') as file:
            tsv_output = csv.writer(file, delimiter='\t')

            # write headers
            for row in self.data[HEADER]:
                file.write('#')
                tsv_output.writerow(row)
            # write rows
            for row in self.data[ROWS]:
                tsv_output.writerow(row)

        Log.confirm("\tReport files successfully created for module ["
                    + self.module_name + "]")

    def build_directory(self, overwrite):
        """Builds a directory for a given module. Will delete pre-existing directory
        with matching name if [-D] is selected in args
        """

        # Attempts to build directory, catches exception if folder already exists
        try:
            Log.notify("\nBuilding directory [" + self.working_path + "]...")
            os.mkdir(self.working_path)
        except FileExistsError:
            # If option to overwrite existing directories has been selected
            if overwrite:
                Log.warning("Directory already exists. [-D] selected, deleting existing directory...")
                shutil.rmtree(self.working_path)
                os.mkdir(self.working_path)
            # Else, exit program
            else:
                Log.fail("\n Folder in output directory named [" + self.working_path + "] already exists."
                         "\n Please choose an empty working directory to avoid this problem or select "
                         "[-D] as a parameter to overwrite pre-existing files.")
                sys.exit(30)

        Log.confirm("Directory [" + self.working_path + "] created.")

    def pull_data(self, module_name):
        """Returns list of filter text, header/s and row/s. Also sets encoding variable for use in some graphs"""

        filter_text = ''
        header = []
        table = []

        with open(self.file) as f:
            for line in f:
                line = line.lower()
                # Searching for entry point of a given module, sets filter text and breaks when found
                if line.startswith(ENTRY + module_name.lower()):
                    filter_text = re.sub(ENTRY + module_name.lower() + '[\t]', '', line).strip('\n')
                    break
            for line in f:
                # Searching for exit point, breaks when found
                if line.startswith(END_MODULE):
                    break
                # If line is a header, add text to header[]
                if line.startswith('#'):
                    line = line.replace('#', '')
                    header.append(line.replace('\n', '').split('\t'))
                # Else, text is part of row data
                else:
                    # sets encoding variable used in mod_1_graph() - found in basic statistics
                    # this is always found before mod_1_graph() is called as basic statistics is first module parsed
                    if line.startswith("Encoding"):
                        self.encoding = line.replace("Encoding\t", '').strip('\n')
                    # add text to table[]
                    table.append(line.replace('\n', '').split('\t'))

        return filter_text, header, table

    def show_basic_statistics(self):
        """Creates table of Basic Statistics to display to console window."""

        data = self.pull_data("Basic Statistics")
        header = data[HEADER][0]
        rows = data[ROWS]

        Log.notify("\nBasic Statistics:\n")
        # formats into a nice-looking table
        Log.bold(tabulate(rows, headers=header))
