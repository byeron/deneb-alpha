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


def factory_handlers(control, experiment, fluctuation_input, correction_input):
    factory = GetFileFactory()
    injector = Injector(factory.configure)
    get_file_handler = injector.get(IGetFile)

    factory = FluctuationFactory(
        control,
        experiment,
        fluctuation_input["alpha"],
    )
    injector = Injector(factory.configure)
    fluctuation_handler = injector.get(IFluctuation)

    factory = CorrectionFactory(
        correction_input["method"],
        fluctuation_input["alpha"],
    )
    injector = Injector(factory.configure)
    correction_handler = injector.get(IMultipleCorrection)

    return (get_file_handler, fluctuation_handler, correction_handler)


app = typer.Typer(callback=callback)


@app.command()
def correlation(
    control: str = "control",
    experiment: str = "experiment",
    corr_method: str = "pearson",
    dissimilarity: str = "abslinear",
):
    # handler生成
    get_file_handler, fluctuation_handler, correction_handler = factory_handlers(
        control,
        experiment,
        fluctuation_input,
        correction_input,
    )
    factory = DissimilarityFactory(experiment, corr_method, dissimilarity)
    injector = Injector(factory.configure)
    dissimilarity_handler = injector.get(IDissimilarity)

    # 等分散検定
    feature_data = get_file_handler.run(featuredata_input["id"])
    pvals, reject = fluctuation_handler.run(feature_data)
    if correction_input["multipletest"]:
        pvals_corrected, reject = correction_handler.run(pvals)

    # 非類似度計算
    feature_data.fluctuation = reject
    d = dissimilarity_handler.run(feature_data)

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
    # handler 生成
    factory = ClusteringFactory(cutoff, rank, linkage_method, criterion)
    injector = Injector(factory.configure)
    clustering_handler = injector.get(IClustering)

    # クラスタリング
    d = correlation(
        control=control,
        experiment=experiment,
        corr_method=corr_method,
        dissimilarity=dissimilarity,
    )

    clusters = clustering_handler.run(d)

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
