import React from 'react';
import ReactDOM from 'react-dom';

import ProgressLoaderWidget from 'paraviewweb/src/React/Widgets/ProgressLoaderWidget';

import network from './network';
import MainView from './MainView';

function start() {
  // Mount UI
  const container = document.querySelector('.content');

  network
    .getClient()
    .UserProtocol.getViews()
    .then((viewIds) => {
      ReactDOM.unmountComponentAtNode(container);
      ReactDOM.render(<MainView viewIds={viewIds} />, container);
    });
}

function loading(message = 'Loading ParaView...') {
  // Mount UI
  const container = document.querySelector('.content');
  ReactDOM.unmountComponentAtNode(container);
  ReactDOM.render(<ProgressLoaderWidget message={message} />, container);
}

export function connect(config = {}) {
  loading();
  network.onReady(start);
  network.onError(loading);
  network.onClose(() => loading('Server disconnected'));
  network.connect(config);
}
