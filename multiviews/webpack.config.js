const webpack = require('webpack');
const path = require('path');
const autoprefixer = require('autoprefixer');

const entry = path.join(__dirname, './src/index.js');
const outputPath = path.join(__dirname, './www');

module.exports = {
  entry,
  output: {
    path: outputPath,
    filename: 'multi-view.js',
    libraryTarget: 'umd',
  },
  module: {
    rules: [
  {
        test: entry,
        loader: 'expose-loader?MultiView',
  },
      {
        test: /\.js$/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              presets: ['env', 'react'],
            },
          },
        ],
      },
      {
        test: /\.mcss$/,
        use: [
          { loader: 'style-loader' },
          {
            loader: 'css-loader',
            options: {
              localIdentName: '[name]-[local]_[sha512:hash:base32:5]',
              modules: true,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              plugins: () => [autoprefixer('last 2 version', 'ie >= 10')],
            },
          },
        ],
      },
    ],
  },
  resolve: {
    alias: {
      PVWStyle: path.join(__dirname, './node_modules/paraviewweb/style'),
    },
  },
};
