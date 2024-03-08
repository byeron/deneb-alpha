import typer_cloup as typer
# for injection
from injector import Injector

from domain.interface.fluctuation import IFluctuation
from domain.interface.get_file import IGetFile
from domain.interface.multiple_correction import IMultipleCorrection
from factory.correction import CorrectionFactory
from factory.fluctuation import FluctuationFactory
from factory.get_file import GetFileFactory
# from ui.cli.wire import FluctuationMethod, WireFluctuation
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
        factory = GetFileFactory()
        injector = Injector(factory.configure)
        get_file_handler = injector.get(IGetFile)

        factory = FluctuationFactory(control, experiment, alpha)
        injector = Injector(factory.configure)
        fluctuation_handler = injector.get(IFluctuation)

        factory = CorrectionFactory(
            correction_input["method"], alpha, correction_input["multipletest"]
        )
        injector = Injector(factory.configure)
        multiple_correction_handler = injector.get(IMultipleCorrection)

        feature_data = get_file_handler.run(featuredata_input["id"])
        pvals, reject = fluctuation_handler.run(feature_data)

        if correction_input["multipletest"]:
            pvals_corrected, reject = multiple_correction_handler.run(pvals)

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
    print(f"rejected: {sum(result.loc[:, 'reject'].to_list())}")


if __name__ == "__main__":
    app()
