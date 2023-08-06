"""
This is an example parser used to show how to use the Dispatcher model to organize Parsers by their components.
"""

import re

from mwcp import Parser, FileObject
from mwcp.utils import construct
from mwcp.utils import pefileutils


class Carrier(Parser):
    """A carrier for the Bar dropper."""

    DESCRIPTION = "Bar Carrier"

    MARKER = re.compile(b"BARCAR\x01\x02(?P<embed_data>.+)\x02\x01CARBAR")

    @classmethod
    def identify(cls, file_object):
        """
        Identifies Bar carrier by looking for a PE file that has the BARCAR\x01\x02 carrier.

        :returns: boolean indicating if file is a Bar Carrier.
        """
        return file_object.pe and cls.MARKER.search(file_object.file_data)

    def run(self):
        """Extracts config and embedded Bar dropper."""
        # Pull embedded dropper.
        match = self.MARKER.search(self.file_object.file_data)
        embed_data = match.group("embed_data")

        # Dispatch embedded dropper to be picked up by another ComponentParser.
        self.dispatcher.add_to_queue(FileObject(embed_data, self.reporter))


class Dropper(Parser):
    """A dropper for the Bar implant."""

    DESCRIPTION = "Bar Dropper"

    @classmethod
    def identify(cls, file_object):
        """
        Identifies Bar dropper by looking for '.DROPPER' resource directory.

        :returns: boolean indicating if file is a Bar Dropper.
        """
        return file_object.pe and pefileutils.check_rsrc_dir(".DROPPER", pe=file_object.pe)

    def run(self):
        """Extracts config and embedded Implant files."""
        # Dispatch all the files in the ".DROPPER" resource directory.
        for rsrc in pefileutils.iter_rsrc(self.file_object.pe, ".DROPPER"):
            self.dispatcher.add_to_queue(FileObject(rsrc.data, self.reporter, file_name=rsrc.idname))


class Implant(Parser):
    """A Bar implant found as a python script."""

    DESCRIPTION = "Bar Implant"

    @classmethod
    def identify(cls, file_object):
        """
        Identifies Bar implant by looking for the .py extension.
        (This condition is unique enough for the Bar family for now.)

        :returns: boolean indicating if file is a Bar Dropper.
        """
        return file_object.file_name.endswith(".py")

    def run(self):
        """Extracts config and embedded Implant files."""
        # Extract the callback and port numbers found in this python script.
        for match in re.finditer(b"http://(?P<callback>.+?):(?P<port>\d+)", self.file_object.file_data):
            callback, port = match.groups()
            self.reporter.add_metadata("c2_socketaddress", (callback, port, "tcp"))


class ImplantV2(Parser):
    """An alternative version of Bar Implant using an exe instead."""

    DESCRIPTION = "Bar Implant V2"

    CALLBACK_RE = re.compile(b"BARCALL:(?P<callback>.+?):(?P<port>\d+)", re.DOTALL)
    CALLBACK = construct.Regex(CALLBACK_RE, port=construct.Int32ul)

    @classmethod
    def identify(cls, file_object):
        """
        Identifies Bar implant by looking for a PE file contains some markers we are looking for.
        (Since this ComponentParser is the last in the list

        :returns: boolean indicating if file is a Bar Dropper.
        """
        return file_object.pe and cls.CALLBACK_RE.search(file_object.file_data)

    def run(self):
        """Extracts config and embedded Implant files."""
        # Extract the callback and port numbers found in this .exe script.
        for config in self.CALLBACK[:].parse(self.file_object.file_data):
            self.reporter.add_metadata("c2_socketaddress", (config.callback, str(config.port), "tcp"))
