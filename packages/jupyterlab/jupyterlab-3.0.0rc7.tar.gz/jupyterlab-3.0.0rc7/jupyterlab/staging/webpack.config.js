// This file is auto-generated from the corresponding file in /dev_mode
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

const plib = require('path');
const fs = require('fs-extra');
const Handlebars = require('handlebars');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const webpack = require('webpack');
const merge = require('webpack-merge').default;
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
  .BundleAnalyzerPlugin;
const baseConfig = require('@jupyterlab/builder/lib/webpack.config.base');
const { ModuleFederationPlugin } = webpack.container;

const Build = require('@jupyterlab/builder').Build;
const WPPlugin = require('@jupyterlab/builder').WPPlugin;
const package_data = require('./package.json');

// Handle the extensions.
const jlab = package_data.jupyterlab;
const extensions = jlab.extensions;
const mimeExtensions = jlab.mimeExtensions;
const { externalExtensions } = jlab;
const packageNames = Object.keys(mimeExtensions).concat(
  Object.keys(extensions),
  Object.keys(externalExtensions)
);

// go throught each external extension
// add to mapping of extension and mime extensions, of package name
// to path of the extension.
for (const key in externalExtensions) {
  const {
    jupyterlab: { extension, mimeExtension }
  } = require(`${key}/package.json`);
  if (extension !== undefined) {
    extensions[key] = extension === true ? '' : extension;
  }
  if (mimeExtension !== undefined) {
    mimeExtensions[key] = mimeExtension === true ? '' : mimeExtension;
  }
}

// Ensure a clear build directory.
const buildDir = plib.resolve(jlab.buildDir);
if (fs.existsSync(buildDir)) {
  fs.removeSync(buildDir);
}
fs.ensureDirSync(buildDir);

const outputDir = plib.resolve(jlab.outputDir);

// Build the assets
const extraConfig = Build.ensureAssets({
  packageNames: packageNames,
  output: outputDir
});

// Build up singleton metadata for module federation.
const singletons = {};

package_data.jupyterlab.singletonPackages.forEach(element => {
  singletons[element] = { singleton: true };
});

// Go through each external extension
// add to mapping of extension and mime extensions, of package name
// to path of the extension.
for (const key in externalExtensions) {
  const {
    jupyterlab: { extension, mimeExtension }
  } = require(`${key}/package.json`);
  if (extension !== undefined) {
    extensions[key] = extension === true ? '' : extension;
  }
  if (mimeExtension !== undefined) {
    mimeExtensions[key] = mimeExtension === true ? '' : mimeExtension;
  }
}

// Create the entry point file.
const source = fs.readFileSync('index.js').toString();
const template = Handlebars.compile(source);
const extData = {
  jupyterlab_extensions: extensions,
  jupyterlab_mime_extensions: mimeExtensions
};
const result = template(extData);

fs.writeFileSync(plib.join(buildDir, 'index.out.js'), result);
fs.copySync('./package.json', plib.join(buildDir, 'package.json'));
if (outputDir !== buildDir) {
  fs.copySync(
    plib.join(outputDir, 'imports.css'),
    plib.join(buildDir, 'imports.css')
  );
}

// Make a bootstrap entrypoint
const entryPoint = plib.join(buildDir, 'bootstrap.js');
const bootstrap = 'import("./index.out.js");';
fs.writeFileSync(entryPoint, bootstrap);

// Set up variables for the watch mode ignore plugins
const watched = {};
const ignoreCache = Object.create(null);
let watchNodeModules = false;
Object.keys(jlab.linkedPackages).forEach(function (name) {
  if (name in watched) {
    return;
  }
  const localPkgPath = require.resolve(plib.join(name, 'package.json'));
  watched[name] = plib.dirname(localPkgPath);
  if (localPkgPath.indexOf('node_modules') !== -1) {
    watchNodeModules = true;
  }
});

// Set up source-map-loader to look in watched lib dirs
const sourceMapRes = Object.values(watched).reduce((res, name) => {
  res.push(new RegExp(name + '/lib'));
  return res;
}, []);

/**
 * Sync a local path to a linked package path if they are files and differ.
 * This is used by `jupyter lab --watch` to synchronize linked packages
 * and has no effect in `jupyter lab --dev-mode --watch`.
 */
function maybeSync(localPath, name, rest) {
  const stats = fs.statSync(localPath);
  if (!stats.isFile(localPath)) {
    return;
  }
  const source = fs.realpathSync(plib.join(jlab.linkedPackages[name], rest));
  if (source === fs.realpathSync(localPath)) {
    return;
  }
  fs.watchFile(source, { interval: 500 }, function (curr) {
    if (!curr || curr.nlink === 0) {
      return;
    }
    try {
      fs.copySync(source, localPath);
    } catch (err) {
      console.error(err);
    }
  });
}

/**
 * A filter function set up to exclude all files that are not
 * in a package contained by the Jupyterlab repo. Used to ignore
 * files during a `--watch` build.
 */
function ignored(path) {
  path = plib.resolve(path);
  if (path in ignoreCache) {
    // Bail if already found.
    return ignoreCache[path];
  }

  // Limit the watched files to those in our local linked package dirs.
  let ignore = true;
  Object.keys(watched).some(name => {
    const rootPath = watched[name];
    const contained = path.indexOf(rootPath + plib.sep) !== -1;
    if (path !== rootPath && !contained) {
      return false;
    }
    const rest = path.slice(rootPath.length);
    if (rest.indexOf('node_modules') === -1) {
      ignore = false;
      maybeSync(path, name, rest);
    }
    return true;
  });
  ignoreCache[path] = ignore;
  return ignore;
}

const shared = {
  ...package_data.resolutions,
  ...singletons
};

// Webpack module sharing expects version numbers, so if a resolution was a
// filename, extract the right version number from what was installed
Object.keys(shared).forEach(k => {
  const v = shared[k];
  if (typeof v === 'string' && v.startsWith('file:')) {
    shared[k] = require(`${k}/package.json`).version;
  }
});

const plugins = [
  new WPPlugin.NowatchDuplicatePackageCheckerPlugin({
    verbose: true,
    exclude(instance) {
      // ignore known duplicates
      return ['domelementtype', 'hash-base', 'inherits'].includes(
        instance.name
      );
    }
  }),
  new HtmlWebpackPlugin({
    chunksSortMode: 'none',
    template: plib.join(__dirname, 'templates', 'template.html'),
    title: jlab.name || 'JupyterLab'
  }),
  // custom plugin for ignoring files during a `--watch` build
  new WPPlugin.FilterWatchIgnorePlugin(ignored),
  // custom plugin that copies the assets to the static directory
  new WPPlugin.FrontEndPlugin(buildDir, jlab.staticDir),
  new ModuleFederationPlugin({
    library: {
      type: 'var',
      name: ['_JUPYTERLAB', 'CORE_LIBRARY_FEDERATION']
    },
    name: 'CORE_FEDERATION',
    shared
  })
];

if (process.argv.includes('--analyze')) {
  plugins.push(new BundleAnalyzerPlugin());
}

module.exports = [
  merge(baseConfig, {
    mode: 'development',
    entry: {
      main: ['./publicpath', 'whatwg-fetch', entryPoint]
    },
    output: {
      path: plib.resolve(buildDir),
      publicPath: '{{page_config.fullStaticUrl}}/',
      filename: '[name].[contenthash].js'
    },
    optimization: {
      splitChunks: {
        chunks: 'all'
      }
    },
    module: {
      rules: [
        {
          test: /\.js$/,
          include: sourceMapRes,
          use: ['source-map-loader'],
          enforce: 'pre'
        }
      ]
    },
    devtool: 'inline-source-map',
    externals: ['node-fetch', 'ws'],
    plugins
  })
].concat(extraConfig);

// Needed to watch changes in linked extensions in node_modules
// (jupyter lab --watch)
// See https://github.com/webpack/webpack/issues/11612
if (watchNodeModules) {
  module.exports[0].snapshot = { managedPaths: [] };
}

const logPath = plib.join(buildDir, 'build_log.json');
fs.writeFileSync(logPath, JSON.stringify(module.exports, null, '  '));
