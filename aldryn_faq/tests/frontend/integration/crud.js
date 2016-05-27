'use strict';

var helpers = require('djangocms-casper-helpers');
var globals = helpers.settings;
var casperjs = require('casper');
var cms = helpers(casperjs);
var xPath = casperjs.selectXPath;

casper.test.setUp(function (done) {
    casper.start()
        .then(cms.login())
        .run(done);
});

casper.test.tearDown(function (done) {
    casper.start()
        .then(cms.logout())
        .run(done);
});

casper.test.begin('Creation / deletion of the apphook', function (test) {
    casper
        .start(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            test.assertVisible('#content', 'Admin loaded');
            this.click(
                xPath(cms.getXPathForAdminSection({
                    section: 'Aldryn_Faq',
                    row: 'Configs',
                    link: 'Add'
                }))
            );
        })
        .waitForUrl(/add/)
        .waitUntilVisible('#faqconfig_form')
        .then(function () {
            test.assertVisible('#faqconfig_form', 'Apphook creation form loaded');

            this.fill('#faqconfig_form', {
                namespace: 'Test namespace',
                app_title: 'Test FAQ'
            }, true);
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The config "FAQ / Test namespace" was added successfully.',
                'Apphook config was created'
            );

            test.assertElementCount(
                '#result_list tbody tr',
                2,
                'There are 2 apphooks now'
            );

            this.clickLabel('FAQ / Test namespace', 'a');
        })
        .waitUntilVisible('.deletelink', function () {
            this.click('.deletelink');
        })
        .waitForUrl(/delete/, function () {
            this.click('input[value="Yes, I\'m sure"]');
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The config "FAQ / Test namespace" was deleted successfully.',
                'Apphook config was deleted'
            );
        })
        .run(function () {
            test.done();
        });
});

casper.test.begin('Creation / deletion of the category and question', function (test) {
    casper
        .start()
        .then(cms.addPage({ title: 'FAQ' }))
        .then(cms.addApphookToPage({
            page: 'FAQ',
            apphook: 'FaqApp'
        }))
        .then(cms.publishPage({
            page: 'FAQ'
        }))
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText('li', 'No entry found.', 'No questions yet');
        })
        .thenOpen(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            test.assertVisible('#content', 'Admin loaded');
            this.click(
                xPath(cms.getXPathForAdminSection({
                    section: 'Aldryn_Faq',
                    row: 'Categories',
                    link: 'Add'
                }))
            );
        })
        .waitForUrl(/add/)
        .waitUntilVisible('#category_form')
        .then(function () {
            test.assertVisible('#category_form', 'Category creation form loaded');

            this.fill('#category_form', {
                name: 'Test category',
                appconfig: '1'
            }, true);
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The category "Test category" was added successfully.',
                'Category was created'
            );

            test.assertElementCount(
                '#result_list tbody tr',
                1,
                'There is 1 category available'
            );
        })
        .thenOpen(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            test.assertVisible('#content', 'Admin loaded');
            this.click(
                xPath(cms.getXPathForAdminSection({
                    section: 'Aldryn_Faq',
                    row: 'Questions',
                    link: 'Add'
                }))
            );
        })
        .waitForUrl(/add/)
        .waitUntilVisible('#question_form')
        .then(function () {
            test.assertVisible('#question_form', 'Question creation form loaded');

            this.fill('#question_form', {
                title: 'What is the Answer to the Ultimate Question of Life, The Universe, and Everything?',
                category: '1'
            }, false);

        })
        .waitUntilVisible('.cke_inner', function () {
            this.evaluate(function () {
                CMS.CKEditor.editor.setData('42');
            });

            this.click('input[value="Save"]');
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The question "What is the Answer to the Ultimate Question of Life, The Universe,' +
                ' and Everything?" was added successfully.',
                'Question was created'
            );

            test.assertElementCount(
                '#result_list tbody tr',
                1,
                'There is 1 question available'
            );
        })
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText(
                'li a h3',
                'Test category',
                'Category title is available on the page'
            );

            this.click('li a h3');
        })
        .waitForSelector('.cms-toolbar-expanded', function () {
            test.assertSelectorHasText(
                'li a h3',
                'What is the Answer to the Ultimate Question of Life, The Universe, and Everything?',
                'Question is available on the page'
            );
        })
        .thenOpen(globals.adminUrl)
        .waitUntilVisible('#content', function () {
            this.click(
                xPath(cms.getXPathForAdminSection({
                    section: 'Aldryn_Faq',
                    row: 'Questions'
                }))
            );
        })
        .waitForUrl(/question/, function () {
            this.clickLabel('What is the Answer to the Ultimate Question of Life, The Universe, and Everything?', 'a');
        })
        .waitUntilVisible('.deletelink', function () {
            this.click('.deletelink');
        })
        .waitForUrl(/delete/, function () {
            this.click('input[value="Yes, I\'m sure"]');
        })
        .waitUntilVisible('.success', function () {
            test.assertSelectorHasText(
                '.success',
                'The question "What is the Answer to the Ultimate Question of Life, The Universe, and Everything?" ' +
                'was deleted successfully.',
                'Question was deleted'
            );
        })
        .then(cms.removePage())
        .run(function () {
            test.done();
        });
});

casper.test.begin('Latest questions plugin', function (test) {
    casper
        .start()
        .then(cms.addPage({ title: 'Home' }))
        .then(cms.addPlugin({
            type: 'LatestQuestionsPlugin',
            content: {
                id_questions: 1
            }
        }))
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText(
                '.cms-plugin li',
                'No entry found.',
                'No questions yet'
            );
        })
        .then(cms.openSideframe())
        // add articles
        .withFrame(0, function () {
            this.waitForSelector('.cms-pagetree-breadcrumbs')
                .then(function () {
                    this.click('.cms-pagetree-breadcrumbs a:first-child');
                })
                .waitForUrl(/admin/)
                .waitForSelector('.dashboard', function () {
                    this.click(xPath(cms.getXPathForAdminSection({
                        section: 'Aldryn_Faq',
                        row: 'Questions',
                        link: 'Add'
                    })));
                })
                .waitForUrl(/add/)
                .waitUntilVisible('#question_form')
                .then(function () {
                    test.assertVisible('#question_form', 'Question creation form loaded');

                    this.fill('#question_form', {
                        title: 'What is the Answer to the Ultimate Question of Life, The Universe, and Everything?',
                        category: '1'
                    }, false);

                })
                .waitUntilVisible('.cke_inner', function () {
                    this.evaluate(function () {
                        CMS.CKEditor.editor.setData('42');
                    });
                })
                .wait(3000, function () {
                    this.click('input[value="Save and add another"]');
                })
                .waitForSelector('.success', function () {
                    test.assertSelectorHasText(
                        '.success',
                        'The question "What is the Answer to the Ultimate Question of Life,' +
                        ' The Universe, and Everything?"' +
                        ' was added successfully. You may add another question below.',
                        'First question added'
                    );

                    this.fill('#question_form', {
                        title: 'Another question',
                        category: '1'
                    }, false);
                })
                .waitUntilVisible('.cke_inner', function () {
                    this.evaluate(function () {
                        CMS.CKEditor.editor.setData('another answer');
                    });

                    this.click('input[value="Save"]');
                })
                .waitForSelector('.success');
        })
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText(
                '.cms-plugin li',
                'No entry found',
                'Still no questions yet (no apphooked page yet)'
            );
        })
        .then(cms.addPage({ title: 'FAQ' }))
        .then(cms.addApphookToPage({
            page: 'FAQ',
            apphook: 'FaqApp'
        }))
        .then(cms.publishPage({ page: 'FAQ' }))
        .thenOpen(globals.editUrl, function () {
            test.assertSelectorHasText(
                '.cms-plugin li a h3',
                'Another question',
                'Latest question is visible on the page'
            );
            test.assertElementCount(
                '.cms-plugin li',
                1,
                'Only one latest article is visible on the page'
            );
        })
        // remove articles
        .then(cms.openSideframe())
        .withFrame(0, function () {
            this.waitForSelector('.cms-pagetree-breadcrumbs')
                .then(function () {
                    this.click('.cms-pagetree-breadcrumbs a:first-child');
                })
                .waitForUrl(/admin/)
                .waitForSelector('.dashboard', function () {
                    this.click(xPath(cms.getXPathForAdminSection({
                        section: 'Aldryn_Faq',
                        row: 'Questions'
                    })));
                })
                .waitForSelector('#changelist-form', function () {
                    this.click('th input[type="checkbox"]');
                    this.fill('#changelist-form', {
                        action: 'delete_selected'
                    }, true);

                })
                .waitForSelector('.delete-confirmation', function () {
                    this.click('input[value="Yes, I\'m sure"]');
                })
                .waitForSelector('.success', function () {
                    test.assertSelectorHasText(
                        '.success',
                        'Successfully deleted 2 questions.',
                        'Questions deleted'
                    );
                });
        })
        .then(cms.removePage())
        .then(cms.removePage())
        .run(function () {
            test.done();
        });
});

casper.test.begin('Delete category', function (test) {
    casper
        .start()
        .then(cms.addPage({ title: 'Home' }))
        .thenOpen(globals.editUrl)
        // remove category
        .then(cms.openSideframe())
        .withFrame(0, function () {
            this.waitForSelector('.cms-pagetree-breadcrumbs')
                .then(function () {
                    this.click('.cms-pagetree-breadcrumbs a:first-child');
                })
                .waitForUrl(/admin/)
                .waitForSelector('.dashboard', function () {
                    this.click(xPath(cms.getXPathForAdminSection({
                        section: 'Aldryn_Faq',
                        row: 'Categories'
                    })));
                })
                .waitForSelector('#changelist-form', function () {
                    this.click('th input[type="checkbox"]');
                    this.fill('#changelist-form', {
                        action: 'delete_selected'
                    }, true);
                })
                .waitForSelector('.delete-confirmation', function () {
                    this.click('input[value="Yes, I\'m sure"]');
                })
                .waitForSelector('.success', function () {
                    test.assertSelectorHasText(
                        '.success',
                        'Successfully deleted 1 category.',
                        'Categories deleted'
                    );
                });
        })
        .then(cms.removePage())
        .run(function () {
            test.done();
        });
});
