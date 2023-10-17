import sys

import typer_cloup as typer

from containers import FtestContainer, MultipletestContiner

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

    # Get feature file by id from database
    """
    container = GetFileContainer()
    container.config.from_dict(
        {
            "id": featurefile_input["id"],
        }
    )
    container.wire(modules=[sys.modules[__name__]])
    get_file_handler = container.get_file_handler()
    feature_data = get_file_handler.run()
    """

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
    pvalues, reject = fluctuation_handler.run() # feature_data

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
        pvalues_adj, reject = multipletest_handler.run(pvalues)

    print("pvalues: ", pvalues)
    print("reject: ", reject)


if __name__ == "__main__":
    app()
