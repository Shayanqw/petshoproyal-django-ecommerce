(function ($) {
    "use strict";

    /*----------------------------------------
      Sticky Menu Activation
    ------------------------------------------*/
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 150) {
            $('.header-sticky').addClass('sticky');
        } else {
            $('.header-sticky').removeClass('sticky');
        }
    });

    /*---------------------
        Header Search Action
    ---------------------*/
    $(".action-execute").on('click', function() {
        if ($(".action-execute, .header-search-form").hasClass("visible-execute")) {
            $(".action-execute, .header-search-form").removeClass("visible-execute");
        } else {
            $(".action-execute, .header-search-form").removeClass("visible-execute");
            $(".action-execute, .header-search-form").addClass("visible-execute");
        }
    });

    /*---------------------
        Header Cart Toggle
    ---------------------*/
    $(".cart-visible").click(function(){
        $(".header-cart-content").slideToggle("slow");
    });

    /*-----------------------------------------
      Off Canvas Mobile Menu
    -------------------------------------------*/
    $(".header-action-btn-menu").on('click', function () {
        $("body").addClass('fix');
        $(".mobile-menu-wrapper").addClass('open');
    });
    $(".offcanvas-btn-close, .offcanvas-overlay").on('click', function () {
        $("body").removeClass('fix');
        $(".mobile-menu-wrapper").removeClass('open');
    });

    /*-----------------------------------------
      Toggle Function Active
    -------------------------------------------*/
    $('#showlogin').on('click', function () {
        $('#checkout-login').slideToggle(500);
    });
    $('#showcoupon').on('click', function () {
        $('#checkout_coupon').slideToggle(500);
    });
    $('#cbox').on('click', function () {
        $('#cbox-info').slideToggle(500);
    });
    $('#ship-box').on('click', function () {
        $('#ship-box-info').slideToggle(1000);
    });

    /*----------------------------------------
      Responsive Mobile Menu
    ------------------------------------------*/
    const $offCanvasNav = $('.mobile-menu, .category-menu'),
          $offCanvasNavSubMenu = $offCanvasNav.find('.dropdown');
    $offCanvasNavSubMenu.slideUp();
    $offCanvasNav.on('click', 'li a, li .menu-expand', function(e) {
        const $this = $(this);
        if (
            ($this.parent().attr('class').match(/\b(menu-item-has-children|has-children|has-sub-menu)\b/)) &&
            ($this.attr('href') === '#' || $this.hasClass('menu-expand'))
        ) {
            e.preventDefault();
            if ($this.siblings('ul:visible').length) {
                $this.parent('li').removeClass('active');
                $this.siblings('ul').slideUp();
            } else {
                $this.parent('li').addClass('active');
                $this.closest('li').siblings('li').removeClass('active').find('li').removeClass('active');
                $this.closest('li').siblings('li').find('ul:visible').slideUp();
                $this.siblings('ul').slideDown();
            }
        }
    });

    /*----------------------------------------
      Slider Activation
    ------------------------------------------*/

    // Hero Slider
    const heroSlider = new Swiper('.hero-slider.swiper-container', {
        loop: true,
        speed: 1150,
        spaceBetween: 30,
        slidesPerView: 1,
        effect: 'fade',
        pagination: {
            el: '.hero-slider .swiper-pagination',
            type: 'bullets',
            clickable: true
        },
        navigation: {
            nextEl: '.hero-slider .home-slider-next',
            prevEl: '.hero-slider .home-slider-prev'
        }
    });

    // Product Deal Carousel
    const dealCarousel = new Swiper('.product-deal-carousel .swiper-container', {
        loop: true,
        slidesPerView: 1,
        spaceBetween: 20,
        watchSlidesVisibility: true,
        pagination: {
            el: '.product-deal-carousel .swiper-pagination',
            type: 'bullets',
            clickable: true
        },
        navigation: {
            nextEl: '.product-deal-carousel .swiper-deal-button-next',
            prevEl: '.product-deal-carousel .swiper-deal-button-prev'
        }
    });

    // Testimonial Carousel
    const testimonialGalleryTop = new Swiper('.testimonial-gallery-top', {
        slidesPerView: 1,
        loop: true,
        effect: 'fade',
        fadeEffect: { crossFade: true },
        grabCursor: false,
        centeredSlides: true
    });
    const testimonialGalleryThumbs = new Swiper('.testimonial-gallery-thumbs', {
        loop: true,
        effect: 'coverflow',
        coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 50,
            modifier: 6,
            slideShadows: false
        },
        pagination: {
            el: '.testimonial-gallery-thumbs .swiper-pagination',
            clickable: true
        },
        thumbs: {
            swiper: testimonialGalleryTop
        }
    });

    // Single Product Gallery
    const productGalleryThumbs = new Swiper('.product-gallery-thumbs', {
        spaceBetween: 10,
        slidesPerView: 3,
        freeMode: true,
        watchSlidesVisibility: true,
        watchSlidesProgress: true
    });
    const productGalleryTop = new Swiper('.product-gallery-top', {
        spaceBetween: 10,
        loop: true,
        navigation: {
            nextEl: '.product-gallery-top .swiper-button-next',
            prevEl: '.product-gallery-top .swiper-button-prev'
        },
        thumbs: {
            swiper: productGalleryThumbs
        }
    });

    // Shop Grid Carousel
    const productGridCarousel = new Swiper('.product-carousel .swiper-container', {
        loop: true,
        slidesPerView: 4,
        spaceBetween: 20,
        observer: true,
        observeParents: true,
        watchSlidesVisibility: true,
        pagination: {
            el: '.product-carousel .swiper-pagination',
            type: 'bullets',
            clickable: true
        },
        navigation: {
            nextEl: '.product-carousel .swiper-button-next',
            prevEl: '.product-carousel .swiper-button-prev'
        },
        breakpoints: {
            320:  { slidesPerView: 1, spaceBetween: 10 },
            480:  { slidesPerView: 2, spaceBetween: 20 },
            768:  { slidesPerView: 3, spaceBetween: 20 },
            992:  { slidesPerView: 3, spaceBetween: 20 },
            1200: { slidesPerView: 4, spaceBetween: 20 }
        }
    });

    // Modal Product Carousel
    const productModalCarousel = new Swiper('.modal-product-carousel .swiper-container', {
        loop: true,
        slidesPerView: 1,
        spaceBetween: 0,
        navigation: {
            nextEl: '.modal-product-carousel .swiper-product-button-next',
            prevEl: '.modal-product-carousel .swiper-product-button-prev'
        }
    });

    // ----- Offer Carousel (responsive 1‑1 on mobile) -----
    /*const offerSwiper = new Swiper('.offer .swiper-container', {
        loop: true,
        slidesPerView: 1,
        spaceBetween: 30,
        pagination: {
            el: '.offer .swiper-pagination',
            type: 'bullets',
            clickable: true
        },
        navigation: {
            nextEl: '.offer .swiper-button-next',
            prevEl: '.offer .swiper-button-prev'
        },
        breakpoints: {
            // viewport width >= 0px
            0:   { slidesPerView: 1, spaceBetween: 10 },
            // 576px – 767px: still 1 slide but more gutter
            576: { slidesPerView: 1, spaceBetween: 20 },
            // 768px – 991px: 2 slides
            768: { slidesPerView: 2, spaceBetween: 30 },
            // 992px and up: back to 3 slides
            992: { slidesPerView: 3, spaceBetween: 30 }
        }
    });*/

    /*----------------------------------------
      Shop Grid View Toggle
    ------------------------------------------*/
    $('.shop_toolbar_btn > button').on('click', function (e) {
        e.preventDefault();
        $('.shop_toolbar_btn > button').removeClass('active');
        $(this).addClass('active');

        const viewMode = $(this).data('role'),
              parentsDiv = $('.shop_wrapper');

        parentsDiv.removeClass('grid_3 grid_4 grid_5 grid_list').addClass(viewMode);

        if (viewMode === 'grid_3') {
            parentsDiv.children().addClass('col-lg-4 col-md-4 col-sm-6')
                      .removeClass('col-lg-3 col-cust-5 col-12');
        } else if (viewMode === 'grid_4') {
            parentsDiv.children().addClass('col-xl-3 col-lg-4 col-md-4 col-sm-6')
                      .removeClass('col-lg-4 col-cust-5 col-12');
        } else if (viewMode === 'grid_list') {
            parentsDiv.children().addClass('col-12')
                      .removeClass('col-xl-3 col-lg-3 col-lg-4 col-md-6 col-md-4 col-sm-6 col-cust-5');
        }
    });

    /*----------------------------------------
      Countdown
    ------------------------------------------*/
    $('[data-countdown]').each(function() {
        const $this = $(this),
              finalDate = $this.data('countdown');
        $this.countdown(finalDate, function(event) {
            $this.html(event.strftime(
                '<div class="single-countdown"><span class="single-countdown_time">%D</span><span class="single-countdown_text">Days</span></div>' +
                '<div class="single-countdown"><span class="single-countdown_time">%H</span><span class="single-countdown_text">Hours</span></div>' +
                '<div class="single-countdown"><span class="single-countdown_time">%M</span><span class="single-countdown_text">Mins</span></div>' +
                '<div class="single-countdown"><span class="single-countdown_time">%S</span><span class="single-countdown_text">Secs</span></div>'
            ));
        });
    });

    /*----------------------------------------
      Cart Plus Minus Button
    ------------------------------------------*/
    $('.cart-plus-minus').append(
        '<div class="dec qtybutton">-</div><div class="inc qtybutton">+</div>'
    );
    $('.qtybutton').on('click', function () {
        const $button  = $(this),
              oldValue = parseFloat($button.parent().find('input').val()),
              newVal   = $button.hasClass('inc') ? oldValue + 1
                         : (oldValue > 1 ? oldValue - 1 : 1);
        $button.parent().find('input').val(newVal);
    });

    /*----------------------------------------
      LightGallery Active
    ------------------------------------------*/
    $(".popup-gallery").lightGallery({
        pager: false,
        thumbnail: false,
        fullScreen: true,
        zoom: true,
        rotateLeft: true,
        rotateRight: true
    });

    /*---------------------------------
      MailChimp
    -----------------------------------*/
    $('#mc-form').ajaxChimp({
        language: 'en',
        callback: mailChimpResponse,
        url: 'http://devitems.us11.list-manage.com/subscribe/post?u=6bbb9b6f5827bd842d9640c82&amp;id=05d85f18ef'
    });
    function mailChimpResponse(resp) {
        if (resp.result === 'success') {
            $('.mailchimp-success').html(resp.msg).fadeIn(900);
            $('.mailchimp-error').fadeOut(400);
        } else if (resp.result === 'error') {
            $('.mailchimp-error').html(resp.msg).fadeIn(900);
        }
    }

    /*-------------------------
      Ajax Contact Form
    ---------------------------*/
    $(function() {
        const form         = $('#contact-form'),
              formMessages = $('.form-messege');
        $(form).submit(function(e) {
            e.preventDefault();
            const formData = $(form).serialize();
            $.ajax({
                type: 'POST',
                url: form.attr('action'),
                data: formData
            })
            .done(function(response) {
                formMessages.removeClass('error').addClass('success').text(response);
                $('#contact-form input,#contact-form textarea').val('');
            })
            .fail(function(data) {
                formMessages.removeClass('success').addClass('error')
                            .text(data.responseText || 'Oops! An error occurred and your message could not be sent.');
            });
        });
    });

    /*----------------------------------------
      Scroll to Top
    ------------------------------------------*/
    function scrollToTop() {
        const $scrollUp = $('#scroll-top'),
              $window   = $(window);
        let   lastScrollTop = 0;

        $window.on('scroll', function () {
            const st = $(this).scrollTop();
            if (st > lastScrollTop) {
                $scrollUp.removeClass('show');
            } else if ($window.scrollTop() > 200) {
                $scrollUp.addClass('show');
            } else {
                $scrollUp.removeClass('show');
            }
            lastScrollTop = st;
        });

        $scrollUp.on('click', function (evt) {
            $('html, body').animate({scrollTop: 0}, 600);
            evt.preventDefault();
        });
    }
    scrollToTop();

    /*----------------------------------------
      When document is loading, do
    ------------------------------------------*/
    $(window).on('load', function() {
        AOS.init({ once: true });
    });

})(jQuery);
