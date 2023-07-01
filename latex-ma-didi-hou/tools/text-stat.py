import textstat
import sys
from optparse import OptionParser

usage = (
    sys.argv[0]
    + " [-t|--tex=<text.tex>] [-h|--help]"
)

parser = OptionParser(usage)

parser.add_option(
    "-t",
    "--tex",
    dest="texFile",
    help="TeX File",
    metavar="text.tex",
    default="text.tex",
)


(options, args) = parser.parse_args()

textstat.set_lang("en")
with open(options.texFile, 'r') as file:
    data = file.read().replace('\n', '')
    grade = textstat.flesch_reading_ease(data)
    print(round(grade))