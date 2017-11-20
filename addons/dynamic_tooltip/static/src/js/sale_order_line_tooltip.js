odoo.define('dynamic_tooltip', function(require) {

    var core = require('web.core'), // get tree view widgets
        Model = require('web.DataModel'); // make asynchronous calls to the DB

    /* Make a special widget to include dynamic tooltips for the product name char field,
       see addons/web/static/src/js/views/list_view.js for reference.
    */
    var DynamicTooltip = core.list_widget_registry.get('field').extend({
        _format: function (row_data, options) {
        var value = row_data[this.id].value;
        var product_tmpl_id = row_data[this.id].value[0],
            product_name = row_data[this.id].value[1];

        // Create a Query() object to make a request to the DB
        var productTemplate = new Model('product.template')
        productTemplate.query(['description_sale'])
                       .filter([['id', '=', product_tmpl_id]])
                       .first()
                       .then(function(res) {
                           if (res) {
                               // Attach the tooltip asynchronously after the corresponding element is rendered
                               $('#' + product_tmpl_id).prop('title', res.description_sale);
                           };
                       })
        // Return a <p> tag with id of the product_temlate record
        return '<p id="' + product_tmpl_id + '">' + product_name + '</p>';
        }
    });

    // Make the created widget accessible by other models
    core.list_widget_registry.add('field.dynamic_tooltip', DynamicTooltip);
})