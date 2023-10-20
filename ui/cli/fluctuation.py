import sys

import typer_cloup as typer

from ui.cli.wire import WireFluctuation

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

    # Setup WireFluctuation
    wired = WireFluctuation(
        control=control,
        experiment=experiment,
        alpha=alpha,
        multipletest=correction_input["multipletest"],
        method=correction_input["method"],

    )
    try:
        feature_data = wired.get_file_handler.run(featuredata_input["id"])
        pvals, reject = wired.fluctuation_handler.run(feature_data)

        if correction_input["multipletest"]:
            pvals_corrected, reject = wired.multipletest_handler.run(pvals)
            pvals = pvals_corrected
    except Exception as e:
        print(e)
        return

    print("p_values: ", pvals)
    print("reject: ", reject)


if __name__ == "__main__":
    app()
