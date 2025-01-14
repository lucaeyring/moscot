from types import MappingProxyType
from typing import Any, Dict, List, Tuple, Union, Mapping, Optional, Sequence

from matplotlib import colors as mcolors
from matplotlib.axes import Axes
import matplotlib as mpl

import numpy as np

from anndata import AnnData

from moscot.problems.base import CompoundProblem  # type: ignore[attr-defined]
from moscot.problems.time import LineageProblem, TemporalProblem  # type: ignore[attr-defined]
from moscot.plotting._utils import _sankey, _heatmap, _plot_temporal, _input_to_adatas, _create_col_colors
from moscot._docs._docs_plot import d_plotting
from moscot._constants._constants import AdataKeys, PlottingKeys, PlottingDefaults


@d_plotting.dedent
def cell_transition(
    inp: Union[AnnData, Tuple[AnnData, AnnData], CompoundProblem],
    uns_key: str = PlottingKeys.CELL_TRANSITION,
    row_labels: Optional[str] = None,
    col_labels: Optional[str] = None,
    annotate: Optional[str] = "{x:.2f}",
    fontsize: float = 7.0,
    cmap: Union[str, mcolors.Colormap] = "viridis",
    figsize: Optional[Tuple[float, float]] = None,
    dpi: Optional[int] = None,
    save: Optional[str] = None,
    ax: Optional[Axes] = None,
    return_fig: bool = False,
    cbar_kwargs: Mapping[str, Any] = MappingProxyType({}),
    **kwargs: Any,
) -> mpl.figure.Figure:
    """
    Plot a cell transition matrix.

    %(desc_cell_transition)s

    Parameters
    ----------
    %(input_plotting)s
    %(uns_key)s
    %(transition_labels_cell_transition)s
    %(fontsize)s
    %(cmap)s
    %(figsize_dpi_save)s
    %(cbar_kwargs_cell_transition)s

    Returns
    -------
    %(return_cell_transition)s

    Notes
    -----
    %(notes_cell_transition)s
    """
    adata1, adata2 = _input_to_adatas(inp)

    key = PlottingDefaults.CELL_TRANSITION if uns_key is None else uns_key
    try:
        _ = adata1.uns[AdataKeys.UNS][PlottingKeys.CELL_TRANSITION][key]
    except KeyError:
        raise KeyError(f"No data found in `adata.uns[{AdataKeys.UNS!r}][{PlottingKeys.CELL_TRANSITION!r}][{key!r}]`.")

    data = adata1.uns[AdataKeys.UNS][PlottingKeys.CELL_TRANSITION][key]
    fig = _heatmap(
        row_adata=adata1,
        col_adata=adata2,
        transition_matrix=data["transition_matrix"],
        row_annotation=data["source_groups"]
        if isinstance(data["source_groups"], str)
        else next(iter(data["source_groups"])),
        col_annotation=data["target_groups"]
        if isinstance(data["target_groups"], str)
        else next(iter(data["target_groups"])),
        row_annotation_label=data["source"] if row_labels is None else row_labels,
        col_annotation_label=data["target"] if col_labels is None else col_labels,
        cont_cmap=cmap,
        annotate_values=annotate,
        fontsize=fontsize,
        figsize=figsize,
        dpi=dpi,
        ax=ax,
        save=save,
        cbar_kwargs=cbar_kwargs,
        **kwargs,
    )
    if return_fig:
        return fig


@d_plotting.dedent
def sankey(
    inp: Union[AnnData, TemporalProblem, LineageProblem],
    uns_key: Optional[str] = None,
    captions: Optional[List[str]] = None,
    title: Optional[str] = None,
    colors_dict: Optional[Dict[str, float]] = None,
    alpha: float = 1.0,
    interpolate_color: bool = False,
    cmap: Union[str, mcolors.Colormap] = "viridis",
    figsize: Optional[Tuple[float, float]] = None,
    dpi: Optional[int] = None,
    save: Optional[str] = None,
    ax: Optional[Axes] = None,
    return_fig: bool = False,
    **kwargs: Any,
) -> mpl.figure.Figure:
    """
    Plot a Sankey diagram.

    {desc_sankey}

    Parameters
    ----------
    %(input_plotting)s
    %(uns_key)s
    %(captions_sankey)s
    %(title)s
    %(colors_dict_sankey)s
    %(alpha_transparency)s
    %(interpolate_color)s
    %(cmap)s
    %(figsize_dpi_save)s
    %(sankey_kwargs)s

    Returns
    -------
    %(return_sankey)s

    Notes
    -----
    %(notes_sankey)s
    """
    adata, _ = _input_to_adatas(inp)

    key = PlottingDefaults.SANKEY if uns_key is None else uns_key
    try:
        _ = adata.uns[AdataKeys.UNS][PlottingKeys.SANKEY][key]
    except KeyError:
        raise KeyError(f"No data found in `adata.uns[{AdataKeys.UNS!r}][{PlottingKeys.SANKEY!r}][{key!r}]`.")

    data = adata.uns[AdataKeys.UNS][PlottingKeys.SANKEY][key]
    fig = _sankey(
        adata=adata,
        key=data["key"],
        transition_matrices=data["transition_matrices"],
        captions=data["captions"] if captions is None else captions,
        colorDict=colors_dict,
        cont_cmap=cmap,
        title=title,
        figsize=figsize,
        dpi=dpi,
        ax=ax,
        alpha=alpha,
        interpolate_color=interpolate_color,
        **kwargs,
    )
    if save:
        fig.figure.savefig(save)
    if return_fig:
        return fig


@d_plotting.dedent
def push(
    inp: Union[AnnData, TemporalProblem, LineageProblem, CompoundProblem],
    uns_key: Optional[str] = None,
    time_points: Optional[Sequence[float]] = None,
    basis: str = "umap",
    fill_value: float = np.nan,
    scale: bool = True,
    title: Optional[Union[str, List[str]]] = None,
    suptitle: Optional[str] = None,
    cmap: Optional[Union[str, mcolors.Colormap]] = None,
    dot_scale_factor: float = 2.0,
    na_color: str = "#e8ebe9",
    figsize: Optional[Tuple[float, float]] = None,
    dpi: Optional[int] = None,
    save: Optional[str] = None,
    ax: Optional[Axes] = None,
    return_fig: bool = False,
    suptitle_fontsize: Optional[float] = None,
    **kwargs: Any,
) -> mpl.figure.Figure:
    """
    Visualise the push result in an embedding.

    %(desc_sankey)s

    Parameters
    ----------
    %(input_plotting)s
    %(uns_key)s
    %(time_points_push_pull)s
    %(basis_push_pull)s
    %(fill_value_push_pull)s
    %(scale_push_pull)s
    %(title)s
    %(cmap)s
    %(dot_scale_factor)s
    %(na_color)s
    %(figsize_dpi_save)s
    %(suptitle_fontsize)s

    Returns
    -------
    %(return_push_pull)s

    Notes
    -----
    %(return_push_pull)s
    """
    adata, _ = _input_to_adatas(inp)

    key = PlottingDefaults.PUSH if uns_key is None else uns_key
    if key not in adata.obs:
        raise KeyError(f"No data found in `adata.obs[{key!r}]`.")
    data = adata.uns[AdataKeys.UNS][PlottingKeys.PUSH][key]
    if data["data"] is not None and data["subset"] is not None and cmap is None:
        cmap = _create_col_colors(adata, data["data"], data["subset"])
    fig = _plot_temporal(
        adata=adata,
        temporal_key=data["temporal_key"],
        key_stored=key,
        source=data["source"],
        target=data["target"],
        categories=data["subset"],
        push=True,
        time_points=time_points,
        basis=basis,
        constant_fill_value=fill_value,
        scale=scale,
        save=save,
        cont_cmap=cmap,
        dot_scale_factor=dot_scale_factor,
        na_color=na_color,
        title=title,
        suptitle=suptitle,
        figsize=figsize,
        dpi=dpi,
        ax=ax,
        suptitle_fontsize=suptitle_fontsize,
        **kwargs,
    )
    if return_fig:
        return fig.figure


@d_plotting.dedent
def pull(
    inp: Union[AnnData, TemporalProblem, LineageProblem, CompoundProblem],
    uns_key: Optional[str] = None,
    time_points: Optional[Sequence[float]] = None,
    basis: str = "umap",
    fill_value: float = np.nan,
    scale: bool = True,
    title: Optional[Union[str, List[str]]] = None,
    suptitle: Optional[str] = None,
    cmap: Optional[Union[str, mcolors.Colormap]] = None,
    dot_scale_factor: float = 2.0,
    na_color: str = "#e8ebe9",
    figsize: Optional[Tuple[float, float]] = None,
    dpi: Optional[int] = None,
    save: Optional[str] = None,
    ax: Optional[Axes] = None,
    return_fig: bool = False,
    suptitle_fontsize: Optional[float] = None,
    **kwargs: Any,
) -> mpl.figure.Figure:
    """
    Visualise the pull result in an embedding.

    %(desc_sankey)s

    Parameters
    ----------
    %(input_plotting)s
    %(uns_key)s
    %(time_points_push_pull)s
    %(basis_push_pull)s
    %(fill_value_push_pull)s
    %(scale_push_pull)s
    %(title)s
    %(cmap)s
    %(dot_scale_factor)s
    %(na_color)s
    %(figsize_dpi_save)s
    %(suptitle_fontsize)s

    Returns
    -------
    %(return_push_pull)s

    Notes
    -----
    %(return_push_pull)s
    """
    adata, _ = _input_to_adatas(inp)

    key = PlottingDefaults.PULL if uns_key is None else uns_key
    if key not in adata.obs:
        raise KeyError(f"No data found in `adata.obs[{key!r}]`.")
    data = adata.uns[AdataKeys.UNS][PlottingKeys.PULL][key]
    if data["data"] is not None and data["subset"] is not None and cmap is None:
        cmap = _create_col_colors(adata, data["data"], data["subset"])
    fig = _plot_temporal(
        adata=adata,
        temporal_key=data["temporal_key"],
        key_stored=key,
        source=data["source"],
        target=data["target"],
        categories=data["subset"],
        push=False,
        time_points=time_points,
        basis=basis,
        constant_fill_value=fill_value,
        scale=scale,
        save=save,
        cont_cmap=cmap,
        dot_scale_factor=dot_scale_factor,
        na_color=na_color,
        title=title,
        suptitle=suptitle,
        figsize=figsize,
        dpi=dpi,
        ax=ax,
        suptitle_fontsize=suptitle_fontsize,
        **kwargs,
    )
    if return_fig:
        return fig.figure
