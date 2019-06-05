import React, { Component } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "./css/buttonGroup.css";

class ButtonGroup extends Component {
    handleInput = event => {
        this.props.addFiles(event.target.files);
        event.target.value = "";
    };

    render() {
        return (
            <div className="button-group">
                <ButtonAdd handleInput={this.handleInput} />
                <ButtonConvert
                    progState={this.props.progState}
                    convert={this.props.convert}
                />
            </div>
        );
    }
}

const ButtonAdd = props => {
    return (
        <div>
            <input
                type="file"
                className="inputFile"
                name="file[]"
                id="file"
                onChange={props.handleInput}
                multiple
            />
            <label htmlFor="file" className="button button-accent">
                Add Documents <FontAwesomeIcon icon="plus-circle" size="sm" />
            </label>
        </div>
    );
};

const ButtonConvert = props => {
    let buttonIcon, buttonText;
    if (props.progState === "default") {
        buttonText = "Convert ";
        buttonIcon = <FontAwesomeIcon icon="sync" size="sm" />;
    } else {
        buttonText = "Converting ";
        buttonIcon = <FontAwesomeIcon icon="sync" size="sm" spin />;
    }

    return (
        <button
            className="button button-primary align-right"
            onClick={() => props.convert()}
        >
            {buttonText}
            {buttonIcon}
        </button>
    );
};

export default ButtonGroup;
