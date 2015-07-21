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
    it('logs in to the site with valid username and password', function () {
        // go to the main page
        browser.get(faqPage.site);

        // check if the page already exists
        faqPage.testLink.isPresent().then(function (present) {
            if (present === true) {
                // go to the main page
                browser.get(faqPage.site + '?edit');
            } else {
                // click edit mode link
                faqPage.editModeLink.click();
            }

            // wait for username input to appear
            browser.wait(function () {
                return browser.isElementPresent(faqPage.usernameInput);
            }, faqPage.mainElementsWaitTime);

            // login to the site
            faqPage.cmsLogin();
        });
    });

});
