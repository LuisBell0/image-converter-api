from PIL import ImageFilter
from PIL.Image import Resampling

RESAMPLING_FILTERS: dict = {
    'NEAREST': Resampling.NEAREST,
    'BOX': Resampling.BOX,
    'BILINEAR': Resampling.BILINEAR,
    'HAMMING': Resampling.HAMMING,
    'BICUBIC': Resampling.BICUBIC,
    'LANCZOS': Resampling.LANCZOS,
}

BASIC_FILTERS: dict = {
    'BLUR': ImageFilter.BLUR,
    'CONTOUR': ImageFilter.CONTOUR,
    'DETAIL': ImageFilter.DETAIL,
    'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
    'EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
    'EMBOSS': ImageFilter.EMBOSS,
    'FIND_EDGES': ImageFilter.FIND_EDGES,
    'SHARPEN': ImageFilter.SHARPEN,
    'SMOOTH': ImageFilter.SMOOTH,
    'SMOOTH_MORE': ImageFilter.SMOOTH_MORE,
}

RANK_FILTERS: dict = {
    'MIN': ImageFilter.MinFilter,
    'MEDIAN': ImageFilter.MedianFilter,
    'MAX': ImageFilter.MaxFilter,
}

MULTIBAND_FILTERS: dict = {
    'UNSHARPMASK': ImageFilter.UnsharpMask,
    'GAUSSIANBLUR': ImageFilter.GaussianBlur,
    'BOXBLUR': ImageFilter.BoxBlur,
}
