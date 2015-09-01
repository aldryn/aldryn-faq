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

            return faqPage.administrationOptions.first().click();
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

            // wait for iframe side menu to reload
            browser.wait(function () {
                return browser.isElementPresent(faqPage.addConfigsButton);
            }, faqPage.mainElementsWaitTime);

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
                return browser.switchTo().frame(browser.findElement(By.css(
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

        // wait for iframe side menu to reload
        browser.wait(function () {
            return browser.isElementPresent(faqPage.addConfigsButton);
        }, faqPage.mainElementsWaitTime);

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
                    faqPage.appconfigSelect.sendKeys('FAQ / aldryn_faq');
                    return faqPage.appconfigOption.click();
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
            faqPage.categorySelect.sendKeys('Test category');
            return faqPage.categoryOption.click();
        }).then(function () {
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
            expect(faqPage.successNotification.isDisplayed()).toBeTruthy();
            // validate edit question link
            expect(faqPage.editQuestionLinks.first().isDisplayed())
                .toBeTruthy();
        });
    });

    it('adds a new faq block on the page', function () {
        // switch to default page content
        browser.switchTo().defaultContent();

        // add faq to the page only if it was not added before
        faqPage.aldrynFAQBlock.isPresent().then(function (present) {
            if (present === false) {
                // click the Page link in the top menu
                return faqPage.userMenus.get(1).click().then(function () {
                    // wait for top menu dropdown options to appear
                    browser.wait(function () {
                        return browser.isElementPresent(faqPage.userMenuDropdown);
                    }, faqPage.mainElementsWaitTime);

                    faqPage.advancedSettingsOption.click();

                    // wait for modal iframe to appear
                    browser.wait(function () {
                        return browser.isElementPresent(faqPage.modalIframe);
                    }, faqPage.iframeWaitTime);

                    // switch to modal iframe
                    browser.switchTo().frame(browser.findElement(By.css(
                        '.cms_modal-frame iframe')));

                    // wait for Application select to appear
                    browser.wait(function () {
                        return browser.isElementPresent(faqPage.applicationSelect);
                    }, faqPage.mainElementsWaitTime);

                    // set Application
                    faqPage.applicationSelect.click();
                    faqPage.applicationSelect.sendKeys('FAQ')
                        .then(function () {
                        faqPage.applicationSelect.click();
                    });

                    // switch to default page content
                    browser.switchTo().defaultContent();

                    browser.wait(function () {
                        return browser.isElementPresent(faqPage.saveModalButton);
                    }, faqPage.mainElementsWaitTime);

                    browser.actions().mouseMove(faqPage.saveModalButton)
                        .perform();
                    return faqPage.saveModalButton.click();
                });
            }
        }).then(function () {
            // wait for aldryn-faq block to appear
            browser.wait(function () {
                return browser.isElementPresent(faqPage.aldrynFAQBlock);
            }, faqPage.mainElementsWaitTime);

            faqPage.categoryLink.click();

            // wait for question link to appear
            browser.wait(function () {
                return browser.isElementPresent(faqPage.questionLink);
            }, faqPage.mainElementsWaitTime);

            faqPage.questionLink.click();

            browser.wait(function () {
                return browser.isElementPresent(faqPage.questionTitle);
            }, faqPage.mainElementsWaitTime);

            // validate question title
            expect(faqPage.questionTitle.isDisplayed()).toBeTruthy();
        });
    });

    it('deletes question', function () {
        // wait for modal iframe to appear
        browser.wait(function () {
            return browser.isElementPresent(faqPage.sideMenuIframe);
        }, faqPage.iframeWaitTime);

        // switch to sidebar menu iframe
        browser.switchTo()
            .frame(browser.findElement(By.css('.cms_sideframe-frame iframe')));

        // wait for edit question link to appear
        browser.wait(function () {
            return browser.isElementPresent(faqPage.editQuestionLinks.first());
        }, faqPage.mainElementsWaitTime);

        // validate edit question links texts to delete proper question
        faqPage.editQuestionLinks.first().getText().then(function (text) {
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
            browser.wait(function () {
                return browser.isElementPresent(faqPage.deleteButton);
            }, faqPage.mainElementsWaitTime);

            browser.actions().mouseMove(faqPage.saveAndContinueButton)
                .perform();
            return faqPage.deleteButton.click();
        }).then(function () {
            // wait for confirmation button to appear
            browser.wait(function () {
                return browser.isElementPresent(faqPage.sidebarConfirmationButton);
            }, faqPage.mainElementsWaitTime);

            faqPage.sidebarConfirmationButton.click();

            browser.wait(function () {
                return browser.isElementPresent(faqPage.successNotification);
            }, faqPage.mainElementsWaitTime);

            // validate success notification
            expect(faqPage.successNotification.isDisplayed())
                .toBeTruthy();

            // switch to default page content
            browser.switchTo().defaultContent();

            // refresh the page to see changes
            browser.refresh();
        });
    });

});
