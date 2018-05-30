import React from 'react';
import PropTypes from 'prop-types';

import VtkRenderer from 'paraviewweb/src/React/Renderers/VtkRenderer';

import network from './network';

export default function MainView(props) {
  console.log(props.viewIds);
  return (
    <div>
      {props.viewIds.map((id) => (
        <VtkRenderer
          key={id}
          connection={network.getConnection()}
          client={network.getClient()}
          viewId={id}

          stillQuality={100}
          interactiveQuality={60}
          stillRatio={1}
          interactiveRatio={1}
        />
      ))}
    </div>
  );
}

MainView.propTypes = {
  viewIds: PropTypes.array,
};

MainView.defaultProps = {
  viewIds: [],
};
