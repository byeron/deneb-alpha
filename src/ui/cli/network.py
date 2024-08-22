from typing_extensions import Annotated
import typer
from injector import Injector

from domain.dissimilarity_metric import DissimilarityMetric
from domain.fluctuation_method import FluctuationMethod
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
from usecase.output_heatmap import OutputHeatmap

featuredata_input = {"id": None}
fluctuation_input = {"alpha": 0.05, "method": "ftest", "threshold": 2.0}
correction_input = {"multiple_correction": True, "method": "fdr_bh"}


def callback(
    id: Annotated[str, typer.Argument(...)],
    alpha: Annotated[float, typer.Option("--alpha", "-a", help="Significance level")] = 0.05,
    fluctuation_method: Annotated[FluctuationMethod, typer.Option("--fluctuation-method", "-fm", help="Fluctuation method")] = FluctuationMethod.ftest,
    fluctuation_threshold: Annotated[float, typer.Option("--fluctuation-threshold", "-ft", help="Fluctuation threshold")] = 2.0,
    multiple_correction: Annotated[bool, typer.Option()] = True,
    multiple_correction_method: Annotated[str, typer.Option("--multiple-correction-method", "-mm", help="Multiple correction method")] = "fdr_bh",
):
    featuredata_input["id"] = id
    fluctuation_input["alpha"] = alpha
    fluctuation_input["threshold"] = fluctuation_threshold
    fluctuation_input["method"] = fluctuation_method
    correction_input["multiple_correction"] = multiple_correction
    if multiple_correction:
        correction_input["method"] = multiple_correction_method
    print(f"id: {id}")


def factory_handlers(experiment, fluctuation_input, correction_input, control=None):
    factory = GetFileFactory()
    injector = Injector(factory.configure)
    get_file_handler = injector.get(IGetFile)

    factory = FluctuationFactory(
        control=control,
        experiment=experiment,
        method=fluctuation_input["method"],
        alpha=fluctuation_input["alpha"],
        threshold=fluctuation_input["threshold"],
    )
    injector = Injector(factory.configure)
    fluctuation_handler = injector.get(IFluctuation)

    factory = CorrectionFactory(
        correction_input["method"],
        fluctuation_input["alpha"],
        correction_input["multiple_correction"],
    )
    injector = Injector(factory.configure)
    correction_handler = injector.get(IMultipleCorrection)

    return (get_file_handler, fluctuation_handler, correction_handler)


app = typer.Typer(callback=callback)


@app.command()
def correlation(
    expr: Annotated[str, typer.Option("--expr", "-e", help="experimental group")] = "experiment",
    corr_method: Annotated[str, typer.Option("--corr-method", "-cm", help="correlation method")] = "pearson",
    dissimilarity: Annotated[DissimilarityMetric, typer.Option("--dissimilarity", "-d", help="dissimilarity method")] = DissimilarityMetric.abslinear,
    ctrl: Annotated[str, typer.Option("--ctrl", "-c", help="control group")] = None,
):
    # handler生成
    get_file_handler, fluctuation_handler, correction_handler = factory_handlers(
        expr,
        fluctuation_input,
        correction_input,
        control=ctrl,
    )
    factory = DissimilarityFactory(expr, corr_method, dissimilarity)
    injector = Injector(factory.configure)
    dissimilarity_handler = injector.get(IDissimilarity)

    # 等分散検定
    print(f"fluctuation method: {fluctuation_input['method']}")
    feature_data = get_file_handler.run(featuredata_input["id"])
    pvals, reject = fluctuation_handler.run(feature_data)

    if fluctuation_handler.can_correction():
        print(f"alpha: {fluctuation_input['alpha']}")
    else:
        print(f"threshold: {fluctuation_input['threshold']}")
        print("multipletest method: No")

    if correction_input["multiple_correction"] and fluctuation_handler.can_correction():
        print(f"multipletest method: {correction_input['method']}")
        _, reject = correction_handler.run(pvals)

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
    expr: Annotated[str, typer.Option("--expr", "-e", help="experimental group")] = "experiment",
    corr_method: Annotated[str, typer.Option("--corr-method", "-cm", help="correlation method")] = "pearson",
    dissimilarity: Annotated[DissimilarityMetric, typer.Option("--dissimilarity", "-d", help="dissimilarity method")] = DissimilarityMetric.abslinear,
    cutoff: Annotated[float, typer.Option("--cutoff", "-co", help="cutoff value")] = 0.5,
    rank: Annotated[int, typer.Option("--rank", "-r", help="rank value")] = 1,
    linkage_method: Annotated[str, typer.Option("--linkage-method", "-lm", help="linkage method")] = "average",
    criterion: Annotated[str, typer.Option("--criterion", "-cr", help="criterion method")] = "distance",
    ctrl: Annotated[str, typer.Option("--ctrl", "-c", help="control group")] = None,
):
    # handler 生成
    factory = ClusteringFactory(cutoff, rank, linkage_method, criterion)
    injector = Injector(factory.configure)
    clustering_handler = injector.get(IClustering)

    # クラスタリング
    d = correlation(
        ctrl=ctrl,
        expr=expr,
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

    factory = GetFileFactory()
    injector = Injector(factory.configure)
    get_file_handler = injector.get(IGetFile)
    feature_data = get_file_handler.run(featuredata_input["id"])
    output = OutputHeatmap(_id=featuredata_input["id"])
    output.run(
        feature_data,
        clusters[1],
    )


if __name__ == "__main__":
    app()
