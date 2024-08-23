from enum import Enum


class FluctuationMethod(str, Enum):
    ftest = "ftest"
    mad_ftest = "mad-ftest"
    std_ratio = "std-ratio"
    mad_ratio = "mad-ratio"
    levene = "levene"
    std_inner_var = "std-inner-var"
    mad_inner_var = "mad-inner-var"
