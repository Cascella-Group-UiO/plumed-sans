import argparse
import os

# atomic scattering lengths
# Sears, Neutron News, 3, 26 (1992)
at_scatlen = {
    "H": -3.7406,
    "D": 6.671,
    "C": 6.6511,
    "N": 9.37,
    "O": 5.803,
    "P": 5.13,
    "S": 2.804,
    "Na": 3.63,
}


def get_one_molecule_scatlen(filehandler):
    """Calculate scattering lengths for a single molecule"""
    # create beads dictionary
    for line in filehandler:
        if "[ martini ]" in line:
            break

    line = filehandler.readline()  # read line with beads

    beads = {b: [] for b in line.split()}

    # add atom types to beads
    for line in filehandler:
        if "[ atoms ]" in line:
            break

    for line in filehandler:
        idx, atom, bead = line.split()
        if atom[:2] in at_scatlen.keys():
            atname = atom[:2]
        elif atom[0] in at_scatlen.keys():
            atname = atom[0]
        else:
            raise AssertionError(f"Atom name for {atom} not found in at_scatlen dictionary.")
        beads[bead].append(atname)

    filehandler.close()

    nbeads = len(beads.items())

    out_scatlens = ""
    # for each bead compute the scattering length
    for k, v in beads.items():
        bslen = 0.0
        for at in v:
            bslen += at_scatlen[at]

        out_scatlens += "SCATLEN{{}}={:.4f}\n".format(bslen)

    return nbeads, out_scatlens


def write_scatlen_file(
    outfile, single_scatlens, n_beads, n_mol, start_index, overwrite, append
):
    """Given the scattering lengths for a molecule, repeat it to have
    the whole system and write to a file."""
    if os.path.exists(outfile) and not (overwrite or append):
        error_str = (
            f"The specified output file {outfile} already exists. "
            f'Use --overwrite ("-f" flag) to overwrite '
            f'or --append ("-a" flag) to append. '
            f'You can also write to a different file with --outfile ("-o" flag).'
        )
        raise FileExistsError(error_str)

    write_mode = "a" if append else "w"

    with open(outfile, write_mode) as f:
        for i in range(n_mol):
            atnum = []
            for j in range(1, n_beads + 1):
                atnum.append(i * n_beads + start_index - 1 + j)
            f.write(single_scatlens.format(*atnum))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given a .map file from CGBuilder, creates file containing the SCATLEN to be included in PLUMED."
    )
    parser.add_argument("mapfile", type=argparse.FileType("r"), help=".map file")
    parser.add_argument("nmol", type=int, help="number of molecules")
    parser.add_argument(
        "-o",
        "--outfile",
        default="scatlens.plumed",
        help='output file containing the SCATLENs (default="scatlens.plumed")',
    )
    parser.add_argument(
        "-f",
        "--overwrite",
        default=False,
        action="store_true",
        help="force overwrite of output file",
    )
    parser.add_argument(
        "-a",
        "--append",
        default=False,
        action="store_true",
        help="append output to file if file already exists.",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=1,
        help="starting index YYY for SCATLENYYY (default=1)",
    )
    args = parser.parse_args()

    # get the sctattering lengths for a single molecule
    n_beads, single_scatlens = get_one_molecule_scatlen(args.mapfile)

    # write the scatlen file
    write_scatlen_file(
        args.outfile,
        single_scatlens,
        n_beads,
        args.nmol,
        args.start_index,
        args.overwrite,
        args.append,
    )
