odoo.define('sce.ComplementMenu', function(require) {

"use strict";

var UserMenu = require('web.UserMenu');

var ComplementMenu = UserMenu.include({
    _onMenuMeusdados: function () {
        var self = this;
        var session = this.getSession();
        this.trigger_up('clear_uncommitted_changes', {
            callback: function () {
                self._rpc({
                        route: "/web/action/load",
                        params: {
                            action_id: "sce.action_res_partner_simple_edit_my",
                        },
                    })
                    .done(function (result) {
                        result.res_id = session.partner_id;
                        self.do_action(result);
                    });
            },
        });
     }
  });

return ComplementMenu;

});