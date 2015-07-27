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

    // adding new page
    userMenuDropdown: element(by.css(
        '.cms_toolbar-item-navigation-hover')),
    administrationOptions: element.all(by.css(
        '.cms_toolbar-item-navigation a[href="/en/admin/"]')),
    sideMenuIframe: element(by.css('.cms_sideframe-frame iframe')),
    pagesLink: element(by.css('.model-page > th > a')),
    addPageLink: element(by.css('.sitemap-noentry .addlink')),
    titleInput: element(by.id('id_title')),
    slugErrorNotification: element(by.css('.errors.slug')),
    saveButton: element(by.css('.submit-row [name="_save"]')),
    editPageLink: element(by.css('.col1 [href*="preview/"]')),

    // adding new apphook config
    breadcrumbsLinks: element.all(by.css('.breadcrumbs a')),
    faqConfigsLink: element(by.css('.model-faqconfig > th > a')),
    editConfigsLink: element(by.css('.row1 th > a')),
    addConfigsButton: element(by.css('.object-tools .addlink')),
    namespaceInput: element(by.id('id_namespace')),
    applicationTitleInput: element(by.id('id_app_title')),
    successNotification: element(by.css('.messagelist .success')),

    // adding new category
    categoriesLink: element(by.css('.model-category > th > a')),
    languageTabs: element.all(by.css('.parler-language-tabs > .empty > a')),
    nameInput: element(by.id('id_name')),
    appconfigSelect: element(by.id('id_appconfig')),

    // adding new question
    addQuestionButton: element(by.css('.model-question .addlink')),
    categorySelect: element(by.id('id_category')),
    ckeIframe: element(by.css('#cke_1_contents iframe')),
    ckeEditableBlock: element(by.css('.cke_editable')),
    saveAndContinueButton: element(by.css('.submit-row [name="_continue"]')),
    editQuestionLinks: element.all(by.css(
        '.results th > [href*="/aldryn_faq/question/"]')),

    // adding faq block to the page
    aldrynFAQBlock: element(by.css('.aldryn-faq-categories')),
    advancedSettingsOption: element(by.css(
        '.cms_toolbar-item-navigation [href*="advanced-settings"]')),
    modalIframe: element(by.css('.cms_modal-frame iframe')),
    applicationSelect: element(by.id('application_urls')),
    saveModalButton: element(by.css('.cms_modal-buttons .cms_btn-action')),
    categoryLink: element(by.css('.aldryn-faq-categories a')),
    questionLink: element(by.css('.aldryn-faq .list-group a')),
    questionTitle: element(by.css('.aldryn-faq-detail h2 > div')),

    // deleting question
    deleteButton: element(by.css('.deletelink-box a')),
    sidebarConfirmationButton: element(by.css('#content [type="submit"]')),

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
            return faqPage.passwordInput.sendKeys(
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
