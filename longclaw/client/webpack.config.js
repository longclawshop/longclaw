var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: {
    orders: './src/orders/index.jsx',
    longclawclient: ['./src/api/api.js'],
    vendors: [
      'react', 'whatwg-fetch', // 'isomorphic-fetch', 
      'immutable', 
    ]
  },
  output: {
      path: path.resolve('../core/static/core/js/'),
      filename: "[name].bundle.js"
  },

  module: {
    // loaders: [{
    rules: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
      loader: 'babel-loader',
      options: {
        // presets: ['@babel/preset-stage-0']
      }
    }, {
      test: /\.css$/,
      use: 'style!css'
    }, {
      test: /\.less$/,
      use: 'style-loader!css-loader!postcss-loader!less'
    },
    {
      test: /api.js$/,
      use: [
        { 
          loader: 'expose-loader',
          options: {
            exposes: {
              globalName: 'longclawclient'
            }
          }
        },
        { 
          loader: 'babel-loader', 
          options: { 
            // presets: ['@babel/preset-stage-0'] 
          } 
        }
      ]
    }]
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      ie: 'component-ie',
      // 'isomorphic-fetch': 'fetch-mock-forwarder'
    }
  },
  // debug: false,

  // optimization: {
  //   runtimeChunk: "single",
  //   splitChunks: {
  //     cacheGroups: {
  //       default: {
  //         // name: "vendors",
  //         chunks: "all",
  //       }
  //     }
  //   }
  // },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    // new webpack.optimize.CommonsChunkPlugin({
    //   name: 'vendors', 
    //   filename: 'vendors.bundle.js', 
    //   minChunks: Infinity
    // }),
    // new webpack.optimize.DedupePlugin(),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production')
      }
    }),
    new webpack.SourceMapDevToolPlugin({
      // filename: 'bundle.js.map',
      filename: '[file].map[query]',
      append: '\n//# sourceMappingURL=http://127.0.0.1:3001/dist/js/[url]'
    }),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
  ]
}