import typer_cloup as typer

# for injection
from injector import Injector

from domain.interface.fluctuation import IFluctuation
from domain.interface.get_file import IGetFile
from domain.interface.multiple_correction import IMultipleCorrection
from factory.correction import CorrectionFactory
from factory.fluctuation import FluctuationFactory
from factory.get_file import GetFileFactory
from usecase.output_fluctuated_features import OutputFluctuatedFeatures
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
def madftest(
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

        method = "mad-ftest"
        factory = FluctuationFactory(
            control=control,
            experiment=experiment,
            method=method,
            alpha=alpha,
        )
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
    output = OutputFluctuation(_id=featuredata_input["id"], method=method)
    result = output.run(
        features=feature_data.features,
        pvals=pvals,
        reject=reject,
        pvals_corrected=pvals_corrected,
    )
    print(result)
    print(f"rejected: {sum(result.loc[:, 'reject'].to_list())}")

    output = OutputFluctuatedFeatures(_id=featuredata_input["id"])
    _ = output.run(feature_data, reject)


@app.command()
def levene(
    control: str = "control",
    experiment: str = "experiment",
    alpha: float = 0.05,
):
    pvals_corrected = None
    print(f"control: {control}, experiment: {experiment}, alpha: {alpha}")

    try:
        factory = GetFileFactory()
        injector = Injector(factory.configure)
        get_file_handler = injector.get(IGetFile)

        method = "levene"
        factory = FluctuationFactory(
            control=control,
            experiment=experiment,
            method=method,
            alpha=alpha,
        )
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
    output = OutputFluctuation(_id=featuredata_input["id"], method=method)
    result = output.run(
        features=feature_data.features,
        pvals=pvals,
        reject=reject,
        pvals_corrected=pvals_corrected,
    )
    print(result)
    print(f"rejected: {sum(result.loc[:, 'reject'].to_list())}")

    output = OutputFluctuatedFeatures(_id=featuredata_input["id"])
    _ = output.run(feature_data, reject)


@app.command()
def madratio(
    control: str = "control",
    experiment: str = "experiment",
    mad_threshold: float = 2.0,
):
    print(
        f"control: {control}, experiment: {experiment}, MAD threshold: {mad_threshold}"
    )

    pvals_corrected = None

    try:
        factory = GetFileFactory()
        injector = Injector(factory.configure)
        get_file_handler = injector.get(IGetFile)

        method = "mad-ratio"
        factory = FluctuationFactory(
            control=control,
            experiment=experiment,
            method=method,
            mad_threshold=mad_threshold,
        )
        injector = Injector(factory.configure)
        fluctuation_handler = injector.get(IFluctuation)

        feature_data = get_file_handler.run(featuredata_input["id"])
        pvals, reject = fluctuation_handler.run(feature_data)

    except Exception as e:
        print(e)
        return

    # Output
    output = OutputFluctuation(_id=featuredata_input["id"], method=method)
    result = output.run(
        features=feature_data.features,
        pvals=pvals,
        reject=reject,
        pvals_corrected=pvals_corrected,
    )
    print(result)
    print(f"rejected: {sum(result.loc[:, 'reject'].to_list())}")

    output = OutputFluctuatedFeatures(_id=featuredata_input["id"])
    _ = output.run(feature_data, reject)


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

        method = "ftest"
        factory = FluctuationFactory(
            control=control,
            experiment=experiment,
            method=method,
            alpha=alpha,
        )
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

    output = OutputFluctuatedFeatures(_id=featuredata_input["id"])
    _ = output.run(feature_data, reject)


if __name__ == "__main__":
    app()
