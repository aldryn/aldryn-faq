/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser */

// #############################################################################
// INTEGRATION TEST
var faqPage = require('../pages/page.faq.crud.js');

describe('Aldryn FAQ tests: ', function () {
    it('opens the main page', function () {
        // go to the main page
        browser.get(faqPage.site);
    });

});
