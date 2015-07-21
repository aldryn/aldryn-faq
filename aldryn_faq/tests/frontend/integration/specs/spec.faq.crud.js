/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser, By, expect */

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

    it('creates a new test page', function () {
        // click the example.com link in the top menu
        faqPage.userMenus.first().click().then(function () {
            // wait for top menu dropdown options to appear
            browser.wait(function () {
                return browser.isElementPresent(faqPage.userMenuDropdown);
            }, faqPage.mainElementsWaitTime);

            faqPage.administrationOptions.first().click();
        }).then(function () {
            // wait for modal iframe to appear
            browser.wait(function () {
                return browser.isElementPresent(faqPage.sideMenuIframe);
            }, faqPage.iframeWaitTime);

            // switch to sidebar menu iframe
            browser.switchTo().frame(browser.findElement(
                By.css('.cms_sideframe-frame iframe')));

            browser.wait(function () {
                return browser.isElementPresent(faqPage.pagesLink);
            }, faqPage.mainElementsWaitTime);

            faqPage.pagesLink.click();

            // check if the page already exists and return the status
            return faqPage.addPageLink.isPresent();
        }).then(function (present) {
            if (present === true) {
                // page is absent - create new page
                browser.wait(function () {
                    return browser.isElementPresent(faqPage.addPageLink);
                }, faqPage.mainElementsWaitTime);

                faqPage.addPageLink.click();

                browser.wait(function () {
                    return browser.isElementPresent(faqPage.titleInput);
                }, faqPage.mainElementsWaitTime);

                faqPage.titleInput.sendKeys('Test').then(function () {
                    faqPage.saveButton.click();

                    return faqPage.slugErrorNotification.isPresent();
                }).then(function (present) {
                    if (present === false) {
                        browser.wait(function () {
                            return browser.isElementPresent(faqPage.editPageLink);
                        }, faqPage.mainElementsWaitTime);

                        // wait till the editPageLink will become clickable
                        browser.sleep(500);

                        // validate/click edit page link
                        faqPage.editPageLink.click();

                        // switch to default page content
                        browser.switchTo().defaultContent();

                        browser.wait(function () {
                            return browser.isElementPresent(faqPage.testLink);
                        }, faqPage.mainElementsWaitTime);

                        // validate test link text
                        faqPage.testLink.getText().then(function (title) {
                            expect(title).toEqual('Test');
                        });
                    }
                });
            }
        });
    });

});
