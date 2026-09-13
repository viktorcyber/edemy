const { defineConfig, globalIgnores } = require('eslint/config');
const expoConfig = require('eslint-config-expo/flat');
const eslintPluginPrettierRecommended = require('eslint-plugin-prettier/recommended');
const globals = require('globals');
const pluginQuery = require('@tanstack/eslint-plugin-query');

module.exports = defineConfig([
  globalIgnores(['dist/*']),
  expoConfig,
  eslintPluginPrettierRecommended,
  ...pluginQuery.configs['flat/recommended'],
  {
    files: ['babel.config.js'],
    languageOptions: {
      globals: globals.node,
    },
    rules: {
      'react/display-name': 'off',
    },
  },
]);
