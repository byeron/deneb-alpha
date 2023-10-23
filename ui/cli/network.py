import sys

import typer_cloup as typer

from container.dissimilarity import AbsLinearContainer
from ui.cli.wire import FluctuationMethod, WireFluctuation

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

        if dissimilarity == "abslinear":
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
            print(d)

    except Exception as e:
        print(e)
        return
    pass


if __name__ == "__main__":
    app()
