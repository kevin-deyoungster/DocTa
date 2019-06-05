import React, { Component } from "react";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
    faSync,
    faTrash,
    faPlusCircle,
    faMinusCircle,
    faCloudUploadAlt
} from "@fortawesome/free-solid-svg-icons";
import axios from "axios";
import Header from "./Header";
import ButtonGroup from "./ButtonGroup";
import DocumentPanel from "./DocumentPanel";

import UTILS from "./utils";
import { CONFIG } from "./config";

library.add(faSync, faTrash, faPlusCircle, faMinusCircle, faCloudUploadAlt);

class App extends Component {
    componentDidMount = () => (document.title = CONFIG.title);
    state = {
        ...{
            files: [],
            fileNames: [],
            progState: "default",
            sizeLimitMB: 6,
            filterREGEX: /.docx/
        },
        ...CONFIG
    };

    addFiles = fileList => {
        fileList = Array.from(fileList);
        const files = this.filterFiles(fileList);
        if (files) {
            console.log(files);
            let newFileList = [...this.state.files, ...files];
            this.setState({
                files: newFileList,
                fileNames: this.getFileNames(newFileList)
            });
        }
    };

    filterFiles = files => {
        return files.filter(file => {
            return (
                UTILS.isWithinSizeLimits(file, this.state.sizeLimitMB) &
                this.state.filterREGEX.test(file.name) &
                !this.state.fileNames.includes(file.name)
            );
        });
    };

    getFileNames = files => files.map(file => file.name);

    removeFile = fileIndex => {
        const { files } = this.state;
        let newFileList = files.filter((file, i) => {
            return i !== fileIndex;
        });
        this.setState({
            files: newFileList,
            fileNames: this.getFileNames(newFileList)
        });
    };

    clearFiles = () => {
        this.setState({ files: [], fileNames: [] });
    };

    convert = async () => {
        this.setState({ progState: "progress" });
        let formData = new FormData();
        this.state.files.forEach(file => {
            formData.append("file[]", file);
        });
        try {
            const response = await axios({
                method: "post",
                url: this.state.api_url,
                data: formData,
                responseType: "arraybuffer",
                config: { headers: { "Content-Type": "multipart/form-data" } }
            });
            UTILS.downloadFile(response.data, this.state.default_download_name);
        } catch (e) {
            this.setState({ progState: "default" });
            UTILS.alertError(e);
        }
        this.setState({ progState: "default" });
    };

    render() {
        return (
            <div className="container">
                <Header title={this.state.title} version={this.state.version} />
                <ButtonGroup
                    progState={this.state.progState}
                    addFiles={this.addFiles}
                    convert={this.convert}
                />
                <DocumentPanel
                    count={this.state.files.length}
                    clearFiles={this.clearFiles}
                    addFiles={this.addFiles}
                    removeFile={this.removeFile}
                    files={this.state.files}
                />
            </div>
        );
    }
}

export default App;
