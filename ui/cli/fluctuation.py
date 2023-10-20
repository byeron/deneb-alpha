import sys

import typer_cloup as typer

from container.fluctuation import FtestContainer, MultipletestContiner
from container.get_file import GetFileContainer

# Default parameters for correction_input
featurefile_input = {"id": None}
correction_input = {"multipletest": True, "method": "fdr_bh"}


def callback(id: str, multipletest: bool = True, method: str = "fdr_bh"):
    featurefile_input["id"] = id
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

    container = GetFileContainer()
    container.config.from_yaml("config.yml")
    container.wire(modules=[sys.modules[__name__]])
    get_file_handler = container.handler()
    try:
        feature_data = get_file_handler.run(featurefile_input["id"])
    except Exception as e:
        print(e)
        return
    print(f"{feature_data.file_name}: {feature_data.created_at}")

    # Setup FtestHandler
    container = FtestContainer()
    container.config.from_dict(
        {
            "control": control,
            "experiment": experiment,
            "alpha": alpha,
        }
    )
    container.wire(modules=[sys.modules[__name__]])
    fluctuation_handler = container.fluctuation_handler()
    pvals, reject = fluctuation_handler.run(feature_data)
    print(pvals)
    print(reject)

    # Setup MultipletestHandler
    if correction_input["multipletest"]:
        print(f"method: {correction_input['method']}, alpha: {alpha}")
        container = MultipletestContiner()
        container.config.from_dict(
            {
                "method": correction_input["method"],  # "fdr_bh"
                "alpha": alpha,
            }
        )
        container.wire(modules=[sys.modules[__name__]])
        multipletest_handler = container.multipletest_handler()
        pvals_corrected, reject = multipletest_handler.run(pvals)

    print("p_values: ", pvals_corrected)
    print("reject: ", reject)


if __name__ == "__main__":
    app()
