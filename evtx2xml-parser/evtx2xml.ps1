from Evtx.Evtx import Evtx
import sys

input_file = ".\eventlog.evtx"
output_file = "eventlog.xml"

with Evtx(input_file) as evtx_log, open(output_file, "w") as xml_file:
    xml_file.write("<Events>\n")
    for record in evtx_log.records():
        xml_file.write(record.xml() + "\n")
    xml_file.write("</Events>")

