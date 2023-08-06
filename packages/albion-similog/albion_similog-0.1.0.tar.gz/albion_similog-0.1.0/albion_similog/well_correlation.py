"""Well correlation using FAMSA algorithm, originally developped in biological studies. For more
details, see https://github.com/refresh-bio/FAMSA.

"""

import os
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from pychangepoints import algo_changepoints
from skbio import read
from skbio.alignment import TabularMSA
from skbio.sequence import Protein
from sklearn import linear_model, preprocessing

from albion_similog.log import setup_logger


logger = setup_logger(__name__)

FAMSA_PATH = Path("famsa-workdir")
FAMSA_PATH.mkdir(exist_ok=True)


def compute_mean_segmentation(vector, indices):
    """

    Parameters
    ----------

    Results
    -------
    """
    n = len(indices) - 1
    resultat = np.zeros(n)
    for j in range(n):
        sub_well = vector[indices[j] : indices[j + 1]]
        resultat[j] = np.mean(sub_well)
    return resultat


def consensus_pd(msa, freq):
    """

    Parameters
    ----------

    Results
    -------
    """
    consensus = ""
    for position in msa.columns:
        h = msa[position].value_counts()
        res = h.idxmax().decode("utf-8")
        if (res == "-") & (h[0] < freq * len(msa)):
            res = h.index[1].decode("utf-8")
        consensus = consensus + (res)
    return consensus


def classif_SAX(data, vect_quantile, vect_alphabet):
    """

    Parameters
    ----------

    Results
    -------
    """
    indice = 0
    vect_limit = np.concatenate((np.array([-1e8]), np.append(vect_quantile, 1e8)))
    while data > vect_limit[indice]:
        indice = indice + 1
    a = vect_alphabet[indice - 1]
    return a


def custom_SAX(data, vect_quantile, vect_alphabet):
    """

    Parameters
    ----------

    Results
    -------
    """
    resultat = ""
    for j in data:
        resultat = resultat + classif_SAX(j, vect_quantile, vect_alphabet)
    return resultat


class algo_correlation:
    """WellCorrelation class."""

    def __init__(
        self,
        data_log,
        data_tops,
        variable_match_,
        MIN_SEG_,
        PELT_sup_,
        NORM_,
        PELT_,
        UNSUPERVISED_,
    ):
        self.variable_match = variable_match_
        self.MIN_SEG = MIN_SEG_
        self.PELT_sup = PELT_sup_
        self.NORM = NORM_
        self.PELT = PELT_
        self.UNSUPERVISED = True
        self.depth_min_MIN = 10
        self.depth_max_MAX = 200
        self.PENALTY_PELT = int(1e-8)
        self.CONSENSUS_per = 0.5
        self.quantiles_list = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
        self.vect_alphabet = np.array(
            [
                "A",
                "R",
                "N",
                "D",
                "C",
                "Q",
                "E",
                "G",
                "H",
                "I",
                "L",
                "K",
                "M",
                "F",
                "P",
                "S",
                "T",
                "W",
                "Y",
                "V",
                "B",
                "Z",
                "X",
            ]
        )[0 : (len(self.quantiles_list) + 1)]

        self.data_log = data_log
        self.data_tops = data_tops
        self.data_log_prepared = []
        self.list_well = data_log["API"].unique()
        self.depth_name = "MD"
        self.log_normalisation = True

        self.sequence_logs = []
        self.dict_data = {}
        self.dict_data_original = {}
        self.select_tops = []
        self.value_alphabet = []
        self.results_unsupervised = None
        self.depth_match_global_algo = None
        self.dict_segmentation = {}
        self.list_wells = None
        self.consensus = None
        self.index_global_consensus = None
        self.dict_res_tops = None
        self.tops_alg_pd = None

    def prepare_logs(self):
        """

        Parameters
        ----------

        """
        short_sequences = []
        quantile_wells = []
        all_data = np.array([])
        all_squared_data = np.array([])

        for well_api in self.list_well:
            depth_min = self.depth_min_MIN
            depth_max = self.depth_max_MAX
            current_MIN_SEG = self.MIN_SEG

            query = self.data_log.loc[self.data_log.API == well_api].copy()
            query.set_index(self.depth_name, inplace=True)
            query.dropna(inplace=True)

            query = query.loc[(query.index > depth_min) & (query.index < depth_max)]
            query = query[query[self.variable_match] > 0]
            query = query[query[self.variable_match] < 1000]
            if self.log_normalisation:
                query[self.variable_match] = np.log(query[self.variable_match])

            ref_match = query

            if self.PELT:
                method = "mll_mean"
                scale_dat = pd.DataFrame(
                    preprocessing.scale(ref_match[[self.variable_match]])
                )
                seg_temp = algo_changepoints.pelt(
                    scale_dat, self.PENALTY_PELT, current_MIN_SEG, method
                )[0]
                seg_temp = np.sort(seg_temp)
                seg_match_small = seg_temp - 1
            else:
                seg_match_small = np.arange(
                    0, len(ref_match[[self.variable_match]]), current_MIN_SEG
                ).astype(int)

            well_name = str(well_api)
            self.dict_segmentation[well_name] = seg_match_small
            mean_query = compute_mean_segmentation(
                query[[self.variable_match]].values, seg_match_small
            )
            pd_mean_query = pd.DataFrame({self.variable_match: (mean_query)})
            self.dict_data[well_name] = pd_mean_query
            self.dict_data_original[well_name] = query
            quantile_wells.append(
                pd_mean_query[self.variable_match].quantile(self.quantiles_list)
            )
            all_data = np.concatenate((all_data, pd_mean_query[self.variable_match]))
            all_squared_data = np.concatenate(
                (all_squared_data, pd_mean_query[self.variable_match])
            )

        quantile_wells = np.array(quantile_wells)
        global_quantiles = np.mean(quantile_wells, axis=0)
        u = pd.DataFrame({self.variable_match: (all_squared_data)})
        del all_squared_data
        del all_data
        global_quantiles = u[self.variable_match].quantile(self.quantiles_list)

        lr = linear_model.LinearRegression()

        for key, well in self.dict_data.items():
            query = well
            lr.fit(
                query[self.variable_match]
                .quantile(self.quantiles_list)
                .values.reshape(-1, 1),
                global_quantiles.values.reshape(-1, 1),
            )

            if self.NORM:
                query[self.variable_match + "_norm"] = lr.predict(
                    query[[self.variable_match]]
                )
            else:
                query[self.variable_match + "_norm"] = query[[self.variable_match]]

            sequence = custom_SAX(
                (query[self.variable_match + "_norm"]),
                global_quantiles,
                self.vect_alphabet,
            )
            rec1 = SeqRecord(Seq(sequence), id=key, description=key)
            short_sequences.append(rec1)
        self.sequence_logs = short_sequences

        global_quantiles_vect = global_quantiles.values
        global_quantiles_vect_value = np.append(
            global_quantiles_vect, (u[self.variable_match].quantile(0.975))
        )

        global_quantiles_vect_value = np.concatenate(
            [
                np.array([u[self.variable_match].quantile(0.01)]),
                global_quantiles_vect_value,
            ]
        )
        global_quantiles_vect_value = (
            np.diff(global_quantiles_vect_value) / 2
            + global_quantiles_vect_value[0 : len(global_quantiles_vect_value) - 1]
        )
        self.value_alphabet = pd.DataFrame(
            {"alphabet": self.vect_alphabet, "quantile": global_quantiles_vect_value}
        ).set_index("alphabet")
        self.global_quantiles_vect = global_quantiles_vect
        SeqIO.write(short_sequences, FAMSA_PATH / "short_seqs.fasta", "fasta")

    def run_algorithm_unsupervised(self):
        """

        Parameters
        ----------

        """
        try:
            os.remove(FAMSA_PATH / "result_famsa.fasta")
        except Exception:
            pass
        subprocess.call(
            [
                "./famsa",
                "-go",
                "20",
                "-ge",
                "5",
                "-r",
                "100",
                str(FAMSA_PATH / "short_seqs.fasta"),
                str(FAMSA_PATH / "result_famsa.fasta"),
            ]
        )
        method = "famsa"
        # dict position alignment
        depth_match_global_algo = {}
        depth_match_global = {}
        series = []
        # import alignment
        msa = read(
            str(FAMSA_PATH / "result_famsa.fasta"),
            format="fasta",
            into=TabularMSA,
            constructor=Protein,
        )

        list_p = []

        u = msa.to_dict()
        # u_d data_frame of the alignment without the API
        u_d = pd.DataFrame(u).transpose()
        # " extract the API
        for j in range(len(u_d)):
            list_p.append(msa.loc[j].metadata["id"])
        list_p = np.array(list_p)
        u_d["API"] = list_p
        u_d.set_index("API", inplace=True)
        u_d.sort_index(inplace=True)
        # u_d is now clean
        # construction of the consensus (percentage of the letter)
        msa_consensus = consensus_pd(u_d, self.CONSENSUS_per)
        msa_consensus_clean = ""
        index_clean_consensus = []
        index_clean_global_consensus = []
        # consensus index
        count_consensus = 0
        for j in range(len(msa_consensus)):
            if msa_consensus[j] != "-":
                index_clean_consensus.append(j)
                msa_consensus_clean += msa_consensus[j]
                count_consensus += 1
            index_clean_global_consensus.append(count_consensus)
        index_clean_global_consensus = np.array(index_clean_global_consensus)
        index_clean_consensus = np.array(index_clean_consensus)
        # convert consensus of letter to numeric
        for j in range(len(msa_consensus_clean)):
            for p in range(self.MIN_SEG):
                series.append(
                    self.value_alphabet.loc[msa_consensus_clean[j], "quantile"]
                )

        global_align = {}
        for j in range(len(self.dict_data)):
            global_align[msa.loc[j].metadata["id"]] = str(msa[j])

        for key in self.dict_data:
            array_align = np.array(list(global_align[key]))
            current_align_df = pd.DataFrame(array_align).reset_index()
            current_align_df["indices"] = np.nan
            current_align_df.loc[current_align_df[0] != "-", "indices"] = np.arange(
                0, len(current_align_df[current_align_df[0] != "-"])
            )
            current_align_df.loc[0, "indices"] = 0
            current_align_df["indices"] = current_align_df.indices.fillna(
                method="ffill"
            ).astype("int")
            index_align_0 = current_align_df["indices"].values
            ref_match = self.dict_data_original[key]

            try:
                seg_match_small = self.dict_segmentation[key]
                depth_match_global[key] = np.array(
                    ref_match.index[seg_match_small[index_align_0]]
                )
            except Exception as e:
                logger.error(e)
                continue
        # dictionnary matching the  letter in the alignment with the depth for each well
        depth_match_global_algo[method] = depth_match_global
        self.depth_match_global_algo = depth_match_global

        # clean frequency of the alignment
        res_freq = u_d.apply(pd.value_counts)
        res_freq["alphabet"] = res_freq.index.values.astype(str)
        res_freq.set_index("alphabet", inplace=True)

        # Building consensus series
        freq_df = res_freq.T
        list_value_letter = []
        for letter in self.value_alphabet.index:
            list_value_letter.append(letter + "_value")
            freq_df[letter + "_value"] = (
                freq_df[letter] * self.value_alphabet.loc[letter]["quantile"]
            )
        freq_df["freq_tot"] = freq_df[self.value_alphabet.index].sum(axis=1)
        freq_df["mean_value"] = (
            freq_df[list_value_letter].sum(axis=1) / freq_df["freq_tot"]
        )
        freq_df["consensus_ts"] = freq_df["mean_value"]
        freq_df.loc[
            freq_df["freq_tot"] <= (1 - self.CONSENSUS_per) * len(u_d), "consensus_ts"
        ] = 0

        index_global_consensus = freq_df.loc[freq_df["consensus_ts"] > 0].index.values

        consensus_series = []
        freq_consensus = []
        for j in index_global_consensus:
            for p in range(self.MIN_SEG):
                consensus_series.append(freq_df.loc[j, "consensus_ts"])
                freq_consensus.append(freq_df.loc[j, "freq_tot"] / len(u_d))
        self.index_global_consensus = index_global_consensus
        pd_consensus_series = pd.DataFrame(
            {
                self.variable_match: (np.array(consensus_series)),
                "MD": np.round(
                    np.arange(0, np.round(len(consensus_series) * 0.1, 1), 0.1), 1
                ),
                "freq": freq_consensus,
            }
        ).set_index("MD")
        self.consensus = pd_consensus_series
        seg_signal = algo_changepoints.pelt(
            pd.DataFrame(
                preprocessing.scale((pd_consensus_series[self.variable_match]))
            ),
            self.PELT_sup,
            2,
            "mll_mean",
        )[0]
        seg_signal = np.sort(seg_signal)
        seg_signal = seg_signal - 1
        tops_alg_pd = pd.DataFrame(
            {
                "MD": pd_consensus_series.index[seg_signal],
                "Formation": np.arange(len(seg_signal)),
            }
        )
        tops_alg_pd["from"] = tops_alg_pd["MD"].shift(1, fill_value=0)
        tops_alg_pd["to"] = tops_alg_pd["MD"]
        tops_alg_pd["marker"] = tops_alg_pd["Formation"].apply(lambda x: chr(x + 65))

        tops_algn_position = np.unique(
            index_global_consensus[seg_signal // self.MIN_SEG]
        ).astype(int)
        # Finding the consensus marker in the wells
        list_tops = []
        for key in self.dict_data:
            try:
                tops_current = depth_match_global_algo[method][str(key)][
                    tops_algn_position
                ]
                i_j = 1
                while (i_j < len(tops_current) - 1) & (
                    tops_current[i_j] == tops_current[0]
                ):
                    i_j += 1
                m_tot = len(tops_current) - 1
                j_i = m_tot - 1
                while (j_i > 1) & (tops_current[j_i] == tops_current[m_tot]):
                    j_i = j_i - 1
                dict_current = {
                    "MD": tops_current[(i_j - 1) : (j_i + 2)],
                    "Markers_Name": np.arange(len(tops_algn_position))[
                        (i_j - 1) : (j_i + 2)
                    ],
                    "holeid": key,
                }
                resultat_current = pd.DataFrame(dict_current)
                list_tops.append(resultat_current)
            except Exception:
                continue
        self.results_unsupervised = pd.concat(list_tops, ignore_index=True)
