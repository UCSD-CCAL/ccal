from pandas import concat

from ._single_sample_gseas import _single_sample_gseas
from .multiprocess import multiprocess
from .split_df import split_df


def single_sample_gseas(
    gene_x_sample, gene_sets, statistic="ks", n_job=1, file_path=None
):

    score__gene_set_x_sample = concat(
        multiprocess(
            _single_sample_gseas,
            (
                (gene_x_sample, gene_sets_, statistic)
                for gene_sets_ in split_df(gene_sets, 0, min(gene_sets.shape[0], n_job))
            ),
            n_job,
        )
    )

    if file_path is not None:

        score__gene_set_x_sample.to_csv(file_path, sep="\t")

    return score__gene_set_x_sample
