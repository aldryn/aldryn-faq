/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global browser, by, element, expect */

// #############################################################################
// INTEGRATION TEST PAGE OBJECT

var page = {
    site: 'http://127.0.0.1:8000/en/',

    // log in
    editModeLink: element(by.css('.inner a[href="/?edit"]')),
    usernameInput: element(by.id('id_username')),
    passwordInput: element(by.id('id_password')),
    loginButton: element(by.css('input[type="submit"]')),
    userMenus: element.all(by.css('.cms-toolbar-item-navigation > li > a')),

    // adding new page
    modalCloseButton: element(by.css('.cms-modal-close')),
    userMenuDropdown: element(by.css(
        '.cms-toolbar-item-navigation-hover')),
    administrationOptions: element.all(by.css(
        '.cms-toolbar-item-navigation a[href="/en/admin/"]')),
    sideMenuIframe: element(by.css('.cms-sideframe-frame iframe')),
    pagesLink: element(by.css('.model-page > th > a')),
    addPageLink: element(by.css('.object-tools .addlink')),
    titleInput: element(by.id('id_title')),
    slugErrorNotification: element(by.css('.errors.slug')),
    saveButton: element(by.css('.submit-row [name="_save"]')),
    editPageLink: element(by.css('.cms-tree-item-preview [href*="preview/"]')),
    testLink: element(by.cssContainingText('a', 'Test')),
    sideFrameClose: element(by.css('.cms-sideframe-close')),

    // adding new apphook config
    breadcrumbs: element(by.css('.breadcrumbs')),
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
    appconfigOption: element(by.css('#id_appconfig > option:nth-child(2)')),

    // adding new question
    addQuestionButton: element(by.css('.model-question .addlink')),
    editQuestionButton: element(by.css('.model-question .changelink')),
    categorySelect: element(by.id('id_category')),
    categoryOption: element(by.css('#id_category > option:nth-child(2)')),
    ckeIframe: element(by.css('#cke_1_contents iframe')),
    ckeEditableBlock: element(by.css('.cke_editable')),
    saveAndContinueButton: element(by.css('.submit-row [name="_continue"]')),
    editQuestionLinksTable: element(by.css('.results')),
    editQuestionLinks: element.all(by.css(
        '.results th > [href*="/aldryn_faq/question/"]')),

    // adding faq block to the page
    aldrynFAQBlock: element(by.css('ul.nav ~ ul')),
    advancedSettingsOption: element(by.css(
        '.cms-toolbar-item-navigation [href*="advanced-settings"]')),
    modalIframe: element(by.css('.cms-modal-frame iframe')),
    applicationSelect: element(by.id('application_urls')),
    faqOption: element(by.css('option[value="FaqApp"]')),
    saveModalButton: element(by.css('.cms-modal-buttons .cms-btn-action')),
    categoryLink: element(by.css('a[href*="/test-category/"]')),
    questionLink: element(by.css('a[href*="/test-category/test-question"]')),
    questionTitle: element(by.css('article h2')),

    // deleting question
    deleteButton: element(by.css('.deletelink-box a')),
    sidebarConfirmationButton: element(by.css('#content [type="submit"]')),

    cmsLogin: function (credentials) {
        // object can contain username and password, if not set it will
        // fallback to 'admin'
        credentials = credentials ||
            { username: 'admin', password: 'admin' };

        page.usernameInput.clear();

        // fill in email field
        page.usernameInput.sendKeys(
            credentials.username).then(function () {
            page.passwordInput.clear();

            // fill in password field
            return page.passwordInput.sendKeys(
                credentials.password);
        }).then(function () {
            return page.loginButton.click();
        }).then(function () {
            // this is required for django1.6, because it doesn't redirect
            // correctly from admin
            browser.get(page.site);

            // wait for user menu to appear
            browser.wait(browser.isElementPresent(
                page.userMenus.first()),
                page.mainElementsWaitTime);

            // validate user menu
            expect(page.userMenus.first().isDisplayed())
                .toBeTruthy();
        });
    }

};

module.exports = page;
