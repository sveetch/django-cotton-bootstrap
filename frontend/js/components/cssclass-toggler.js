/*!
 * Simple component to toggle classes from a click on an element
 *
 * Trigger element must have :
 *
 * - A class name 'class-toggler';
 * - An HTML attribute 'data-target' which contain a valid CSS selector ('#foo',
 *   '.bar', etc..);
 *
 * Trigger element may have :
 *
 * - An HTML attribute 'data-target-css' to define a custom CSS classname to toggle
 *   on target element instead of the default one 'is-open';
 * - An HTML attribute 'data-trigger-css' to define a custom CSS classname to toggle
 *   on trigger element instead of the default one 'is-active';
 *
 */

export function CssClassToggler() {
    "use strict";

    const triggers = Array.prototype.slice.call(
        document.querySelectorAll(".class-toggler"), 0
    );
    // Default CSS classnames to toggle
    const default_target_css = "is-open";
    const default_trigger_css = "is-active";

    // Check if there are any trigger
    if (triggers.length > 0) {
        // Add a click event on each of them
        triggers.forEach(function(trigger_element) {
            trigger_element.addEventListener("click", function() {
                // Get the target from the "data-target" attribute
                if (trigger_element.dataset.target) {
                    const targets = Array.prototype.slice.call(
                        document.querySelectorAll(trigger_element.dataset.target), 0
                    );
                    const target_css = trigger_element.dataset.targetCss
                                       ? trigger_element.dataset.targetCss
                                       : default_target_css;
                    const trigger_css = trigger_element.dataset.triggerCss
                                        ? trigger_element.dataset.triggerCss
                                        : default_trigger_css;

                    targets.forEach(function(el) {
                        trigger_element.classList.toggle(trigger_css);
                        trigger_element.setAttribute(
                            "aria-expanded",
                            trigger_element.classList.contains(trigger_css)
                        );

                        el.classList.toggle(target_css);
                    });
                }
            });
        });
    }
};
