import React, { Component } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import "./css/documentPanel.css";

class DocumentPanel extends Component {
    handleDropInput = event => {
        event.preventDefault();
        event.stopPropagation();
        this.props.addFiles(event.dataTransfer.files);
    };

    handleDragOver = event => {
        event.preventDefault();
        event.stopPropagation();
    };

    render() {
        const { count, clearFiles, removeFile, files } = this.props;
        return (
            <div
                className="documentPanel"
                onDrop={this.handleDropInput}
                onDragOver={this.handleDragOver}
            >
                <div className="info">
                    <LabelCount count={count} />
                    <ButtonClear clearFiles={clearFiles} />
                </div>
                <hr />

                <FileList files={files} removeFile={removeFile} />
            </div>
        );
    }
}

const LabelCount = props => {
    return (
        <span
            className={
                "documentCount" + (props.count === 0 ? " colorEmpty" : "")
            }
        >
            {props.count} Documents
        </span>
    );
};

const ButtonClear = props => {
    return (
        <span className="clearButton" onClick={props.clearFiles}>
            <span> </span>
            <FontAwesomeIcon icon="minus-circle" size="sm" />
        </span>
    );
};

const FileList = props => {
    const FileTiles = props.files.map((file, index) => {
        return (
            <FileTile
                file={file}
                key={index}
                id={index}
                removeFile={props.removeFile}
            />
        );
    });

    if (FileTiles.length === 0) {
        return (
            <div className="dropIndicator">
                <FontAwesomeIcon icon="cloud-upload-alt" size="5x" />
                <p> Drop Documents Here </p>
            </div>
        );
    } else {
        return <ol className="fileList"> {FileTiles} </ol>;
    }
};

const FileTile = props => {
    const file = props.file;
    return (
        <li className="file">
            {file.name}
            <span
                className="removeFile"
                onClick={() => props.removeFile(props.id)}
            >
                <FontAwesomeIcon icon="trash" size="sm" color="#d8497d" />
            </span>
        </li>
    );
};

export default DocumentPanel;
