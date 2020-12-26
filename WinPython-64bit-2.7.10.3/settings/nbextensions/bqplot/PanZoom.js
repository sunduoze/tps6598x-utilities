/* Copyright 2015 Bloomberg Finance L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

define(["base/js/utils", "./components/d3/d3", "./utils", "./Interaction"], function(ipy_utils, d3, utils, InteractionViewModule) {
    "use strict";

    // TODO avoid code duplication of 'x' and 'y'

    var PanZoom = InteractionViewModule.Interaction.extend({
        render: function() {
            PanZoom.__super__.render.apply(this);
            var that = this;
            this.el
              .style({"cursor": "move"})
              .on("mousedown", function() { that.mousedown(); })
              .on("mousemove", function() { that.mousemove(); })
              .on("mouseup", function() { that.mouseup(); })
              .on("mousewheel", function() { that.mousewheel(); });
            this.active = false;

            this.update_scales();
            this.listenTo(this.model, "change:scales", this.update_scales, this);

            this.set_ranges();
            this.listenTo(this.parent, "margin_updated", this.set_ranges, this);
        },
        update_scales: function() {
            var scales = this.model.get("scales");
            var that = this;
            this.scale_promises = ipy_utils.resolve_promises_dict({
                "x": Promise.all((scales.x || []).map(function(model) {
                        return that.create_child_view(model);
                     })),
                "y": Promise.all((scales.y || []).map(function(model) {
                        return that.create_child_view(model);
                     })),
            });
        },
        set_ranges: function() {
           var that = this;
           var i;
           this.scale_promises.then(function(scale_views) {
               var xscale_views = scale_views.x;
               for (i=0; i<xscale_views.length; i++) {
                   xscale_views[i].set_range(that.parent.padded_range("x",
                                                    xscale_views[i].model));
               }
               var yscale_views = scale_views.y;
               for (i=0; i<yscale_views.length; i++) {
                   yscale_views[i].set_range(that.parent.padded_range("y",
                                                    yscale_views[i].model));
               }
           });
        },
        mousedown: function () {
            var scales = this.model.get("scales");
            this.active = true;
            this.el.style({"cursor": "move"});
            this.previous_pos = d3.mouse(this.el.node());
            // A copy of the original domains is required to avoid additional
            // drift when Paning.
            this.domains = {
                "x": (scales.x || []).map(function(s) {
                    return s.domain.slice(0);
                }),
                "y": (scales.y || []).map(function(s) {
                    return s.domain.slice(0);
                }),
            };
        },
        mouseup: function () {
            this.active = false;
        },
        mousemove: function() {
            if (this.active && this.model.get("allow_pan")) {
                // If memory is set to true, intermediate positions between the
                // last position of the mouse and the current one will be
                // interpolated.
                var mouse_pos = d3.mouse(this.el.node());
                if (!("previous_pos" in this)) {
                    this.previous_pos = mouse_pos;
                }
                var scales = this.model.get("scales");
                var that = this;
                this.scale_promises.then(function(scale_views) {
                    var xscale_views = scale_views.x;
                    var xdomains = that.domains.x;
                    var xdiffs = xscale_views.map(function(view) {
                        if (view.scale.invert) {
                            // Categorical scales don't have an inversion.
                            return view.scale.invert(mouse_pos[0]) -
                                   view.scale.invert(that.previous_pos[0]);
                        }
                    });
                    var i, domain, min, max;
                    for (i=0; i<xscale_views.length; i++) {
                        domain = xdomains[i];
                        min = domain[0] - xdiffs[i];
                        max = domain[1] - xdiffs[i];
                        that.set_scale_attribute(scales.x[i], "min", min);
                        that.set_scale_attribute(scales.x[i], "max", max);
                        // TODO? Only do in mouseup?
                        xscale_views[i].touch();
                    }

                    var yscale_views = scale_views.y;
                    var ydomains = that.domains.y;
                    var ydiffs = yscale_views.map(function(view) {
                        if (view.scale.invert) {
                            // Categorical scales don't have an inversion.
                            return view.scale.invert(mouse_pos[1]) -
                                   view.scale.invert(that.previous_pos[1]);
                        }
                    });
                    for (i=0; i<yscale_views.length; i++) {
                        domain = ydomains[i];
                        min = domain[0] - ydiffs[i];
                        max = domain[1] - ydiffs[i];
                        that.set_scale_attribute(scales.y[i], "min", min);
                        that.set_scale_attribute(scales.y[i], "max", max);
                        // TODO? Only do this on mouseup?
                        yscale_views[i].touch();
                    }
                });
            }
        },
        mousewheel: function() {
            if (this.model.get("allow_zoom")) {
                d3.event.preventDefault();
                var delta = d3.event.wheelDelta;
                var mouse_pos = d3.mouse(this.el.node());
                if (delta) {
                    if (delta > 0) {
                        this.el.style({"cursor": "zoom-in"});
                    } else {
                        this.el.style({"cursor": "zoom-out"});
                    }
                    var scales = this.model.get("scales");
                    var that = this;
                    this.scale_promises.then(function(scale_views) {
                        var i, domain, min, max;
                        var xscale_views = scale_views.x;
                        var xpos = xscale_views.map(function(view) {
                             return view.scale.invert(mouse_pos[0]);
                        });
                        var factor = Math.exp(-delta * 0.001);
                        for (i=0; i<xscale_views.length; i++) {
                            domain = scales.x[i].domain;
                            min = domain[0];
                            max = domain[1];
                            that.set_scale_attribute(scales.x[i], "min",
                                        (1 - factor) * xpos[i] + factor * min);
                            that.set_scale_attribute(scales.x[i], "max",
                                        (1 - factor) * xpos[i] + factor * max);
                            // TODO? Only do in mouseup?
                            xscale_views[i].touch();
                        }

                        var yscale_views = scale_views.y;
                        var ypos = yscale_views.map(function(view) {
                            return view.scale.invert(mouse_pos[1]);
                        });
                        for (i=0; i<yscale_views.length; i++) {
                            domain = scales.y[i].domain;
                            min = domain[0];
                            max = domain[1];
                            that.set_scale_attribute(scales.y[i], "min",
                                        (1 - factor) * ypos[i] + factor * min);
                            that.set_scale_attribute(scales.y[i], "max",
                                        (1 - factor) * ypos[i] + factor * max);
                            // TODO? Only do this on mouseup?
                            yscale_views[i].touch();
                        }
                    });
                }
            }
        },
        set_scale_attribute: function(scale, attribute_name, value) {
            // The difference of two dates is an int. So we want to cast it to
            // a date when setting the attribute for the date scale
            if(scale.type == "date") {
                value = (value instanceof Date) ? value : new Date(value);
                //TODO: Function for setting date can be made the same as for
                //other scale once the _pack_models is fixes
                scale.set_date_elem(attribute_name, value);
            } else {
                scale.set(attribute_name, value);
            }
        },
    });

    return {
        PanZoom: PanZoom,
    };
});

