import os
import shutil
from annogesiclib.gff3 import Gff3Parser
from annogesiclib.lib_reader import read_wig, read_libs


def check_start_and_end(start, end, covers):
    if (start - 2) < 0:
        c_start = 0
    else:
        c_start = start - 2
    if (end + 2) > len(covers):
        c_end = len(covers)
    else:
        c_end = end + 2
    return c_start, c_end


def detect_coverage(wigs, tran, infos):
    for strain, conds in wigs.items():
        if strain == tran.seq_id:
            for cond, tracks in conds.items():
                for lib_name, covers in tracks.items():
                    track = lib_name.split("|")[-3]
                    lib_strand = lib_name.split("|")[-2]
                    lib_type = lib_name.split("|")[-1]
                    infos[track] = {"avg": -1, "high": -1, "low": -1}
                    total = 0
                    pos = 0
                    c_start, c_end = check_start_and_end(tran.start, tran.end, covers)
                    for cover in covers[c_start: c_end]:
                        cover_pos = pos + c_start
                        if (cover_pos >= tran.start) and (
                                cover_pos <= tran.end):
                            total = cover + total
                            if cover > infos[track]["high"]:
                                infos[track]["high"] = cover
                            if (cover < infos[track]["low"]) or (
                                    infos[track]["low"] == -1):
                                infos[track]["low"] = cover
                        pos += 1
                    infos[track]["avg"] = (float(total) /
                                           float(tran.end - tran.start + 1))


def print_associate(associate, tran, out):
    if associate in tran.attributes.keys():
        out.write("\t" + tran.attributes[associate])
    else:
        out.write("\tNA")


def compare_ta_genes(tran, genes, out):
    ass_genes = []
    if len(genes) != 0:
        for gene in genes:
            if (gene.seq_id == tran.seq_id) and (
                    gene.strand == tran.strand):
                if ((tran.start <= gene.start) and (
                        tran.end >= gene.end)) or (
                        (tran.start >= gene.start) and (
                        tran.end <= gene.end)) or (
                        (tran.start <= gene.start) and (
                        tran.end <= gene.end) and (
                        tran.end >= gene.start)) or (
                        (tran.start >= gene.start) and (
                        tran.start <= gene.end) and (
                        tran.end >= gene.end)):
                    if "gene" in gene.attributes.keys():
                        ass_genes.append(gene.attributes["gene"])
                    elif "locus_tag" in gene.attributes.keys():
                        ass_genes.append(gene.attributes["locus_tag"])
                    else:
                        ass_genes.append("".join([
                            "gene:", str(gene.start), "-",
                            str(gene.end), "_", gene.strand]))
    if len(ass_genes) != 0:
        out.write("\t" + ",".join(ass_genes))
    else:
        out.write("\tNA")


def print_coverage(trans, out, out_gff, wigs_f, wigs_r, gff_file):
    genes = []
    if gff_file is not None:
        gff_f = open(gff_file, "r")
        for entry in Gff3Parser().entries(gff_f):
            if (entry.feature == "gene"):
                genes.append(entry)
    for tran in trans:
        infos = {}
        tran.attributes["detect_lib"] = tran.attributes["detect_lib"].replace(
                                                        "tex_notex", "TEX+/-")
        out.write("\t".join([tran.seq_id, tran.attributes["Name"],
                             str(tran.start), str(tran.end), tran.strand,
                             tran.attributes["detect_lib"]]))
        compare_ta_genes(tran, genes, out)
        print_associate("associated_tss", tran, out)
        print_associate("associated_term", tran, out)
        if tran.strand == "+":
            detect_coverage(wigs_f, tran, infos)
        else:
            detect_coverage(wigs_r, tran, infos)
        out.write("\t")
        best = -1
        best_track = ""
        best_cover = {}
        for track, cover in infos.items():
            if best != -1:
                out.write(";")
            out.write("{0}({1})".format(
                      track, str(cover["avg"])))
            if cover["avg"] > best:
                best = cover["avg"]
                best_track = track
                best_cover = cover
        out.write("\n")
        new_attrs = {}
        for key, value in tran.attributes.items():
            if ("high_coverage" not in key) and (
                    "low_coverage" not in key):
                new_attrs[key] = value
        new_attrs["best_avg_coverage"] = str(best_cover["avg"])
        attribute_string = ";".join(
            ["=".join(items) for items in new_attrs.items()])
        out_gff.write("\t".join([tran.info_without_attributes,
                                 attribute_string]) + "\n")


def gen_table_transcript(gff_folder, args_tran):
    '''generate the detail table of transcript'''
    libs, texs = read_libs(args_tran.libs, args_tran.merge_wigs)
    for gff in os.listdir(gff_folder):
        if os.path.isfile(os.path.join(gff_folder, gff)):
            wigs_f = read_wig(os.path.join(args_tran.wig_path, "_".join([
                              gff.replace("_transcript.gff", ""),
                              "forward.wig"])), "+", libs)
            wigs_r = read_wig(os.path.join(args_tran.wig_path, "_".join([
                              gff.replace("_transcript.gff", ""),
                              "reverse.wig"])), "-", libs)
            th = open(os.path.join(gff_folder, gff), "r")
            trans = []
            out = open(os.path.join(args_tran.out_folder, "tables",
                       gff.replace(".gff", ".csv")), "w")
            out_gff = open(os.path.join(args_tran.out_folder, "tmp_gff"), "w")
            out_gff.write("##gff-version 3\n")
            out.write("\t".join(["Genome", "Name", "Start", "End", "Strand",
                                 "Detect_lib_type", "Associated_gene",
                                 "Associated_tss", "Associated_term",
                                 "Coverage_details"]) + "\n")
            gff_parser = Gff3Parser()
            for entry in gff_parser.entries(th):
                trans.append(entry)
            if args_tran.gffs is not None:
                gff_file = os.path.join(args_tran.gffs,
                                        gff.replace("_transcript", ""))
                if not os.path.isfile(gff_file):
                    gff_file = None
            else:
                gff_file = None
            print_coverage(trans, out, out_gff, wigs_f, wigs_r, gff_file)
            out.close()
            out_gff.close()
            shutil.move(os.path.join(args_tran.out_folder, "tmp_gff"),
                        os.path.join(gff_folder, gff))
