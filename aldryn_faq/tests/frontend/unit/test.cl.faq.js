/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global Cl, describe, it, expect, beforeEach, afterEach, fixture, spyOn */

// #############################################################################
// UNIT TEST
describe('cl.faq.js:', function () {
    beforeEach(function () {
        fixture.setBase('frontend/fixtures');
        this.markup = fixture.load('faq.html');
        this.preventEvent = { preventDefault: function () {} };
    });

    afterEach(function () {
        fixture.cleanup();
    });

    it('runs dummy test', function () {
        expect('dummy test').toEqual('dummy test');
    });

});
