import typer
from injector import Injector
from typing_extensions import Annotated

from domain.fluctuation_method import FluctuationMethod
from domain.interface.dnb_score import IDNBScore
from domain.interface.get_file import IGetFile
from factory.dnb_score import DNBScoreFactory
from factory.get_file import GetFileFactory
from usecase.output_dnb_score import OutputDNBScore

featuredata_input = {"id": None}
fluctuation_input = {"alpha": 0.05, "method": "ftest"}
correction_input = {"multiple_correction": True, "method": "fdr_bh"}
dissimilarity_input = {"method": "pearson", "metric": "abslinear"}
clustering_input = {
    "cutoff": 0.5,
    "rank": 1,
    "linkage_method": "average",
    "criterion": "distance",
}


def callback(
    id: Annotated[str, typer.Argument(...)],
    alpha: Annotated[float, typer.Option("--alpha", "-a")] = 0.05,
    threshold: Annotated[float, typer.Option("--threshold", "-t")] = 2.0,
    fluctuation_method: Annotated[
        FluctuationMethod, typer.Option("--fluctuation-method", "-f")
    ] = FluctuationMethod.ftest,
    multiple_correction: Annotated[
        bool, typer.Option("--multiple-correction", "-mc")
    ] = True,
    multiple_correction_method: Annotated[
        str, typer.Option("--multiple-correction-method", "-mm")
    ] = "fdr_bh",
    dissimilarity_method: Annotated[
        str, typer.Option("--dissimilarity-method", "-dm")
    ] = "pearson",
    dissimilarity_metric: Annotated[
        str, typer.Option("--dissimilarity-metric", "-dmt")
    ] = "abslinear",
    clustering_cutoff: Annotated[
        float, typer.Option("--clustering-cutoff", "-cc")
    ] = 0.5,
    clustering_rank: Annotated[int, typer.Option("--clustering-rank", "-cr")] = 1,
    clustering_linkege_method: Annotated[
        str, typer.Option("--clustering-linkage-method", "-clm")
    ] = "average",
    clustering_criterion: Annotated[
        str, typer.Option("--clustering-criterion", "-ccr")
    ] = "distance",
):
    featuredata_input["id"] = id
    fluctuation_input["alpha"] = alpha
    fluctuation_input["threshold"] = threshold
    fluctuation_input["method"] = fluctuation_method
    correction_input["multiple_correction"] = multiple_correction
    if multiple_correction:
        correction_input["method"] = multiple_correction_method
    dissimilarity_input["method"] = dissimilarity_method
    dissimilarity_input["metric"] = dissimilarity_metric
    clustering_input["cutoff"] = clustering_cutoff
    clustering_input["rank"] = clustering_rank
    clustering_input["linkage_method"] = clustering_linkege_method
    clustering_input["criterion"] = clustering_criterion
    print(f"id: {id}")
    print(f"multipletest: {multiple_correction}, method: {multiple_correction_method}")


app = typer.Typer(callback=callback)


@app.command()
def score(experiment: str = "experiment", control: str = None):
    # handler生成
    factory = GetFileFactory()
    injector = Injector(factory.configure)
    get_file_handler = injector.get(IGetFile)

    factory = DNBScoreFactory(
        experiment=experiment,
        fluctuation_method=fluctuation_input["method"],
        fluctuation_threshold=fluctuation_input["threshold"],
        fluctuation_alpha=fluctuation_input["alpha"],
        is_apply_multiple_correction=correction_input["multiple_correction"],
        multiple_correction_method=correction_input["method"],
        corr_method=dissimilarity_input["method"],
        dissimilarity_metric=dissimilarity_input["metric"],
        cutoff=clustering_input["cutoff"],
        rank=clustering_input["rank"],
        linkage_method=clustering_input["linkage_method"],
        criterion=clustering_input["criterion"],
        control=control,
    )
    injector = Injector(factory.configure)
    dnb_score_handler = injector.get(IDNBScore)

    feature_data = get_file_handler.run(featuredata_input["id"])
    result = dnb_score_handler.run(feature_data)

    output = OutputDNBScore(
        _id=featuredata_input["id"],
    )
    r = output.run(result)
    for n, rr in enumerate(r):
        print(f"#{n+1}")
        print(rr)


if __name__ == "__main__":
    app()
