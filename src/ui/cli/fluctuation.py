import sys

import typer_cloup as typer

from ui.cli.wire import FluctuationMethod, WireFluctuation
from usecase.output_fluctuation import OutputFluctuation

# Default parameters for correction_input
featuredata_input = {"id": None}
correction_input = {"multipletest": True, "method": "fdr_bh"}


def callback(id: str, multipletest: bool = True, method: str = "fdr_bh"):
    featuredata_input["id"] = id
    correction_input["multipletest"] = multipletest
    if multipletest:
        correction_input["method"] = method
    print(f"id: {id}")
    print(f"multipletest: {multipletest}, method: {method}")


app = typer.Typer(callback=callback)


@app.command()
def ftest(
    control: str = "control",
    experiment: str = "experiment",
    alpha: float = 0.05,
):
    print(f"control: {control}, experiment: {experiment}, alpha: {alpha}")

    pvals_corrected = None
    try:
        # Setup WireFluctuation
        wired = WireFluctuation(
            control=control,
            experiment=experiment,
            fluctuation_method=FluctuationMethod.FTEST,
            alpha=alpha,
            multipletest=correction_input["multipletest"],
            multipletest_method=correction_input["method"],
        )
        feature_data = wired.get_file_handler.run(featuredata_input["id"])
        pvals, reject = wired.fluctuation_handler.run(feature_data)

        if correction_input["multipletest"]:
            pvals_corrected, reject = wired.multipletest_handler.run(pvals)
    except Exception as e:
        print(e)
        return

    # Output
    output = OutputFluctuation(_id=featuredata_input["id"])
    result = output.run(
        features=feature_data.features,
        pvals=pvals,
        reject=reject,
        pvals_corrected=pvals_corrected,
    )
    print(result)


if __name__ == "__main__":
    app()
