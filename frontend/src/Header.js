import React from "react";

const Header = props => {
    const { title, version } = props;
    return (
        <div>
            <h1>
                {title}
                <span className="lbl-version">{version}</span>
            </h1>
        </div>
    );
};

export default Header;
