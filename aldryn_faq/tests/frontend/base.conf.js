/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';

// #############################################################################
// CONFIGURATION
var b2s = require('browserslist-saucelabs');

module.exports = {
    formatTaskName: function formatTaskName(browserName) {
        return [
            'Test', browserName, 'for',
            process.env.TRAVIS_REPO_SLUG,
            // eslint-disable-next-line no-negated-condition
            process.env.TRAVIS_PULL_REQUEST !== 'false' ?
            'pull request #' + process.env.TRAVIS_PULL_REQUEST : '',
            'build #' + process.env.TRAVIS_JOB_NUMBER
        ].join(' ');
    },

    sauceLabsBrowsers: b2s({ browsers: ['chrome 42'] })
};
