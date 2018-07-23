# Managing the Mouse-Brain-Atlas on the cloud

### Functionality types:

1. **PRE** Preprocessing and section-to-section alignment.
1. **BA** `Browsing and Annotation` - The user retrieves a section and annotates it or corrects the annotation on it, then stores the annotation. This is used across an entire brain to annotate new landmarks or for one or few sections to correct software generated registration.
1. **Reg** `Landmark-based Registration`: This takes a sectioned brain as input and returning registered sections that is annotated with landmarks.
1. **L** `Learning:` Taking a set of registered brain sections as input and generating an improved registration function.

## The cloud
* `AWS` - the amazon cloud
	* `ec2` - computers for rent
	* `s3 / Glacier` - Storage for rent:
		* `S3`: 30$ per TB X Month
		* `Glacier`: 7$ per TB X Month
* `github`,`bitbucket` - repositories with version control (any past version of any committed file can be retrieved). Intended for software/documentation/ anything that is small (typically < 1MB).

## Programming languages
* `Python` - an interpreted language, easy to learn and write in, weak type-checking. Has an extensive set of libraries.
	* `pip, conda` - installers for python libraries
	* Installing a python program requires first installing python and  the set of required libraries - can be a pain to make work on all operating systems.
* `Jupyter Notebook` A development environment that is good for experimenting and documenting the experiments. Not good for distribution of code.
* `C++` - the standard language for writing efficient, stand-alone computer code.
   * Installation requires linking with libraries. Creating a reliable installation is hard.
* `sh, bash` - languages used to write scripts for the unix/mac.
* `javascript` - A language that runs inside a browser sandbox. re
