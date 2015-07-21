/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global by, element, browser, expect */

// #############################################################################
// INTEGRATION TEST PAGE OBJECT

var faqPage = {
    site: 'http://127.0.0.1:8000/en/',
    mainElementsWaitTime: 12000,
    iframeWaitTime: 15000,

    // log in
    editModeLink: element(by.css('.inner a[href="/?edit"]')),
    usernameInput: element(by.id('id_cms-username')),
    passwordInput: element(by.id('id_cms-password')),
    loginButton: element(by.css('.cms_form-login input[type="submit"]')),
    userMenus: element.all(by.css('.cms_toolbar-item-navigation > li > a')),
    testLink: element(by.css('.selected a')),

    cmsLogin: function (credentials) {
        // object can contain username and password, if not set it will
        // fallback to 'admin'
        credentials = credentials ||
            { username: 'admin', password: 'admin' };

        faqPage.usernameInput.clear();

        // fill in email field
        faqPage.usernameInput.sendKeys(
            credentials.username).then(function () {
            faqPage.passwordInput.clear();

            // fill in password field
            faqPage.passwordInput.sendKeys(
                credentials.password);
        }).then(function () {
            faqPage.loginButton.click();

            // wait for user menu to appear
            browser.wait(browser.isElementPresent(
                faqPage.userMenus.first()),
                faqPage.mainElementsWaitTime);

            // validate user menu
            expect(faqPage.userMenus.first().isDisplayed())
                .toBeTruthy();
        });
    }

};

module.exports = faqPage;
