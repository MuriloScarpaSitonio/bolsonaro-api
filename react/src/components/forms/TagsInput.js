import React, { Component, createRef } from "react";

import "./TagsInput.scss"


export default class TagsInput extends Component {
    constructor(props) {
        super(props)
        this.ref = createRef()
        let initialValues = this.props.initialValues || []
        this.whitelist = this.props.whitelist || []
        let initialDropdown = [...this.whitelist]
        if ((Array.isArray(initialValues)) && (initialValues.length > 0)) {
            for (var i = 0; i < initialValues.length; i++) {
                let index = initialDropdown.indexOf(initialValues[i])
                initialDropdown.splice(index, 1)
            }
        }
        this.state = {
            tags: [...initialValues],
            dropdown: initialDropdown,
            searchDropdown: "",
            showDropdown: false
        }
    }

    componentDidMount() {
        document.addEventListener('mousedown', this.handleClickOutside);
    }

    componentWillUnmount() {
        document.removeEventListener('mousedown', this.handleClickOutside);
    }

    handleClickOutside = (e) => {
        if (this.ref.current && !this.ref.current.contains(e.target)) {
            this.setState({ showDropdown: false })
        }
    }

    removeTag = i => e => {
        const newTags = [...this.state.tags];
        const removed_tag = newTags.splice(i, 1)[0]
        this.setState({ tags: newTags })
        this.props.form.setFieldValue("tags", newTags)
        this.setState({ dropdown: [...this.state.dropdown, removed_tag] })
    }

    checkIfAlreadyTagged = (val) => {
        return this.state.tags.find(tag => tag.toLowerCase() === val.toLowerCase())
    }

    inputKeyDown = (e) => {
        let val = e.target.value;
        if (e.key === "Enter") {
            e.preventDefault()
            if (val && this.whitelist.includes(val)) {
                if (this.checkIfAlreadyTagged(val)) {
                    return
                }
                this.addTag(val, this.state.dropdown.indexOf(val))
                this.tagInput.value = null
            }
        }
        return false
    }


    addTag = (tag, i) => {
        const newTags = [...this.state.tags, tag]
        this.setState({ tags: newTags })
        this.props.form.setFieldValue("tags", newTags)
        let newDropdown = [...this.state.dropdown]
        newDropdown.splice(i, 1)
        this.setState({ dropdown: newDropdown, searchDropdown: "", showDropdown: false })
        this.tagInput.value = null
    }

    getDropdownItems = () => {
        let items = []
        for (var i = 0; i < this.state.dropdown.length; i++) {
            let item = this.state.dropdown[i]
            if (this.state.searchDropdown) {
                if (item.toLowerCase().startsWith(this.state.searchDropdown.toLowerCase())) {
                    items.push(item)
                }
            }
            else {
                items.push(item)
            }
        }
        return items
    }

    getClassName = () => {
        if (this.props.noValidate) return 
        if (this.props.form.touched.tags) {
            if (this.props.form.errors.tags) {
                return "error__box"
            }
            return "valid__box"
        }
    }

    render() {
        return (
            <div ref={this.ref}>
                <div className={`input-tags ${this.getClassName()}`}
                >
                    {this.state.tags.map((tag, i) => (
                        <div className="input-tags__tag my-1" key={tag}>
                            <span id={tag}>{tag}</span>
                            <button type="button"
                                onClick={this.removeTag(i)}
                            //onMouseEnter={() => document.getElementById(`${tag}-wrapper`).classList.add("d")}
                            //onMouseLeave={() => document.getElementById(`${tag}-wrapper`).classList.remove("d")}
                            >x</button>
                        </div>
                    ))}
                    <div className="input-tags__input">
                        <input
                            className="form-control"
                            name="tags"
                            placeholder={this.props.placeholder}
                            onFocus={() => this.setState({ showDropdown: true })}
                            onBlur={this.props.form.handleBlur("tags")}
                            onKeyDown={this.inputKeyDown}
                            onChange={e => this.setState({ searchDropdown: e.target.value })}
                            ref={c => { this.tagInput = c }}
                        />
                    </div>
                </div>
                <div className={`input-tags__dropdown__wrapper ${!this.state.showDropdown ? "hide" : ""}`}>
                    <div className="d-flex flex-wrap justify-content-center">
                        {this.getDropdownItems().map((item, i) => (
                            <div
                                className="tag text-center"
                                onClick={() => this.addTag(item, i)}
                                key={item}
                            >
                                {item}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }
}

/*
<div className="d-flex justify-content-end">
    <button type="button" onClick={() => this.setState({ showDropdown: false })}>x</button>
</div>
*/