from msbuddy import assign_subformula


def filter_by_ms2_explanation(row, explanation_cutoff=0.60):
    """
    Calculate the MS2 explanation
    """
    if row['selected'] and row['MS2'] is not None:

        if len(row['MS2']) == 0 or row['MS2'].shape[0] == 0:
            row['ms2_explained_intensity'] = 0.0
            return row

        if row['MS2'][:, 1].sum() < 1e-2:
            row['ms2_explained_intensity'] = 0.0
            return row

        try:
            explained_intensity = 0.0
            subformla_list = assign_subformula(row['MS2'][:, 0],
                                               precursor_formula=row['neutralized_formula'],
                                               adduct=row['t_adduct'],
                                               ms2_tol=0.02, ppm=False)
        except:
            row['ms2_explained_intensity'] = 1.0
            return row

        if subformla_list is None:  # formula elements outside common elements
            row['ms2_explained_intensity'] = 1.0
            return row

        for subformula in subformla_list:
            explained_intensity += row['MS2'][:, 1][subformula.idx] if subformula.subform_list else 0.0
        row['ms2_explained_intensity'] = explained_intensity / row['MS2'][:, 1].sum()

        if row['ms2_explained_intensity'] < explanation_cutoff:
            row['selected'] = False
            row['discard_reason'] = 'MS2 explanation below cutoff'

    return row
