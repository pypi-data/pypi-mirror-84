// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';
import { ModalEnum, ModalInfo } from '../Mito';
import DefaultModal from '../DefaultModal';

// import css
import "../../../css/margins.css";
import "../../../css/filter_modal.css"

export enum FilterCondition {
    NONE = 'none',
    NUMBER_EXACTLY = 'number_exactly',
    GREATER = 'greater',
    GREATER_THAN_OR_EQUAL = 'greater_than_or_equal',
    LESS = 'less',
    LESS_THAN_OR_EQUAL = 'less_than_or_equal',
    EMPTY = 'empty',
    NOT_EMPTY = 'not_empty',
    CONTAINS = 'contains',
    STRING_EXACTLY = 'string_exactly'
}


enum FilterTypeIdentifier {
    STRING = 'string',
    NUMBER = 'number'
}

export interface StringFilterCondition {
    type: FilterTypeIdentifier.STRING;
    condition: FilterCondition;
    value: string;
}

export interface NumberFilterCondition {
    type: FilterTypeIdentifier.NUMBER;
    condition: FilterCondition;
    value: number;
}

export type FilterColumnStateType = 
    | StringFilterCondition 
    | NumberFilterCondition

interface FilterModalState {
    filterColumnState: FilterColumnStateType;
    valueInput: string;
}

type FilterModalProps = {
    columnHeader: string,
    selectedSheetIndex: number,
    columnFilterInfo: FilterColumnStateType,
    setModal: (modalInfo: ModalInfo) => void,
    send: (msg: Record<string, unknown>) => void,
}

// if one of these filters are selected, don't display the value input
const noInputFilters = [FilterCondition.NONE, FilterCondition.EMPTY, FilterCondition.NOT_EMPTY]

function getFilterCondition(condition: string) : FilterCondition {
    if (condition === 'none') {
        return FilterCondition.NONE
    } else if (condition === 'number_exactly') {
        return FilterCondition.NUMBER_EXACTLY
    } else if (condition === 'greater') {
        return FilterCondition.GREATER
    } else if (condition === 'greater_than_or_equal') {
        return FilterCondition.GREATER_THAN_OR_EQUAL
    } else if (condition === 'less') {
        return FilterCondition.LESS
    } else if (condition === 'less_than_or_equal') {
        return FilterCondition.LESS_THAN_OR_EQUAL
    } else if (condition === 'empty') {
        return FilterCondition.EMPTY
    } else if (condition === 'not_empty') {
        return FilterCondition.NOT_EMPTY
    } else if (condition === 'contains') {
        return FilterCondition.CONTAINS
    } else if (condition === 'string_exactly') {
        return FilterCondition.STRING_EXACTLY
    } else {
        return FilterCondition.NONE
    } 
}

/*
    A modal that allows a user to filter a column
*/
class FilterModal extends React.Component<FilterModalProps, FilterModalState> {

    constructor(props: FilterModalProps) {
        super(props);

        this.state = {
            filterColumnState: props.columnFilterInfo,
            valueInput: props.columnFilterInfo.value ? props.columnFilterInfo.value?.toString() : '' // value displayed in the input field, separated out to avoid unnecessary type casting
        }

        if (props.columnFilterInfo.value === '' && props.columnFilterInfo.type === FilterTypeIdentifier.NUMBER) {
            this.state.filterColumnState.value = 0
        }

        this.filterColumn = this.filterColumn.bind(this);
        this.setFilterModalState = this.setFilterModalState.bind(this);
        this.handleConditionChange = this.handleConditionChange.bind(this);
        this.handleValueChange = this.handleValueChange.bind(this);
    }

    filterColumn = () : void => {

        window.logger?.track({
            userId: window.user_id,
            event: 'button_filter_log_event',
            properties: {
                'sheet_index': this.props.selectedSheetIndex,
                'column': this.props.columnHeader,
                'condition': this.state.filterColumnState.condition,
                'value': this.state.filterColumnState.value,
            }
        })

        this.props.send({
            'event': 'edit_event',
            'type': 'filter',
            'sheet_index': this.props.selectedSheetIndex,
            'column': this.props.columnHeader,
            'condition': this.state.filterColumnState.condition,
            'value': this.state.filterColumnState.value,
            'id': '123',
            'timestamp': '456'
        })

        this.props.setModal({type: ModalEnum.None});
    }

    setFilterModalState = (condition : FilterCondition, value: string | number) : void => {
        /*
            We'd prefer to check this.state.filterColumnState.type, and case on that, but the compiler
            isn't smart enough to figure out the types - so we case on the type of the value instead.
        */
        if (typeof this.state.filterColumnState.value === 'string') {
            // We cast the value to a string, as we're working with strings
            const stringValue = String(value)

            const updatedFilterState = {
                type: FilterTypeIdentifier.STRING,
                condition: condition,
                value: stringValue 
            } as StringFilterCondition;
            this.setState({filterColumnState: updatedFilterState})
        } else {
            // Otherwise, we're working a number
            // TODO: cast to make this a number
            const numberValue = Number(value);
            const updatedFilterState = {
                type: FilterTypeIdentifier.NUMBER,
                condition: condition,
                value: numberValue 
            } as NumberFilterCondition;

            this.setState({filterColumnState: updatedFilterState})
        }
    }

    handleConditionChange(e : React.ChangeEvent<HTMLSelectElement>) : void {
        const filterCondition = getFilterCondition(e.target.value);
        this.setFilterModalState(filterCondition, this.state.filterColumnState.value);
    }

    handleValueChange(e : React.ChangeEvent<HTMLInputElement>) : void {
        this.setState({
            valueInput: e.target.value
        });
        this.setFilterModalState(this.state.filterColumnState.condition, e.target.value)
    }

    render() : JSX.Element {

        // only display the value input when the condition requires a value
        const displayValueInput = !noInputFilters.includes(this.state.filterColumnState.condition)
    
        return (
            <DefaultModal
                header={`Filter ${this.props.columnHeader}`}
                modalType={ModalEnum.Filter}
                viewComponent= {
                    <Fragment>
                        <div className="filter-modal-container">
                            <div className="mt-1 filter-modal-center">
                                <div className="filter-modal-p-div">
                                    <p> Filter Condition </p>
                                </div>
                                <select className="filter-modal-input" value={this.state.filterColumnState.condition} onChange={this.handleConditionChange} >
                                    <option value={FilterCondition.NONE}>None</option>
                                    {this.state.filterColumnState.type === FilterTypeIdentifier.NUMBER && 
                                    <>
                                        <option value={FilterCondition.NUMBER_EXACTLY}>=</option>
                                        <option value={FilterCondition.GREATER}>&gt;</option>
                                        <option value={FilterCondition.GREATER_THAN_OR_EQUAL}>&ge;</option>
                                        <option value={FilterCondition.LESS}>&lt;</option>
                                        <option value={FilterCondition.LESS_THAN_OR_EQUAL}>&le;</option>
                                    </>
                                    }
                                    {this.state.filterColumnState.type === FilterTypeIdentifier.STRING && 
                                    <>
                                        <option value={FilterCondition.CONTAINS}>contains</option>
                                        <option value={FilterCondition.STRING_EXACTLY}>is exactly</option>
                                    </>
                                    }
                                    <option value={FilterCondition.EMPTY}>is empty</option>
                                    <option value={FilterCondition.NOT_EMPTY}>is not empty</option>
                                </select>
                            </div>

                            {displayValueInput && 
                                <div className="mt-2">
                                    <div className="filter-modal-p-div">
                                        <p> Filter Value </p>
                                    </div>
                                    <input className="filter-modal-input" value={this.state.valueInput} onChange={this.handleValueChange}/>
                                </div>
                            }
                        </div>
                    </Fragment>
                }
                buttons = {
                    <Fragment>
                        <div className='modal-close-button modal-dual-button-left' onClick={() => {this.props.setModal({type: ModalEnum.None})}}> Close </div>
                        <div className='modal-action-button modal-dual-button-right' onClick={this.filterColumn}> {"Filter"}</div>
                    </Fragment>
                }
            />
        );
    }
}

export default FilterModal;