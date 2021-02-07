import React from 'react';

const Iframe = ({ source }) => {

    if (source == null) {
        return <div>Loading...</div>;
    }

    const src = source;     
    return (
        // basic bootstrap classes. you can change with yours.
        <div>
            <div className="emdeb-responsive">
                <iframe id="igraph" title="Stroms Graph" scrolling="no" seamless="seamless" src={src} height="525" width="100%"></iframe>
            </div>
        </div>
    );
};

export default Iframe;