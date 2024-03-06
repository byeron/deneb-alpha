import typer_cloup as typer
from injector import Injector

from domain.interface.clustering import IClustering
from domain.interface.dissimilarity import IDissimilarity
from domain.interface.fluctuation import IFluctuation
from domain.interface.get_file import IGetFile
from domain.interface.multiple_correction import IMultipleCorrection
from factory.clustering import ClusteringFactory
from factory.correction import CorrectionFactory
from factory.dissimilarity import DissimilarityFactory
from factory.fluctuation import FluctuationFactory
from factory.get_file import GetFileFactory
from usecase.output_clustering import OutputClustering
from usecase.output_correlation import OutputCorrelation
from factory.dnb_score import DNBScoreFactory
from domain.interface.dnb_score import IDNBScore

featuredata_input = {"id": None}
fluctuation_input = {"alpha": 0.05, "method": "ftest"}
correction_input = {"multipletest": True, "method": "fdr_bh"}
dissimilarity_input = {"method": "pearson", "metric": "abslinear"}
clustering_input = {"cutoff": 0.5, "rank": 1,
                    "linkage_method": "average", "criterion": "distance"}


def callback(
    id: str,
    alpha: float = 0.05,
    fluctuation_method: str = "ftest",
    multipletest: bool = True,
    multipletest_method: str = "fdr_bh",
    dissimilarity_method: str = "pearson",
    dissimilarity_metric: str = "abslinear",
    clustering_cutoff: float = 0.5,
    clustering_rank: int = 1,
    clustering_linkege_method: str = "average",
    clustering_criterion: str = "distance",
):
    featuredata_input["id"] = id
    fluctuation_input["alpha"] = alpha
    fluctuation_input["method"] = fluctuation_method
    correction_input["multipletest"] = multipletest
    if multipletest:
        correction_input["method"] = multipletest_method
    dissimilarity_input["method"] = dissimilarity_method
    dissimilarity_input["metric"] = dissimilarity_metric
    clustering_input["cutoff"] = clustering_cutoff
    clustering_input["rank"] = clustering_rank
    clustering_input["linkage_method"] = clustering_linkege_method
    clustering_input["criterion"] = clustering_criterion
    print(f"id: {id}")
    print(f"multipletest: {multipletest}, method: {multipletest_method}")


app = typer.Typer(callback=callback)


@app.command()
def score(
        control: str = "control",
        experiment: str = "experiment"
):
    # handler生成
    factory = GetFileFactory()
    injector = Injector(factory.configure)
    get_file_handler = injector.get(IGetFile)

    factory = DNBScoreFactory(
        control=control,
        experiment=experiment,
        alpha=fluctuation_input["alpha"],
        multiple_correction_method=correction_input["method"],
        corr_method=dissimilarity_input["method"],
        dissimilarity_metric=dissimilarity_input["metric"],
        cutoff=clustering_input["cutoff"],
        rank=clustering_input["rank"],
        linkage_method=clustering_input["linkage_method"],
        criterion=clustering_input["criterion"],
    )
    injector = Injector(factory.configure)
    dnb_score_handler = injector.get(IDNBScore)

    feature_data = get_file_handler.run(featuredata_input["id"])
    result = dnb_score_handler.run(feature_data)
    print(result)


if __name__ == "__main__":
    app()
