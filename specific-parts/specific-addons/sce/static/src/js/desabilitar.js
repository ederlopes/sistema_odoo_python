odoo.define('module.extension_name', function (require) {
    var FormView = require('web.FormView');
    FormView.include({
     load_record: function() {
      this._super.apply(this, arguments);
      if (this.model === 'exportador') {

          console.log(this)
          if (this.datarecord && (this.datarecord.state === 'state')) {
            this.$buttons.find('.o_form_button_edit').css({'display':'none'});
          }
          else {
            this.$buttons.find('.o_form_button_edit').css({'display':''});
          }
       }
    });
});