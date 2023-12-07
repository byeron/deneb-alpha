import sys

import typer_cloup as typer

from container.clustering import ClusteringContainer
from container.dissimilarity import AbsLinearContainer
from ui.cli.wire import FluctuationMethod, WireFluctuation
from usecase.output_clustering import OutputClustering
from usecase.output_correlation import OutputCorrelation

featuredata_input = {"id": None}
fluctuation_input = {"alpha": 0.05, "method": "ftest"}
correction_input = {"multipletest": True, "method": "fdr_bh"}


def callback(
    id: str,
    alpha: float = 0.05,
    fluctuation_method: str = "ftest",
    multipletest: bool = True,
    multipletest_method: str = "fdr_bh",
):
    featuredata_input["id"] = id
    fluctuation_input["alpha"] = alpha
    fluctuation_input["method"] = fluctuation_method
    correction_input["multipletest"] = multipletest
    if multipletest:
        correction_input["method"] = multipletest_method
    print(f"id: {id}")
    print(f"multipletest: {multipletest}, method: {multipletest_method}")


app = typer.Typer(callback=callback)


@app.command()
def correlation(
    control: str = "control",
    experiment: str = "experiment",
    corr_method: str = "pearson",
    dissimilarity: str = "abslinear",
):
    fluctuation_method = None
    d = None
    try:
        match fluctuation_input["method"]:
            case "ftest":
                fluctuation_method = FluctuationMethod.FTEST
            case _:
                raise ValueError(f"Invalid method: {fluctuation_input['method']}")

        wired = WireFluctuation(
            control=control,
            experiment=experiment,
            fluctuation_method=fluctuation_method,
            alpha=fluctuation_input["alpha"],
            multipletest=correction_input["multipletest"],
            multipletest_method=correction_input["method"],
        )

        feature_data = wired.get_file_handler.run(featuredata_input["id"])
        pvals, reject = wired.fluctuation_handler.run(feature_data)
        if correction_input["multipletest"]:
            pvals_corrected, reject = wired.multipletest_handler.run(pvals)
            pvals = pvals_corrected

        try:
            match dissimilarity:
                case "abslinear":
                    feature_data.fluctuation = reject
                    container = AbsLinearContainer()
                    container.config.from_dict(
                        {
                            "experiment": experiment,
                            "corr_method": corr_method,
                            "dissimilarity": dissimilarity,
                        }
                    )
                    container.wire(modules=[sys.modules[__name__]])
                    dissimilarity_handler = container.handler()
                    d = dissimilarity_handler.run(feature_data)
                case _:
                    raise ValueError(f"Invalid dissimilarity: {dissimilarity}")
        except ValueError as e:
            print(f"Error:\t{e}")
            sys.exit(1)

    except Exception as e:
        print(e)
        return

    output = OutputCorrelation(
        _id=featuredata_input["id"],
        metric=dissimilarity,
    )
    result = output.run(d)
    print(result)
    return result


@app.command()
def clustering(
    control: str = "control",
    experiment: str = "experiment",
    corr_method: str = "pearson",
    dissimilarity: str = "abslinear",
    cutoff: float = 0.5,
    rank: int = 1,
    linkage_method: str = "average",
    criterion: str = "distance",
):
    d = correlation(
        control=control,
        experiment=experiment,
        corr_method=corr_method,
        dissimilarity=dissimilarity,
    )

    container = ClusteringContainer()
    container.config.from_dict(
        {
            "cutoff": cutoff,
            "rank": rank,
            "method": linkage_method,
            "criterion": criterion,
        }
    )
    container.wire(modules=[sys.modules[__name__]])
    clustering_handler = container.handler()

    try:
        clusters = clustering_handler.run(d)
    except ValueError as e:
        print(f"Error:\t{e}")
        sys.exit(1)

    # Output
    output = OutputClustering(
        _id=featuredata_input["id"],
        cutoff=cutoff,
        rank=rank,
    )
    output.run(clusters[1])
    print(clusters)


if __name__ == "__main__":
    app()
