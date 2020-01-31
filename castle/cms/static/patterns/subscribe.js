/* global define */

define([
  'jquery',
  'mockup-patterns-base',
], function($, Base) {
  'use strict';

  var Subscription = Base.extend({
    name: 'subscribe',
    trigger: '.pat-subscribe',
    parser: 'mockup',
    defaults: {
    },
    init: function() {
      var self = this;

      self.setupForm();
    },
    setupForm: function() {
      var self = this;
      self.$form = self.$el.find('form');
      self.url = self.$form.attr('action');
      self.$form.submit(function(e) {
        e.preventDefault();

        self.$form.ajaxSubmit({
          type: 'POST',
          url: self.url,
          data: {
            'form.buttons.subscribe': 'subscribe'
          },
          failure: function(data) {
            alert("There was a problem while submitting your subscription.");
            console.log('Subscribe attempt failed: ' + data);
          },
          success: function(responseText, statusText, xhr) {
            self.$el.find('.portalMessage').remove();
            var message = $('.portalMessage', responseText);

            $('.documentFirstHeading', self.$el).append(message);

            // These lines were added to fix a bug where sign up
            // field was rendered when form submitted.
            $("p").remove(".discreet");
            $("h1").remove(".documentFirstHeading");
            $('form', self.$el).replaceWith('<h3>Please check you email to confirm subscription(s).</h3>');

            //When we get a valid submit, the form
            //"Disappears" off the top of the viewport sometimes
            var formTop = self.$el.find('h1').offset().top;
            $('body').scrollTop(formTop);

            //We replaced the form, so reset the submit handler
            self.setupForm();
          },
        });
      });
    }
  });

  return Subscription;

});
