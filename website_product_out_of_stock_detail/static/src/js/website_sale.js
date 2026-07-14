odoo.define('website_product_out_of_stock_detail.website_sale', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    require('website_sale.website_sale');

    publicWidget.registry.WebsiteSale.include({
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // On initial load, if the product is NOT orderable, hide the sticky cart button
                var $stickyAddToCart = $('.tp-sticky-add-to-cart, .tp-bottom-bar-add-to-cart');
                var $ctaWrapper = $('#o_wsale_cta_wrapper');
                if ($stickyAddToCart.length && $ctaWrapper.length && $ctaWrapper.hasClass('d-none')) {
                    $stickyAddToCart.find('.product-add-to-cart').addClass('d-none');
                }
            });
        },
        _onChangeCombination: function (ev, $parent, combination) {
            this._super.apply(this, arguments);

            var hasNoStock = combination.product_type === 'product' && 
                             (combination.free_qty !== undefined && combination.free_qty < 1);
            var isOrderable = !hasNoStock || combination.allow_out_of_stock_order;

            var $outOfStockMessage = $('#out_of_stock_message');
            var $inStockMessage = $('#in_stock_message');
            var $ctaWrapper = $('#o_wsale_cta_wrapper');

            // 1. Handle Banners
            if (hasNoStock) {
                if (combination.out_of_stock_message) {
                    $outOfStockMessage.find('#out_of_stock_text').html(combination.out_of_stock_message);
                } else {
                    $outOfStockMessage.find('#out_of_stock_text').text('Out of Stock');
                }
                $outOfStockMessage.removeClass('d-none').addClass('d-flex');
                $inStockMessage.removeClass('d-flex').addClass('d-none');
            } else {
                $outOfStockMessage.removeClass('d-flex').addClass('d-none');
                $inStockMessage.removeClass('d-none').addClass('d-flex');
            }

            // 2. Handle Add to Cart button (CTA Wrapper)
            if (isOrderable) {
                $ctaWrapper.removeClass('d-none').addClass('d-flex');
            } else {
                $ctaWrapper.removeClass('d-flex').addClass('d-none');
            }

            // 3. Handle Sticky Add to Cart
            var $stickyAddToCart = $('.tp-sticky-add-to-cart, .tp-bottom-bar-add-to-cart');
            if ($stickyAddToCart.length) {
                if (isOrderable) {
                    $stickyAddToCart.find('.product-add-to-cart').removeClass('d-none');
                } else {
                    $stickyAddToCart.find('.product-add-to-cart').addClass('d-none');
                }
            }
        },
    });
});

