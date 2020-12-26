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

define(["./components/d3/d3", "./Selector" ], function(d3, BaseSelectors) {
    "use strict";

    var FastIntervalSelector = BaseSelectors.BaseXSelector.extend({
        render : function() {
            FastIntervalSelector.__super__.render.apply(this);
            this.freeze_but_move = true;
            this.freeze_dont_move = false;
            this.active = false;
            this.size = this.model.get("size");

            this.width = this.parent.width - this.parent.margin.left - this.parent.margin.right;
            this.height = this.parent.height - this.parent.margin.top - this.parent.margin.bottom;

            var self = this;
            var scale_creation_promise = this.create_scales();
            Promise.all([this.mark_views_promise, scale_creation_promise]).then(function() {
                //container for mouse events
                self.background = self.el.append("rect")
                    .attr("x", 0)
                    .attr("y", 0)
                    .attr("width", self.width)
                    .attr("height", self.height)
                    .attr("class", "selector selectormouse")
                    .attr("pointer-events", "all")
                    .attr("visibility", "hidden");

                self.background.on("mousemove", _.bind(self.mousemove, self))
                    .on("click", _.bind(self.click, self))
                    .on("dblclick", _.bind(self.dblclick, self));

                self.rect = self.el.append("rect")
                .attr("class", "selector intsel")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", self.size)
                .attr("height", self.height)
                .attr("pointer-events", "none")
                .attr("display", "none");

                if(self.model.get("color") !== null) {
                    self.rect.style("fill", self.model.get("color"));
                }

                self.create_listeners();
            });
        },
        create_listeners: function() {
            FastIntervalSelector.__super__.create_listeners.apply(this);
            this.listenTo(this.model, "change:color", this.color_change, this);
        },
        color_change: function() {
            if(this.model.get("color") !== null) {
                this.rect.style("fill", this.model.get("color"));
            }
        },
        click: function () {
            this.active = true;
            this.rect.style("display", "inline");
            this.freeze_but_move = this.model.get("size") ?
                true : !this.freeze_but_move;
        },
        dblclick: function () {
            this.freeze_dont_move = !this.freeze_dont_move;
        },
        mousemove: function() {
            if (this.freeze_dont_move || !this.active) {
                return;
            }

            var mouse_pos = d3.mouse(this.background.node());
            var int_len = this.size > 0 ?
                this.size : parseInt(this.rect.attr("width"));
            var vert_factor = (this.height - mouse_pos[1]) / this.height;
            var interval_size = this.freeze_but_move ?
                int_len : Math.round(vert_factor * this.width);

            var start;
            if (mouse_pos[0] - interval_size / 2 < 0) {
                start = 0;
            } else if ((mouse_pos[0] + interval_size / 2) > this.width) {
                start = this.width - interval_size;
            } else {
                start = mouse_pos[0] - interval_size / 2;
            }

            //update the interval location and size
            this.rect.attr("x", start);
            this.rect.attr("width", interval_size);
            this.model.set_typed_field("selected",
                                       this.invert_range(start,
                                                         start + interval_size), { js_ignore : true});
            _.each(this.mark_views, function(mark_view) {
                mark_view.invert_range(start, start + interval_size);
            });
            this.touch();
        },
        invert_range: function(start, end) {
            return this.scale.invert_range([start, end]);
        },
        scale_changed: function() {
            this.reset();
            this.create_scale();
        },
        remove: function() {
            this.rect.remove();
            this.background.remove();
            FastIntervalSelector.__super__.remove.apply(this);
        },
        relayout: function() {
            FastIntervalSelector.__super__.relayout.apply(this);
            this.background.attr("width", this.width)
                .attr("height", this.height);
            this.rect.attr("height", this.height);
            this.set_range([this.scale]);
        },
        reset: function() {
            this.rect.attr("x", 0)
                .attr("width", 0);
            this.model.set_typed_field("selected", [], {js_ignore : true});
            _.each(this.mark_views, function(mark_view) {
                mark_view.invert_range([]);
            });
            this.touch();
        },
        update_scale_domain: function(ignore_gui_update) {
            // Call the base class function to update the scale.
            FastIntervalSelector.__super__.update_scale_domain.apply(this);
            if(ignore_gui_update !== true) {
                this.selected_changed();
            }
        },
        selected_changed: function(model, value, options) {
            //TODO: should the size get overridden if it was set previously and
            //then selected was changed from the python side?
            if(options && options.js_ignore) {
                //this change was most probably triggered from the js side and
                //should be ignored.
                return;
            }
            //reposition the interval selector and set the selected attribute.
            var selected = this.model.get_typed_field("selected");
            if(selected.length === 0) {
                this.reset();
            } else if (selected.length != 2) {
                // invalid value for selected. Ignoring the value
                return;
            } else {
                var self = this;
                var pixels = selected.map(function(d) { return self.scale.scale(d); });
                pixels = pixels.sort(function(a, b) { return a - b; });

                this.rect.attr({ x: pixels[0],
                                 width: (pixels[1] - pixels[0])})
                    .style("display", "inline");
                this.active = true;
                _.each(this.mark_views, function(mark_view) {
                    mark_view.invert_range(pixels[0], pixels[1]);
                });
            }
        },
    });

    return {
        FastIntervalSelector: FastIntervalSelector,
    };
});

