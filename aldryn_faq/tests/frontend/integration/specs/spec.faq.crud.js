/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global describe, it, browser, By, expect */

// #############################################################################
// INTEGRATION TEST
var faqPage = require('../pages/page.faq.crud.js');
var cmsProtractorHelper = require('cms-protractor-helper');

describe('Aldryn FAQ tests: ', function () {
    // create random question name
    var questionName = 'Test question ' + (Math.floor(Math.random() * 10001));

    it('logs in to the site with valid username and password', function () {
        // go to the main page
        browser.get(faqPage.site);

        // check if the page already exists
        faqPage.testLink.isPresent().then(function (present) {
            if (present === true) {
                // go to the main page
                browser.get(faqPage.site + '?edit');
                browser.sleep(1000);
                cmsProtractorHelper.waitForDisplayed(faqPage.usernameInput);
            }

            // login to the site
            faqPage.cmsLogin();
        });
    });

    it('creates a new test page', function () {
        // close the wizard if necessary
        faqPage.modalCloseButton.isDisplayed().then(function (displayed) {
            if (displayed) {
                faqPage.modalCloseButton.click();
            }
        });

        cmsProtractorHelper.waitForDisplayed(faqPage.userMenus.first());
        // have to wait till animation finished
        browser.sleep(300);

        // click the example.com link in the top menu
        return faqPage.userMenus.first().click().then(function () {
            // wait for top menu dropdown options to appear
            cmsProtractorHelper.waitFor(faqPage.userMenuDropdown);

            return faqPage.administrationOptions.first().click();
        }).then(function () {
            // wait for modal iframe to appear
            cmsProtractorHelper.waitFor(faqPage.sideMenuIframe);

            // switch to sidebar menu iframe
            browser.switchTo().frame(browser.findElement(
                By.css('.cms-sideframe-frame iframe')));

            cmsProtractorHelper.waitFor(faqPage.pagesLink);

            faqPage.pagesLink.click();

            // wait for iframe side menu to reload
            cmsProtractorHelper.waitFor(faqPage.addConfigsButton);

            // check if the page already exists and return the status
            return faqPage.addPageLink.isPresent();
        }).then(function (present) {
            if (present === true) {
                // page is absent - create new page
                cmsProtractorHelper.waitFor(faqPage.addPageLink);

                faqPage.addPageLink.click();

                cmsProtractorHelper.waitFor(faqPage.titleInput);

                return faqPage.titleInput.sendKeys('Test').then(function () {
                    faqPage.saveButton.click();

                    return faqPage.slugErrorNotification.isPresent();
                }).then(function (present) {
                    if (present === false) {
                        cmsProtractorHelper.waitFor(faqPage.editPageLink);

                        // wait till the editPageLink will become clickable
                        browser.sleep(500);

                        // validate/click edit page link
                        faqPage.editPageLink.click();

                        // switch to default page content
                        browser.switchTo().defaultContent();

                        cmsProtractorHelper.waitFor(faqPage.testLink);

                        // validate test link text
                        faqPage.testLink.getText().then(function (title) {
                            expect(title).toEqual('Test');
                        });
                    }
                });
            }
        });
    });

    it('creates a new apphook config', function () {
        // check if the focus is on sidebar ifarme
        return faqPage.editPageLink.isPresent().then(function (present) {
            if (present === false) {
                // wait for modal iframe to appear
                cmsProtractorHelper.waitFor(faqPage.sideMenuIframe);

                // switch to sidebar menu iframe
                return browser.switchTo().frame(browser.findElement(By.css(
                    '.cms-sideframe-frame iframe')));
            }
        }).then(function () {
            // click the Home link in breadcrumbs
            browser.sleep(1000);

            faqPage.breadcrumbs.isPresent().then(function (present) {
                if (present) {
                    // click the Home link in breadcrumbs
                    cmsProtractorHelper.waitFor(faqPage.breadcrumbsLinks.first());
                    faqPage.breadcrumbsLinks.first().click();
                }
            });

            cmsProtractorHelper.waitFor(faqPage.faqConfigsLink);

            faqPage.faqConfigsLink.click();

            // check if the apphook config already exists and return the status
            return faqPage.editConfigsLink.isPresent();
        }).then(function (present) {
            if (present === false) {
                // apphook config is absent - create new apphook config
                cmsProtractorHelper.waitFor(faqPage.addConfigsButton);

                faqPage.addConfigsButton.click();

                cmsProtractorHelper.waitFor(faqPage.namespaceInput);

                return faqPage.namespaceInput.sendKeys('aldryn_faq')
                    .then(function () {
                    return faqPage.applicationTitleInput.sendKeys('Test title');
                }).then(function () {
                    faqPage.saveButton.click();

                    cmsProtractorHelper.waitFor(faqPage.successNotification);
                });
            }
        });
    });

    it('creates a new category', function () {
        cmsProtractorHelper.waitFor(faqPage.breadcrumbsLinks.first());

        // click the Home link in breadcrumbs
        faqPage.breadcrumbsLinks.first().click();

        cmsProtractorHelper.waitFor(faqPage.categoriesLink);

        faqPage.categoriesLink.click();

        // wait for iframe side menu to reload
        cmsProtractorHelper.waitFor(faqPage.addConfigsButton);

        // check if the category already exists and return the status
        return faqPage.editConfigsLink.isPresent().then(function (present) {
            if (present === false) {
                // category is absent - create new category
                cmsProtractorHelper.waitFor(faqPage.addConfigsButton);

                faqPage.addConfigsButton.click();

                cmsProtractorHelper.waitFor(faqPage.languageTabs.first());

                // switch to English language tab
                faqPage.languageTabs.first().click().then(function () {
                    cmsProtractorHelper.waitFor(faqPage.nameInput);

                    return faqPage.nameInput.sendKeys('Test category');
                }).then(function () {
                    // set Appconfig
                    return cmsProtractorHelper.selectOption(faqPage.appconfigSelect,
                        'FAQ / aldryn_faq', faqPage.appconfigOption);
                }).then(function () {
                    faqPage.saveButton.click();

                    cmsProtractorHelper.waitFor(faqPage.successNotification);
                });
            }
        });
    });

    it('creates a new question', function () {
        cmsProtractorHelper.waitFor(faqPage.breadcrumbsLinks.first());

        // click the Home link in breadcrumbs
        faqPage.breadcrumbsLinks.first().click();

        cmsProtractorHelper.waitFor(faqPage.addQuestionButton);

        faqPage.addQuestionButton.click();

        cmsProtractorHelper.waitFor(faqPage.languageTabs.first());

        // switch to English language tab
        return faqPage.languageTabs.first().click().then(function () {
            cmsProtractorHelper.waitFor(faqPage.titleInput);

            return faqPage.titleInput.sendKeys(questionName);
        }).then(function () {
            // set Category
            return cmsProtractorHelper.selectOption(faqPage.categorySelect,
                        'Test category', faqPage.categoryOption);
        }).then(function () {
            // wait for cke iframe to appear
            cmsProtractorHelper.waitFor(faqPage.ckeIframe);

            // switch to cke iframe
            browser.switchTo().frame(browser.findElement(
                By.css('#cke_1_contents iframe')));

            cmsProtractorHelper.waitFor(faqPage.ckeEditableBlock);

            return faqPage.ckeEditableBlock.sendKeys('Test question');
        }).then(function () {
            // switch to default page content
            browser.switchTo().defaultContent();

            // wait for modal iframe to appear
            cmsProtractorHelper.waitFor(faqPage.sideMenuIframe);

            // switch to sidebar menu iframe
            browser.switchTo().frame(browser.findElement(By.css(
                '.cms-sideframe-frame iframe')));

            cmsProtractorHelper.waitFor(faqPage.saveAndContinueButton);

            browser.actions().mouseMove(faqPage.saveAndContinueButton)
                .perform();
            faqPage.saveButton.click();

            cmsProtractorHelper.waitFor(faqPage.successNotification);

            // validate success notification
            expect(faqPage.successNotification.isDisplayed()).toBeTruthy();
            // validate edit question link
            expect(faqPage.editQuestionLinks.first().isDisplayed())
                .toBeTruthy();
        });
    });

    it('adds a new faq block on the page', function () {
        // go to the main page
        browser.get(faqPage.site);

        // switch to default page content
        browser.switchTo().defaultContent();

        cmsProtractorHelper.waitFor(faqPage.testLink);

        // wait till animation finishes
        browser.sleep(300);

        // add faq to the page only if it was not added before
        return faqPage.aldrynFAQBlock.isPresent().then(function (present) {
            if (present === false) {
                // click the Page link in the top menu
                return faqPage.userMenus.get(1).click().then(function () {
                    // wait for top menu dropdown options to appear
                    cmsProtractorHelper.waitFor(faqPage.userMenuDropdown);

                    faqPage.advancedSettingsOption.click();

                    // wait for modal iframe to appear
                    cmsProtractorHelper.waitFor(faqPage.modalIframe);

                    // switch to modal iframe
                    browser.switchTo().frame(browser.findElement(By.css(
                        '.cms-modal-frame iframe')));

                    // wait for Application select to appear
                    cmsProtractorHelper.waitFor(faqPage.applicationSelect);

                    // set Application
                    return cmsProtractorHelper.selectOption(faqPage.applicationSelect,
                        'FAQ', faqPage.faqOption);
                }).then(function () {
                    // switch to default page content
                    browser.switchTo().defaultContent();

                    cmsProtractorHelper.waitFor(faqPage.saveModalButton);

                    browser.actions().mouseMove(faqPage.saveModalButton)
                        .perform();
                    return faqPage.saveModalButton.click();
                });
            }
        }).then(function () {
            // refresh the page to see changes
            browser.refresh();

            // wait for aldryn-faq block to appear
            cmsProtractorHelper.waitFor(faqPage.aldrynFAQBlock);

            // wait till animation of sideframe opening finishes
            browser.sleep(300);

            // close sideframe (it covers the link)
            cmsProtractorHelper.waitFor(faqPage.sideFrameClose);
            faqPage.sideFrameClose.click();

            // wait till animation finishes
            browser.sleep(300);

            faqPage.categoryLink.click();

            // wait for question link to appear
            cmsProtractorHelper.waitFor(faqPage.questionLink);

            faqPage.questionLink.click();

            cmsProtractorHelper.waitFor(faqPage.questionTitle);

            // validate question title
            expect(faqPage.questionTitle.isDisplayed()).toBeTruthy();
        });
    });

    it('deletes question', function () {
        cmsProtractorHelper.waitForDisplayed(faqPage.userMenus.first());
        // have to wait till animation finished
        browser.sleep(300);
        // click the example.com link in the top menu
        faqPage.userMenus.first().click().then(function () {
            // wait for top menu dropdown options to appear
            cmsProtractorHelper.waitForDisplayed(faqPage.userMenuDropdown);

            return faqPage.administrationOptions.first().click();
        }).then(function () {
            // wait for modal iframe to appear
            cmsProtractorHelper.waitFor(faqPage.sideMenuIframe);
        });


        // switch to sidebar menu iframe
        browser.switchTo()
            .frame(browser.findElement(By.css('.cms-sideframe-frame iframe')));

        cmsProtractorHelper.waitFor(faqPage.editQuestionButton);
        browser.sleep(100);
        faqPage.editQuestionButton.click().then(function () {
            // wait for edit job opening link to appear
            return cmsProtractorHelper.waitFor(faqPage.editQuestionLinksTable);
        }).then(function () {
            // validate edit faq entry links texts to delete proper faq entry
            return faqPage.editQuestionLinks.first().getText();
        }).then(function (text) {
            if (text === questionName) {
                return faqPage.editQuestionLinks.first().click();
            } else {
                return faqPage.editQuestionLinks.get(1).getText()
                    .then(function (text) {
                    if (text === questionName) {
                        return faqPage.editQuestionLinks.get(1).click();
                    } else {
                        return faqPage.editQuestionLinks.get(2).getText()
                            .then(function (text) {
                            if (text === questionName) {
                                return faqPage.editQuestionLinks.get(2).click();
                            }
                        });
                    }
                });
            }
        }).then(function () {
            // wait for delete button to appear
            cmsProtractorHelper.waitFor(faqPage.deleteButton);

            browser.actions().mouseMove(faqPage.saveAndContinueButton)
                .perform();
            return faqPage.deleteButton.click();
        }).then(function () {
            // wait for confirmation button to appear
            cmsProtractorHelper.waitFor(faqPage.sidebarConfirmationButton);

            faqPage.sidebarConfirmationButton.click();

            cmsProtractorHelper.waitFor(faqPage.successNotification);

            // validate success notification
            expect(faqPage.successNotification.isDisplayed()).toBeTruthy();

            // switch to default page content
            browser.switchTo().defaultContent();

            // refresh the page to see changes
            browser.refresh();
        });
    });

});
