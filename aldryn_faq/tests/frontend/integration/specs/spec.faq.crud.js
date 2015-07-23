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

    it('creates a new apphook config', function () {
        // check if the focus is on sidebar ifarme
        faqPage.editPageLink.isPresent().then(function (present) {
            if (present === false) {
                // wait for modal iframe to appear
                browser.wait(function () {
                    return browser.isElementPresent(faqPage.sideMenuIframe);
                }, faqPage.iframeWaitTime);

                // switch to sidebar menu iframe
                browser.switchTo().frame(browser.findElement(By.css(
                    '.cms_sideframe-frame iframe')));
            }
        }).then(function () {
            browser.wait(function () {
                return browser.isElementPresent(faqPage.breadcrumbsLinks.first());
            }, faqPage.mainElementsWaitTime);

            // click the Home link in breadcrumbs
            faqPage.breadcrumbsLinks.first().click();

            browser.wait(function () {
                return browser.isElementPresent(faqPage.faqConfigsLink);
            }, faqPage.mainElementsWaitTime);

            faqPage.faqConfigsLink.click();

            // check if the apphook config already exists and return the status
            return faqPage.editConfigsLink.isPresent();
        }).then(function (present) {
            if (present === false) {
                // apphook config is absent - create new apphook config
                browser.wait(function () {
                    return browser.isElementPresent(faqPage.addConfigsButton);
                }, faqPage.mainElementsWaitTime);

                faqPage.addConfigsButton.click();

                browser.wait(function () {
                    return browser.isElementPresent(faqPage.namespaceInput);
                }, faqPage.mainElementsWaitTime);

                faqPage.namespaceInput.sendKeys('aldryn_faq')
                    .then(function () {
                    return faqPage.applicationTitleInput.sendKeys('Test title');
                }).then(function () {
                    faqPage.saveButton.click();

                    browser.wait(function () {
                        return browser.isElementPresent(faqPage.successNotification);
                    }, faqPage.mainElementsWaitTime);
                });
            }
        });
    });

    it('creates a new category', function () {
        browser.wait(function () {
            return browser.isElementPresent(faqPage.breadcrumbsLinks.first());
        }, faqPage.mainElementsWaitTime);

        // click the Home link in breadcrumbs
        faqPage.breadcrumbsLinks.first().click();

        browser.wait(function () {
            return browser.isElementPresent(faqPage.categoriesLink);
        }, faqPage.mainElementsWaitTime);

        faqPage.categoriesLink.click();

        // check if the category already exists and return the status
        faqPage.editConfigsLink.isPresent().then(function (present) {
            if (present === false) {
                // category is absent - create new category
                browser.wait(function () {
                    return browser.isElementPresent(faqPage.addConfigsButton);
                }, faqPage.mainElementsWaitTime);

                faqPage.addConfigsButton.click();

                browser.wait(function () {
                    return browser.isElementPresent(faqPage.languageTabs.first());
                }, faqPage.mainElementsWaitTime);

                // switch to English language tab
                faqPage.languageTabs.first().click().then(function () {
                    browser.wait(function () {
                        return browser.isElementPresent(faqPage.nameInput);
                    }, faqPage.mainElementsWaitTime);

                    return faqPage.nameInput.sendKeys('Test category');
                }).then(function () {
                    // wait for Appconfig select to appear
                    browser.wait(function () {
                        return browser.isElementPresent(faqPage.appconfigSelect);
                    }, faqPage.mainElementsWaitTime);

                    // set Appconfig
                    faqPage.appconfigSelect.click();
                    return faqPage.appconfigSelect.sendKeys('FAQ / aldryn_faq');
                }).then(function () {
                    faqPage.appconfigSelect.click();

                    faqPage.saveButton.click();

                    browser.wait(function () {
                        return browser.isElementPresent(faqPage.successNotification);
                    }, faqPage.mainElementsWaitTime);
                });
            }
        });
    });

    it('creates a new question', function () {
        browser.wait(function () {
            return browser.isElementPresent(faqPage.breadcrumbsLinks.first());
        }, faqPage.mainElementsWaitTime);

        // click the Home link in breadcrumbs
        faqPage.breadcrumbsLinks.first().click();

        browser.wait(function () {
            return browser.isElementPresent(faqPage.addQuestionButton);
        }, faqPage.mainElementsWaitTime);

        faqPage.addQuestionButton.click();

        browser.wait(function () {
            return browser.isElementPresent(faqPage.languageTabs.first());
        }, faqPage.mainElementsWaitTime);

        // switch to English language tab
        faqPage.languageTabs.first().click().then(function () {
            browser.wait(function () {
                return browser.isElementPresent(faqPage.titleInput);
            }, faqPage.mainElementsWaitTime);

            return faqPage.titleInput.sendKeys(questionName);
        }).then(function () {
            // set Category
            faqPage.categorySelect.click();
            return faqPage.categorySelect.sendKeys('Test category');
        }).then(function () {
            faqPage.categorySelect.click();

            // wait for cke iframe to appear
            browser.wait(function () {
                return browser.isElementPresent(faqPage.ckeIframe);
            }, faqPage.iframeWaitTime);

            // switch to cke iframe
            browser.switchTo().frame(browser.findElement(
                By.css('#cke_1_contents iframe')));

            browser.wait(function () {
                return browser.isElementPresent(faqPage.ckeEditableBlock);
            }, faqPage.mainElementsWaitTime);

            return faqPage.ckeEditableBlock.sendKeys('Test question');
        }).then(function () {
            // switch to default page content
            browser.switchTo().defaultContent();

            // wait for modal iframe to appear
            browser.wait(function () {
                return browser.isElementPresent(faqPage.sideMenuIframe);
            }, faqPage.iframeWaitTime);

            // switch to sidebar menu iframe
            browser.switchTo().frame(browser.findElement(By.css(
                '.cms_sideframe-frame iframe')));

            browser.wait(function () {
                return browser.isElementPresent(faqPage.saveAndContinueButton);
            }, faqPage.iframeWaitTime);

            browser.actions().mouseMove(faqPage.saveAndContinueButton)
                .perform();
            faqPage.saveButton.click();

            browser.wait(function () {
                return browser.isElementPresent(faqPage.successNotification);
            }, faqPage.mainElementsWaitTime);

            // validate success notification
            expect(faqPage.successNotification.isDisplayed())
                .toBeTruthy();
            // validate edit question link
            expect(faqPage.editQuestionLinks.first().isDisplayed())
                .toBeTruthy();
        });
    });

});
