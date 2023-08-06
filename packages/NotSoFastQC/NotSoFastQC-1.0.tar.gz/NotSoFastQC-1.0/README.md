# NotSoFastQC
This package is deigned to generate imitation reports for each module in the FastQC tool. All modules create
filter text and QC report text files and selected modules generate graphs that mimic those seen in FastQC.

### Installation
NotSoFastQC can be installed from my [github repository](https://github.com/jamesfox96/NotSoFastQC), 
either by following the link or using git:
```sh
git clone https://github.com/jamesfox96/NotSoFastQC
cd NotSoFastQC
python setup.py install
```

### Usage
NotSoFastQC can be run from the command line in a variety of ways based on your needs.

To run report generation for all modules:
```sh
NotSoFastQC -I fastqc.txt -O output_directory/ --all
```

*OR*

By manually selecting desired modules:
```sh
NotSoFastQC -I fastqc.txt -O output_directory/ -M 1 2 3 9 10 11
```

Options:
- **-I**: Input FastQC report text file.
- **-O**: Output directory.
- **-D**: To overwrite any folders in selected output directory with the same name as the folders generated.
- **-M**: To select individual module numbers separated by spaces.

*OR*
- **--all**: To select all modules for report generation. This will override any individually selected modules.

Details of modules available for selection are seen here below:

|    Module arg    | Description |
| ---------------- | ----------- |
|        1         | Per base sequence quality |
|        2         | Per tile sequence quality |
|        3         | Per sequence quality scores |
|        4         | Per base sequence content |
|        5         | Per sequence GC content |
|        6         | Per base N content |
|        7         | Sequence Length Distribution |
|        8         | Sequence Duplication Levels |
|        9         | Overrepresented sequences |
|        10        | Adapter Content |
|        11        | K-mer Content |

**Note**: Module 11 (K-mer content) does not produce a FastQC-like graph.
 This is because of missing data in the given files

### Rationale
NotSoFastQC has been created as part of an assignment submission for the [Applied Bioinformatics](https://www.cranfield.ac.uk/courses/taught/applied-bioinformatics)
 module **Introduction to Bioinformatics Using Python** at Cranfield University. The package is designed to use the files
 supplied in the *TestData/* folder.
 
### Contact
James Fox: james-fox@mail.com


