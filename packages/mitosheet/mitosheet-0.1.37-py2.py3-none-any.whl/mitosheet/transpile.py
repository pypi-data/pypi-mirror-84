#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the transpile function, which takes the backend widget
container and generates transpiled Python code.
"""

from mitosheet.mito_analytics import analytics, static_user_id
from .topological_sort import topological_sort_columns
from .sheet_functions import FUNCTIONS


def transpile(widget_state_container):
    """
    Takes the Python code in the widget_state_container and linearizes it
    so it can be consumed by the front-end. 
    
    When there are multiple sheets, the first sheets code is first, followed
    by the second sheets code, etc. 
    """
    analytics.track(static_user_id, 'transpiler_started_log_event')

    code = []

    filled_step_count = 0
    
    for step_id, step in enumerate(widget_state_container.steps):

        if step['step_type'] == 'formula':
            step_code = []

            for sheet_index in range(len(step['column_evaluation_graph'])):

                topological_sort = topological_sort_columns(step['column_evaluation_graph'][sheet_index])

                # If there are columns that were created during this step that aren't defined in their 
                # original creation order, we write out the creation order
                topological_sort_of_new_columns = [column for column in topological_sort if column in step['added_columns'][sheet_index]]
                if topological_sort_of_new_columns != step['added_columns'][sheet_index]:
                    # Append a comment to explain what's going on
                    step_code.append(
                        '# Make sure the columns are defined in the correct order'
                    )
                    step_code.append(
                        '; '.join(
                            [
                                f'{widget_state_container.df_names[sheet_index]}[\'{added_column}\'] = 0'
                                for added_column in step['added_columns'][sheet_index]
                            ]
                        )
                    )

                for column in topological_sort:
                    column_formula_changes = step['column_python_code'][sheet_index][column]['column_formula_changes']
                    if column_formula_changes != '':
                        # We replace the data frame in the code with it's parameter name!
                        column_formula_changes = column_formula_changes.strip().replace('df', f'{widget_state_container.df_names[sheet_index]}')
                        step_code.append(column_formula_changes)
        elif step['step_type'] == 'merge':
            step_code = step['merge_code']

        elif step['step_type'] == 'column_rename':
            step_code = step['rename_code']
        elif step['step_type'] == 'column_delete':
            step_code = step['delete_code']
        elif step['step_type'] == 'filter':
            step_code = step['filter_code']

        if len(step_code) > 0:
            # We start each step with a comment saying which step it is.
            # NOTE: the step number displayed is _not_ the step id that is used in the backend.
            # as we only display non empty steps - so we keep things incrementing so users aren't
            # confused!
            code.append(f'# Step {filled_step_count + 1}')
            filled_step_count += 1
            
            code.extend(step_code)

    functions = ','.join(FUNCTIONS.keys())

    analytics.track(static_user_id, 'transpiler_finished_log_event')

    return {
        'imports': f'from mitosheet import {functions}',
        'code': code
    }