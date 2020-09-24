"""Main module."""
import sys
import runpy
import argparse
from typing import List, Union, Iterator, Protocol, Sequence

from beancount.ingest import importer
from beancount.loader import load_file
from beancount.core.data import Balance, Transaction
from beancount.ingest.extract import print_extracted_entries


class FetcherProtocol(Protocol):
    def fetch(self) -> Iterator[Union[Transaction, Balance]]:
        ...


def main(args: List[str] = None) -> Sequence[Union[Transaction, Balance]]:
    if args is None:
        args = sys.argv
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    parser.add_argument("-e", "--exist")
    result = parser.parse_args(args)
    if result.exist:
        existed_entries = load_file(result.exist)[0]
    else:
        existed_entries = None
    extracted = []
    for f in result.files[1:]:
        mod = runpy.run_path(f)
        config: List[importer.ImporterProtocol] = mod["CONFIG"]
        for imp in config:
            extracted.extend(imp.extract(None, existed_entries))
    return extracted


if __name__ == "__main__":
    print_extracted_entries(main(), sys.stdout)
